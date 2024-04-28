import streamlit as st
import functions as f
import dashboard_page as db
import parameter_dictionary_page as pd

# This script contains the main structure of the user-interface of the Log Data Visualizer program.

def main():

    # Create a sidebar with options
    st.sidebar.title("Menu")
    selection = st.sidebar.radio("Go to", ["Data Visualizer", "Parameter Dictionary", "About", "Contact"])

    # Home page
    if selection == "Data Visualizer":
        db.display_data_dashboard()
    
    # Parameter Dictionary page
    elif selection == "Parameter Dictionary":
        pd.display_parameter_dictionary()
        

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
