# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Re-integrated `Flask-SQLAlchemy` for database persistence with PostgreSQL on Heroku and SQLite for local development.
- Implemented full CRUD functionality with `POST`, `PUT`, and `DELETE` endpoints for managing employees.
- Added API key authentication using an `X-API-Key` header to protect all write-access endpoints.
- Added a thematic `POST /lumon-api/employees/{id}/toggle-mode` endpoint to switch an employee's mode between 'innie' and 'outie'.
- Added a `flask init-db` command to initialize the database and pre-populate it with sample data.
- Expanded the test suite to cover all new CRUD functionality and authentication logic.

### Changed
- The application now reads from and writes to a database instead of a static `employees.json` file.

### Security
- All API endpoints, including `GET` requests, are now protected by API key authentication.

## [2.0.0] - 2025-12-23

### Changed
- **Breaking Change:** All API endpoints have been moved from `/api/*` to `/lumon-api/*`.

## [1.0.0] - 2025-12-20

### Changed

- Re-architected the application to remove all database dependencies. Data is now served from a static `employees.json` file, making the application read-only.

### Removed

- All database-related dependencies (`Flask-SQLAlchemy`, `psycopg2-binary`).
- API endpoints for creating, updating, and deleting employees (`POST /api/employees`, `PUT /api/employees/{id}`, `DELETE /api/employees/{id}`).
- The `init-db` command and all related database setup instructions.

## [0.2.1] - 2025-12-20

### Added
- Initial implementation of the employee API.
- Semantic versioning with `bump2version`.
- Automated releases via GitHub Actions.
- `/version` endpoint to return the application version.
