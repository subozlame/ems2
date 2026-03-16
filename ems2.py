import tkinter as tk
from tkinter import ttk, messagebox
import csv
import os

EMP_FILE = "employees.csv"
MANAGER_FILE = "manager.csv"
SUGGESTIONS_FILE = "suggestions.csv"
ENQUIRIES_FILE = "enquiries.csv"
BOSS_FILE = "boss.csv"

employees = {}
suggestions = []
enquiries = []
managers = {}  # For multiple managers if needed

boss = {"username": "boss", "password": "boss123"}
manager = {"username": "manager", "password": "manager123"}

# ---------------- CSV ----------------


def load_employees():

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

    if not os.path.exists(SUGGESTIONS_FILE):
        return

    with open(SUGGESTIONS_FILE, newline="") as f:

        reader = csv.DictReader(f)

        for r in reader:

            suggestions.append(r)


def save_suggestions():

    with open(SUGGESTIONS_FILE, "w", newline="") as f:

        fields = ["employee", "suggestion", "date"]

        writer = csv.DictWriter(f, fieldnames=fields)

        writer.writeheader()

        for s in suggestions:
            writer.writerow(s)


def load_enquiries():

    if not os.path.exists(ENQUIRIES_FILE):
        return

    with open(ENQUIRIES_FILE, newline="") as f:

        reader = csv.DictReader(f)

        for r in reader:

            enquiries.append(r)


def save_enquiries():

    with open(ENQUIRIES_FILE, "w", newline="") as f:

        fields = ["employee", "enquiry", "date"]

        writer = csv.DictWriter(f, fieldnames=fields)

        writer.writeheader()

        for e in enquiries:
            writer.writerow(e)

# ---------------- BOSS CSV ----------------


def load_boss():
    global boss

    if not os.path.exists(BOSS_FILE):
        # Create default boss if file doesn't exist
        boss = {"username": "boss", "password": "boss123"}
        save_boss()
        return

    with open(BOSS_FILE, newline="") as f:
        reader = csv.DictReader(f)
        for r in reader:
            boss = {
                "username": r["username"],
                "password": r["password"]
            }
            break  # Only one boss record


