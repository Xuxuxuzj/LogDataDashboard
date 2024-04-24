import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

def list_subdirectories(directory):
    subdirectories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    # sort subdirectories in ascending order
    subdirectories.sort()
    return subdirectories

def display_amplifier_parameters():
    pass


def view_historical_data():
    st.write("## View Historical Data")

    # Define directory path
    data_dir = "Data"

    # List scanner directories
    scanner_dirs = [dir for dir in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, dir))]

    if not scanner_dirs:
        st.warning("No scanner directories found in the 'Data' directory.")
        return

    # Let user select a scanner
    selected_scanner = st.selectbox("Select a Scanner", ["Alpha", "Omega", "Ingenia"])

    # Let user search for a parameter or select from the list
    st.write("### Select a subsystem of the scanner to view its parameters")
    # list of sbusystems
    list_subsystems = ["Amplifier", "Circulator", "RF Coil", "Cooling System", "Magnet", "Room", "Spikes", "Exam and Scan Summary"]
    # sort subsystems in ascending order
    list_subsystems.sort()
    # display all subsystems as links to a page that shows all parameters of this subsystem
    for subsystem in list_subsystems:
        st.write(f"- [{subsystem}](#{subsystem.replace(' ', '-').lower()})")

    # link a page to view the data model of all parameters with URL hash
    st.write("To learn about all subsystems parameters, see the parameter dictionary [here](#parameter-dictionary).")

    # search for a parameter
    st.write("### Search for a parameter")
    search_parameter = st.text_input("Alternatively, search for a known parameter from the [parameter dictionary](#parameter-dictionary):")
    if search_parameter:
        list_subsystems = [subsystem for subsystem in list_subsystems if search_parameter.lower() in subsystem.lower()]
    
    # import the list of parameters and roots
    with open('list_parameters.txt', 'r') as file:
        list_parameters_and_roots = file.readlines()
    # get a list of parameters

    list_parameters = [parameter.split(":")[0].strip() for parameter in list_parameters_and_roots]

    # if user selects a subsystem, only show parameters from that subsystem
    if select_subsystem:
        if select_subsystem == "Amplifier":
            pass
            # display amplifier parameters

        elif select_subsystem == "Circulator":
            list_parameters = [parameter for parameter in list_parameters if "Circulator" in parameter]
        elif select_subsystem == "RF Coil":
            list_parameters = [parameter for parameter in list_parameters if "RF Coil" in parameter]
        elif select_subsystem == "Cooling System":
            list_parameters = [parameter for parameter in list_parameters if "Cooling System" in parameter]
        elif select_subsystem == "Magnet":
            list_parameters = [parameter for parameter in list_parameters if "Magnet" in parameter]
        elif select_subsystem == "Room":
            list_parameters = [parameter for parameter in list_parameters if "Room" in parameter]
        elif select_subsystem == "Spikes":
            list_parameters = [parameter for parameter in list_parameters if "Spikes" in parameter]
        # map the select subsystem to a csv file
    elif search_parameter:
        pass
        # map the search parameter to a csv file




    if search_parameter:
        list_parameters = [parameter for parameter in list_parameters if search_parameter.lower() in parameter.lower()]
    # or select from the list
    selected_parameter = st.selectbox("Select a Parameter", list_parameters)


    if not csv_files:
        st.warning(f"No CSV files found in the '{selected_scanner}' directory.")
        return

    # Let user select a CSV file with size limit of 500MB
    selected_file = st.selectbox(f"Select a CSV file from {selected_scanner}", csv_files)

    # Read selected CSV file into pandas DataFrame
    df = pd.read_csv(os.path.join(data_dir, selected_scanner, selected_file))

    # Display DataFrame
    st.write("## DataFrame")
    st.write(df)

    # Display trends for each column
    st.write("## Column Trends")

    for column in df.columns:
        st.write(f"### {column}")
        
        # Plot column data
        fig, ax = plt.subplots()
        ax.plot(df[column])
        ax.set_title(column)
        ax.set_xlabel("Index")
        ax.set_ylabel("Value")
        
        st.pyplot(fig)

def process_new_log_file():
    # prompt user to upload a new .log file less than 500MB
    st.write("## Process New Log File")
    uploaded_file = st.file_uploader("Upload a new log file", type=["log"])


def main():
# Create a sidebar with links
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", ["Home", "Data Dashboard", "Parameter Dictionary", "About", "Contact"])


    # Home page
    if selection == "Home":
        st.title("Log Visualizer Home Page")
        st.write("Welcome to Log Visualizer!")
            # Display two options, one for "View Historical Data" and another for "Process New Log File"
        option = st.radio("Select an Option", ["View Historical Data", "Process New Log File"])

        if option == "View Historical Data":
            view_historical_data()
        else:
            process_new_log_file()
    
    # Data Dashboard page
    elif selection == "Data Dashboard":
        st.title("Data Dashboard")
        st.write("This page displays the data dashboard.")
        # Display a data dashboard
        st.write("## Data Dashboard")
        st.write("This is the data dashboard.")
    
    # Parameter Dictionary page
    elif selection == "Parameter Dictionary":
        st.title("Parameter Dictionary")
        st.write("This page displays the dictionary of parameters.")

        # Read the list of parameters from list_parameters.txt
        with open('list_parameters.txt', 'r') as file:
            for line in file:
                st.write(line)

    # About page
    elif selection == "About":
        st.title("About")
        st.write("This program visualizes parameter data from three Philips MRI scanner system files in the Amsterdam UMC. The parameters are used to monitor scanner performance.")
        # link to a dictionary of terms
        st.write("## Dictionary of Parameters")
        st.write("A dictionary of parameters can be found [here](https://www.google.com).")

    # Contact page
    elif selection == "Contact":
        st.title("Contact")
        st.write("Author: Jiaxu Zhang")
        st.write("Email: jiaxuzhangjx@gmail.com")


    
    


if __name__ == "__main__":
    main()
