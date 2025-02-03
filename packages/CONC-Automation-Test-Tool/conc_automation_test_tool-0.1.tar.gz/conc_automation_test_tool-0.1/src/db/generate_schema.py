import pandas as pd
from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime
import os

def map_dtype(dtype):
    """Map pandas dtype to SQLAlchemy Column type."""
    if dtype == 'int64':
        return 'Integer'
    elif dtype == 'float64':
        return 'Float'
    elif dtype == 'bool':
        return 'Boolean'
    elif dtype == 'datetime64[ns]':
        return 'DateTime'
    elif dtype == 'object':
        return 'String'
    else:
        return 'String'

def generate_schema(xls_file, output_file):
    """Generate SQLAlchemy schema from XLSX file."""
    if not os.path.exists(xls_file):
        print(f"Error: File '{xls_file}' not found.")
        return

    available_sheets = pd.ExcelFile(xls_file).sheet_names
    print(f"Available sheets in the XLS file: {available_sheets}")

    with open(output_file, 'w') as f:
        f.write("from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime\n")
        f.write("from sqlalchemy.ext.declarative import declarative_base\n\n")
        f.write("Base = declarative_base()\n\n")

        for sheet_name in available_sheets:
            df = pd.read_excel(xls_file, sheet_name=sheet_name)
            columns = df.columns.tolist()
            data_types = df.dtypes.tolist()

            f.write(f"class {sheet_name.capitalize()}(Base):\n")
            f.write(f"    __tablename__ = '{sheet_name.lower()}'\n")
            f.write(f"    id = Column(Integer, primary_key=True, index=True)\n")
            for col, dtype in zip(columns, data_types):
                if col != 'id':  # Ensure we don't overwrite the primary key column
                    f.write(f"    {col} = Column({map_dtype(dtype)})\n")
            f.write("\n")

    print(f"Schema created successfully and saved to {output_file}")

if __name__ == "__main__":
    xls_file = '/Users/printrip/Desktop/Code/CISCO_DSE/conc_automation_test_tool/src/my_project/db/test.xlsx'
    output_file = '/Users/printrip/Desktop/Code/CISCO_DSE/conc_automation_test_tool/src/my_project/db/schema.py'
    generate_schema(xls_file, output_file)