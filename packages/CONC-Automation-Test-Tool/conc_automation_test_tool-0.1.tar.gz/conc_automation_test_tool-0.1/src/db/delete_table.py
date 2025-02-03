import sys
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import declarative_base
from .db_config import engine

Base = declarative_base()

def delete_table(table_name):
    metadata = MetaData()
    metadata.reflect(bind=engine)
    if table_name.lower() in metadata.tables:
        table = Table(table_name.lower(), metadata, autoload_with=engine)
        table.drop(engine)
        print(f"Table '{table_name}' deleted successfully!")
    else:
        print(f"Table '{table_name}' does not exist.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python -m src.my_project.db.delete_table <table_name>")
    else:
        table_name = sys.argv[1]
        delete_table(table_name)