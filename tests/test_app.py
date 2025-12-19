import pytest
import os
import sys
from unittest.mock import patch

# Add the parent directory (project root) to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the app module itself, so we can access and modify its global variables
import app as app_module

@pytest.fixture
def client():
    # Configure app for testing: use an in-memory SQLite database
    app_module.app.config['TESTING'] = True
    app_module.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app_module.app.test_client() as client:
        with app_module.app.app_context():
            # Create all tables in the in-memory database
            app_module.db.create_all()

            # Pre-populate some data for tests
            employees_data = [
                {'first_name': 'Mark', 'last_name': 'Scout', 'department': 'Macrodata Refinement', 'is_severed': True, 'mode': 'innie'},
                {'first_name': 'Dylan', 'last_name': 'George', 'department': 'Macrodata Refinement', 'is_severed': True, 'mode': 'innie'},
                {'first_name': 'Irving', 'last_name': 'Bailiff', 'department': 'Macrodata Refinement', 'is_severed': True, 'mode': 'innie'}
            ]
            for emp_data in employees_data:
                employee = app_module.Employee(**emp_data)
                app_module.db.session.add(employee)
            app_module.db.session.commit()

        yield client # This is where the test code runs

        with app_module.app.app_context():
            # Clean up after each test: drop all tables
            app_module.db.session.remove()
            app_module.db.drop_all()

def test_get_all_employees(client):
    response = client.get('/api/employees')
    assert response.status_code == 200
    assert len(response.json) == 3 # Should have 3 pre-populated employees

def test_create_employee(client):
    response = client.post('/api/employees', json={
        'first_name': 'Helly',
        'last_name': 'R',
        'department': 'Macrodata Refinement'
    })
    assert response.status_code == 201
    assert response.json['first_name'] == 'Helly'
    assert response.json['id'] is not None # ID should be assigned by DB

    response = client.get('/api/employees')
    assert len(response.json) == 4 # 3 pre-populated + 1 new

def test_get_single_employee(client):
    # Assuming Mark Scout (id=1) is one of the pre-populated employees
    response = client.get('/api/employees/1')
    assert response.status_code == 200
    assert response.json['first_name'] == 'Mark'

def test_get_nonexistent_employee(client):
    response = client.get('/api/employees/999')
    assert response.status_code == 404
    assert 'Employee not found' in response.json['message']

def test_update_employee(client):
    # Assuming Mark Scout (id=1) is one of the pre-populated employees
    response = client.put('/api/employees/1', json={
        'department': 'Severed Floor'
    })
    assert response.status_code == 200
    assert response.json['department'] == 'Severed Floor'

    # Verify the update
    updated_employee = client.get('/api/employees/1').json
    assert updated_employee['department'] == 'Severed Floor'

def test_update_nonexistent_employee(client):
    response = client.put('/api/employees/999', json={
        'department': 'Severed Floor'
    })
    assert response.status_code == 404
    assert 'Employee not found' in response.json['message']

def test_delete_employee(client):
    # Assuming Mark Scout (id=1) is one of the pre-populated employees
    response = client.delete('/api/employees/1')
    assert response.status_code == 204

    # Verify deletion
    response = client.get('/api/employees')
    assert len(response.json) == 2 # 3 pre-populated - 1 deleted

    response = client.get('/api/employees/1')
    assert response.status_code == 404

def test_delete_nonexistent_employee(client):
    response = client.delete('/api/employees/999')
    assert response.status_code == 404
    assert 'Employee not found' in response.json['message']

def test_create_employee_missing_data(client):
    response = client.post('/api/employees', json={
        'first_name': 'Ricken',
    })
    assert response.status_code == 400
    assert 'Missing data for new employee' in response.json['message']