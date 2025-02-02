import pytest
import pandas as pd
from scdhelper import SCDType2

def test_scd_type_2():
    # Example test case
    current_df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Alice', 'Bob'],
        'address': ['Street A', 'Street B'],
        'inserted_date': ['2021-01-01', '2021-02-01'],
        'end_date': [None, None],
        'is_current': [True, True]
    })
    
    new_df = pd.DataFrame({
        'id': [1, 2],
        'name': ['Alice', 'Bob'],
        'address': ['Street X', 'Street B'],
        'inserted_date': ['2025-01-01', '2025-02-01'],
        'end_date': [None, None],
        'is_current': [True, True]
    })
    
    scd = SCDType2(
        key_columns=['id'],
        tracked_columns=['name', 'address'],
        start_date_column="inserted_date",
        end_date_column="end_date",
        is_current_column="is_current"
    )
    
    updated_df = scd.apply(current_df, new_df)
    
    # Add assertions to test the expected output
    assert not updated_df.empty
