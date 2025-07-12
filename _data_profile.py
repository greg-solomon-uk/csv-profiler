# python script to do data profiling on a group of csv files in a folder
# it should write the results to a new csv called _data_profile.csv
# this csv should have columns: file_name, field_name, count_of_nulls, count_of_distinct_values, min_value, max_value, data_type, sql_data_type, count_of_non_nulls, percent_nulls, most_frequent_value, frequency_of_most_common, mean_value, median_value, std_deviation, min_length, max_length, pattern_sample, is_unique, is_constant, smallest_five_values, largest_five_values, five_most_frequent_values

import os
import pandas as pd
import numpy as np
from datetime import datetime

# Directory containing the CSV files
folder_path = './'  # Change this to your target folder path

# List to store profiling results
profile_data = []

# Helper function to detect SQL data type
def detect_sql_type(series):
    if pd.api.types.is_bool_dtype(series):
        return 'BOOLEAN'
    elif pd.api.types.is_integer_dtype(series):
        return 'INTEGER'
    elif pd.api.types.is_float_dtype(series):
        return 'FLOAT'
    elif pd.api.types.is_datetime64_any_dtype(series):
        return 'DATETIME'
    else:
        try:
            pd.to_datetime(series.dropna().iloc[0])
            return 'DATETIME'
        except:
            pass
        return 'VARCHAR'

# Iterate over all CSV files in the folder
for file_name in os.listdir(folder_path):
    if file_name != "_data_profile.csv" and file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        try:
            df = pd.read_csv(file_path)
        except Exception:
            continue

        for column in df.columns:
            series = df[column]
            non_null_series = series.dropna()
            str_series = non_null_series.astype(str)

            data_type = str(series.dtype)
            sql_data_type = detect_sql_type(series)
            count_of_nulls = series.isnull().sum()
            count_of_non_nulls = series.notnull().sum()
            percent_nulls = (count_of_nulls / len(series)) * 100 if len(series) > 0 else 0
            count_of_distinct_values = series.nunique(dropna=True)
            is_unique = count_of_distinct_values == len(series)
            is_constant = count_of_distinct_values == 1
            most_frequent_value = series.mode().iloc[0] if not series.mode().empty else None
            frequency_of_most_common = series.value_counts().iloc[0] if not series.value_counts().empty else None

            mean_value = series.mean() if pd.api.types.is_numeric_dtype(series) else None
            median_value = series.median() if pd.api.types.is_numeric_dtype(series) else None
            std_deviation = series.std() if pd.api.types.is_numeric_dtype(series) else None

            min_value = str_series.min() if not str_series.empty else None
            max_value = str_series.max() if not str_series.empty else None
            min_length = str_series.map(len).min() if not str_series.empty else None
            max_length = str_series.map(len).max() if not str_series.empty else None

            smallest_five_values = sorted(str_series.unique())[:5]
            largest_five_values = sorted(str_series.unique())[-5:]

            pattern_sample = ', '.join(str_series.sample(min(3, len(str_series)), random_state=1).unique()) if not str_series.empty else None
            five_most_frequent_values = series.value_counts().head(5).to_dict()

            profile_data.append({
                'file_name': file_name,
                'field_name': column,
                'data_type': data_type,
                'sql_data_type': sql_data_type,
                'count_of_nulls': count_of_nulls,
                'count_of_non_nulls': count_of_non_nulls,
                'percent_nulls': percent_nulls,
                'count_of_distinct_values': count_of_distinct_values,
                'is_unique': is_unique,
                'is_constant': is_constant,
                'most_frequent_value': most_frequent_value,
                'frequency_of_most_common': frequency_of_most_common,
                'min_value': min_value,
                'max_value': max_value,
                'mean_value': mean_value,
                'median_value': median_value,
                'std_deviation': std_deviation,
                'min_length': min_length,
                'max_length': max_length,
                'pattern_sample': pattern_sample,
                'smallest_five_values': smallest_five_values,
                'largest_five_values': largest_five_values,
                'five_most_frequent_values': five_most_frequent_values
            })

# Create a DataFrame from the profiling results
profile_df = pd.DataFrame(profile_data)

# Write the profiling results to a new CSV file
profile_df.to_csv('_data_profile.csv', index=False)

print("Data profiling completed. Results saved to '_data_profile.csv'.")

