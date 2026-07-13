import pandas as pd


def get_sheet_names(file_path):
    """
    Returns all sheet names present in the workbook.
    """
    excel_file = pd.ExcelFile(file_path)
    return excel_file.sheet_names


def read_sheet(file_path, sheet_name):

    if sheet_name == "Change Log":

        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            header=2,
            dtype=str
        )

    else:

        df = pd.read_excel(
            file_path,
            sheet_name=sheet_name,
            dtype=str
        )

    # Replace NaN values with empty strings
    df = df.fillna("")

    # Remove leading/trailing spaces from column names
    df.columns = df.columns.str.strip()

    # Convert all cell values to strings and strip spaces
    df = df.astype(str).apply(
        lambda col: col.str.strip()
    )

    return df