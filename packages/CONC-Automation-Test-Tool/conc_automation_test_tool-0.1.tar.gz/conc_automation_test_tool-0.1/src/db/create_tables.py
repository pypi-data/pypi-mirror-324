import inspect
from sqlalchemy import MetaData
from sqlalchemy.orm import sessionmaker
from config.db_config import db
from apps.app1.models import WorkFlow, SimulatedData
from apps.app2.models import AnotherTable
from config.settings import app  # Import the Flask app

def create_tables():
    with app.app_context():
        db.init_app(app)  # Ensure the db is initialized with the app
        db.create_all()  # Create all tables
        print("Tables created successfully!")

if __name__ == "__main__":
    create_tables()