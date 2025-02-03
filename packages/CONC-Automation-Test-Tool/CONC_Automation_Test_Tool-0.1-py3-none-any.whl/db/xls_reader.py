import pandas as pd

def get_table_schema(xls_file, sheet_name):
    df = pd.read_excel(xls_file, sheet_name=sheet_name)
    columns = df.columns.tolist()
    data_types = df.dtypes.tolist()
    return columns, data_types