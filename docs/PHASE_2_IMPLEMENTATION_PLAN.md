# Lumon API: Phase 2 Implementation Plan

This document outlines the step-by-step plan to implement the features detailed in the `PHASE_2_SPEC.md`. The implementation will proceed in a logical order to ensure a smooth and testable development process.

## Step 1: Foundational Setup - Database and Dependencies

The first priority is to re-introduce the database and restore the project's ability to handle persistent data.

1.  **Update Dependencies:**
    *   Add `Flask-SQLAlchemy` and `psycopg2-binary` back to the `requirements.txt` file. `psycopg2-binary` is required for connecting to Heroku's PostgreSQL database. (COMPLETED)

2.  **Re-configure `app.py` for Database:**
    *   Import `os` and `SQLAlchemy`.
    *   Set up the Flask app configuration to use the `DATABASE_URL` environment variable for the database URI, with a fallback to a local `sqlite:///app.db` file for local development.
    *   Initialize the `db = SQLAlchemy(app)` instance. (COMPLETED)

3.  **Define Data Model:**
    *   Re-implement the `Employee` class in `app.py` as a `db.Model`, exactly as defined in the specification. Include a `to_dict()` method to facilitate JSON serialization. (COMPLETED)

4.  **Create Database Initialization Command:**
    *   Implement an `init-db` Flask CLI command. This command will be responsible for creating the database tables from the models (`db.create_all()`).
    *   To ensure a good developer experience, this command should also pre-populate the database with the initial set of employees if the table is empty. (COMPLETED)

5.  **Remove Static JSON File:**
    *   Delete the `employees.json` file.
    *   Update the `get_employees` and `get_employee` endpoints in `app.py` to query the database using `db.session` instead of reading from the JSON file. (COMPLETED)

## Step 2: Implement API Authentication

Before adding endpoints that modify data, we will implement the authentication layer to ensure security from the start.

1.  **Create an Authentication Decorator:**
    *   In `app.py`, create a Python decorator (e.g., `@api_key_required`).
    *   This decorator will check for the `X-API-Key` header in incoming requests.
    *   It will compare the provided key against the `LUMON_API_KEY` environment variable.
    *   If the key is missing or invalid, it will return a `401 Unauthorized` error. If valid, it will proceed to the decorated route function. (COMPLETED)

## Step 3: Implement CRUD Endpoints (COMPLETED)

With the database and authentication in place, we can now build the endpoints for modifying data.

1.  **Create Employee (`POST`):**
    *   Create the `POST /lumon-api/employees` endpoint.
    *   Apply the `@api_key_required` decorator to this route.
    *   The function will get JSON data from the request, create a new `Employee` object, add it to the `db.session`, and commit.
    *   It will return the newly created employee's data, including its ID.

2.  **Update Employee (`PUT`):**
    *   Create the `PUT /lumon-api/employees/{id}` endpoint.
    *   Apply the `@api_key_required` decorator.
    *   The function will query for the employee by ID. If found, it will update the employee's attributes from the request JSON, commit the changes, and return the updated object.

3.  **Delete Employee (`DELETE`):**
    *   Create the `DELETE /lumon-api/employees/{id}` endpoint.
    *   Apply the `@api_key_required` decorator.
    *   The function will query for the employee by ID, delete it from the `db.session`, and commit. It will return a `204 No Content` response.

4.  **Implement Thematic Endpoint (`toggle-mode`):**
    *   Create the `POST /lumon-api/employees/{id}/toggle-mode` endpoint.
    *   Apply the `@api_key_required` decorator.
    *   The function will find the employee, flip their `mode` from `'innie'` to `'outie'` (or vice versa), commit the change, and return the updated employee object.

## Step 4: Testing and Validation (COMPLETED)

Comprehensive testing is crucial to ensure all new functionality works as expected.

1.  **Update Test Fixture:**
    *   Modify the `pytest` `client` fixture in `tests/test_app.py`. It should be configured to use an in-memory SQLite database (`sqlite:///:memory:`) for test isolation.
    *   The fixture will be responsible for creating the database schema (`db.create_all()`) before each test and tearing it down (`db.drop_all()`) afterward.

2.  **Write New Tests:**
    *   Create tests for all new `POST`, `PUT`, and `DELETE` endpoints.
    *   Write tests for the `toggle-mode` endpoint.
    *   Crucially, write tests for the authentication mechanism. This includes testing that protected endpoints return a `401` error without a key, with an invalid key, and that they succeed with a valid key.

## Step 5: Documentation and Finalization (COMPLETED)

The final step is to update the project's documentation to reflect all the new changes.

1.  **Update `README.md`:**
    *   Add instructions on how to set up and run the database locally (`flask init-db`).
    *   Update the API Endpoints table to include all the new `POST`, `PUT`, and `DELETE` endpoints.
    *   Add a new section explaining how to use API key authentication, including the header name (`X-API-Key`) and the environment variable (`LUMON_API_KEY`).
    *   Add instructions for Heroku deployment, including creating the Postgres add-on and running `heroku run flask init-db`.
2.  **Update `CHANGELOG.md`:**
    *   Add entries for all the new features and improvements under the `[Unreleased]` section.
