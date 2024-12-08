import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

DATABASE_NAME = "result.db"

def initialize_db():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                course TEXT NOT NULL,
                contact TEXT NOT NULL
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL UNIQUE,
                password TEXT NOT NULL
            )
        """)
        cursor.execute("INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)", 
                       ("admin", "admin"))
        conn.commit()

def verify_user(username, password):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ? AND password = ?", (username, password))
        return cursor.fetchone()

def register_user(username, password):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        try:
            cursor.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
            conn.commit()
            messagebox.showinfo("Registration", "Registration Successful")
        except sqlite3.IntegrityError:
            messagebox.showerror("Error", "Username already exists")

def add_student(name, age, gender, course, contact):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, gender, course, contact) VALUES (?, ?, ?, ?, ?)", 
                       (name, age, gender, course, contact))
        conn.commit()

def update_student(student_id, name, age, gender, course, contact):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students 
            SET name = ?, age = ?, gender = ?, course = ?, contact = ? 
            WHERE id = ?
        """, (name, age, gender, course, contact, student_id))
        conn.commit()

def delete_student(student_id):
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()

def fetch_students():
    with sqlite3.connect(DATABASE_NAME) as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        return cursor.fetchall()

def login(root):
    username = username_var.get()
    password = password_var.get()

    if verify_user(username, password):
        messagebox.showinfo("Login", "Login Successful")
        root.destroy()
        open_main_app()
    else:
        messagebox.showerror("Error", "Invalid Username or Password")

def register(root):
    root.destroy()
    registration_ui()

def open_main_app():
    root = tk.Tk()
    setup_ui(root)
    root.mainloop()

def setup_ui(root):
    global name_var, age_var, gender_var, course_var, contact_var, selected_id, tree

    name_var = tk.StringVar()
    age_var = tk.IntVar()
    gender_var = tk.StringVar()
    course_var = tk.StringVar()
    contact_var = tk.StringVar()
    selected_id = None

    root.title("Student Management System")
    root.geometry("1200x650")
    root.config(bg="whitesmoke")

    title = tk.Label(root, text="Student Management System", font=("bold", 28, "bold"), fg="white", bg="firebrick3", pady=10)
    title.pack(side=tk.TOP, fill=tk.X)

    input_frame = tk.LabelFrame(root, text="Student Registration", font=("Poppins", 16, "bold"), padx=20, pady=20, bd=3, bg="whitesmoke", relief="solid", fg="black")
    input_frame.place(x=20, y=100, width=400, height=400)

    tk.Label(input_frame, text="Name:", font=("Arial", 14)).grid(row=0, column=0, pady=10, sticky=tk.W)
    tk.Entry(input_frame, textvariable=name_var, font=("Arial", 15), bd=2, relief="solid", width=20).grid(row=0, column=1, pady=10, padx=10)
    tk.Label(input_frame, text="Age:", font=("Arial", 14)).grid(row=1, column=0, pady=10, sticky=tk.W)
    tk.Entry(input_frame, textvariable=age_var, font=("Arial", 15), bd=2, relief="solid", width=20).grid(row=1, column=1, pady=10, padx=10)
    tk.Label(input_frame, text="Contact:", font=("Arial", 14)).grid(row=2, column=0, pady=10, sticky=tk.W)
    tk.Entry(input_frame, textvariable=contact_var, font=("Arial", 15), bd=2, relief="solid", width=20).grid(row=2, column=1, pady=10, padx=10)
    tk.Label(input_frame, text="Gender:", font=("Arial", 14)).grid(row=3, column=0, pady=10, sticky=tk.W)
    gender_combo = ttk.Combobox(input_frame, textvariable=gender_var, values=("Male", "Female"), state="readonly", font=("Arial", 15), width=20)
    gender_combo.grid(row=3, column=1, pady=10, padx=10)
    gender_combo.set("Select Gender")

    tk.Label(input_frame, text="Course:", font=("Arial", 14)).grid(row=4, column=0, pady=10, sticky=tk.W)
    course_combo = ttk.Combobox(input_frame, textvariable=course_var, 
                                values=("BS in Information Technology (BSIT)", 
                                        "BS in Civil Engineering (BSCE)", 
                                        "BS in Mechanical Engineering (BSME)", 
                                        "BS in Industrial Technology (Culinary Arts)", 
                                        "BS in Industrial Technology (Electronics)"), 
                                state="readonly", font=("Arial", 15), width=20)
    course_combo.grid(row=4, column=1, pady=10, padx=10)
    course_combo.set("Select Course")

    btn_frame = tk.Frame(input_frame, bg="#ECEFF1")
    btn_frame.grid(row=5, column=0, columnspan=2, pady=15, padx=10)

    tk.Button(btn_frame, text="Add", command=add_record, font=("Arial", 14), bg="#4CAF50", fg="white", width=5).grid(row=0, column=0, padx=10)
    tk.Button(btn_frame, text="Update", command=update_record, font=("Arial", 14), bg="#2196F3", fg="white", width=5).grid(row=0, column=1, padx=10)
    tk.Button(btn_frame, text="Delete", command=delete_record, font=("Arial", 14), bg="#F44336", fg="white", width=5).grid(row=0, column=2, padx=10)
    table_frame = tk.Frame(root, bd=2, relief=tk.RIDGE, bg="#ECEFF1")
    table_frame.place(x=450, y=100, width=700, height=400)

    tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Age", "Gender", "Course", "Contact"), show="headings")
    tree.heading("ID", text="ID")
    tree.heading("Name", text="Name")
    tree.heading("Age", text="Age")
    tree.heading("Gender", text="Gender")
    tree.heading("Course", text="Course")
    tree.heading("Contact", text="Contact")

    tree.column("ID", width=50, anchor=tk.CENTER)
    tree.column("Name", width=150)
    tree.column("Age", width=50, anchor=tk.CENTER)
    tree.column("Gender", width=100, anchor=tk.CENTER)
    tree.column("Course", width=150)
    tree.column("Contact", width=150)
    tree.pack(fill=tk.BOTH, expand=True)
    tree.bind("<ButtonRelease-1>", select_record)
    load_data(tree)

