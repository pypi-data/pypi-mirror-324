from flask import Blueprint
from apps.app1.controllers import get_data_workflow, get_data_simulated_data, post_data_workflow, post_data_simulated_data

app1 = Blueprint('app1', __name__)

@app1.route('/getDataWorkflow', methods=['GET'])
def get_data_workflow_route():
    return get_data_workflow()

@app1.route('/getDataSimulatedData', methods=['GET'])
def get_data_simulated_data_route():
    return get_data_simulated_data()

@app1.route('/postDataWorkflow', methods=['POST'])
def post_data_workflow_route():
    return post_data_workflow()

@app1.route('/postDataSimulatedData', methods=['POST'])
def post_data_simulated_data_route():
    return post_data_simulated_data()