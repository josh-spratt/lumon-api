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
    os.environ['LUMON_API_KEY'] = 'test-key'
    response = client.get('/lumon-api/employees', headers={'X-API-Key': 'test-key'})
    assert response.status_code == 200
    assert len(response.json) == 3
    del os.environ['LUMON_API_KEY']

def test_auth_required_for_get_all(client):
    response = client.get('/lumon-api/employees')
    assert response.status_code == 401

def test_get_single_employee(client):
    os.environ['LUMON_API_KEY'] = 'test-key'
    response = client.get('/lumon-api/employees/1', headers={'X-API-Key': 'test-key'})
    assert response.status_code == 200
    assert response.json['first_name'] == 'Mark'
    del os.environ['LUMON_API_KEY']

def test_auth_required_for_get_one(client):
    response = client.get('/lumon-api/employees/1')
    assert response.status_code == 401

def test_create_employee(client):
    # This test will fail without a valid API key
    os.environ['LUMON_API_KEY'] = 'test-key'
    
    response = client.post('/lumon-api/employees', json={
        'first_name': 'Helly',
        'last_name': 'R',
        'department': 'Macrodata Refinement'
    }, headers={'X-API-Key': 'test-key'})
    
    assert response.status_code == 201
    assert response.json['first_name'] == 'Helly'
    assert response.json['id'] is not None

    response = client.get('/lumon-api/employees', headers={'X-API-Key': 'test-key'})
    assert len(response.json) == 4
    
    del os.environ['LUMON_API_KEY']

def test_auth_required_for_create(client):
    response = client.post('/lumon-api/employees', json={
        'first_name': 'Helly',
        'last_name': 'R',
        'department': 'Macrodata Refinement'
    })
    assert response.status_code == 401 # Unauthorized

def test_update_employee(client):
    os.environ['LUMON_API_KEY'] = 'test-key'
    
    response = client.put('/lumon-api/employees/1', json={
        'department': 'Optics and Design'
    }, headers={'X-API-Key': 'test-key'})
    
    assert response.status_code == 200
    assert response.json['department'] == 'Optics and Design'
    
    del os.environ['LUMON_API_KEY']

def test_delete_employee(client):
    os.environ['LUMON_API_KEY'] = 'test-key'
    
    response = client.delete('/lumon-api/employees/1', headers={'X-API-Key': 'test-key'})
    assert response.status_code == 204

    # Verify deletion
    response = client.get('/lumon-api/employees', headers={'X-API-Key': 'test-key'})
    assert len(response.json) == 2
    
    del os.environ['LUMON_API_KEY']

def test_toggle_mode(client):
    os.environ['LUMON_API_KEY'] = 'test-key'
    
    # Get initial mode
    initial_response = client.get('/lumon-api/employees/1', headers={'X-API-Key': 'test-key'})
    assert initial_response.status_code == 200
    initial_mode = initial_response.json['mode']
    
    # Toggle mode
    response = client.post('/lumon-api/employees/1/toggle-mode', headers={'X-API-Key': 'test-key'})
    assert response.status_code == 200
    
    # Verify mode has changed
    new_mode = response.json['mode']
    assert new_mode != initial_mode
    
    # Toggle back
    response = client.post('/lumon-api/employees/1/toggle-mode', headers={'X-API-Key': 'test-key'})
    final_mode = response.json['mode']
    assert final_mode == initial_mode
    
    del os.environ['LUMON_API_KEY']

def test_get_single_employee(client):
    os.environ['LUMON_API_KEY'] = 'test-key'
    response = client.get('/lumon-api/employees/1', headers={'X-API-Key': 'test-key'})
    assert response.status_code == 200
    assert response.json['first_name'] == 'Mark'
    del os.environ['LUMON_API_KEY']

def test_get_nonexistent_employee(client):
    os.environ['LUMON_API_KEY'] = 'test-key'
    response = client.get('/lumon-api/employees/999', headers={'X-API-Key': 'test-key'})
    assert response.status_code == 404
    assert 'Employee not found' in response.json['message']
    del os.environ['LUMON_API_KEY']

def test_get_version(client):
    response = client.get('/version')
    assert response.status_code == 200
    assert len(response.json['version'].split('.')) == 3
