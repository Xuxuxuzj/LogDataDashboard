import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os



def list_subdirectories(directory):
    subdirectories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    # sort subdirectories in ascending order
    subdirectories.sort()
    return subdirectories

def display_amplifier_parameters(scanner_dir):

    # Display amplifier parameters title
    st.write("### Amplifier Parameters")
    
    # Read CSV files from scanner directory
    csv_file_path = scanner_dir + "/Amp Power" + "/data.csv"


    # Read selected CSV file into pandas DataFrame
    df = pd.read_csv(csv_file_path)

    # Combine the Date and Time columns into a single column with datetime format
    df["Date-Time"] = pd.to_datetime(df["Date"] + " " + df["Time"])

    # Move the Date-Time column to the first position
    df.insert(0, "Date-Time", df.pop("Date-Time"))

    # drop the Date and Time columns
    df.drop(columns=["Date", "Time"], inplace=True)
    # sort the DataFrame by Date-Time
    df.sort_values("Date-Time", inplace=True)
    # reset the index
    df.reset_index(drop=True, inplace=True)

    st.write('## DataFrame')
    st.write(df)

    # get the list of columns except "Date" and "Time" and "Exam ID" columns
    selectable_columns = [col for col in df.columns if col not in ["Date-Time", "Exam ID"]]
    st.write("### Select a column to view its data")
    # exclude "Date" and "Time" and "Exam ID" columns
    selected_column = st.selectbox("Select a Column", selectable_columns)

    if "Date-Time" in df.columns:
        st.write("### Select a Date Range")
        date_range = st.date_input("Select a Date Range", [df["Date-Time"].min(), df["Date-Time"].max()])
        
        # Extract start and end dates from the selected date range
        start_date = pd.to_datetime(date_range[0]).strftime('%Y-%m-%d')
        end_date = pd.to_datetime(date_range[1]).strftime('%Y-%m-%d')
        
        # Construct lower and upper bounds for the selected date range
        lower_bound = start_date + " 00:00:00"
        upper_bound = end_date + " 23:59:59"
        
        mask = (df["Date-Time"] >= lower_bound) & (df["Date-Time"] <= upper_bound)
        df_filtered = df.loc[mask]
    else: 
        df_filtered = df

    # give user an option to put a threshold on the plot
    st.write("### Select a Threshold Value")
    st.write("The threshold value is used to highlight data points that exceed the threshold. Default threshold is set at the 99.99th percentile of the selected column.")
    # set a default threshold at the 99th percentile of the selected column and round it to 2 decimal places
    threshold = st.number_input("Threshold", value=df_filtered[selected_column].quantile(0.9999))
    threshold = round(threshold, 2)

    # Validate threshold value based on data range
    if "Date-Time" in df_filtered.columns:
        min_value = df_filtered[selected_column].min()
        max_value = df_filtered[selected_column].max()

        if threshold < min_value:
            st.warning(f"Threshold should be greater than or equal to {min_value}.")
            threshold = min_value

        if threshold > max_value:
            st.warning(f"Threshold should be less than or equal to {max_value}.")
            threshold = max_value

    # plot selected column data from filtered DataFrame
    st.write("### Plot of Selected Column Data")
    fig, ax = plt.subplots()
    ax.plot(df_filtered["Date-Time"], df_filtered[selected_column])
    ax.set_xlabel("Date-Time")
    ax.set_ylabel(selected_column)
    ax.set_title(f"Plot of {selected_column}")

    # plot the threshold line if the threshold is not None
    if threshold is not None:
        ax.axhline(y=threshold, color='r', linestyle='--', label=f'Threshold = {threshold}')
        ax.legend()

    st.pyplot(fig)

    # if a threshold is set, display the option to view date-time and exam-ID of the data points that exceed the threshold
    if threshold is not None:
        st.write("### View Data Points Exceeding Threshold")
        # get the data points exceeding the threshold
        df_threshold_exceeded = df_filtered[df_filtered[selected_column] > threshold]
        st.write(df_threshold_exceeded[["Date-Time", "Exam ID", selected_column]])


