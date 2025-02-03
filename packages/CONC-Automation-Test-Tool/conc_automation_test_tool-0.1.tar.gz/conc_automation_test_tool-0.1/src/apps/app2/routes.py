from flask import Blueprint

app = Blueprint('app2', __name__)

@app.route('/app2')
def index():
    return "Hello from App 2"