# CONC-Automation-Test-Tool

This project aims to establish a unified, automated testing framework for feature, nightly, and scale tests tailored to each microservice, eliminating node setup dependencies. It involves key microservice components like Kafka messaging, REST calls, cache, and database interactions, orchestrated to ensure thorough validation of microservice functionalities. The framework utilizes a Test Orchestrator to automate test inputs, execute workflows, and validate outputs by leveraging dynamically generated orchestration XLS files. Additionally, it supports concurrent testing of multiple microservices on virtual machines, enabling faster test execution and seamless integration of new features and regression tests.

## Features
- Modular code structure in the `src/` directory.
- Unit tests in the `tests/` folder.
- Configurations separated in the `config/` directory.
- Comprehensive documentation in `docs/`.

## Setup Instructions

### Prerequisites

1. **Python 3.6+**: Ensure you have Python 3.6 or higher installed on your machine.
2. **PostgreSQL**: Ensure you have PostgreSQL installed and running.

### Step-by-Step Instructions

1. **Clone the Repository**:
    ```bash
    git clone <repository_url>
    cd conc_automation_test_tool
    ```

2. **Create and Activate a Virtual Environment**:
    ```bash
    python3 -m venv venv
    source venv/bin/activate  # On Windows: .\venv\Scripts\activate
    ```

3. **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

4. **Configure Environment Variables**:
    Create a [.env](http://_vscodecontentref_/2) file in the root directory of the project. This file will store your environment variables, such as database connection details and secret keys.

    ```bash
    touch .env
    ```

    Add the following content to the [.env](http://_vscodecontentref_/3) file:

    ```
    DATABASE_URL=postgresql://myuser:prince123@localhost/test1
    SECRET_KEY=your_secret_key
    ```

    Replace `myuser`, `prince123`, `localhost`, and `test1` with your actual PostgreSQL username, password, host, and database name, respectively. Replace `your_secret_key` with a secret key of your choice.

5. **Set Up the Database**:

    - **Define Models**:
        The database schema is defined in the `models.py` file located in [app1](http://_vscodecontentref_/4). Ensure that the models are correctly defined.

    - **Create Tables**:
        Run the `create_tables.py` script to create the tables in the database.

        ```bash
        export PYTHONPATH=$(pwd)/src
        python -m db.create_tables
        ```

6. **Running the Flask Application**:
    Start the Flask application by running the `run.py` script.

    ```bash
    python src/run.py
    ```

    The application will start, and you can access it at `http://127.0.0.1:5000`.

7. **Accessing API Endpoints**:
    The following API endpoints are available:

    #### GET Requests

    - **GET `/api/v1/getDataWorkflow`**: Fetch data from the `WorkFlow` table.
      ```bash
      curl http://127.0.0.1:5000/api/v1/getDataWorkflow
      ```

    - **GET `/api/v1/getDataSimulatedData`**: Fetch data from the `SimulatedData` table.
      ```bash
      curl http://127.0.0.1:5000/api/v1/getDataSimulatedData
      ```

    #### POST Requests

    - **POST `/api/v1/postDataWorkflow`**: Insert records into the `WorkFlow` table.
      ```bash
      curl -X POST -H "Content-Type: application/json" -d '{"WorkflowUID": "UID3", "Workflow": "newWorkflow", "Step": 3, "Mock_Factor": 50, "Batch_Number": 10, "Input_type": "REST", "REST_input": [{"attributeName": "deviceID", "attributeValue": "123"}], "Kafka_Input": [], "Input_Mock_type": [{"attributeName": "deviceID", "attributeType": ""}], "Output_type": "REST", "Output_Sample_Content": [{"attributeName": "deviceID", "attributeType": ""}], "Output_Mock_type": [{"attributeName": "deviceID", "attributeType": ""}], "Dependent_Rest_APIs": [], "Dependent_DBData": [], "total_expected_runs": 100, "noOfExecutions_done": 0, "Status": "pending"}' http://127.0.0.1:5000/api/v1/postDataWorkflow
      ```

    - **POST `/api/v1/postDataSimulatedData`**: Insert records into the `SimulatedData` table.
      ```bash
      curl -X POST -H "Content-Type: application/json" -d '{"workflow_UID": "UID3", "Input_SimulatedData": [{"attributeName": "deviceID", "attributeValue": "123"}], "Output_SimulatedData": [{"attributeName": "", "attributeValue": ""}], "ValidationStatus": "pending", "Step_Number": 3}' http://127.0.0.1:5000/api/v1/postDataSimulatedData
      ```

8. **Inserting Dummy Data**:
    Run the `insert_data.py` script to insert dummy data into the database.

    ```bash
    export PYTHONPATH=$(pwd)/src
    python -m db.insert_data
    ```

## Project Structure
```plaintext
src/
├── apps/
│   ├── app1/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── controllers.py
│   │   ├── routes.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_app1.py
│   ├── app2/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── controllers.py
│   │   ├── routes.py
│   │   └── tests/
│   │       ├── __init__.py
│   │       └── test_app2.py
│   └── __init__.py
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── db_config.py
├── db/
│   ├── __init__.py
│   ├── generate_schema.py
│   ├── create_tables.py
│   ├── insert_data.py
│   ├── delete_table.py
│   ├── update_table.py
│   └── schema.py
├── docs/
│   └── db_readme.md
├── utils/
│   ├── __init__.py
│   └── utility_scripts.py
├── tests/
│   ├── __init__.py
│   └── test_all.py
├── venv/  # Virtual environment folder
├── .gitignore
├── requirements.txt
├── README.md
└── run.py
```

## License
This project is licensed under the [MIT License](LICENSE).
