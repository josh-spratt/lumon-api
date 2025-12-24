# Gemini CLI Project Configuration

This file provides instructions for the Gemini CLI on how to interact with this project.

## Project Overview

This is a Python-based API server for the Severance project. It uses the Flask framework and SQLAlchemy to provide a full CRUD API for managing employee data. The API is deployed to Heroku and uses a PostgreSQL database in production, with a local SQLite fallback for development. All endpoints are protected by API key authentication. The project uses `pytest` for testing and `bump2version` for semantic versioning.

## Building and Running

### Dependencies

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

### Database Setup

For local development, the database must be initialized once:

```bash
export FLASK_APP=app.py
flask init-db
```

### Running the Application

To run the development server, you must set the `FLASK_APP` and `LUMON_API_KEY` environment variables:

```bash
export FLASK_APP=app.py
export LUMON_API_KEY='your-secret-key-here'
flask run
```

The API will be available at `http://127.0.0.1:5000/`.

### Running Tests

To run the test suite, use:

```bash
FLASK_ENV=testing pytest
```

## Development Conventions

### API Authentication

All API endpoints require an API key to be sent in the `X-API-Key` request header. The key is configured via the `LUMON_API_KEY` environment variable.

### Versioning

This project uses `bump2version` to manage semantic versioning. The version is tracked in `app.py` and `CHANGELOG.md`. To create a new version, use one of the following commands:

```bash
# Bump a patch version (e.g., 3.0.0 -> 3.0.1)
bump2version patch

# Bump a minor version (e.g., 3.0.1 -> 3.1.0)
bump2version minor

# Bump a major version (e.g., 3.1.0 -> 4.0.0)
bump2version major
```

### Releases

New releases are created automatically by a GitHub Actions workflow when a new version tag is pushed to the repository. To trigger a release, push the tags to the remote repository:

```bash
git push --tags
```