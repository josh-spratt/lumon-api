from flask import Flask, jsonify
import json

__version__ = "0.1.0"

app = Flask(__name__)

# Load employee data from JSON file
with open('employees.json') as f:
    employees = json.load(f)

@app.route('/version', methods=['GET'])
def get_version():
    return jsonify({'version': __version__})

@app.route('/lumon-api/employees', methods=['GET'])
def get_employees():
    return jsonify(employees)

@app.route('/lumon-api/employees/<int:employee_id>', methods=['GET'])
def get_employee(employee_id):
    employee = next((emp for emp in employees if emp['id'] == employee_id), None)
    if employee:
        return jsonify(employee)
    return jsonify({'message': 'Employee not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
