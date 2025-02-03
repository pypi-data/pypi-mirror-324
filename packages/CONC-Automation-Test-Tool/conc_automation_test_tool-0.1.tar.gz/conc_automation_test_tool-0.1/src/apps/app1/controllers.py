# Define your controller functions here
from flask import request, jsonify
from config.db_config import db
from apps.app1.models import WorkFlow, SimulatedData

def get_data_workflow():
    workflows = WorkFlow.query.all()
    return jsonify([workflow.to_dict() for workflow in workflows])

def get_data_simulated_data():
    simulated_data = SimulatedData.query.all()
    return jsonify([data.to_dict() for data in simulated_data])

def post_data_workflow():
    data = request.get_json()
    new_workflow = WorkFlow(**data)
    db.session.add(new_workflow)
    db.session.commit()
    return jsonify(new_workflow.to_dict()), 201

def post_data_simulated_data():
    data = request.get_json()
    new_simulated_data = SimulatedData(**data)
    db.session.add(new_simulated_data)
    db.session.commit()
    return jsonify(new_simulated_data.to_dict()), 201

# Helper method to convert SQLAlchemy objects to dictionaries
def to_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

WorkFlow.to_dict = to_dict
SimulatedData.to_dict = to_dict