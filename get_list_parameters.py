import os
import pandas as pd

def get_parameter_file_map(directory_path):
    parameter_file_map = {}  # Dictionary to store parameter-file mapping
    
    # Traverse through the directory and its subdirectories
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(root, file)
                
                # Read CSV file to get column names (parameters)
                df = pd.read_csv(file_path, nrows=0)  # Read only the header row
                parameters = set(df.columns)
                
                # Update parameter-file map
                for param in parameters:
                    parameter_file_map[param] = file_path
    
    return parameter_file_map

def save_parameter_file_map(mapping, output_file):
    with open(output_file, 'w') as file:
        for param, file_path in mapping.items():
            file.write(f"{param}: {file_path}\n")

if __name__ == "__main__":
    # Define directory path
    directory_path = "data"

    # Get parameter-file map
    parameter_file_map = get_parameter_file_map(directory_path)

    # Save parameter-file map to a text file
    output_file = "parameter_file_map.txt"
    save_parameter_file_map(parameter_file_map, output_file)
    
    print(f"Parameter-file map saved to {output_file}")
