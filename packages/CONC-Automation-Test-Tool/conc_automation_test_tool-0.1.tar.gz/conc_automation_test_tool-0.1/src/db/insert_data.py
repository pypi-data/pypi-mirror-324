import inspect
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from config.db_config import db, engine, SessionLocal
from apps.app1.models import WorkFlow, SimulatedData  # Import the models

def get_table_classes(base):
    """Get all table classes defined in the schema."""
    table_classes = []
    for name, cls in inspect.getmembers(base, inspect.isclass):
        print(f"Inspecting class: {name}")
        if issubclass(cls, base) and hasattr(cls, '__tablename__'):
            table_classes.append(cls)
            print(f"Identified table class: {name} with tablename: {cls.__tablename__}")
    return table_classes

def insert_dummy_data():
    session = SessionLocal()
    try:
        # Create dummy data for the WorkFlow table
        workflow_data = [
            WorkFlow(
                WorkflowUID="UID1",
                Workflow="circuitCollection",
                Step=1,
                Mock_Factor=100,
                Batch_Number=25,
                Input_type="Kafka",
                REST_input=None,
                Kafka_Input=["topic1", "topic2"],
                Input_Mock_type=[{"attributeName": "deviceID", "attributeType": ""}],
                Output_type="Kafka",
                Output_Sample_Content=[{"attributeName": "deviceID", "attributeType": ""}],
                Output_Mock_type=[{"attributeName": "deviceID", "attributeType": ""}],
                Dependent_Rest_APIs=None,
                Dependent_DBData=None,
                total_expected_runs=300,
                noOfExecutions_done=1,
                Status="completed"
            ),
            WorkFlow(
                WorkflowUID="UID2",
                Workflow="circuitCollection",
                Step=2,
                Mock_Factor=100,
                Batch_Number=25,
                Input_type="Kafka",
                REST_input=None,
                Kafka_Input=["topic3", "topic4"],
                Input_Mock_type=[{"attributeName": "deviceID", "attributeType": ""}],
                Output_type="Kafka",
                Output_Sample_Content=[{"attributeName": "deviceID", "attributeType": ""}],
                Output_Mock_type=[{"attributeName": "deviceID", "attributeType": ""}],
                Dependent_Rest_APIs=[{"url": "", "reqtype": "", "payload": "", "queryParam": [""]}],
                Dependent_DBData=None,
                total_expected_runs=300,
                noOfExecutions_done=1,
                Status="inprogress"
            )
        ]

        # Insert data into the WorkFlow table
        session.bulk_save_objects(workflow_data)
        session.commit()
        print("Dummy data inserted successfully into the WorkFlow table!")

        # Create dummy data for the SimulatedData table
        simulated_data = [
            SimulatedData(
                workflow_UID="UID1",
                Input_SimulatedData=[{"attributeName": "deviceID", "attributeValue": "xxx"}],
                Output_SimulatedData=[{"attributeName": "", "attributeValue": ""}],
                ValidationStatus="completed",
                Step_Number=1
            ),
            SimulatedData(
                workflow_UID="UID2",
                Input_SimulatedData=[{"attributeName": "deviceID", "attributeValue": "xxx"}],
                Output_SimulatedData=[{"attributeName": "", "attributeValue": ""}],
                ValidationStatus="inprogress",
                Step_Number=2
            )
        ]

        # Insert data into the SimulatedData table
        session.bulk_save_objects(simulated_data)
        session.commit()
        print("Dummy data inserted successfully into the SimulatedData table!")

    except Exception as e:
        session.rollback()
        print(f"Error inserting data: {e}")
    finally:
        session.close()

if __name__ == "__main__":
    insert_dummy_data()