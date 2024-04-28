import os
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import seaborn as sns

# read the csv file and sort the data by Date-Time
def read_and_sort_csv_file(csv_file_path):
    # Read selected CSV file into pandas DataFrame
    df = pd.read_csv(csv_file_path)
    # combine the Date and Time columns into a single column with datetime format
    if "Date-Time" in df.columns:
        pass
    else:
        df["Date-Time"] = pd.to_datetime(df["Date"] + " " + df["Time"])
        # move the Date-Time column to the first position
        df.insert(0, "Date-Time", df.pop("Date-Time"))
        # drop the Date and Time columns
        df.drop(columns=["Date", "Time"], inplace=True)
        # sort the DataFrame by Date-Time
    df.sort_values("Date-Time", inplace=True)
    return df

def get_csv_path(scanner_dir, subsystem, parameter, coil, is_coil_parameter, channel):
    if not is_coil_parameter:
        csv_file_path = scanner_dir + "\\" + subsystem.lower() + "_data.csv"
    else:
        csv_file_path = f".\\Data\\Data_Alpha\\{parameter}\\{coil}\\channel_{channel}.csv"
    return csv_file_path

def filter_df(df):
    df_filtered = df
    # let user select a date range to filter the data from 2019-01-01 to 2023-09-30
    if "Date-Time" in df.columns:
        st.write("### Select a Date Range from 2019-01-01 to 2023-09-30")
        date_range = st.date_input("Select a Date Range", [pd.to_datetime("2019-01-01"), pd.to_datetime("2023-09-30")])
        
        # Extract start and end dates from the selected date range
        start_date = pd.to_datetime(date_range[0]).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(date_range[1]).strftime('%Y-%m-%d')
        
        # Construct lower and upper bounds for the selected date range
        lower_bound = start_date + " 00:00:00"
        upper_bound = end_date + " 23:59:59"
        
        mask = (df["Date-Time"] >= lower_bound) & (df["Date-Time"] <= upper_bound)
        df_filtered = df.loc[mask]
        
    else:
        st.write("Not timestamped data.")
    
    
    return df_filtered

def select_threshold_values(df, selected_parameter):
    st.write("### Select a Threshold Value")
    st.write("The threshold value is used to highlight data points that exceed the threshold. Default threshold is set at the 99.99th percentile (i.e. 0.01% of the data points are outliers) of the selected column over the entire period.")
    upper_threshold = st.number_input("Threshold", value=df[selected_parameter].quantile(0.9999))
    # Validate thresholds to ensure they are within the range of the data
    if upper_threshold > df[selected_parameter].max():
        st.write(f"Threshold value exceeds the maximum value of {selected_parameter}.")
        upper_threshold = None
    if upper_threshold < df[selected_parameter].min():
        st.write(f"Threshold value is below the minimum value of {selected_parameter}.")
        upper_threshold = None
    if upper_threshold is not None:
        upper_threshold = round(upper_threshold, 2)
    lower_threshold = None
    return upper_threshold, lower_threshold

def display_summary_statistics(df):
    st.write("### Summary Statistics")
    st.write(df.describe())





            



