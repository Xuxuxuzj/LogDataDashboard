import streamlit as st
import os

def display_parameter_dictionary():
    # get list of parameters and roots
    with open('list_parameters.txt', 'r') as file:
        list_parameters_and_roots = file.readlines()
    
    # Title of the page
    st.title("Parameter Dictionary")
    st.write("### This page displays the dictionary of parameters.")
    
    # display two options to view by subsystem or view all parameters by alphabetical order
    option_dict = st.radio("Select an Option", ["View Parameters by Subsystem", "View All Parameters"])
    if option_dict == "View Parameters by Subsystem":
        # write the title of the section in bold
        st.write("### Amplifier Parameters")
        # add explanation of the parameters "Measured Power" and "Expected Power" in bold
        st.write("##### Expected Power TX1/TX2")
        st.write("Expected power of the amplifier transmit channel (TX) 1 or 2 in Watss")
        st.write("##### Measured Power TX1/TX2")
        st.write("Measured power of the amplifier transmit channel (TX) 1 or 2 in Watts")
        st.write("##### M/E Ratio TX1/TX2")
        st.write("Measured/expected power ratio of the amplifier transmit channel (TX) 1 or 2")
        st.write("### Circulator Parameters")
        

    elif option_dict == "View All Parameters":
        # display the list of parameters from the list_parameters.txt file
        st.write("## All Parameters")
        for parameter in list_parameters_and_roots:
            st.write(parameter)