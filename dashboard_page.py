import streamlit as st
import functions as f
import data_visualizer as dv

# This script contains the main functions of the home page

def display_data_dashboard():
    
    st.title("Log Data Visualizer")
    st.write("Welcome to Log Data Visualizer!")
    # Display two options, one for "View Historical Data" and another for "Process New Log File"
    option = st.radio("Select an Option", ["View Historical Data", "Process New Log File"])

    if option == "View Historical Data":
        view_historical_data()
    else:
        process_new_log_file()

def view_historical_data():
    # Initialize list of subsystems
    list_subsystems = ["Amplifier", "Circulator", "RF Coil"]
    # sort subsystems in ascending order
    list_subsystems.sort()
    
    st.write("## View Historical Data")

    # Let user select a scanner and a subsystem
    col1, col2 = st.columns(2)

    with col1:
        selected_scanner = st.selectbox("Select a Scanner", ["Alpha", "Omega", "Ingenia"])

    with col2:
        selected_subsystem = st.selectbox("Select a Subsystem", list_subsystems)

    # get the directory of the scanner
    scanner_dir = "Demo_Data\\" + "Data_" + selected_scanner + "\\" + selected_subsystem

    # visualize the parameters of based on the selected subsystem
    if selected_subsystem == "RF Coil":
        dv.visualize_coil_parameters(scanner_dir, selected_subsystem)
    else:
        dv.visualize_other_parameters(scanner_dir, selected_subsystem)

def process_new_log_file():
    # prompt user to upload a new .log file less than 500MB
    st.write("## Process New Log File")
    uploaded_file = st.file_uploader("Upload a new log file", type=["log"])