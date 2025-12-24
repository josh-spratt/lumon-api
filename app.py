from flask import Flask, jsonify, request
import json
import os
from flask_sqlalchemy import SQLAlchemy
import functools

__version__ = "3.0.0"

app = Flask(__name__)

# Database configuration
db_uri = os.environ.get('DATABASE_URL', 'sqlite:///app.db')
if db_uri.startswith("postgres://"):
    db_uri = db_uri.replace("postgres://", "postgresql://", 1)
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Employee Model
class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    department = db.Column(db.String(120), nullable=False)
    is_severed = db.Column(db.Boolean, default=False)
    mode = db.Column(db.String(20), default='outie') # 'innie' or 'outie'

    def __repr__(self):
        return f'<Employee {self.first_name} {self.last_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'department': self.department,
            'is_severed': self.is_severed,
            'mode': self.mode
        }

# Function to initialize the database and potentially pre-populate data
def init_db():
    with app.app_context():
        db.create_all()

        # Pre-populate data only if the employee table is empty and not in testing environment
        if db.session.get(Employee, 1) is None and os.environ.get('FLASK_ENV') != 'testing':
            employees_data = [
                {'first_name': 'Mark', 'last_name': 'Scout', 'department': 'Macrodata Refinement', 'is_severed': True, 'mode': 'innie'},
                {'first_name': 'Dylan', 'last_name': 'George', 'department': 'Macrodata Refinement', 'is_severed': True, 'mode': 'innie'},
                {'first_name': 'Irving', 'last_name': 'Bailiff', 'department': 'Macrodata Refinement', 'is_severed': True, 'mode': 'innie'},
                {'first_name': 'Helly', 'last_name': 'Riggs', 'department': 'Macrodata Refinement', 'is_severed': True, 'mode': 'innie'},
                {'first_name': 'Seth', 'last_name': 'Milchick', 'department': 'Management', 'is_severed': False, 'mode': 'outie'},
                {'first_name': 'Harmony', 'last_name': 'Cobel', 'department': 'Management', 'is_severed': False, 'mode': 'outie'}
            ]
            for emp_data in employees_data:
                employee = Employee(**emp_data)
                db.session.add(employee)
            db.session.commit()
            print("Database pre-populated with sample employee data.")

@app.cli.command("init-db")
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    print("Initialized the database.")


# API Key decorator
def api_key_required(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        api_key = request.headers.get('X-API-Key')
        if not api_key or api_key != os.environ.get('LUMON_API_KEY'):
            return jsonify({'message': 'Unauthorized. Invalid or missing API key.'}), 401
        return f(*args, **kwargs)
    return decorated_function




@app.route('/version', methods=['GET'])
def get_version():
    return jsonify({'version': __version__})

@app.route('/lumon-api/employees', methods=['GET'])
@api_key_required
def get_employees():
    employees = db.session.execute(db.select(Employee)).scalars().all()
    return jsonify([emp.to_dict() for emp in employees])

@app.route('/lumon-api/employees/<int:employee_id>', methods=['GET'])
@api_key_required
def get_employee(employee_id):
    employee = db.session.get(Employee, employee_id)
    if employee:
        return jsonify(employee.to_dict())
    return jsonify({'message': 'Employee not found'}), 404

@app.route('/lumon-api/employees', methods=['POST'])
@api_key_required
def create_employee():
    data = request.get_json()
    if not data or not all(key in data for key in ['first_name', 'last_name', 'department']):
        return jsonify({'message': 'Missing data for new employee'}), 400

    new_employee = Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        department=data['department'],
        is_severed=data.get('is_severed', False),
        mode=data.get('mode', 'outie')
    )
    db.session.add(new_employee)
    db.session.commit()
    return jsonify(new_employee.to_dict()), 201

@app.route('/lumon-api/employees/<int:employee_id>', methods=['PUT'])
@api_key_required
def update_employee(employee_id):
    data = request.get_json()
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    if 'first_name' in data:
        employee.first_name = data['first_name']
    if 'last_name' in data:
        employee.last_name = data['last_name']
    if 'department' in data:
        employee.department = data['department']
    if 'is_severed' in data:
        employee.is_severed = data['is_severed']
    if 'mode' in data:
        employee.mode = data['mode']

    db.session.commit()
    return jsonify(employee.to_dict())

@app.route('/lumon-api/employees/<int:employee_id>', methods=['DELETE'])
@api_key_required
def delete_employee(employee_id):
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    db.session.delete(employee)
    db.session.commit()
    return '', 204

@app.route('/lumon-api/employees/<int:employee_id>/toggle-mode', methods=['POST'])
@api_key_required
def toggle_employee_mode(employee_id):
    employee = db.session.get(Employee, employee_id)
    if not employee:
        return jsonify({'message': 'Employee not found'}), 404

    employee.mode = 'innie' if employee.mode == 'outie' else 'outie'
    db.session.commit()
    return jsonify(employee.to_dict())

if __name__ == '__main__':
    app.run(debug=True)
