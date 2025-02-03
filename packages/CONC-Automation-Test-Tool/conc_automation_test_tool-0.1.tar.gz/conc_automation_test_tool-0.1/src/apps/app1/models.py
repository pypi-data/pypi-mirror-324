from sqlalchemy import Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from config.db_config import db

class WorkFlow(db.Model):
    __tablename__ = 'workflow'
    WorkflowUID = Column(String, primary_key=True, unique=True, nullable=False)
    Workflow = Column(String, nullable=False)
    Step = Column(Integer, nullable=False)
    Mock_Factor = Column(Integer, nullable=False)
    Batch_Number = Column(Integer, nullable=False)
    Input_type = Column(String, nullable=False)
    REST_input = Column(JSON)  # list of JSON blobs
    Kafka_Input = Column(JSON)  # list of Kafka topics
    Input_Mock_type = Column(JSON)  # list of JSON blobs
    Output_type = Column(JSON, nullable=False)  # list of JSON blobs
    Output_Sample_Content = Column(JSON)  # list of JSON blobs
    Output_Mock_type = Column(JSON)  # list of JSON blobs
    Dependent_Rest_APIs = Column(JSON)  # list of JSON blobs
    Dependent_DBData = Column(JSON)  # list of JSON blobs
    total_expected_runs = Column(Integer, nullable=False)
    noOfExecutions_done = Column(Integer, nullable=False)
    Status = Column(String, nullable=False)

    simulated_data = relationship("SimulatedData", back_populates="workflow")

class SimulatedData(db.Model):
    __tablename__ = 'simulated_data'
    id = Column(Integer, primary_key=True, index=True)
    workflow_UID = Column(String, ForeignKey('workflow.WorkflowUID'), nullable=False)
    Input_SimulatedData = Column(JSON, nullable=False)  # list of JSON blobs
    Output_SimulatedData = Column(JSON, nullable=False)  # list of JSON blobs
    ValidationStatus = Column(String, nullable=False)
    Step_Number = Column(Integer, nullable=False)

    workflow = relationship("WorkFlow", back_populates="simulated_data")