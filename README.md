# Severance API Project

This project implements a basic API inspired by the Apple TV show *Severance*, focusing on employee management. It now uses SQLAlchemy for database persistence.

## Setup Instructions

To run this project locally, follow these steps:

### 1. Clone the repository (if you haven't already)

```bash
# git clone <repository-url>
# cd severance-project
```

### 2. Create and Activate a Python Virtual Environment

It's recommended to use a virtual environment to manage project dependencies.

```bash
python3 -m venv venv
```

**Activate the virtual environment:**

*   **On macOS and Linux:**
    ```bash
    source venv/bin/activate
    ```
*   **On Windows (Command Prompt):**
    ```bash
    venv\Scripts\activate.bat
    ```
*   **On Windows (PowerShell):
    ```powershell
    venv\Scripts\Activate.ps1
    ```

### 3. Install Dependencies

With your virtual environment activated, install the required packages:

```bash
pip install -r requirements.txt
```

### 4. Initialize the Database

The application uses SQLAlchemy. Locally, it defaults to a SQLite database named `app.db`. You need to initialize the database schema by running the `init-db` command:

```bash
export FLASK_APP=app.py
flask init-db
```
This command will create the `app.db` file and pre-populate it with sample employee data if it's empty.

### 5. Run the Application

To start the Flask development server:

```bash
export FLASK_APP=app.py
flask run
```

The API will typically be available at `http://127.0.0.1:5000/`.

### 6. Run Tests

To execute the unit tests for the application (which use an in-memory SQLite database for isolation):

```bash
pytest
```

---

## Deployment to Heroku

This application is configured for easy deployment to Heroku using a `Procfile` and a PostgreSQL database.

1.  **Ensure you have the Heroku CLI installed** and are logged in.
2.  **Create a Heroku app:**
    ```bash
    heroku create my-severance-api-app # Replace with your unique app name
    ```
3.  **Add the Heroku Postgres add-on (Hobby Dev - free tier):**
    ```bash
    heroku addons:create heroku-postgresql:hobby-dev
    ```
    This will automatically set the `DATABASE_URL` environment variable for your app.
4.  **Push your code to Heroku:**
    ```bash
    git push heroku main
    ```
5.  **Initialize the database on Heroku:**
    ```bash
    heroku run flask init-db
    ```
    This command runs `init_db()` on a one-off dyno, creating your database tables and populating them.
6.  **Open your app:**
    ```bash
    heroku open
    ```
    Your API will be live at the URL provided by Heroku.

---

## API Endpoints

| Method | Endpoint                  | Description                |
|--------|---------------------------|----------------------------|
| `GET`    | `/api/employees`          | Get a list of all employees. |
| `GET`    | `/api/employees/{id}`     | Get a single employee by ID. |
| `POST`   | `/api/employees`          | Create a new employee.     |
| `PUT`    | `/api/employees/{id}`     | Update an employee's details.|
| `DELETE` | `/api/employees/{id}`     | Delete an employee.        |

---

## Versioning and Releases

This project follows semantic versioning (`major.minor.patch`). To create a new release, use the `bump2version` tool.

First, make sure you have installed the project dependencies, including `bump2version`.

To bump the version, use one of the following commands:
```bash
# Bump a patch version (e.g., 0.1.0 -> 0.1.1)
bump2version patch

# Bump a minor version (e.g., 0.1.1 -> 0.2.0)
bump2version minor

# Bump a major version (e.g., 0.2.0 -> 1.0.0)
bump2version major
```

This will automatically update the version in `app.py`, create a new Git commit, and tag the commit with the new version (e.g., `v1.0.0`).

To trigger the automated release workflow, push the newly created tag to GitHub:
```bash
git push --tags
```
This will trigger a GitHub Action that creates a new release on the project's GitHub page.