def load_data(tree):
    tree.delete(*tree.get_children())
    students = fetch_students()
    for student in students:
        tree.insert("", tk.END, values=student)

def add_record():
    name, age, gender, course, contact = name_var.get(), age_var.get(), gender_var.get(), course_var.get(), contact_var.get()
    if name and age and gender != "Select Gender" and course != "Select Course" and contact:
        add_student(name, age, gender, course, contact)
        load_data(tree)
        clear_form()
    else:
        messagebox.showerror("Error", "All fields are required!")

def update_record():
    global selected_id
    if selected_id:
        name, age, gender, course, contact = name_var.get(), age_var.get(), gender_var.get(), course_var.get(), contact_var.get()
        if name and age and gender != "Select Gender" and course != "Select Course" and contact:
            update_student(selected_id, name, age, gender, course, contact)
            load_data(tree)
            clear_form()
        else:
            messagebox.showerror("Error", "All fields are required!")
    else:
        messagebox.showerror("Error", "No record selected!")

def delete_record():
    global selected_id
    if selected_id:
        delete_student(selected_id)
        load_data(tree)
        clear_form()
    else:
        messagebox.showerror("Error", "No record selected!")

def select_record(event):
    global selected_id
    selected = tree.selection()
    if selected:
        data = tree.item(selected, "values")
        selected_id = data[0]
        name_var.set(data[1])
        age_var.set(data[2])
        gender_var.set(data[3])
        course_var.set(data[4])
        contact_var.set(data[5])

def clear_form():
    name_var.set("")
    age_var.set(0)
    gender_var.set("Select Gender")
    course_var.set("Select Course")
    contact_var.set("")
    global selected_id
    selected_id = None

