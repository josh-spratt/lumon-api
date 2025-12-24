# Gemini CLI Project Configuration

This file provides instructions for the Gemini CLI on how to interact with this project.

## Project Overview

This is a Python-based API server for the Severance project. It uses the Flask framework to create a simple API for managing employee data. The data is stored in a flat file, `employees.json`. The project uses `pytest` for testing and `bump2version` for semantic versioning.

## Building and Running

### Dependencies

To install the dependencies, run:

```bash
pip install -r requirements.txt
```

### Running the Application

To run the development server, use:

```bash
flask run
```

The API will be available at `http://127.0.0.1:5000/`.

### Running Tests

To run the test suite, use:

```bash
pytest
```

## Development Conventions

### Versioning

This project uses `bump2version` to manage semantic versioning. The version is tracked in `app.py` and `CHANGELOG.md`. To create a new version, use one of the following commands:

```bash
# Bump a patch version (e.g., 0.1.0 -> 0.1.1)
bump2version patch

# Bump a minor version (e.g., 0.1.1 -> 0.2.0)
bump2version minor

# Bump a major version (e.g., 0.2.0 -> 1.0.0)
bump2version major
```

### Releases

New releases are created automatically by a GitHub Actions workflow when a new version tag is pushed to the repository. To trigger a release, push the tags to the remote repository:

```bash
git push --tags
```