def save_boss():
    with open(BOSS_FILE, "w", newline="") as f:
        fields = ["username", "password"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerow(boss)

# ---------------- MANAGER CSV ----------------


def load_managers():
    global managers
    managers = {}

    if not os.path.exists(MANAGER_FILE):
        # Create default managers if file doesn't exist
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
            },
            "manager2": {
                "username": "manager2",
                "password": "manager456",
                "name": "Jane Smith",
                "age": "42",
                "address": "456 Oak Ave",
                "phone": "555-5678",
                "email": "manager2@company.com",
                "position": "Operations Manager",
                "id": "MGR002"
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
    try:
        with open(MANAGER_FILE, "w", newline="") as f:
            fields = ["username", "password", "name", "age", "address",
                      "phone", "email", "position", "id"]
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()
            for manager_data in managers.values():
                writer.writerow(manager_data)
        return True
    except Exception as e:
        print(f"Save managers error: {e}")
        return False


load_employees()
load_managers()
load_suggestions()
load_enquiries()
load_boss()
current_boss = boss["username"] if boss else None
current_manager = None
employee_name = None

# ---------------- WINDOW ----------------

root = tk.Tk()
root.title("Employee Management System")

w = root.winfo_screenwidth()
h = root.winfo_screenheight()

root.geometry(f"{w}x{h}")

bg = "#f1f5f9"
sidebar_color = "#1e293b"
btn = "#2563eb"

root.configure(bg=bg)

# ---------------- LAYOUT ----------------

sidebar = tk.Frame(root, bg=sidebar_color, width=250)
sidebar.pack(side="left", fill="y")

content = tk.Frame(root, bg=bg)
content.pack(side="right", expand=True, fill="both")

# ---------------- UTIL ----------------


def clear(frame):

    for i in frame.winfo_children():
        i.destroy()

# ---------------- LOGOUT ----------------


def logout():

    global current_manager, current_boss, employee_name

    clear(sidebar)
    clear(content)
    main_menu()

# ---------------- TABLE ----------------


def view_employees():

    clear(content)

    tk.Label(content, text="Employees",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=20)

    table = ttk.Treeview(content)

    table["columns"] = ("id", "designation", "age",
                        "address", "salary", "email")

    table.heading("#0", text="Name")
    table.heading("id", text="ID")
    table.heading("designation", text="Designation")
    table.heading("age", text="Age")
    table.heading("address", text="Address")
    table.heading("salary", text="Salary")
    table.heading("email", text="Email")

    table.pack(fill="both", expand=True, padx=20, pady=20)

    def load(data):

        table.delete(*table.get_children())

        for n, d in data.items():

            table.insert("", tk.END, text=n,
                         values=(d["id"], d["designation"], d["age"],
                                 d["address"], d["salary"], d["email"]))

    load(employees)

# ---------------- ADD ----------------


def add_employee():

    clear(content)

    tk.Label(content, text="Add Employee",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=20)

    form = tk.Frame(content, bg=bg)
    form.pack()

    fields = ["name", "id", "designation", "age",
              "address", "salary", "email", "password"]

    entries = {}

    for i, f in enumerate(fields):
        tk.Label(form, text=f.capitalize() + " *",
                 font=("Arial", 14), bg=bg).grid(row=i, column=0, padx=10, pady=10, sticky="e")

        e = tk.Entry(form, font=("Arial", 14), width=30)
        e.grid(row=i, column=1, pady=5)

        # Add tooltip or hint for specific fields
        if f == "age":
            e.insert(0, "Enter number only")
            e.bind("<FocusIn>", lambda event,
                   entry=e: clear_placeholder(entry, "Enter number only"))
        elif f == "salary":
            e.insert(0, "Enter number only")
            e.bind("<FocusIn>", lambda event,
                   entry=e: clear_placeholder(entry, "Enter number only"))
        elif f == "email":
            e.insert(0, "example@domain.com")
            e.bind("<FocusIn>", lambda event, entry=e: clear_placeholder(
                entry, "example@domain.com"))
        elif f == "password":
            e.config(show="*")

        entries[f] = e

    # Add note about required fields
    tk.Label(content, text="* Required fields", font=("Arial", 10, "italic"),
             bg=bg, fg="gray").pack()

    def clear_placeholder(entry, placeholder):
        """Clear placeholder text when entry gets focus"""
        if entry.get() == placeholder:
            entry.delete(0, tk.END)

    def validate_fields():
        """Validate all fields before saving"""
        empty_fields = []
        invalid_fields = []

        # Check for empty fields
        for f in fields:
            value = entries[f].get().strip()
            if not value or value in ["Enter number only", "example@domain.com"]:
                empty_fields.append(f.capitalize())

        if empty_fields:
            messagebox.showerror(
                "Error", f"The following fields cannot be empty:\n{', '.join(empty_fields)}")
            return False

        # Validate age (must be number)
        age_value = entries["age"].get().strip()
        try:
            age = int(age_value)
            if age < 18 or age > 100:
                invalid_fields.append("Age must be between 18 and 100")
        except ValueError:
            invalid_fields.append("Age must be a valid number")

        # Validate salary (must be number)
        salary_value = entries["salary"].get().strip()
        try:
            salary = float(salary_value)
            if salary < 0:
                invalid_fields.append("Salary cannot be negative")
        except ValueError:
            invalid_fields.append("Salary must be a valid number")

        # Validate email format
        email_value = entries["email"].get().strip()
        if "@" not in email_value or "." not in email_value:
            invalid_fields.append("Email must be valid (contain @ and .)")

        # Check if employee ID already exists
        id_value = entries["id"].get().strip()
        for emp_data in employees.values():
            if emp_data["id"] == id_value:
                invalid_fields.append(
                    f"Employee ID '{id_value}' already exists")
                break

        # Check if email already exists
        for emp_data in employees.values():
            if emp_data["email"] == email_value:
                invalid_fields.append(
                    f"Email '{email_value}' is already registered")
                break

        if invalid_fields:
            messagebox.showerror("Validation Error", "\n".join(invalid_fields))
            return False

        return True

    def reset_form():
        """Clear all fields after successful save"""
        for f in fields:
            entries[f].delete(0, tk.END)

        # Reset placeholders
        entries["age"].insert(0, "Enter number only")
        entries["salary"].insert(0, "Enter number only")
        entries["email"].insert(0, "example@domain.com")

    def save():

        if not validate_fields():
            return

        name = entries["name"].get().strip()

        # Check if employee name already exists
        if name in employees:
            messagebox.showerror("Error", f"Employee '{name}' already exists!")
            return

        # Create employee dictionary
        employees[name] = {
            "name": name,
            "id": entries["id"].get().strip(),
            "designation": entries["designation"].get().strip(),
            "age": entries["age"].get().strip(),
            "address": entries["address"].get().strip(),
            "salary": entries["salary"].get().strip(),
            "email": entries["email"].get().strip(),
            "password": entries["password"].get().strip()
        }

        # Save to CSV
        save_employees()

        messagebox.showinfo(
            "Success", f"Employee '{name}' added successfully!")

        # Reset all fields for next entry
        reset_form()

    # Button frame
    button_frame = tk.Frame(content, bg=bg)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Save Employee", font=("Arial", 14),
              bg="green", fg="white", command=save, width=15).pack(side=tk.LEFT, padx=10)

    tk.Button(button_frame, text="Clear Form", font=("Arial", 14),
              bg="orange", fg="white", command=reset_form, width=15).pack(side=tk.LEFT, padx=10)


# ---------------- EDIT ----------------


def edit_employee():

    clear(content)

    tk.Label(content, text="Edit Employee",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=20)

    # Create a frame for the name input and load button
    name_frame = tk.Frame(content, bg=bg)
    name_frame.pack(pady=10)

    # Label for name
    tk.Label(name_frame, text="Employee Name:", font=(
        "Arial", 14), bg=bg).pack(side=tk.LEFT, padx=5)

    # Name entry field
    name_entry = tk.Entry(name_frame, font=("Arial", 14), width=30)
    name_entry.pack(side=tk.LEFT, padx=5)

    # Load button on the right side
    tk.Button(name_frame, text="Load", bg="blue", fg="white",
              font=("Arial", 12), command=lambda: load()).pack(side=tk.LEFT, padx=5)

    form = tk.Frame(content, bg=bg)
    form.pack(pady=20)

    fields = ["designation", "age", "address", "salary", "email"]

    entries = {}

    for i, f in enumerate(fields):
        tk.Label(form, text=f.capitalize() + ":", font=("Arial", 14),
                 bg=bg).grid(row=i, column=0, padx=10, pady=5, sticky="e")
        e = tk.Entry(form, font=("Arial", 14), width=30)
        e.grid(row=i, column=1, pady=5)
        entries[f] = e

    def load():

        name = name_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Please enter an employee name!")
            return

        if name in employees:

            d = employees[name]

            for f in fields:
                entries[f].delete(0, tk.END)
                entries[f].insert(0, d[f])

            messagebox.showinfo("Success", f"Data loaded for {name}")

        else:
            messagebox.showerror("Error", f"Employee '{name}' not found")
            # Clear fields if employee not found
            for f in fields:
                entries[f].delete(0, tk.END)

    def save():

        name = name_entry.get().strip()

        if not name:
            messagebox.showerror("Error", "Please enter an employee name!")
            return

        if name in employees:

            # Check for empty fields
            empty_fields = []
            for f in fields:
                if not entries[f].get().strip():
                    empty_fields.append(f)

            if empty_fields:
                messagebox.showerror(
                    "Error", f"The following fields cannot be empty:\n{', '.join(empty_fields)}")
                return

            for f in fields:
                employees[name][f] = entries[f].get().strip()

            save_employees()

            messagebox.showinfo("Success", "Employee updated successfully!")

            # Clear all fields after successful save
            name_entry.delete(0, tk.END)  # Clear the name field
            for f in fields:
                entries[f].delete(0, tk.END)  # Clear all other fields

        else:
            messagebox.showerror("Error", f"Employee '{name}' not found")

    # Save button
    tk.Button(content, text="Save Changes", bg="green", fg="white",
              font=("Arial", 14), command=save, width=15).pack(pady=10)


