# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

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
