import sys
from sqlalchemy import MetaData, Table, update
from sqlalchemy.orm import sessionmaker
from .db_config import engine, SessionLocal

def update_table(table_name, update_data, condition):
    session = SessionLocal()
    try:
        table = Table(table_name.lower(), MetaData(), autoload_with=engine)
        stmt = update(table).where(condition).values(update_data)
        session.execute(stmt)
        session.commit()
        print(f"Table '{table_name}' updated successfully!")
    except Exception as e:
        session.rollback()
        print(f"Error updating table: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python -m src.my_project.db.update_table <table_name> <update_data> <condition>")
    else:
        table_name = sys.argv[1]
        update_data = eval(sys.argv[2])  # Example: "{'fname': 'UpdatedName'}"
        condition = eval(sys.argv[3])  # Example: "table.c.id == 1"
        update_table(table_name, update_data, condition)