def login_ui(root):
    global username_var, password_var
    root.title("Student Management System")
    root.geometry("500x400")
    root.config(bg="whitesmoke") 

    title = tk.Label(root, text="Login Account", font=("bold", 28, "bold"), fg="white", bg="firebrick3", pady=10)
    title.pack(side=tk.TOP, fill=tk.X)
    frame = tk.Frame(root, bg="whitesmoke")
    frame.pack(pady=10, padx=20)

    tk.Label(frame, text="Username:", font=("Arial", 14), bg="whitesmoke", anchor="w").grid(row=0, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(frame, textvariable=username_var, font=("Arial", 14), bd=2, relief="solid", width=25).grid(row=0, column=1, pady=10, padx=10)

    tk.Label(frame, text="Password:", font=("Arial", 14), bg="whitesmoke", anchor="w").grid(row=1, column=0, pady=10, padx=10, sticky="w")
    tk.Entry(frame, textvariable=password_var, font=("Arial", 14), bd=2, relief="solid", show="*", width=25).grid(row=1, column=1, pady=10, padx=10)

    button_frame = tk.Frame(root, bg="whitesmoke")
    button_frame.pack(pady=20)

    tk.Button(button_frame, text="Login", command=lambda: login(root), font=("Arial", 14), bg="#4CAF50", fg="white", width=12).grid(row=0, column=0, padx=10, pady=5)
    tk.Button(button_frame, text="Register", command=lambda: register(root), font=("Arial", 14), bg="#2196F3", fg="white", width=12).grid(row=0, column=1, padx=10, pady=5)
    tk.Button(button_frame, text="Exit", command=root.destroy, font=("Arial", 14), bg="#F44336", fg="white", width=12).grid(row=1, column=0, columnspan=2, pady=10)

def registration_ui():
    reg_root = tk.Tk()
    reg_root.title("Register Form")
    reg_root.geometry("500x400")
    reg_root.config(bg="whitesmoke")

    reg_username_var = tk.StringVar()
    reg_password_var = tk.StringVar()

    def showpassword():
        if password_entry.cget('show') == '*':
            password_entry.config(show='')
            toggle_btn.config(text="Hide")
        else:
            password_entry.config(show='*')
            toggle_btn.config(text="Show")

    title = tk.Label(reg_root, text="Register Account", font=("bold", 28, "bold"), fg="white", bg="firebrick3", pady=10)
    title.pack(side=tk.TOP, fill=tk.X)    
    frame = tk.Frame(reg_root, bg="whitesmoke")
    frame.pack(pady=10)

    tk.Label(frame, text="Username:", font=("Arial", 14), bg="whitesmoke").grid(row=0, column=0, pady=5, padx=10, sticky=tk.W)
    tk.Entry(frame, textvariable=reg_username_var, font=("Arial", 14), bd=2, relief="solid", width=25).grid(row=0, column=1, pady=5)

    tk.Label(frame, text="Password:", font=("Arial", 14), bg="whitesmoke").grid(row=1, column=0, pady=5, padx=10, sticky=tk.W)
    password_entry = tk.Entry(frame, textvariable=reg_password_var, font=("Arial", 14), bd=2, relief="solid", show="*", width=25)
    password_entry.grid(row=1, column=1, pady=5)

    toggle_btn = tk.Button(frame, text="Show", font=("Arial", 10), bg="lightgray", command=showpassword)
    toggle_btn.grid(row=1, column=2, padx=5)

    tk.Button(frame, text="Register", command=lambda: register_user(reg_username_var.get(), reg_password_var.get()),font=("Arial", 14), bg="#4CAF50", fg="white", width=12).grid(row=2, column=0, columnspan=2, pady=10)
    tk.Button(frame, text="Back", command=reg_root.destroy, font=("Arial", 14), bg="#F44336", fg="white", width=12).grid(row=3, column=0, columnspan=2, pady=10)
    reg_root.mainloop()

if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    username_var = tk.StringVar()
    password_var = tk.StringVar()
    login_ui(root)
    root.mainloop()