# ---------------- DELETE ----------------


def delete_employee():

    clear(content)

    tk.Label(content, text="Delete Employee",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=20)

    search_frame = tk.Frame(content, bg=bg)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search by:", font=(
        "Arial", 14), bg=bg).pack(side=tk.LEFT, padx=5)

    search_by = ttk.Combobox(search_frame, values=[
                             "Name", "ID", "Email"], font=("Arial", 14), width=10)
    search_by.set("Name")
    search_by.pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(content, font=("Arial", 14), width=40)
    search_entry.pack(pady=5)

    result_frame = tk.Frame(content, bg=bg)
    result_frame.pack(pady=10)

    def search_employee():
        clear(result_frame)

        search_term = search_entry.get().strip().lower()
        search_type = search_by.get()

        if not search_term:
            messagebox.showerror("Error", "Please enter search term")
            return

        found = []

        for name, data in employees.items():
            if search_type == "Name" and search_term in name.lower():
                found.append((name, data))
            elif search_type == "ID" and search_term in data["id"].lower():
                found.append((name, data))
            elif search_type == "Email" and search_term in data["email"].lower():
                found.append((name, data))

        if not found:
            tk.Label(result_frame, text="No employees found",
                     font=("Arial", 14), bg=bg, fg="red").pack()
            return

        for name, data in found:
            emp_frame = tk.Frame(result_frame, bg=bg, relief=tk.RAISED, bd=2)
            emp_frame.pack(fill="x", pady=5, padx=20)

            tk.Label(emp_frame, text=f"Name: {name}", font=(
                "Arial", 12, "bold"), bg=bg).pack(anchor="w", padx=10)
            tk.Label(emp_frame, text=f"ID: {data['id']}", font=(
                "Arial", 12), bg=bg).pack(anchor="w", padx=10)
            tk.Label(emp_frame, text=f"Email: {data['email']}", font=(
                "Arial", 12), bg=bg).pack(anchor="w", padx=10)

            tk.Button(emp_frame, text="Delete", bg="red", fg="white",
                      command=lambda n=name: confirm_delete(n)).pack(pady=5)

    def confirm_delete(name):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
            del employees[name]
            save_employees()
            messagebox.showinfo("Deleted", f"{name} has been deleted")
            search_employee()  # Refresh results

    tk.Button(content, text="Search", command=search_employee,
              bg=btn, fg="white").pack(pady=10)

# ---------------- RESET PASSWORD ----------------


def reset_password():

    clear(content)

    tk.Label(content, text="Reset Password",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=20)

    # Employee Name field with label
    tk.Label(content, text="Employee Name:", font=("Arial", 14), bg=bg).pack()
    name = tk.Entry(content, font=("Arial", 14), width=30)
    name.pack(pady=(0, 10))

    # New Password field with label
    tk.Label(content, text="New Password:", font=("Arial", 14), bg=bg).pack()
    new = tk.Entry(content, font=("Arial", 14), width=30)
    new.pack(pady=(0, 10))

    # Optional: Confirm Password field for better security
    tk.Label(content, text="Confirm Password:",
             font=("Arial", 14), bg=bg).pack()
    confirm = tk.Entry(content, font=("Arial", 14), width=30)
    confirm.pack(pady=(0, 20))

    def reset():

        n = name.get().strip()  # Remove any extra spaces
        new_pass = new.get()
        confirm_pass = confirm.get()

        # Validation
        if not n or not new_pass:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        if n in employees:

            employees[n]["password"] = new_pass

            save_employees()

            messagebox.showinfo("Success", f"Password updated for {n}")

            # Clear fields after successful reset
            name.delete(0, tk.END)
            new.delete(0, tk.END)
            confirm.delete(0, tk.END)

        else:

            messagebox.showerror("Error", f"Employee '{n}' not found")

    # Button frame for better layout
    button_frame = tk.Frame(content, bg=bg)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Reset Password", bg="blue", fg="white",
              command=reset, font=("Arial", 12), width=15).pack(side=tk.LEFT, padx=5)

    tk.Button(button_frame, text="Clear", bg="orange", fg="white",
              command=lambda: [name.delete(0, tk.END), new.delete(
                  0, tk.END), confirm.delete(0, tk.END)],
              font=("Arial", 12), width=10).pack(side=tk.LEFT, padx=5)

    tk.Button(button_frame, text="Back", bg="gray", fg="white",
              command=lambda: login("employee"), font=("Arial", 12), width=10).pack(side=tk.LEFT, padx=5)
# ---------------- EMPLOYEE PAGE ----------------


def employee_dashboard(name):

    clear(sidebar)
    clear(content)

    d = employees[name]

    tk.Label(content, text=f"Welcome {name}",
             font=("Arial", 30, "bold"), bg=bg).pack(pady=30)

    tk.Label(content, text=f"Email: {d['email']}", font=(
        "Arial", 16), bg=bg).pack()
    tk.Label(content, text=f"Designation: {d['designation']}", font=(
        "Arial", 16), bg=bg).pack()

    tk.Button(content, text="Logout", bg="red", fg="white",
              command=logout).pack(pady=30)

# ---------------- EMPLOYEE PROFILE ----------------


