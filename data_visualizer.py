import streamlit as st
import functions as f
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import plotly.graph_objects as go

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
        # convert Date-Time column to datetime format
        df["Date-Time"] = pd.to_datetime(df["Date-Time"])

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

    fig = go.Figure()

    for channel in selected_channels:
        subset_df = df[df['Channel'] == channel]
        fig.add_trace(go.Scatter(x=subset_df.index, y=subset_df["Noise (uV)"], mode='lines', name=f"Channel {channel}"))

    fig.update_layout(
        title=f"Noise (uV) of {coil} Coil",
        xaxis_title="Date-Time",
        yaxis_title="Noise (uV)",
        legend_title="Channels",
        hovermode="x unified"
    )

    st.plotly_chart(fig)

def visualize_other_parameters(scanner_dir, selected_subsystem):
        
    csv_file_path = f.get_csv_path(scanner_dir, selected_subsystem, None, None, False, None)
    df = f.read_and_sort_csv_file(csv_file_path)
    # sort the DataFrame by "Date-Time" column and set it as the index
    df = df.sort_values("Date-Time")
    df.set_index("Date-Time", inplace=True)

    # get the list of columns except "Date" and "Time" and "Exam ID" columns for user to select from
    selectable_columns = [col for col in df.columns if col not in ["Date-Time", "Exam ID", "Coil", "Channel"]]

    st.write(f"## Overview of {selected_subsystem} Parameters")
    # display the first 10 rows of the DataFrame
    st.write("#### First 10 Rows of Data")
    st.write(df.head(10))


    # display summary statistics of the DataFrame of only the selectable columns
    f.display_summary_statistics(df[selectable_columns])

    df_filtered = f.filter_df(df)

    # give user an option to choose a column to view its data
    st.write("### Select a column to view its data")
    # exclude "Date" and "Time" and "Exam ID" columns
    selected_column = st.selectbox("Select a Column", selectable_columns)

    # prompt user to select a date range from 2019-01-01 to 2023-09-30 to filter the data with st
    date_range = st.date_input("Select a Date Range", [pd.to_datetime("2019-01-01"), pd.to_datetime("2023-09-30")])
    
    # ask user to select one or two threshold values
    upper_threshold, lower_threshold = f.select_threshold_values(df_filtered, selected_column)

    # plot the selected parameter of the RF coil
    plot_other_parameters(df_filtered, selected_column, date_range, upper_threshold, lower_threshold)

def plot_other_parameters(df, selected_column, selected_date_range, upper_threshold, lower_threshold):
    fig = go.Figure()
    # plot data of the selected column with the selected date range
    fig.add_trace(go.Scatter(x=df.index, y=df[selected_column], mode='lines', name=selected_column))
    fig.update_xaxes(range=[selected_date_range[0], selected_date_range[1]])


    if upper_threshold:
        fig.add_shape(type="line", x0=df.index[0], y0=upper_threshold, x1=df.index[-1], y1=upper_threshold, line=dict(color="red", dash="dash"), name=f"Threshold: {upper_threshold}")

    if lower_threshold:
        fig.add_shape(type="line", x0=df.index[0], y0=lower_threshold, x1=df.index[-1], y1=lower_threshold, line=dict(color="red", dash="dash"), name=f"Threshold: {lower_threshold}")

    fig.update_layout(
        title=f"Time-series of {selected_column}",
        xaxis_title="Date-Time",
        yaxis_title=selected_column,
        hovermode="x unified"
    )

    st.plotly_chart(fig)
    
    # display the data points in the selected date range that are above the upper threshold
    st.write("### Data Points Above Upper Threshold")
    # convert the selected date range to string format
    start_time = str(selected_date_range[0]) + " 00:00:00"
    end_time = str(selected_date_range[1]) + " 23:59:59"
    df_above_threshold = df[(df[selected_column] > upper_threshold) & (df.index >= pd.to_datetime(start_time)) & (df.index <= pd.to_datetime(end_time))]
    st.write(df_above_threshold)