def view_historical_data(list_subsystems):
    st.write("## View Historical Data")

    # Let user select a scanner
    selected_scanner = st.selectbox("Select a Scanner", ["Alpha", "Omega", "Ingenia"])

    # get the directory of the scanner
    scanner_dir = "Data/" + "Data_" + selected_scanner 

    # Let user search for a parameter or select from the list
    st.write("### Select a subsystem of the scanner to view its parameters")
    
    # sort subsystems in ascending order
    list_subsystems.sort()
    
    # display the list of subsystems as options
    selected_subsystem = st.selectbox("Select a Subsystem", list_subsystems)
    # if the selected subsystem is "Amplifier", display the amplifier parameters
    if selected_subsystem == "Amplifier":
        display_amplifier_parameters(scanner_dir)
            

def process_new_log_file():
    # prompt user to upload a new .log file less than 500MB
    st.write("## Process New Log File")
    uploaded_file = st.file_uploader("Upload a new log file", type=["log"])


def main():
    # Initialize list of subsystems
    list_subsystems = ["Amplifier", "Circulator", "RF Coil", "Cooling System", "Magnet", "Room", "Spikes", "Exam and Scan Summary"]

    # get list of parameters and roots
    with open('list_parameters.txt', 'r') as file:
        list_parameters_and_roots = file.readlines()

    # Create a sidebar with links
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", ["Data Visualizer", "Parameter Dictionary", "About", "Contact"])

    # Home page
    if selection == "Data Visualizer":
        st.title("Log Data")
        st.write("Welcome to Log Data Visualizer!")
        # Display two options, one for "View Historical Data" and another for "Process New Log File"
        option = st.radio("Select an Option", ["View Historical Data", "Process New Log File"])

        if option == "View Historical Data":
            view_historical_data(list_subsystems)
        else:
            process_new_log_file()
    
    # Parameter Dictionary page
    elif selection == "Parameter Dictionary":
        st.title("Parameter Dictionary")
        st.write("### This page displays the dictionary of parameters.")
        # display two options to view by subsystem or view all parameters by alphabetical order
        option_dict = st.radio("Select an Option", ["View Parameters by Subsystem", "View All Parameters"])
        if option_dict == "View Parameters by Subsystem":
            # write the title of the section in bold
            st.write("### Amplifier Parameters")
            # add explanation of the parameters "Measured Power" and "Expected Power" in bold
            st.write("#### Expected Power TX1/TX2")
            st.write("Measured power of the amplifier transmit channel (TX) 1 or 2 in Watss")
            st.write("#### Expected Power")
            st.write("Expected power of the amplifier transmit channel (TX) 1 or 2 in Watts")
            st.write("#### M/E Ratio TX1/TX2")
            st.write("Measured/expected power ratio of the amplifier transmit channel (TX) 1 or 2")


            st.write("### Circulator Parameters")
            

        elif option_dict == "View All Parameters":
            # display the list of parameters from the list_parameters.txt file
            st.write("## All Parameters")
            for parameter in list_parameters_and_roots:
                st.write(parameter)

    # About page
    elif selection == "About":
        st.title("About")
        st.write("This program visualizes parameter data extracted from three Philips MRI scanner system files in the Amsterdam UMC for the purpose of monitoring scanner performance.")
        # link to a dictionary of terms
        st.write("In this program, you can view the historical parameters data from 2019 to 2023 on an interactive [dashboard](#data-dashboard). You can also learn about the parameters in the [parameter dictionary](#parameter-dictionary). For more information, please contact the author.")

    # Contact page
    elif selection == "Contact":
        st.title("Contact")
        st.write("Author: Jiaxu Zhang")
        st.write("Email: jiaxuzhangjx@gmail.com")



if __name__ == "__main__":
    main()