def employee_profile(name):

    clear(content)

    d = employees[name]

    tk.Label(content, text="My Profile",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    # Employee details
    details_frame = tk.Frame(content, bg=bg)
    details_frame.pack(pady=10)

    tk.Label(details_frame, text=f"Name: {name}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")
    tk.Label(details_frame, text=f"ID: {d['id']}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")
    tk.Label(details_frame, text=f"Designation: {d['designation']}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")
    tk.Label(details_frame, text=f"Age: {d['age']}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")
    tk.Label(details_frame, text=f"Address: {d['address']}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")
    tk.Label(details_frame, text=f"Salary: {d['salary']}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")
    tk.Label(details_frame, text=f"Email: {d['email']}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")
    tk.Label(details_frame, text=f"Password: {'*' * len(d['password'])}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")

    tk.Button(content, text="Edit Profile", bg="blue", fg="white",
              command=lambda: employee_edit_profile(name)).pack(pady=10)

    tk.Button(content, text="Back", bg="gray", fg="white",
              command=lambda: employee_dashboard(name)).pack(pady=5)


def employee_edit_profile(name):

    clear(content)

    d = employees[name]

    tk.Label(content, text="Edit My Profile",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    form = tk.Frame(content, bg=bg)
    form.pack()

    # Editable fields (excluding name, id, password for security)
    fields = ["designation", "age", "address", "salary", "email"]
    entries = {}

    for i, f in enumerate(fields):
        tk.Label(form, text=f.capitalize(), font=("Arial", 14),
                 bg=bg).grid(row=i, column=0, padx=10, pady=10)
        e = tk.Entry(form, font=("Arial", 14), width=30)
        e.grid(row=i, column=1)
        e.insert(0, d[f])
        entries[f] = e

    # Password change section
    tk.Label(content, text="Change Password (Optional)",
             font=("Arial", 16, "bold"), bg=bg).pack(pady=20)

    pass_frame = tk.Frame(content, bg=bg)
    pass_frame.pack()

    tk.Label(pass_frame, text="New Password:", font=("Arial", 14),
             bg=bg).grid(row=0, column=0, padx=10, pady=5)
    new_pass = tk.Entry(pass_frame, font=("Arial", 14), width=30)
    new_pass.grid(row=0, column=1)

    tk.Label(pass_frame, text="Confirm Password:", font=(
        "Arial", 14), bg=bg).grid(row=1, column=0, padx=10, pady=5)
    confirm_pass = tk.Entry(pass_frame, font=("Arial", 14), width=30)
    confirm_pass.grid(row=1, column=1)

    def save():
        # Update regular fields
        for f in fields:
            employees[name][f] = entries[f].get()

        # Update password if provided
        if new_pass.get():
            if new_pass.get() == confirm_pass.get():
                employees[name]["password"] = new_pass.get()
            else:
                messagebox.showerror("Error", "Passwords do not match!")
                return

        save_employees()
        messagebox.showinfo("Success", "Profile updated successfully!")
        employee_profile(name)

    tk.Button(content, text="Save Changes", bg="green", fg="white",
              command=save, font=("Arial", 14)).pack(pady=20)

    tk.Button(content, text="Cancel", bg="gray", fg="white",
              command=lambda: employee_profile(name)).pack()

# ---------------- EMPLOYEE SUGGESTIONS ----------------


def employee_suggestions(name):

    clear(content)

    tk.Label(content, text="Give Suggestion",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    tk.Label(content, text="Your Suggestion:",
             font=("Arial", 14), bg=bg).pack()
    suggestion_text = tk.Text(content, font=("Arial", 14), height=10, width=50)
    suggestion_text.pack(pady=10)

    def submit():
        suggestion = suggestion_text.get("1.0", tk.END).strip()
        if not suggestion:
            messagebox.showerror("Error", "Please enter a suggestion")
            return

        from datetime import datetime
        suggestions.append({
            "employee": name,
            "suggestion": suggestion,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_suggestions()

        messagebox.showinfo("Success", "Suggestion submitted successfully!")
        employee_dashboard(name)

    tk.Button(content, text="Submit", bg="green", fg="white",
              command=submit, font=("Arial", 14)).pack(pady=10)

    tk.Button(content, text="Cancel", bg="gray", fg="white",
              command=lambda: employee_dashboard(name)).pack()

# ---------------- EMPLOYEE ENQUIRIES ----------------


def employee_enquiries(name):

    clear(content)

    tk.Label(content, text="Make Enquiry",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    tk.Label(content, text="Your Enquiry:", font=("Arial", 14), bg=bg).pack()
    enquiry_text = tk.Text(content, font=("Arial", 14), height=10, width=50)
    enquiry_text.pack(pady=10)

    def submit():
        enquiry = enquiry_text.get("1.0", tk.END).strip()
        if not enquiry:
            messagebox.showerror("Error", "Please enter an enquiry")
            return

        from datetime import datetime
        enquiries.append({
            "employee": name,
            "enquiry": enquiry,
            "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        })
        save_enquiries()

        messagebox.showinfo("Success", "Enquiry submitted successfully!")
        employee_dashboard(name)

    tk.Button(content, text="Submit", bg="green", fg="white",
              command=submit, font=("Arial", 14)).pack(pady=10)

    tk.Button(content, text="Cancel", bg="gray", fg="white",
              command=lambda: employee_dashboard(name)).pack()

# ---------------- EMPLOYEE RESET PASSWORD ----------------


def employee_reset_password(name):

    clear(content)

    tk.Label(content, text="Reset My Password",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    tk.Label(content, text="Current Password:",
             font=("Arial", 14), bg=bg).pack()
    current = tk.Entry(content, font=("Arial", 14), show="*", width=30)
    current.pack(pady=5)

    tk.Label(content, text="New Password:", font=("Arial", 14), bg=bg).pack()
    new = tk.Entry(content, font=("Arial", 14), show="*", width=30)
    new.pack(pady=5)

    tk.Label(content, text="Confirm New Password:",
             font=("Arial", 14), bg=bg).pack()
    confirm = tk.Entry(content, font=("Arial", 14), show="*", width=30)
    confirm.pack(pady=5)

    def reset():
        current_pass = current.get()
        new_pass = new.get()
        confirm_pass = confirm.get()

        if employees[name]["password"] != current_pass:
            messagebox.showerror("Error", "Current password is incorrect!")
            return

        if not new_pass:
            messagebox.showerror("Error", "New password cannot be empty!")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "New passwords do not match!")
            return

        employees[name]["password"] = new_pass
        save_employees()

        messagebox.showinfo("Success", "Password reset successfully!")
        employee_dashboard(name)

    tk.Button(content, text="Reset Password", bg="blue", fg="white",
              command=reset, font=("Arial", 14)).pack(pady=20)

    tk.Button(content, text="Cancel", bg="gray", fg="white",
              command=lambda: employee_dashboard(name)).pack()


# ---------------- MANAGER PROFILE ----------------
# ---------------- MANAGER PROFILE ----------------
def manager_profile():
    global current_manager, managers
    clear(content)

    # Get data for logged-in manager
    manager_data = managers[current_manager]

    tk.Label(content, text=f"Manager Profile - {manager_data['name']}",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    # Manager details in a frame
    details_frame = tk.Frame(content, bg=bg)
    details_frame.pack(pady=10)

    tk.Label(details_frame, text=f"Manager ID: {manager_data.get('id', 'N/A')}", font=(
        "Arial", 16), bg=bg).pack(anchor="w", pady=2)
    tk.Label(details_frame, text=f"Name: {manager_data.get('name', 'N/A')}", font=(
        "Arial", 16), bg=bg).pack(anchor="w", pady=2)
    tk.Label(details_frame, text=f"Age: {manager_data.get('age', 'N/A')}", font=(
        "Arial", 16), bg=bg).pack(anchor="w", pady=2)
    tk.Label(details_frame, text=f"Address: {manager_data.get('address', 'N/A')}", font=(
        "Arial", 16), bg=bg).pack(anchor="w", pady=2)
    tk.Label(details_frame, text=f"Phone: {manager_data.get('phone', 'N/A')}", font=(
        "Arial", 16), bg=bg).pack(anchor="w", pady=2)
    tk.Label(details_frame, text=f"Email: {manager_data.get('email', 'N/A')}", font=(
        "Arial", 16), bg=bg).pack(anchor="w", pady=2)
    tk.Label(details_frame, text=f"Position: {manager_data.get('position', 'N/A')}", font=(
        "Arial", 16), bg=bg).pack(anchor="w", pady=2)
    tk.Label(details_frame, text=f"Username: {manager_data['username']}", font=(
        "Arial", 16), bg=bg).pack(anchor="w", pady=2)
    tk.Label(details_frame, text=f"Password: {'*' * len(manager_data['password'])}", font=(
        "Arial", 16), bg=bg).pack(anchor="w", pady=2)

    # Button frame
    button_frame = tk.Frame(content, bg=bg)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Edit Profile", bg="blue", fg="white",
              command=manager_edit_profile, font=("Arial", 14), width=15).pack(side=tk.LEFT, padx=10)

    tk.Button(button_frame, text="Reset Password", bg="orange", fg="white",
              command=manager_reset_password, font=("Arial", 14), width=15).pack(side=tk.LEFT, padx=10)


def manager_edit_profile():
    global current_manager, managers
    clear(content)

    # Get data for logged-in manager
    manager_data = managers[current_manager]

    tk.Label(content, text="Edit Manager Profile",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    # Create a form frame
    form_frame = tk.Frame(content, bg=bg)
    form_frame.pack()

    # Personal Information Section
    tk.Label(form_frame, text="Personal Information", font=("Arial", 18, "bold"),
             bg=bg).grid(row=0, column=0, columnspan=2, pady=10)

    # Manager ID (read-only)
    tk.Label(form_frame, text="Manager ID:", font=("Arial", 14), bg=bg).grid(
        row=1, column=0, padx=10, pady=5, sticky="e")
    id_label = tk.Label(form_frame, text=manager_data.get(
        'id', 'N/A'), font=("Arial", 14), bg=bg)
    id_label.grid(row=1, column=1, pady=5, sticky="w")

    # Name field
    tk.Label(form_frame, text="Name:*", font=("Arial", 14),
             bg=bg).grid(row=2, column=0, padx=10, pady=5, sticky="e")
    name_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    name_entry.insert(0, manager_data.get("name", ""))
    name_entry.grid(row=2, column=1, pady=5)

    # Age field
    tk.Label(form_frame, text="Age:*", font=("Arial", 14),
             bg=bg).grid(row=3, column=0, padx=10, pady=5, sticky="e")
    age_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    age_entry.insert(0, manager_data.get("age", ""))
    age_entry.grid(row=3, column=1, pady=5)

    # Address field
    tk.Label(form_frame, text="Address:*", font=("Arial", 14),
             bg=bg).grid(row=4, column=0, padx=10, pady=5, sticky="e")
    address_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    address_entry.insert(0, manager_data.get("address", ""))
    address_entry.grid(row=4, column=1, pady=5)

    # Phone field
    tk.Label(form_frame, text="Phone:*", font=("Arial", 14),
             bg=bg).grid(row=5, column=0, padx=10, pady=5, sticky="e")
    phone_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    phone_entry.insert(0, manager_data.get("phone", ""))
    phone_entry.grid(row=5, column=1, pady=5)

    # Email field
    tk.Label(form_frame, text="Email:*", font=("Arial", 14),
             bg=bg).grid(row=6, column=0, padx=10, pady=5, sticky="e")
    email_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    email_entry.insert(0, manager_data.get("email", ""))
    email_entry.grid(row=6, column=1, pady=5)

    # Position field
    tk.Label(form_frame, text="Position:*", font=("Arial", 14),
             bg=bg).grid(row=7, column=0, padx=10, pady=5, sticky="e")
    position_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    position_entry.insert(0, manager_data.get("position", ""))
    position_entry.grid(row=7, column=1, pady=5)

    # Account Information Section
    tk.Label(form_frame, text="Account Information", font=("Arial", 18, "bold"),
             bg=bg).grid(row=8, column=0, columnspan=2, pady=10)

    # Username field
    tk.Label(form_frame, text="Username:*", font=("Arial", 14),
             bg=bg).grid(row=9, column=0, padx=10, pady=5, sticky="e")
    username_entry = tk.Entry(form_frame, font=("Arial", 14), width=30)
    username_entry.insert(0, manager_data['username'])
    username_entry.grid(row=9, column=1, pady=5)

    # Note about password
    tk.Label(form_frame, text="(To change password, use the Reset Password button)",
             font=("Arial", 12, "italic"), bg=bg, fg="gray").grid(row=10, column=0, columnspan=2, pady=5)

    def save():
        # Get all field values
        new_name = name_entry.get().strip()
        new_age = age_entry.get().strip()
        new_address = address_entry.get().strip()
        new_phone = phone_entry.get().strip()
        new_email = email_entry.get().strip()
        new_position = position_entry.get().strip()
        new_username = username_entry.get().strip()

        # Check for empty required fields
        empty_fields = []
        if not new_name:
            empty_fields.append("Name")
        if not new_age:
            empty_fields.append("Age")
        if not new_address:
            empty_fields.append("Address")
        if not new_phone:
            empty_fields.append("Phone")
        if not new_email:
            empty_fields.append("Email")
        if not new_position:
            empty_fields.append("Position")
        if not new_username:
            empty_fields.append("Username")

        if empty_fields:
            messagebox.showerror(
                "Error", f"The following fields cannot be empty:\n{', '.join(empty_fields)}")
            return

        # Validate age is number
        try:
            age_int = int(new_age)
            if age_int < 18 or age_int > 100:
                messagebox.showerror(
                    "Error", "Age must be between 18 and 100!")
                return
        except ValueError:
            messagebox.showerror("Error", "Age must be a number!")
            return

        # Validate email format (basic)
        if "@" not in new_email or "." not in new_email:
            messagebox.showerror(
                "Error", "Please enter a valid email address!")
            return

        # Check if username already exists (if changed)
        if new_username != current_manager and new_username in managers:
            messagebox.showerror(
                "Error", "Username already exists! Please choose a different username.")
            return

        # Store old username for dict key update
        old_username = current_manager

        # Update manager data
        managers[old_username]["name"] = new_name
        managers[old_username]["age"] = new_age
        managers[old_username]["address"] = new_address
        managers[old_username]["phone"] = new_phone
        managers[old_username]["email"] = new_email
        managers[old_username]["position"] = new_position

        # Update username if changed
        if new_username != old_username:
            managers[new_username] = managers.pop(old_username)
            managers[new_username]["username"] = new_username
            current_manager = new_username

        # SAVE TO CSV FILE
        try:
            # Call save_managers function
            with open(MANAGER_FILE, "w", newline="") as f:
                fields = ["username", "password", "name", "age", "address",
                          "phone", "email", "position", "id"]
                writer = csv.DictWriter(f, fieldnames=fields)
                writer.writeheader()
                for manager_data in managers.values():
                    writer.writerow(manager_data)

            messagebox.showinfo("Success", "Profile Updated Successfully!")
            manager_profile()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save: {str(e)}")
            print(f"Save error: {e}")  # Debug print

    # Buttons frame
    button_frame = tk.Frame(content, bg=bg)
    button_frame.pack(pady=20)

    # Save Changes button
    save_button = tk.Button(button_frame, text="Save Changes", bg="green", fg="white",
                            command=save, font=("Arial", 14), width=15)
    save_button.pack(side=tk.LEFT, padx=10)

    # Cancel button
    cancel_button = tk.Button(button_frame, text="Cancel", bg="gray", fg="white",
                              command=manager_profile, font=("Arial", 14), width=15)
    cancel_button.pack(side=tk.LEFT, padx=10)


def manager_reset_password():
    global current_manager, managers
    clear(content)

    manager_data = managers[current_manager]

    tk.Label(content, text="Reset Manager Password",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    tk.Label(content, text=f"Manager: {manager_data['name']} ({manager_data['username']})",
             font=("Arial", 16), bg=bg).pack(pady=10)

    tk.Label(content, text="Current Password:",
             font=("Arial", 14), bg=bg).pack()
    current = tk.Entry(content, font=("Arial", 14), show="*", width=30)
    current.pack(pady=5)

    tk.Label(content, text="New Password:", font=("Arial", 14), bg=bg).pack()
    new = tk.Entry(content, font=("Arial", 14), show="*", width=30)
    new.pack(pady=5)

    tk.Label(content, text="Confirm New Password:",
             font=("Arial", 14), bg=bg).pack()
    confirm = tk.Entry(content, font=("Arial", 14), show="*", width=30)
    confirm.pack(pady=5)

    def reset():
        current_pass = current.get()
        new_pass = new.get()
        confirm_pass = confirm.get()

        if manager_data["password"] != current_pass:
            messagebox.showerror("Error", "Current password is incorrect!")
            return

        if not new_pass:
            messagebox.showerror("Error", "New password cannot be empty!")
            return

        if new_pass != confirm_pass:
            messagebox.showerror("Error", "New passwords do not match!")
            return

        managers[current_manager]["password"] = new_pass

        # SAVE TO CSV FILE
        save_managers()

        messagebox.showinfo("Success", "Password reset successfully!")
        manager_profile()

    tk.Button(content, text="Reset Password", bg="blue", fg="white",
              command=reset, font=("Arial", 14)).pack(pady=20)

    tk.Button(content, text="Cancel", bg="gray", fg="white",
              command=manager_profile).pack()

# ---------------- MANAGER SEARCH EMPLOYEE ----------------


def manager_search_employee():

    clear(content)

    tk.Label(content, text="Search Employees",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=20)

    search_frame = tk.Frame(content, bg=bg)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search by:", font=(
        "Arial", 14), bg=bg).pack(side=tk.LEFT, padx=5)

    search_by = ttk.Combobox(search_frame, values=[
                             "Name", "ID", "Email"], font=("Arial", 14), width=10)
    search_by.set("Name")
    search_by.pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(content, font=("Arial", 14), width=50)
    search_entry.pack(pady=5)

    result_frame = tk.Frame(content, bg=bg)
    result_frame.pack(pady=10, fill="both", expand=True)

    def search():
        clear(result_frame)

        search_term = search_entry.get().strip().lower()
        search_type = search_by.get()

        if not search_term:
            messagebox.showerror("Error", "Please enter search term")
            return

        found = []

        for name, data in employees.items():
            if search_type == "Name" and search_term in name.lower():
                found.append((name, data))
            elif search_type == "ID" and search_term in data["id"].lower():
                found.append((name, data))
            elif search_type == "Email" and search_term in data["email"].lower():
                found.append((name, data))

        if not found:
            tk.Label(result_frame, text="No employees found",
                     font=("Arial", 14), bg=bg, fg="red").pack()
            return

        # Create table for results
        table = ttk.Treeview(result_frame)
        table["columns"] = ("id", "designation", "email")
        table.heading("#0", text="Name")
        table.heading("id", text="ID")
        table.heading("designation", text="Designation")
        table.heading("email", text="Email")
        table.pack(fill="both", expand=True)

        for name, data in found:
            table.insert("", tk.END, text=name,
                         values=(data["id"], data["designation"], data["email"]))

    tk.Button(content, text="Search", command=search, bg=btn,
              fg="white", font=("Arial", 14)).pack(pady=10)

# ---------------- MANAGER DELETE EMPLOYEE ----------------


def manager_delete_employee():

    clear(content)

    tk.Label(content, text="Delete Employee",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=20)

    search_frame = tk.Frame(content, bg=bg)
    search_frame.pack(pady=10)

    tk.Label(search_frame, text="Search by:", font=(
        "Arial", 14), bg=bg).pack(side=tk.LEFT, padx=5)

    search_by = ttk.Combobox(search_frame, values=[
                             "Name", "ID", "Email"], font=("Arial", 14), width=10)
    search_by.set("Name")
    search_by.pack(side=tk.LEFT, padx=5)

    search_entry = tk.Entry(content, font=("Arial", 14), width=40)
    search_entry.pack(pady=5)

    result_frame = tk.Frame(content, bg=bg)
    result_frame.pack(pady=10, fill="both", expand=True)

    def search():
        clear(result_frame)

        search_term = search_entry.get().strip().lower()
        search_type = search_by.get()

        if not search_term:
            messagebox.showerror("Error", "Please enter search term")
            return

        found = []

        for name, data in employees.items():
            if search_type == "Name" and search_term in name.lower():
                found.append((name, data))
            elif search_type == "ID" and search_term in data["id"].lower():
                found.append((name, data))
            elif search_type == "Email" and search_term in data["email"].lower():
                found.append((name, data))

        if not found:
            tk.Label(result_frame, text="No employees found",
                     font=("Arial", 14), bg=bg, fg="red").pack()
            return

        for name, data in found:
            emp_frame = tk.Frame(result_frame, bg=bg, relief=tk.RAISED, bd=2)
            emp_frame.pack(fill="x", pady=5, padx=20)

            tk.Label(emp_frame, text=f"Name: {name}", font=(
                "Arial", 12, "bold"), bg=bg).pack(anchor="w", padx=10)
            tk.Label(emp_frame, text=f"ID: {data['id']}", font=(
                "Arial", 12), bg=bg).pack(anchor="w", padx=10)
            tk.Label(emp_frame, text=f"Email: {data['email']}", font=(
                "Arial", 12), bg=bg).pack(anchor="w", padx=10)

            tk.Button(emp_frame, text="Delete", bg="red", fg="white",
                      command=lambda n=name: confirm_delete(n)).pack(pady=5)

    def confirm_delete(name):
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete {name}?"):
            del employees[name]
            save_employees()
            messagebox.showinfo("Deleted", f"{name} has been deleted")
            search()  # Refresh results

    tk.Button(content, text="Search", command=search, bg=btn,
              fg="white", font=("Arial", 14)).pack(pady=10)

# ---------------- DASHBOARD ----------------


def dashboard(role):

    clear(sidebar)

    if role == "boss":

        btns = [("Add Employee", add_employee),
                ("View Employees", view_employees),
                ("Edit Employee", edit_employee),
                ("Delete Employee", delete_employee),
                ("Reset Password", reset_password),
                ("Profile", boss_profile)]

    elif role == "manager":
        btns = [("View Employees", view_employees),
                ("Search Employee", manager_search_employee),
                ("Delete Employee", manager_delete_employee),
                ("Add Employee", add_employee),
                ("Edit Employee", edit_employee),
                ("Profile", manager_profile)]

    else:  # employee
        btns = [("My Profile", lambda: employee_profile(employee_name)),
                ("Edit Profile", lambda: employee_edit_profile(employee_name)),
                ("Reset Password", lambda: employee_reset_password(employee_name)),
                ("Give Suggestion", lambda: employee_suggestions(employee_name)),
                ("Make Enquiry", lambda: employee_enquiries(employee_name))]

    for t, c in btns:

        tk.Button(sidebar, text=t, font=("Arial", 14),
                  bg=btn, fg="white", command=c).pack(fill="x", pady=5, padx=10)

    tk.Button(sidebar, text="Logout", bg="red", fg="white",
              command=logout).pack(fill="x", pady=20, padx=10)

# ---------------- LOGIN ----------------


def login(role):
    global current_manager, current_boss, employee_name
    win = tk.Toplevel()

    tk.Label(win, text="Username").pack()
    u = tk.Entry(win)
    u.pack()

    tk.Label(win, text="Password").pack()
    p = tk.Entry(win, show="*")
    p.pack()

    def check():
        username = u.get()
        password = p.get()

        if role == "boss":
            if username == boss["username"] and password == boss["password"]:
                win.destroy()
                global current_boss
                current_boss = username
                dashboard("boss")
                view_employees()
            else:
                messagebox.showerror("Error", "Invalid boss login")

        elif role == "manager":
            # Check if username exists in managers dict and password matches
            if username in managers and managers[username]["password"] == password:
                win.destroy()
                global current_manager
                current_manager = username  # Store which manager is logged in
                dashboard("manager")
                view_employees()
            else:
                messagebox.showerror("Error", "Invalid manager login")

        elif role == "employee":
            if username in employees and employees[username]["password"] == password:
                win.destroy()
                global employee_name
                employee_name = username
                dashboard("employee")
                employee_dashboard(username)
            else:
                messagebox.showerror("Error", "Invalid employee login")

    tk.Button(win, text="Login", command=check).pack(pady=10)

# ---------------- MAIN MENU ----------------


def main_menu():

    tk.Label(sidebar, text="MENU",
             bg=sidebar_color, fg="white",
             font=("Arial", 18, "bold")).pack(pady=20)

    tk.Button(sidebar, text="Boss Login",
              command=lambda: login("boss")).pack(fill="x", pady=5, padx=10)

    tk.Button(sidebar, text="Manager Login",
              command=lambda: login("manager")).pack(fill="x", pady=5, padx=10)

    tk.Button(sidebar, text="Employee Login",
              command=lambda: login("employee")).pack(fill="x", pady=5, padx=10)

    tk.Label(content, text="Employee Management System",
             font=("Arial", 34, "bold"), bg=bg).pack(pady=200)


# ---------------- BOSS PROFILE ---------

def boss_profile():
    global boss
    clear(content)

    tk.Label(content, text=f"Boss Profile - {boss['username']}",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    # Boss details
    details_frame = tk.Frame(content, bg=bg)
    details_frame.pack(pady=10)

    tk.Label(details_frame, text=f"Username: {boss['username']}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")
    tk.Label(details_frame, text=f"Password: {'*' * len(boss['password'])}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")

    # Edit Profile Button
    tk.Button(content, text="Edit Profile", bg="blue", fg="white",
              command=boss_edit_profile).pack(pady=20)

    tk.Button(content, text="Logout", bg="red", fg="white",
              command=logout).pack(pady=10)


def view_manager():
    clear(content)

    tk.Label(content, text="Manager Details",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    # Manager details
    details_frame = tk.Frame(content, bg=bg)
    details_frame.pack(pady=10)

    tk.Label(details_frame, text=f"Username: {manager['username']}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")
    tk.Label(details_frame, text=f"Password: {'*' * len(manager['password'])}", font=(
        "Arial", 16), bg=bg).pack(anchor="w")

    tk.Button(content, text="Back", bg="gray", fg="white",
              command=boss_profile).pack(pady=20)


def view_all_employees():
    view_employees()  # Reuse existing view_employees function


def boss_edit_profile():
    global boss, current_boss
    clear(content)

    tk.Label(content, text="Edit Profile",
             font=("Arial", 28, "bold"), bg=bg).pack(pady=30)

    # Username field
    tk.Label(content, text="Username:", font=("Arial", 14), bg=bg).pack()
    username_entry = tk.Entry(content, font=("Arial", 14))
    username_entry.insert(0, boss['username'])
    username_entry.pack(pady=(0, 10))

    # Password field
    tk.Label(content, text="New Password:", font=("Arial", 14), bg=bg).pack()
    password_entry = tk.Entry(content, font=("Arial", 14))
    password_entry.pack(pady=(0, 10))

    # Confirm Password field
    tk.Label(content, text="Confirm Password:",
             font=("Arial", 14), bg=bg).pack()
    confirm_entry = tk.Entry(content, font=("Arial", 14))
    confirm_entry.pack(pady=(0, 20))

    def save():
        new_username = username_entry.get()
        new_password = password_entry.get()
        confirm_password = confirm_entry.get()

        # Validation
        if not new_username:
            messagebox.showerror("Error", "Username cannot be empty!")
            return

        if new_password and new_password != confirm_password:
            messagebox.showerror("Error", "Passwords do not match!")
            return

        # Update boss dictionary
        old_username = boss["username"]
        boss["username"] = new_username
        if new_password:
            boss["password"] = new_password

        # Update current_boss if username changed
        if new_username != old_username:
            current_boss = new_username

        save_boss()  # Save changes to CSV
        messagebox.showinfo("Success", "Profile Updated Successfully!")
        boss_profile()

    # Buttons frame
    button_frame = tk.Frame(content, bg=bg)
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Save Changes", bg="green", fg="white",
              command=save).pack(side=tk.LEFT, padx=10)

    tk.Button(button_frame, text="Cancel", bg="gray", fg="white",
              command=boss_profile).pack(side=tk.LEFT, padx=10)


def boss_dashboard():

    clear(sidebar)
    clear(content)

    tk.Label(content, text=f"Welcome Boss",
             font=("Arial", 30, "bold"), bg=bg).pack(pady=30)

    tk.Button(content, text="View Manager", bg="green", fg="white",
              command=view_manager).pack(pady=10)

    tk.Button(content, text="View Employees", bg="blue", fg="white",
              command=view_all_employees).pack(pady=10)

    tk.Button(content, text="Logout", bg="red", fg="white",
              command=logout).pack(pady=30)


# ---------------- START ----------------

main_menu()

root.mainloop()
