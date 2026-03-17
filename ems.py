import csv
import os
import getpass
from datetime import datetime

# File constants
EMP_FILE = "employees.csv"
MANAGER_FILE = "manager.csv"
SUGGESTIONS_FILE = "suggestions.csv"
ENQUIRIES_FILE = "enquiries.csv"
BOSS_FILE = "boss.csv"

# Data structures
employees = {}
suggestions = []
enquiries = []
managers = {}

boss = {"username": "boss", "password": "boss123"}
current_boss = None
current_manager = None
current_employee = None

# ---------------- CSV FUNCTIONS ----------------


def load_employees():
    global employees
    employees = {}
    if not os.path.exists(EMP_FILE):
        return
    with open(EMP_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            employees[r["name"]] = r


def save_employees():
    with open(EMP_FILE, "w", newline="") as f:
        fields = ["name", "id", "designation", "age",
                  "address", "salary", "email", "password"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for e in employees.values():
            writer.writerow(e)


def load_suggestions():
    global suggestions
    suggestions = []
    if not os.path.exists(SUGGESTIONS_FILE):
        return
    with open(SUGGESTIONS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            suggestions.append(r)


def save_suggestions():
    with open(SUGGESTIONS_FILE, "w", newline="") as f:
        fields = ["employee", "suggestion", "date", "status"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for s in suggestions:
            writer.writerow(s)


def load_enquiries():
    global enquiries
    enquiries = []
    if not os.path.exists(ENQUIRIES_FILE):
        return
    with open(ENQUIRIES_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            enquiries.append(r)


def save_enquiries():
    with open(ENQUIRIES_FILE, "w", newline="") as f:
        fields = ["employee", "subject", "enquiry",
                  "priority", "date", "status", "response"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for e in enquiries:
            writer.writerow(e)


def load_boss():
    global boss
    if not os.path.exists(BOSS_FILE):
        boss = {"username": "boss", "password": "boss123"}
        save_boss()
        return
    with open(BOSS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            boss = {"username": r["username"], "password": r["password"]}
            break


def save_boss():
    with open(BOSS_FILE, "w", newline="") as f:
        fields = ["username", "password"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerow(boss)


def load_managers():
    global managers
    managers = {}
    if not os.path.exists(MANAGER_FILE):
        managers = {
            "manager1": {
                "username": "manager1",
                "password": "manager123",
                "name": "John Doe",
                "age": "35",
                "address": "123 Main St",
                "phone": "555-1234",
                "email": "manager1@company.com",
                "position": "General Manager",
                "id": "MGR001"
            }
        }
        save_managers()
        return
    with open(MANAGER_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            managers[r["username"]] = {
                "username": r["username"],
                "password": r["password"],
                "name": r.get("name", ""),
                "age": r.get("age", ""),
                "address": r.get("address", ""),
                "phone": r.get("phone", ""),
                "email": r.get("email", ""),
                "position": r.get("position", ""),
                "id": r.get("id", "")
            }


def save_managers():
    with open(MANAGER_FILE, "w", newline="") as f:
        fields = ["username", "password", "name", "age", "address",
                  "phone", "email", "position", "id"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for mgr_data in managers.values():
            writer.writerow(mgr_data)


# Load all data
load_employees()
load_managers()
load_suggestions()
load_enquiries()
load_boss()

# ---------------- UTILITY FUNCTIONS ----------------


def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')


def print_header(title):
    print("\n" + "="*60)
    print(f"{title:^60}")
    print("="*60)


def print_footer():
    print("-"*60)


def pause():
    input("\nPress Enter to continue...")


def validate_email(email):
    return "@" in email and "." in email


def validate_age(age):
    try:
        age_int = int(age)
        return 18 <= age_int <= 100
    except ValueError:
        return False


def validate_phone(phone):
    return phone.replace("-", "").replace(" ", "").isdigit()


# ---------------- LOGIN SYSTEM ----------------


def login():
    global current_boss, current_manager, current_employee
    
    print_header("EMPLOYEE MANAGEMENT SYSTEM - LOGIN")
    print("1. Boss Login")
    print("2. Manager Login")
    print("3. Employee Login")
    print("4. Exit")
    
    choice = input("\nSelect login type (1-4): ").strip()
    
    if choice == "4":
        print("\nThank you for using the system. Goodbye!")
        return False
    
    if choice not in ["1", "2", "3"]:
        print("\nInvalid choice!")
        pause()
        return True
    
    max_attempts = 3
    attempt_count = 0
    
    while attempt_count < max_attempts:
        print(f"\n{'='*40}")
        username = input("Username: ").strip()
        password = getpass.getpass("Password: ")
        
        if choice == "1":  # Boss
            if username == boss["username"] and password == boss["password"]:
                current_boss = username
                print("\n✓ Boss login successful!")
                pause()
                boss_dashboard()
                return True
            else:
                attempt_count += 1
                remaining = max_attempts - attempt_count
                if remaining > 0:
                    print(f"\n✗ Invalid credentials! {remaining} attempt(s) remaining.")
                else:
                    print("\n✗ Too many failed attempts! Exiting...")
                    return False
        
        elif choice == "2":  # Manager
            if username in managers and managers[username]["password"] == password:
                current_manager = username
                print(f"\n✓ Welcome, {managers[username]['name']}!")
                pause()
                manager_dashboard()
                return True
            else:
                attempt_count += 1
                remaining = max_attempts - attempt_count
                if remaining > 0:
                    print(f"\n✗ Invalid credentials! {remaining} attempt(s) remaining.")
                else:
                    print("\n✗ Too many failed attempts! Exiting...")
                    return False
        
        elif choice == "3":  # Employee
            if username in employees and employees[username]["password"] == password:
                current_employee = username
                print(f"\n✓ Welcome, {username}!")
                pause()
                employee_dashboard()
                return True
            else:
                attempt_count += 1
                remaining = max_attempts - attempt_count
                if remaining > 0:
                    print(f"\n✗ Invalid credentials! {remaining} attempt(s) remaining.")
                else:
                    print("\n✗ Too many failed attempts! Exiting...")
                    return False
    
    return False


# ---------------- BOSS DASHBOARD ----------------


def boss_dashboard():
    while True:
        clear_screen()
        print_header(f"BOSS DASHBOARD - Welcome {boss['username']}")
        print("1. Add Employee")
        print("2. View All Employees")
        print("3. Edit Employee")
        print("4. Delete Employee")
        print("5. Search Employees")
        print("6. View Managers")
        print("7. Add Manager")
        print("8. Delete Manager")
        print("9. Reset Employee Password")
        print("10. My Profile")
        print("11. Logout")
        
        choice = input("\nSelect option (1-11): ").strip()
        
        if choice == "1":
            add_employee()
        elif choice == "2":
            view_employees()
        elif choice == "3":
            edit_employee()
        elif choice == "4":
            delete_employee()
        elif choice == "5":
            search_employees()
        elif choice == "6":
            view_managers()
        elif choice == "7":
            add_manager()
        elif choice == "8":
            delete_manager()
        elif choice == "9":
            reset_employee_password()
        elif choice == "10":
            boss_profile()
        elif choice == "11":
            print("\nLogging out...")
            pause()
            break
        else:
            print("\n✗ Invalid option!")
            pause()


# ---------------- MANAGER DASHBOARD ----------------


def manager_dashboard():
    global current_manager
    while True:
        clear_screen()
        manager_data = managers[current_manager]
        print_header(f"MANAGER DASHBOARD - Welcome {manager_data['name']}")
        print("1. View All Employees")
        print("2. Search Employees")
        print("3. Delete Employee")
        print("4. Add Employee")
        print("5. Edit Employee")
        print("6. View Suggestions")
        print("7. View Enquiries")
        print("8. My Profile")
        print("9. Logout")
        
        choice = input("\nSelect option (1-9): ").strip()
        
        if choice == "1":
            view_employees()
        elif choice == "2":
            search_employees()
        elif choice == "3":
            delete_employee()
        elif choice == "4":
            add_employee()
        elif choice == "5":
            edit_employee()
        elif choice == "6":
            view_suggestions()
        elif choice == "7":
            view_enquiries()
        elif choice == "8":
            manager_profile()
        elif choice == "9":
            print("\nLogging out...")
            pause()
            break
        else:
            print("\n✗ Invalid option!")
            pause()


# ---------------- EMPLOYEE DASHBOARD ----------------


def employee_dashboard():
    global current_employee
    while True:
        clear_screen()
        emp_data = employees[current_employee]
        print_header(f"EMPLOYEE DASHBOARD - Welcome {current_employee}")
        print(f"Email: {emp_data['email']} | Designation: {emp_data['designation']}")
        print("-"*60)
        print("1. View My Profile")
        print("2. Edit My Profile")
        print("3. Reset Password")
        print("4. Give Suggestion")
        print("5. Make Enquiry")
        print("6. Logout")
        
        choice = input("\nSelect option (1-6): ").strip()
        
        if choice == "1":
            view_employee_profile()
        elif choice == "2":
            edit_employee_profile()
        elif choice == "3":
            employee_reset_password()
        elif choice == "4":
            give_suggestion()
        elif choice == "5":
            make_enquiry()
        elif choice == "6":
            print("\nLogging out...")
            pause()
            break
        else:
            print("\n✗ Invalid option!")
            pause()


# ---------------- EMPLOYEE FUNCTIONS ----------------


def view_employees():
    clear_screen()
    print_header("ALL EMPLOYEES")
    
    if not employees:
        print("\nNo employees found in the system.")
    else:
        print(f"\n{'Name':<20} {'ID':<10} {'Designation':<15} {'Age':<5} {'Email':<25}")
        print("-"*80)
        for name, data in employees.items():
            print(f"{name:<20} {data['id']:<10} {data['designation']:<15} "
                  f"{data['age']:<5} {data['email']:<25}")
    pause()


def add_employee():
    clear_screen()
    print_header("ADD NEW EMPLOYEE")
    print("(All fields are required)")
    
    # Get employee details
    name = input("Name: ").strip()
    if not name:
        print("\n✗ Name cannot be empty!")
        pause()
        return
    
    if name in employees:
        print(f"\n✗ Employee '{name}' already exists!")
        pause()
        return
    
    emp_id = input("Employee ID: ").strip()
    if not emp_id:
        print("\n✗ Employee ID cannot be empty!")
        pause()
        return
    
    # Check if ID exists
    for data in employees.values():
        if data["id"] == emp_id:
            print(f"\n✗ Employee ID '{emp_id}' already exists!")
            pause()
            return
    
    designation = input("Designation: ").strip()
    if not designation:
        print("\n✗ Designation cannot be empty!")
        pause()
        return
    
    age = input("Age: ").strip()
    if not age or not validate_age(age):
        print("\n✗ Age must be a number between 18 and 100!")
        pause()
        return
    
    address = input("Address: ").strip()
    if not address:
        print("\n✗ Address cannot be empty!")
        pause()
        return
    
    salary = input("Salary: ").strip()
    if not salary:
        print("\n✗ Salary cannot be empty!")
        pause()
        return
    try:
        float(salary)
    except ValueError:
        print("\n✗ Salary must be a number!")
        pause()
        return
    
    email = input("Email: ").strip()
    if not email or not validate_email(email):
        print("\n✗ Please enter a valid email address!")
        pause()
        return
    
    # Check if email exists
    for data in employees.values():
        if data["email"] == email:
            print(f"\n✗ Email '{email}' is already registered!")
            pause()
            return
    
    password = getpass.getpass("Password: ").strip()
    if not password:
        print("\n✗ Password cannot be empty!")
        pause()
        return
    
    # Create employee
    employees[name] = {
        "name": name,
        "id": emp_id,
        "designation": designation,
        "age": age,
        "address": address,
        "salary": salary,
        "email": email,
        "password": password
    }
    
    save_employees()
    print(f"\n✓ Employee '{name}' added successfully!")
    pause()


def edit_employee():
    clear_screen()
    print_header("EDIT EMPLOYEE")
    
    name = input("Enter employee name to edit: ").strip()
    
    if name not in employees:
        print(f"\n✗ Employee '{name}' not found!")
        pause()
        return
    
    emp_data = employees[name]
    print(f"\nEditing employee: {name}")
    print("(Press Enter to keep current value)")
    
    # Designation
    new_designation = input(f"Designation [{emp_data['designation']}]: ").strip()
    if new_designation:
        emp_data['designation'] = new_designation
    
    # Age
    new_age = input(f"Age [{emp_data['age']}]: ").strip()
    if new_age:
        if validate_age(new_age):
            emp_data['age'] = new_age
        else:
            print("✗ Invalid age! Keeping current value.")
    
    # Address
    new_address = input(f"Address [{emp_data['address']}]: ").strip()
    if new_address:
        emp_data['address'] = new_address
    
    # Salary
    new_salary = input(f"Salary [{emp_data['salary']}]: ").strip()
    if new_salary:
        try:
            float(new_salary)
            emp_data['salary'] = new_salary
        except ValueError:
            print("✗ Invalid salary! Keeping current value.")
    
    # Email
    new_email = input(f"Email [{emp_data['email']}]: ").strip()
    if new_email:
        if validate_email(new_email):
            emp_data['email'] = new_email
        else:
            print("✗ Invalid email! Keeping current value.")
    
    save_employees()
    print(f"\n✓ Employee '{name}' updated successfully!")
    pause()


def delete_employee():
    clear_screen()
    print_header("DELETE EMPLOYEE")
    
    search_term = input("Enter Name, ID or Email to search: ").strip().lower()
    if not search_term:
        print("\n✗ Please enter a search term!")
        pause()
        return
    
    found = []
    for name, data in employees.items():
        if (search_term in name.lower() or 
            search_term in data['id'].lower() or 
            search_term in data['email'].lower()):
            found.append((name, data))
    
    if not found:
        print(f"\nNo employees found matching '{search_term}'")
        pause()
        return
    
    print(f"\nFound {len(found)} employee(s):")
    for i, (name, data) in enumerate(found, 1):
        print(f"{i}. {name} - ID: {data['id']} - Email: {data['email']}")
    
    try:
        choice = int(input("\nSelect employee number to delete (0 to cancel): "))
        if 1 <= choice <= len(found):
            name_to_delete = found[choice-1][0]
            confirm = input(f"Are you sure you want to delete '{name_to_delete}'? (y/n): ").lower()
            if confirm == 'y':
                del employees[name_to_delete]
                save_employees()
                print(f"\n✓ Employee '{name_to_delete}' deleted successfully!")
            else:
                print("\nDeletion cancelled.")
        elif choice != 0:
            print("\n✗ Invalid selection!")
    except ValueError:
        print("\n✗ Invalid input!")
    
    pause()


def search_employees():
    clear_screen()
    print_header("SEARCH EMPLOYEES")
    
    print("Search by:")
    print("1. Name")
    print("2. ID")
    print("3. Email")
    print("4. Designation")
    
    search_type = input("\nSelect search type (1-4): ").strip()
    
    search_map = {'1': 'Name', '2': 'ID', '3': 'Email', '4': 'Designation'}
    if search_type not in search_map:
        print("\n✗ Invalid search type!")
        pause()
        return
    
    term = input(f"Enter {search_map[search_type]} to search: ").strip().lower()
    if not term:
        print("\n✗ Please enter a search term!")
        pause()
        return
    
    found = []
    for name, data in employees.items():
        if search_type == '1' and term in name.lower():
            found.append((name, data))
        elif search_type == '2' and term in data['id'].lower():
            found.append((name, data))
        elif search_type == '3' and term in data['email'].lower():
            found.append((name, data))
        elif search_type == '4' and term in data['designation'].lower():
            found.append((name, data))
    
    clear_screen()
    if not found:
        print(f"\nNo employees found matching '{term}'")
    else:
        print_header(f"SEARCH RESULTS ({len(found)} found)")
        print(f"\n{'Name':<20} {'ID':<10} {'Designation':<15} {'Email':<25}")
        print("-"*70)
        for name, data in found:
            print(f"{name:<20} {data['id']:<10} {data['designation']:<15} {data['email']:<25}")
    
    pause()


def reset_employee_password():
    clear_screen()
    print_header("RESET EMPLOYEE PASSWORD")
    
    name = input("Enter employee name: ").strip()
    
    if name not in employees:
        print(f"\n✗ Employee '{name}' not found!")
        pause()
        return
    
    new_pass = getpass.getpass("New password: ").strip()
    if not new_pass:
        print("\n✗ Password cannot be empty!")
        pause()
        return
    
    confirm_pass = getpass.getpass("Confirm password: ").strip()
    
    if new_pass != confirm_pass:
        print("\n✗ Passwords do not match!")
        pause()
        return
    
    employees[name]["password"] = new_pass
    save_employees()
    print(f"\n✓ Password updated successfully for {name}!")
    pause()


# ---------------- EMPLOYEE PROFILE FUNCTIONS ----------------


def view_employee_profile():
    clear_screen()
    emp_data = employees[current_employee]
    print_header(f"MY PROFILE - {current_employee}")
    print(f"Employee ID:   {emp_data['id']}")
    print(f"Name:          {current_employee}")
    print(f"Designation:   {emp_data['designation']}")
    print(f"Age:           {emp_data['age']}")
    print(f"Address:       {emp_data['address']}")
    print(f"Salary:        ${emp_data['salary']}")
    print(f"Email:         {emp_data['email']}")
    print(f"Password:      {'*' * len(emp_data['password'])}")
    pause()


def edit_employee_profile():
    clear_screen()
    emp_data = employees[current_employee]
    print_header("EDIT MY PROFILE")
    print("(Press Enter to keep current value)")
    
    # Designation
    new_designation = input(f"Designation [{emp_data['designation']}]: ").strip()
    if new_designation:
        emp_data['designation'] = new_designation
    
    # Age
    new_age = input(f"Age [{emp_data['age']}]: ").strip()
    if new_age:
        if validate_age(new_age):
            emp_data['age'] = new_age
        else:
            print("✗ Invalid age! Keeping current value.")
    
    # Address
    new_address = input(f"Address [{emp_data['address']}]: ").strip()
    if new_address:
        emp_data['address'] = new_address
    
    # Salary - employees might not be allowed to change salary
    print("\n(Note: Salary changes require manager approval)")
    
    # Email
    new_email = input(f"Email [{emp_data['email']}]: ").strip()
    if new_email:
        if validate_email(new_email):
            # Check if email already exists
            email_exists = False
            for name, data in employees.items():
                if name != current_employee and data['email'] == new_email:
                    email_exists = True
                    break
            if not email_exists:
                emp_data['email'] = new_email
            else:
                print("✗ Email already in use! Keeping current value.")
        else:
            print("✗ Invalid email! Keeping current value.")
    
    save_employees()
    print(f"\n✓ Profile updated successfully!")
    pause()


def employee_reset_password():
    clear_screen()
    print_header("RESET MY PASSWORD")
    
    emp_data = employees[current_employee]
    
    current_pass = getpass.getpass("Current password: ").strip()
    if emp_data['password'] != current_pass:
        print("\n✗ Current password is incorrect!")
        pause()
        return
    
    new_pass = getpass.getpass("New password: ").strip()
    if not new_pass:
        print("\n✗ Password cannot be empty!")
        pause()
        return
    
    if len(new_pass) < 4:
        print("\n✗ Password must be at least 4 characters!")
        pause()
        return
    
    confirm_pass = getpass.getpass("Confirm password: ").strip()
    
    if new_pass != confirm_pass:
        print("\n✗ Passwords do not match!")
        pause()
        return
    
    emp_data['password'] = new_pass
    save_employees()
    print(f"\n✓ Password reset successfully!")
    pause()


def give_suggestion():
    clear_screen()
    print_header("GIVE SUGGESTION")
    
    print("Enter your suggestion (minimum 10 characters):")
    suggestion = input("\n> ").strip()
    
    if not suggestion:
        print("\n✗ Suggestion cannot be empty!")
        pause()
        return
    
    if len(suggestion) < 10:
        print("\n✗ Suggestion must be at least 10 characters!")
        pause()
        return
    
    new_suggestion = {
        "employee": current_employee,
        "suggestion": suggestion,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Pending"
    }
    
    suggestions.append(new_suggestion)
    save_suggestions()
    
    print("\n✓ Thank you! Your suggestion has been submitted.")
    pause()


def make_enquiry():
    clear_screen()
    print_header("MAKE ENQUIRY")
    
    subject = input("Subject: ").strip()
    if not subject:
        print("\n✗ Subject cannot be empty!")
        pause()
        return
    
    print("\nYour enquiry (minimum 10 characters):")
    enquiry = input("> ").strip()
    
    if not enquiry:
        print("\n✗ Enquiry cannot be empty!")
        pause()
        return
    
    if len(enquiry) < 10:
        print("\n✗ Enquiry must be at least 10 characters!")
        pause()
        return
    
    print("\nPriority:")
    print("1. Low")
    print("2. Normal")
    print("3. High")
    print("4. Urgent")
    
    priority_choice = input("Select priority (1-4): ").strip()
    priority_map = {'1': 'Low', '2': 'Normal', '3': 'High', '4': 'Urgent'}
    priority = priority_map.get(priority_choice, 'Normal')
    
    new_enquiry = {
        "employee": current_employee,
        "subject": subject,
        "enquiry": enquiry,
        "priority": priority,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "status": "Pending",
        "response": ""
    }
    
    enquiries.append(new_enquiry)
    save_enquiries()
    
    print(f"\n✓ Your enquiry has been submitted with {priority} priority.")
    pause()


# ---------------- MANAGER FUNCTIONS ----------------


def view_suggestions():
    clear_screen()
    print_header("EMPLOYEE SUGGESTIONS")
    
    if not suggestions:
        print("\nNo suggestions have been submitted yet.")
        pause()
        return
    
    for i, s in enumerate(suggestions, 1):
        print(f"\n--- Suggestion #{i} ---")
        print(f"Employee: {s['employee']}")
        print(f"Date: {s['date']}")
        print(f"Status: {s['status']}")
        print(f"Suggestion: {s['suggestion']}")
        print("-"*40)
    
    # Option to update status
    update = input("\nUpdate suggestion status? (y/n): ").lower()
    if update == 'y':
        try:
            idx = int(input("Enter suggestion number: ")) - 1
            if 0 <= idx < len(suggestions):
                print("\nNew status:")
                print("1. Pending")
                print("2. Reviewed")
                print("3. Implemented")
                print("4. Rejected")
                status_choice = input("Select status (1-4): ").strip()
                status_map = {'1': 'Pending', '2': 'Reviewed', 
                            '3': 'Implemented', '4': 'Rejected'}
                if status_choice in status_map:
                    suggestions[idx]['status'] = status_map[status_choice]
                    save_suggestions()
                    print("✓ Status updated!")
                else:
                    print("✗ Invalid status!")
            else:
                print("✗ Invalid suggestion number!")
        except ValueError:
            print("✗ Invalid input!")
    
    pause()


def view_enquiries():
    clear_screen()
    print_header("EMPLOYEE ENQUIRIES")
    
    if not enquiries:
        print("\nNo enquiries have been submitted yet.")
        pause()
        return
    
    for i, e in enumerate(enquiries, 1):
        priority_color = ""
        if e['priority'] == 'Urgent':
            priority_color = " [URGENT]"
        elif e['priority'] == 'High':
            priority_color = " [HIGH]"
        
        print(f"\n--- Enquiry #{i}{priority_color} ---")
        print(f"Employee: {e['employee']}")
        print(f"Subject: {e['subject']}")
        print(f"Priority: {e['priority']}")
        print(f"Date: {e['date']}")
        print(f"Status: {e['status']}")
        print(f"Enquiry: {e['enquiry']}")
        if e.get('response'):
            print(f"Response: {e['response']}")
        print("-"*40)
    
    # Option to respond
    respond = input("\nRespond to an enquiry? (y/n): ").lower()
    if respond == 'y':
        try:
            idx = int(input("Enter enquiry number: ")) - 1
            if 0 <= idx < len(enquiries):
                print("\nCurrent status:", enquiries[idx]['status'])
                print("Update status:")
                print("1. Pending")
                print("2. In Progress")
                print("3. Resolved")
                print("4. Closed")
                status_choice = input("Select status (1-4): ").strip()
                status_map = {'1': 'Pending', '2': 'In Progress', 
                            '3': 'Resolved', '4': 'Closed'}
                if status_choice in status_map:
                    enquiries[idx]['status'] = status_map[status_choice]
                
                response = input("\nEnter response: ").strip()
                if response:
                    enquiries[idx]['response'] = response
                
                save_enquiries()
                print("✓ Enquiry updated!")
            else:
                print("✗ Invalid enquiry number!")
        except ValueError:
            print("✗ Invalid input!")
    
    pause()


def manager_profile():
    clear_screen()
    mgr_data = managers[current_manager]
    print_header("MANAGER PROFILE")
    print(f"Manager ID:    {mgr_data['id']}")
    print(f"Name:           {mgr_data['name']}")
    print(f"Age:            {mgr_data['age']}")
    print(f"Address:        {mgr_data['address']}")
    print(f"Phone:          {mgr_data['phone']}")
    print(f"Email:          {mgr_data['email']}")
    print(f"Position:       {mgr_data['position']}")
    print(f"Username:       {mgr_data['username']}")
    print(f"Password:       {'*' * len(mgr_data['password'])}")
    
    print("\nOptions:")
    print("1. Edit Profile")
    print("2. Reset Password")
    print("3. Back")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        edit_manager_profile()
    elif choice == "2":
        manager_reset_password()


def edit_manager_profile():
    global current_manager
    mgr_data = managers[current_manager]
    
    clear_screen()
    print_header("EDIT MANAGER PROFILE")
    print("(Press Enter to keep current value)")
    
    # Name
    new_name = input(f"Name [{mgr_data['name']}]: ").strip()
    if new_name:
        mgr_data['name'] = new_name
    
    # Age
    new_age = input(f"Age [{mgr_data['age']}]: ").strip()
    if new_age:
        if validate_age(new_age):
            mgr_data['age'] = new_age
        else:
            print("✗ Invalid age! Keeping current value.")
    
    # Address
    new_address = input(f"Address [{mgr_data['address']}]: ").strip()
    if new_address:
        mgr_data['address'] = new_address
    
    # Phone
    new_phone = input(f"Phone [{mgr_data['phone']}]: ").strip()
    if new_phone:
        if validate_phone(new_phone):
            mgr_data['phone'] = new_phone
        else:
            print("✗ Invalid phone! Keeping current value.")
    
    # Email
    new_email = input(f"Email [{mgr_data['email']}]: ").strip()
    if new_email:
        if validate_email(new_email):
            # Check if email exists
            email_exists = False
            for username, data in managers.items():
                if username != current_manager and data['email'] == new_email:
                    email_exists = True
                    break
            if not email_exists:
                mgr_data['email'] = new_email
            else:
                print("✗ Email already in use! Keeping current value.")
        else:
            print("✗ Invalid email! Keeping current value.")
    
    # Position
    new_position = input(f"Position [{mgr_data['position']}]: ").strip()
    if new_position:
        mgr_data['position'] = new_position
    
    # Username
    new_username = input(f"Username [{mgr_data['username']}]: ").strip()
    if new_username and new_username != current_manager:
        if new_username in managers:
            print("✗ Username already exists! Keeping current value.")
        else:
            managers[new_username] = managers.pop(current_manager)
            current_manager = new_username
    
    save_managers()
    print("\n✓ Profile updated successfully!")
    pause()


def manager_reset_password():
    mgr_data = managers[current_manager]
    
    clear_screen()
    print_header("RESET MANAGER PASSWORD")
    
    current_pass = getpass.getpass("Current password: ").strip()
    if mgr_data['password'] != current_pass:
        print("\n✗ Current password is incorrect!")
        pause()
        return
    
    new_pass = getpass.getpass("New password: ").strip()
    if not new_pass:
        print("\n✗ Password cannot be empty!")
        pause()
        return
    
    confirm_pass = getpass.getpass("Confirm password: ").strip()
    
    if new_pass != confirm_pass:
        print("\n✗ Passwords do not match!")
        pause()
        return
    
    mgr_data['password'] = new_pass
    save_managers()
    print("\n✓ Password reset successfully!")
    pause()


# ---------------- BOSS FUNCTIONS ----------------


def view_managers():
    clear_screen()
    print_header("MANAGER LIST")
    
    if not managers:
        print("\nNo managers in the system.")
        pause()
        return
    
    print(f"\n{'Username':<12} {'Name':<20} {'ID':<8} {'Email':<25} {'Position':<20}")
    print("-"*85)
    for username, data in managers.items():
        print(f"{username:<12} {data['name']:<20} {data['id']:<8} "
              f"{data['email']:<25} {data['position']:<20}")
    pause()


def add_manager():
    clear_screen()
    print_header("ADD NEW MANAGER")
    print("(All fields are required)")
    
    username = input("Username: ").strip()
    if not username:
        print("\n✗ Username cannot be empty!")
        pause()
        return
    
    if username in managers:
        print(f"\n✗ Username '{username}' already exists!")
        pause()
        return
    
    password = getpass.getpass("Password: ").strip()
    if not password:
        print("\n✗ Password cannot be empty!")
        pause()
        return
    
    name = input("Full Name: ").strip()
    if not name:
        print("\n✗ Name cannot be empty!")
        pause()
        return
    
    age = input("Age: ").strip()
    if not age or not validate_age(age):
        print("\n✗ Age must be between 18 and 100!")
        pause()
        return
    
    address = input("Address: ").strip()
    if not address:
        print("\n✗ Address cannot be empty!")
        pause()
        return
    
    phone = input("Phone: ").strip()
    if not phone or not validate_phone(phone):
        print("\n✗ Phone must contain only digits!")
        pause()
        return
    
    email = input("Email: ").strip()
    if not email or not validate_email(email):
        print("\n✗ Please enter a valid email!")
        pause()
        return
    
    # Check if email exists
    for data in managers.values():
        if data["email"] == email:
            print(f"\n✗ Email '{email}' already exists!")
            pause()
            return
    
    position = input("Position: ").strip()
    if not position:
        print("\n✗ Position cannot be empty!")
        pause()
        return
    
    manager_id = input("Manager ID: ").strip()
    if not manager_id:
        print("\n✗ Manager ID cannot be empty!")
        pause()
        return
    
    # Check if ID exists
    for data in managers.values():
        if data["id"] == manager_id:
            print(f"\n✗ Manager ID '{manager_id}' already exists!")
            pause()
            return
    
    managers[username] = {
        "username": username,
        "password": password,
        "name": name,
        "age": age,
        "address": address,
        "phone": phone,
        "email": email,
        "position": position,
        "id": manager_id
    }
    
    save_managers()
    print(f"\n✓ Manager '{name}' added successfully!")
    pause()


def delete_manager():
    clear_screen()
    print_header("DELETE MANAGER")
    
    if not managers:
        print("\nNo managers in the system.")
        pause()
        return
    
    print("\nManagers:")
    for i, (username, data) in enumerate(managers.items(), 1):
        print(f"{i}. {username} - {data['name']} (ID: {data['id']})")
    
    try:
        choice = int(input("\nSelect manager number to delete (0 to cancel): "))
        if 1 <= choice <= len(managers):
            username = list(managers.keys())[choice-1]
            manager_data = managers[username]
            
            confirm = input(f"Are you sure you want to delete '{manager_data['name']}'? (y/n): ").lower()
            if confirm == 'y':
                del managers[username]
                save_managers()
                print(f"\n✓ Manager '{manager_data['name']}' deleted successfully!")
            else:
                print("\nDeletion cancelled.")
        elif choice != 0:
            print("\n✗ Invalid selection!")
    except ValueError:
        print("\n✗ Invalid input!")
    
    pause()


def boss_profile():
    clear_screen()
    print_header("BOSS PROFILE")
    print(f"Username: {boss['username']}")
    print(f"Password: {'*' * len(boss['password'])}")
    
    print("\nOptions:")
    print("1. Edit Profile")
    print("2. Back")
    
    choice = input("\nSelect option: ").strip()
    
    if choice == "1":
        boss_edit_profile()


def boss_edit_profile():
    global current_boss, boss
    
    clear_screen()
    print_header("EDIT BOSS PROFILE")
    print("(Press Enter to keep current value)")
    
    new_username = input(f"Username [{boss['username']}]: ").strip()
    if new_username:
        boss['username'] = new_username
        current_boss = new_username
    
    new_pass = getpass.getpass("New password (Enter to skip): ").strip()
    if new_pass:
        confirm_pass = getpass.getpass("Confirm password: ").strip()
        if new_pass == confirm_pass:
            boss['password'] = new_pass
        else:
            print("✗ Passwords do not match! Password not changed.")
    
    save_boss()
    print("\n✓ Profile updated successfully!")
    pause()


# ---------------- MAIN PROGRAM ----------------


def main():
    while True:
        clear_screen()
        if not login():
            break
    
    print("\nThank you for using the Employee Management System!")


if __name__ == "__main__":
    main()
