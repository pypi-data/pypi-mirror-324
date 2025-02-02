import pandas as pd
from datetime import datetime
from pyspark.sql import DataFrame as SparkDataFrame
import logging

logging.basicConfig(level=logging.INFO)

class SCDType2:
    def __init__(self, key_columns, tracked_columns, start_date_column="start_date", end_date_column="end_date", is_current_column="is_current"):
        self.key_columns = key_columns
        self.tracked_columns = tracked_columns
        self.start_date_column = start_date_column
        self.end_date_column = end_date_column
        self.is_current_column = is_current_column

    def validate_dataframes(self, current_df, new_df):
        
        # Check if key columns exist in both DataFrames
        for df, name in zip([current_df, new_df], ['current_df', 'new_df']):
            if not all(col in df.columns for col in self.key_columns):
                raise ValueError(f"Missing key columns in {name}")
        
        # Check for duplicates in key columns
        for df, name in zip([current_df, new_df], ['current_df', 'new_df']):
            if df.duplicated(subset=self.key_columns).any():
                raise ValueError(f"Duplicate key columns in {name}")
        
        # Check for null values in key columns
        for df, name in zip([current_df, new_df], ['current_df', 'new_df']):
            if df[self.key_columns].isnull().any().any():
                raise ValueError(f"Null values in key columns in {name}")

    def apply(self, current_df, new_df):
        try:
            if isinstance(current_df, SparkDataFrame):
                current_df = current_df.toPandas()
            if isinstance(new_df, SparkDataFrame):
                new_df = new_df.toPandas()

            self.validate_dataframes(current_df, new_df)
            
            # Merge to find changes
            merged_df = pd.merge(
                current_df, new_df, on=self.key_columns, suffixes=("_current", "_new"), how="outer", indicator=True
            )
            
            # New data with no update
            new_rows = merged_df[merged_df["_merge"] == "right_only"].drop(columns=["_merge"])
            new_rows = new_rows.rename(columns={col: col.replace("_new", "") for col in new_rows.columns if col.endswith("_new")})
            new_rows = new_rows[self.key_columns + self.tracked_columns]

            # Identify updated rows (records that exist in both but have different tracked column values)
            track_changed_rows = merged_df[
                (merged_df["_merge"] == "both") &
                (merged_df[[f"{col}_current" for col in self.tracked_columns]].ne(
                    merged_df[[f"{col}_new" for col in self.tracked_columns]].values).any(axis=1))
            ].copy()
            updated_rows = track_changed_rows.rename(columns={col: col.replace("_new", "") for col in track_changed_rows.columns if col.endswith("_new")})
            updated_rows = updated_rows[self.key_columns + self.tracked_columns]

            # Identify rows that are same in the new data also but not changed
            exist_notchanged_rows = merged_df[
                (merged_df["_merge"] == "both") &
                (merged_df[[f"{col}_current" for col in self.tracked_columns]].eq(
                    merged_df[[f"{col}_new" for col in self.tracked_columns]].values).all(axis=1))
            ].copy()

            existing_rows = exist_notchanged_rows.rename(columns={col: col.replace("_current", "") for col in exist_notchanged_rows.columns if col.endswith("_current")})
            existing_rows = existing_rows[self.key_columns + self.tracked_columns]

            # Unchanged data
            unchanged_rows = merged_df[
                (merged_df["_merge"] == "left_only")
            ].copy()
            unchanged_rows = unchanged_rows.rename(columns={col: col.replace("_current", "") for col in unchanged_rows.columns if col.endswith("_current")})
            unchanged_rows = unchanged_rows[self.key_columns + self.tracked_columns]

            # Old data who got updates    
            old_updated_rows = track_changed_rows.rename(columns={col: col.replace("_current", "") for col in track_changed_rows.columns if col.endswith("_current")})
            old_updated_rows = old_updated_rows[self.key_columns + self.tracked_columns]

            if not new_rows.empty:
                new_rows = new_rows[[col for col in new_df.columns]]  # Keep only relevant columns
                new_rows[self.start_date_column] = datetime.now()
                new_rows[self.end_date_column] = None
                new_rows[self.is_current_column] = True

            if not updated_rows.empty:
                updated_rows[self.start_date_column] = datetime.now()
                updated_rows[self.end_date_column] = None
                updated_rows[self.is_current_column] = True

            if not old_updated_rows.empty:
                old_updated_rows[self.end_date_column] = datetime.now()
                old_updated_rows[self.is_current_column] = False

            if not unchanged_rows.empty:
                unchanged_rows[self.end_date_column] = None
                unchanged_rows[self.is_current_column] = True

            if not existing_rows.empty:
                existing_rows[self.end_date_column] = None
                existing_rows[self.is_current_column] = True

            dfs_to_concat = [df for df in [updated_rows, old_updated_rows, unchanged_rows, new_rows, existing_rows] if not df.empty]
            
            if dfs_to_concat:
                result_df = pd.concat(dfs_to_concat, ignore_index=True)
                result_df[self.start_date_column] = pd.to_datetime(result_df[self.start_date_column], errors='coerce')
            else:
                result_df = pd.DataFrame()

            return result_df

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            raise

