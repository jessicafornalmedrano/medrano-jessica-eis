from flask import Flask, render_template, request, redirect, session
from users import Users
from employees import Employees

app = Flask(__name__)
app.secret_key = "okay"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check-user', methods=['POST'])
def check_user():
    username = request.form["username"]
    password = request.form["password"]

    result = Users.check_user(username, password)

    if result:
        return redirect('/employee-list')
    else:
        return render_template('index.html')

@app.route('/employee-list')
def employee_list():
    employees = Employees.get_all()

    if "message" not in session:
        session["message"] = ""

    return render_template('employee_list.html', employees=employees, message=session.pop('message', None))

@app.route('/add-form')
def add_form():
    return render_template('add_employee.html')

@app.route('/add-employee', methods=['POST'])
def add_employee():
    emp_id = request.form["emp_id"]
    lname = request.form["lname"]
    fname = request.form["fname"]
    mname = request.form["mname"]

    success = Employees.add_employee(emp_id, lname, fname, mname)

    if success:
        session["message"] = "Successfully added employee."
    else:
        session["message"] = "Failed to add employee."

    return redirect('/employee-list')

@app.route('/update-form/<emp_id>')
def update_form(emp_id):
    employee = Employees.get_employee(emp_id)
    if employee:
        return render_template('update_employee.html', employee=employee)
    else:
        session["message"] = "Employee not found."
        return redirect('/employee-list')

@app.route('/update-employee', methods=['POST'])
def update_employee():
    emp_id = request.form["emp_id"]
    lname = request.form["lname"]
    fname = request.form["fname"]
    mname = request.form["mname"]

    success = Employees.update_employee(emp_id, lname, fname, mname)

    if success:
        session["message"] = "Successfully updated employee."
    else:
        session["message"] = "Failed to update employee."

    return redirect('/employee-list')

@app.route('/delete/<emp_id>', methods=['POST'])
def delete_employee(emp_id):
    success = Employees.delete_employee(emp_id)
    
    if success:
        session["message"] = "Successfully deleted employee."
    else:
        session["message"] = "Failed to delete employee."
    
    return redirect('/employee-list')

if __name__ == '__main__':
    app.run()
