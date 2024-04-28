import streamlit as st
import functions as f
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

def visualize_coil_parameters(scanner_dir, selected_subsystem):

    # get the csv file path of the data
    # let user select one of the following RF coils to view its parameters
    st.write("### Choose RF Coil to View Parameters")
    list_rf_coils = ["ANTERIOR", "BODY_QUAD", "POSTERIOR"]
    coil_channels_dict = {"ANTERIOR": 16, "BODY_QUAD": 2, "POSTERIOR": 12}
    selected_rf_coil = st.selectbox("Select RF Coil", list_rf_coils)
    if selected_rf_coil in coil_channels_dict:
        number_channels = coil_channels_dict[selected_rf_coil]
        st.write(f"The {selected_rf_coil} coil has {number_channels} channels. Choose a parameter to view its data of all channels.")
        # let user select one of the following parameters to view
        coil_parameters = ["Noise"]
        selected_parameter = st.selectbox("Select a Parameter", coil_parameters)
        csv_file_path = f.get_csv_path(scanner_dir, selected_subsystem, selected_parameter, selected_rf_coil, True, number_channels)
        df = f.read_and_sort_csv_file(csv_file_path)

        # ask user to select a date range to filter the data
        df_filtered = f.filter_df(df)

        if selected_parameter == "Noise":
            selected_column = "Noise (uV)"
        # ask user to select one or two threshold values
        upper_threshold, lower_threshold = f.select_threshold_values(df_filtered, selected_column)
    

        # plot the selected parameter of the RF coil with st
        plot_coil_parameter(df_filtered, selected_rf_coil, upper_threshold, lower_threshold)
    else:
        st.write("Unknown RF Coil selected.")

def plot_coil_parameter(df, coil, upper_threshold=None, lower_threshold=None):
    dict_channels = {"ANTERIOR": 16, "BODY_QUAD": 2, "POSTERIOR": 12}
    number_channels = dict_channels[coil]

    selected_channels = st.multiselect(f"Select One or More Channels", list(range(1, number_channels + 1)), default=[1])

    # for each selected channel, plot the data
    for channel in selected_channels:
        # Set Date-Time as index for easy 
        csv_file_path = f".\\Data\\Data_Alpha\\Noise\\ANTERIOR\\channel_{channel}.csv"
        subset_df = f.read_and_sort_csv_file(csv_file_path)
        subset_df.set_index('Date-Time', inplace=True)
        # plot the "Noise (uV)" parameter against Date-Time
        fig, ax = plt.subplots(figsize=(12, 6))
        ax.plot(subset_df.index, subset_df["Noise (uV)"], label=f"Channel {channel}")
        ax.set_title(f"Noise (uV) of {coil} Coil - Channel {channel}")
        ax.set_xlabel("Date-Time")
        ax.set_ylabel("Noise (uV)")
        ax.legend()
        st.pyplot(fig)
        
    
    pass


def visualize_other_parameters(scanner_dir, selected_subsystem):
        
    csv_file_path = f.get_csv_path(scanner_dir, selected_subsystem, None, None, False, None)
    df = f.read_and_sort_csv_file(csv_file_path)
    # get the list of columns except "Date" and "Time" and "Exam ID" columns for user to select from
    selectable_columns = [col for col in df.columns if col not in ["Date-Time", "Exam ID", "Coil", "Channel"]]

    st.write(f"## Overview of {selected_subsystem} Parameters")
    # display the first 10 rows of the DataFrame
    st.write("#### First 10 Rows of Data")
    st.write(df.head(10))


    # display summary statistics of the DataFrame of only the selectable columns
    f.display_summary_statistics(df[selectable_columns])

    # ask user to select a date range to filter the data
    df_filtered = f.filter_df(df)

    # give user an option to choose a column to view its data
    st.write("### Select a column to view its data")
    # exclude "Date" and "Time" and "Exam ID" columns
    selected_column = st.selectbox("Select a Column", selectable_columns)

    
    # ask user to select one or two threshold values
    upper_threshold, lower_threshold = f.select_threshold_values(df_filtered, selected_column)

    # plot the selected parameter of the RF coil
    plot_other_parameters(df_filtered, selected_column, upper_threshold, lower_threshold)

def plot_other_parameters(df, selected_column, upper_threshold=None, lower_threshold=None):
    # Set Date-Time as index for easy plotting
    df.set_index('Date-Time', inplace=True)
    
    st.write(f"## Time-series of {selected_column}")
    
    # Plotting
    fig, ax = plt.subplots(figsize=(12, 6))
    ax.plot(df.index, df[selected_column], label=selected_column)
    
    if upper_threshold:
        ax.axhline(y=upper_threshold, color='r', linestyle='--', label=f"Threshold: {upper_threshold}")
        
    if lower_threshold:
        ax.axhline(y=lower_threshold, color='r', linestyle='--', label=f"Threshold: {lower_threshold}")
        
    ax.set_title(f"Time-series of {selected_column}")
    ax.set_xlabel("Date-Time")
    ax.set_ylabel(selected_column)
    ax.legend()
    
    # Display the plot in Streamlit
    st.pyplot(fig)
