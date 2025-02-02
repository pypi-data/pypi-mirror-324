# Slowly Changing Dimension (SCD) Type 2 Implementation

## Overview
This document provides a guide to implementing **Slowly Changing Dimension (SCD)** using the `scdhelper` package in Python.

## Prerequisites
Ensure you have the necessary dependencies installed. If the `scdhelper` package is not already installed, install it using:

```bash
pip install scdhelper
```

## SCD Type 2 Module
SCD Type 2 is used to track historical changes to data by maintaining multiple versions of records with effective start and end dates.

## Implementation

### 1. Import Required Libraries
```python
import pandas as pd
from scdtype2 import SCDType2
```

### 2. Prepare Data
Create two DataFrames:
- `df1`: Existing records (historical data)
- `df2`: Incoming records (new updates)

#### Sample Data
```python
data1 = {
    "id": [1, 2],
    "name": ["John", "Alice"],
    "address": ["NY", "LA"],
    "inserted_date": ["2024-01-01", "2024-01-05"],
    "end_date": [None, None],
    "is_current": [1, 1]
}

data2 = {
    "id": [1, 2],
    "name": ["John", "Alice"],
    "address": ["SF", "LA"]
}

df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
```

### 3. Define SCD Type 2 Logic
```python
scd = SCDType2(
    key_columns=["id"],
    tracked_columns=[col for col in df1.columns if col not in ["id"]],
    start_date_column="inserted_date",
    end_date_column="end_date",
    is_current_column="is_current"
)
```

### 4. Apply SCD Type 2
```python
updated_df = scd.apply(df1, df2)
```

### 5. View Results
```python
print(updated_df)
```

## Explanation
1. **Primary Key (`id`) Exclusion**
   - The `id` column uniquely identifies a record and does not change over time.
   - It is **excluded from `tracked_columns`** to ensure only actual data changes trigger new versions.

2. **Tracked Columns**
   - All columns except `id` are monitored for changes.
   - If a change is detected, a new record is inserted, and the previous record is marked as inactive.

3. **Start and End Dates**
   - `inserted_date` marks when the record version became active.
   - `end_date` is updated when a new version of the record is inserted.
   - The `is_current` column indicates whether the record is the latest version.

## Example Output
If `df2` updates the address of `id=1` from "NY" to "SF", the updated SCD table will look like this:

| id | name  | address | inserted_date | end_date   | is_current |
|----|-------|---------|--------------|-----------|------------|
| 1  | John  | NY      | 2024-01-01   | 2024-02-01 | 0          |
| 1  | John  | SF      | 2024-02-01   | NULL      | 1          |
| 2  | Alice | LA      | 2024-01-05   | NULL      | 1          |

## Note
The apply method requires a pandas DataFrame as input. If you are working with PySpark DataFrames, convert them to pandas before passing them:

```
df1 = df1.toPandas()
df2 = df2.toPandas()
updated_df = scd.apply(df1, df2)
```

## Conclusion
This implementation allows you to maintain historical versions of data while tracking changes effectively using **SCD Type 2**. It ensures data integrity while keeping a complete history of attribute changes over time.

