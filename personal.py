import sqlite3
from datetime import datetime

# Connect to the SQLite database (create it if it doesn't exist)
conn = sqlite3.connect('employee_directory.db')
c = conn.cursor()

# Drop the existing employees table if it exists
c.execute("DROP TABLE IF EXISTS employees")

# Create the departments table if it doesn't exist
c.execute('''CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    name TEXT)''')

# Create the employees table with the updated definition
c.execute('''CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT,
    contact TEXT,
    department_id INTEGER,
    hire_date DATE,
    tenure INTEGER,
    area TEXT,
    status TEXT,
    FOREIGN KEY (department_id) REFERENCES departments(department_id))''')

# Function to insert a new employee
def insert_employee():
    name = input("Enter employee name: ")
    contact = input("Enter employee contact: ")
    department_id = int(input("Enter department ID: "))
    hire_date = input("Enter hire date (YYYY-MM-DD): ")
    tenure = calculate_tenure(hire_date)
    area = input("Enter employee area: ")
    status = input("Enter employee status (active/retired): ")
    c.execute("INSERT INTO employees (name, contact, department_id, hire_date, tenure, area, status) VALUES (?, ?, ?, ?, ?, ?, ?)", (name, contact, department_id, hire_date, tenure, area, status))
    conn.commit()
    print("Employee added successfully.")

# Function to calculate the tenure based on the hire date
def calculate_tenure(hire_date):
    hire_date = datetime.strptime(hire_date, '%Y-%m-%d')
    today = datetime.now()
    tenure = (today - hire_date).days // 365
    return tenure

# Function to display all employees
def display_employees():
    c.execute("SELECT * FROM employees")
    employees = c.fetchall()
    print("Employees:")
    for employee in employees:
        print(employee)

# Function to search employees by name
def search_employee():
    name = input("Enter employee name to search: ")
    c.execute("SELECT * FROM employees WHERE name LIKE ?", ('%' + name + '%',))
    employees = c.fetchall()
    print("Search results:")
    for employee in employees:
        print(employee)

# Function to update an employee's contact
def update_contact():
    employee_id = int(input("Enter employee ID to update contact: "))
    new_contact = input("Enter new contact: ")
    c.execute("UPDATE employees SET contact = ? WHERE employee_id = ?", (new_contact, employee_id))
    conn.commit()
    print("Contact updated successfully.")

# Function to delete an employee
def delete_employee():
    employee_id = int(input("Enter employee ID to delete: "))
    c.execute("DELETE FROM employees WHERE employee_id = ?", (employee_id,))
    conn.commit()
    print("Employee deleted successfully.")

# Function to filter employees by hire date range
def filter_by_date_range():
    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")
    c.execute("SELECT * FROM employees WHERE hire_date BETWEEN ? AND ?", (start_date, end_date))
    employees = c.fetchall()
    print("Employees hired between", start_date, "and", end_date, ":")
    for employee in employees:
        print(employee)

# Main program loop
while True:
    print("\nEmployee Directory Menu:")
    print("1. Add New Employee")
    print("2. Display All Employees")
    print("3. Search Employee by Name")
    print("4. Update Employee Contact")
    print("5. Delete Employee")
    print("6. Filter Employees by Hire Date Range")
    print("7. Exit")
    choice = input("Enter your choice: ")

    # Execute the selected option
    if choice == '1':
        insert_employee()
    elif choice == '2':
        display_employees()
    elif choice == '3':
        search_employee()
    elif choice == '4':
        update_contact()
    elif choice == '5':
        delete_employee()
    elif choice == '6':
        filter_by_date_range()
    elif choice == '7':
        break
    else:
        print("Invalid choice. Please enter a number between 1 and 7.")

# Close the database connection
conn.close()
