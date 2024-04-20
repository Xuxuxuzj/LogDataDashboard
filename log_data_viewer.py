import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import os

def list_subdirectories(directory):
    subdirectories = [name for name in os.listdir(directory) if os.path.isdir(os.path.join(directory, name))]
    # sort subdirectories in ascending order
    subdirectories.sort()
    return subdirectories

def main():
    st.title("MRI Log Parameter Viewer")

    # Define directory path
    data_dir = "Data"

    # List scanner directories
    scanner_dirs = [dir for dir in os.listdir(data_dir) if os.path.isdir(os.path.join(data_dir, dir))]

    if not scanner_dirs:
        st.warning("No scanner directories found in the 'Data' directory.")
        return

    # Let user select a scanner
    selected_scanner = st.selectbox("Select a Scanner", scanner_dirs)

    # List all CSV files in the selected scanner directory
    csv_files = [file for file in os.listdir(os.path.join(data_dir, selected_scanner)) if file.endswith('.csv')]

    if not csv_files:
        st.warning(f"No CSV files found in the '{selected_scanner}' directory.")
        return
    
    # Let user select a parameter
    subdirectories = list_subdirectories(data_dir)
    selected_parameter = st.selectbox("Select a Parameter", ["Temperature", "Pressure", "Flow Rate"])

    # Let user select a CSV file
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

if __name__ == "__main__":
    main()
