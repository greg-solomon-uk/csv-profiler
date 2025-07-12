# csv-profiler

This project contains
* A CSV Data Profiler, [_data_profile.py](https://github.com/greg-solomon-uk/csv-profiler/blob/main/_data_profile.py)
* The Chinook data in CSV format

To use it, execute **python _data_profile.py** and it will analyse all the CSV files and create an output file **_data_profile.csv**

The ouput file has format : file_name, field_name, count_of_nulls, count_of_distinct_values, min_value, max_value, data_type, sql_data_type, count_of_non_nulls, percent_nulls, most_frequent_value, frequency_of_most_common, mean_value, median_value, std_deviation, min_length, max_length, pattern_sample, is_unique, is_constant, smallest_five_values, largest_five_values, five_most_frequent_values
