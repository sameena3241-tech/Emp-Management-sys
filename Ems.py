from flask import Flask, render_template, request, redirect,url_for,flash
from flask_sqlalchemy import SQLAlchemy

Ems= Flask(__name__)
#adding flash
Ems.secret_key= "my-secret-key"

#database congigration
Ems.config["SQLALCHEMY_DATABASE_URI"]= "sqlite:///employees.db"
db=SQLAlchemy(Ems)

#Employee model
class Employee(db.Model):
    id= db.Column(db.Integer, primary_key=True)
    name=db.Column(db.String(100), nullable=False)
    department=db.Column(db.String(100), nullable=False)
    salary=db.Column(db.Float, nullable=False)

#create database and table
with Ems.app_context():
    db.create_all()


#home page
@Ems.route("/")
def home():
    return render_template("home.html")

#Display Employees
@Ems.route("/employees")
def employees():
    employee_list=Employee.query.all()

    return render_template("employees.html",employees=employee_list)


#Add Employee

@Ems.route("/add", methods=["GET", "POST"])
def add_employee():

    if request.method == "POST":

        name=request.form["name"].strip()
        department=request.form["department"].strip()
        salary=request.form["salary"].strip()

    # Name validation
        if not name:
            flash("Name cannot be Empty", "error")
            return redirect(url_for("add_employee"))

        if not department:
            flash("Department Cannot be Empty","error")
            return redirect(url_for("add_employee"))
        
    #Exception Handling
        try: 
            salary= float(salary)
        except ValueError:
            flash("Salary must be valid number","error")
            return redirect(url_for("add_employee")) 

        if salary <=0:
            flash("Salary must be greater than 0!","error")
            return redirect(url_for("add_employee"))

        employee=Employee(name=name,department=department,salary=salary)

        db.session.add(employee)
        db.session.commit()

        flash("Employee added Succesfully!", "success")
        return redirect(url_for("employees"))
    
    return render_template("add_employee.html")



#Edit Employee/Update Employee

@Ems.route("/edit/<int:id>", methods=["GET", "POST"])
def edit_employee(id):

    employee=Employee.query.get_or_404(id)

    if request.method == "POST":

        name=request.form["name"].strip()
        department=request.form["department"].strip()
        salary=request.form["salary"].strip()

    #Name validation
        if not name:
            flash("Name cannot be Empty!","error")
            return redirect(url_for("edit_employee", id=id))

        if not department:
            flash("department cannot be empty!","error")  
            return redirect(url_for("edit_employee", id=id))
        
    #Exceptin Handling
        try:
            salary= float(salary)
        except ValueError:
            flash("Salary must be valid number!","error" )
            return redirect(url_for("edit_employee", id=id))

    
        if salary <=0:
            flash ("Salary must be greater than 0!","error")
            return redirect(url_for("edit_employee", id=id)) 
    
    #update employee
        employee.name=name
        employee.department=department
        employee.salary=salary

        db.session.commit()

        flash("Employee updated Successfully!", "success")

        return redirect(url_for("employees"))

    return render_template("edit_employee.html", employee=employee)


#Delete Employee

@Ems.route("/delete/<int:id>")
def delete_employee(id):
    employee=Employee.query.get_or_404(id)

    db.session.delete(employee)
    db.session.commit()

    flash("Employee deleted Succesfully!", "success")
    return redirect(url_for("employees"))


if __name__== "__main__":
    Ems.run(debug=True)