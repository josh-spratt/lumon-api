# Lumon API: Phase 2 Development Specification

## 1. Overview

The objective of Phase 2 is to evolve the Lumon API from a read-only proof-of-concept into a dynamic, persistent, and secure application. This phase will re-introduce a database for data persistence, implement full Create, Read, Update, and Delete (CRUD) functionality, and add a layer of authentication to protect the endpoints.

## 2. Core Requirements

### 2.1. Database Integration and Persistence
The current implementation using a static `employees.json` file is a significant limitation. This requirement brings back a proper database, which is essential for any dynamic application.

*   **Technology:** Re-integrate `Flask-SQLAlchemy` to manage database interactions.
*   **Production Database:** The setup will continue to be optimized for Heroku, using PostgreSQL as the production database. The `DATABASE_URL` environment variable will be used to configure the connection.
*   **Local Development:** For ease of local development, the application will default to using a local SQLite database (`app.db`) if `DATABASE_URL` is not set.
*   **Data Model:** The `Employee` model will be re-introduced to define the structure of the data in the database.

### 2.2. Full CRUD Functionality
To make the API interactive, we will implement endpoints to modify data.

*   **Create Employee:**
    *   `POST /lumon-api/employees`
    *   **Body:** JSON object representing a new employee.
    *   **Response:** The newly created employee object with its database-assigned ID.
*   **Update Employee:**
    *   `PUT /lumon-api/employees/{id}`
    *   **Body:** JSON object with the fields to update.
    *   **Response:** The full, updated employee object.
*   **Delete Employee:**
    *   `DELETE /lumon-api/employees/{id}`
    *   **Response:** A success message or a `204 No Content` status.

### 2.3. API Authentication
With the ability to modify data, it's critical to secure the endpoints. A simple and effective first step is API Key authentication.

*   **Mechanism:** All `POST`, `PUT`, and `DELETE` requests must include a valid API key.
*   **Implementation:** The key will be passed in a request header, for example: `X-API-Key: <your-secret-key>`.
*   **Configuration:** The server will validate the key against a secret key stored in an environment variable (`LUMON_API_KEY`), ensuring no secrets are hardcoded in the source code.
*   **Access Control:** All API endpoints, including `GET` requests, are protected and require authentication.

### 2.4. Thematic Endpoint: Mode Switching
To lean into the *Severance* theme, a dedicated endpoint will be created to manage an employee's "innie" or "outie" state.

*   **Toggle Mode:**
    *   `POST /lumon-api/employees/{id}/toggle-mode`
    *   **Action:** This endpoint will switch an employee's `mode` between `'innie'` and `'outie'`.
    *   **Response:** The updated employee object showing the new mode.
    *   **Authentication:** This endpoint will also be protected by the API key.

## 3. Updated Data Model

The `Employee` model will be defined in `app.py` as follows:

```python
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    is_severed = db.Column(db.Boolean, default=False)
    mode = db.Column(db.String(20), default='outie') # 'innie' or 'outie'
```

## 4. Configuration

The following environment variables will be used for configuration:

*   `DATABASE_URL`: The connection string for the PostgreSQL database on Heroku.
*   `LUMON_API_KEY`: The secret key for authenticating write-access to the API.

## 5. Definition of Done for Phase 2

*   The application uses a database for all data operations.
*   `POST`, `PUT`, and `DELETE` endpoints are implemented and fully functional.
*   The `toggle-mode` endpoint is implemented.
*   Write-access endpoints are secured and reject any request without a valid API key.
*   The `README.md` is updated with instructions for the new endpoints and authentication mechanism.
*   The test suite is expanded to cover all new functionality, including authentication checks.
*   The updated application is successfully deployed and running on Heroku.
