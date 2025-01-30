import pandas as pd
import os

def read_streamflow_data(file_name, folder="data/raw", missing_value_handling="drop", delimiter=","):
    """
    Reads streamflow data from a CSV or TXT file.

    Parameters:
    file_name (str): Name of the streamflow data file.
    folder (str, optional): Folder containing the data file. Default is "data/raw".
    missing_value_handling (str, optional): How to handle missing values.
        - "drop": Remove rows with NaN values.
        - "fill": Fill missing values with the mean.
        Default is "drop".
    delimiter (str, optional): Delimiter used in the file. Default is "," for CSV.

    Returns:
    pd.DataFrame: Processed streamflow data.
    """
    file_path = os.path.join(folder, file_name)
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    # Determine the file type
    file_extension = os.path.splitext(file_path)[1].lower()

    # Read the file based on its extension
    if file_extension in [".csv", ".txt"]:
        df = pd.read_csv(file_path, delimiter=delimiter)
    else:
        raise ValueError("Unsupported file format. Only CSV and TXT are supported.")

    # Ensure the first column is the datetime index
    df.iloc[:, 0] = pd.to_datetime(df.iloc[:, 0])
    df.set_index(df.columns[0], inplace=True)

    # Handle missing values
    if missing_value_handling == "drop":
        df = df.dropna()
    elif missing_value_handling == "fill":
        df = df.fillna(df.mean())

    return df
