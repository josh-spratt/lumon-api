import pytest
import os
import sys
import json

# Add the parent directory (project root) to the sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import the app module itself
import app as app_module

@pytest.fixture
def client():
    app_module.app.config['TESTING'] = True
    with app_module.app.test_client() as client:
        yield client

def test_get_all_employees(client):
    response = client.get('/api/employees')
    assert response.status_code == 200
    with open('employees.json') as f:
        employees_data = json.load(f)
    assert len(response.json) == len(employees_data)

def test_get_single_employee(client):
    response = client.get('/api/employees/1')
    assert response.status_code == 200
    assert response.json['first_name'] == 'Mark'

def test_get_nonexistent_employee(client):
    response = client.get('/api/employees/999')
    assert response.status_code == 404
    assert 'Employee not found' in response.json['message']

def test_get_version(client):
    response = client.get('/version')
    assert response.status_code == 200
    assert len(response.json['version'].split('.')) == 3
