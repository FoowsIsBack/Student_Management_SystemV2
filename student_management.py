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

class LoginApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("400x300")
        self.root.config(bg="whitesmoke")
        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="Login", font=("Poppins", 28, "bold"), fg="white", bg="firebrick3", pady=10)
        title.pack(side=tk.TOP, fill=tk.X)

        frame = tk.Frame(self.root, bg="whitesmoke", pady=20, padx=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Username:", font=("Arial", 14)).grid(row=0, column=0, pady=10, sticky=tk.W)
        tk.Entry(frame, textvariable=self.username_var, font=("Arial", 14), bd=2, relief="solid").grid(row=0, column=1, pady=10)

        tk.Label(frame, text="Password:", font=("Arial", 14)).grid(row=1, column=0, pady=10, sticky=tk.W)
        tk.Entry(frame, textvariable=self.password_var, font=("Arial", 14), bd=2, relief="solid", show="*").grid(row=1, column=1, pady=10)

        tk.Button(frame, text="Login", command=self.login, font=("Arial", 14), bg="#4CAF50", fg="white", width=10).grid(row=2, column=0, columnspan=2, pady=20)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        if verify_user(username, password):
            messagebox.showinfo("Login", "Login Successful")
            self.root.destroy()
            self.open_main_app()
        else:
            messagebox.showerror("Error", "Invalid Username or Password")

    def open_main_app(self):
        root = tk.Tk()
        app = StudentManagementApp(root)
        root.mainloop()

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("1200x650")
        self.root.config(bg="whitesmoke")
        self.name_var = tk.StringVar()
        self.age_var = tk.IntVar()
        self.gender_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.contact_var = tk.StringVar()
        self.selected_id = None
        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="Student Management System", font=("Poppins", 28, "bold"), fg="white", bg="firebrick3", pady=10)
        title.pack(side=tk.TOP, fill=tk.X)

        input_frame = tk.LabelFrame(self.root, text="Student Registration", font=("Poppins", 16, "bold"), padx=20, pady=20, bd=3, bg="whitesmoke", relief="solid", fg="black")
        input_frame.place(x=20, y=100, width=400, height=400)

        tk.Label(input_frame, text="Name:", font=("Arial", 14)).grid(row=0, column=0, pady=10, sticky=tk.W)
        tk.Entry(input_frame, textvariable=self.name_var, font=("Arial", 15), bd=2, relief="solid", width=20).grid(row=0, column=1, pady=10, padx=10)

        tk.Label(input_frame, text="Age:", font=("Arial", 14)).grid(row=1, column=0, pady=10, sticky=tk.W)
        tk.Entry(input_frame, textvariable=self.age_var, font=("Arial", 15), bd=2, relief="solid", width=20).grid(row=1, column=1, pady=10, padx=10)

        tk.Label(input_frame, text="Contact:", font=("Arial", 14)).grid(row=2, column=0, pady=10, sticky=tk.W)
        tk.Entry(input_frame, textvariable=self.contact_var, font=("Arial", 15), bd=2, relief="solid", width=20).grid(row=2, column=1, pady=10, padx=10)

        tk.Label(input_frame, text="Gender:", font=("Arial", 14)).grid(row=3, column=0, pady=10, sticky=tk.W)
        gender_combo = ttk.Combobox(input_frame, textvariable=self.gender_var, values=("Male", "Female"), state="readonly", font=("Arial", 15), width=20)
        gender_combo.grid(row=3, column=1, pady=10, padx=10)
        gender_combo.set("Select Gender")

        tk.Label(input_frame, text="Course:", font=("Arial", 14)).grid(row=4, column=0, pady=10, sticky=tk.W)
        course_combo = ttk.Combobox(input_frame, textvariable=self.course_var, 
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

        tk.Button(btn_frame, text="Add", command=self.add_record, font=("Arial", 14), bg="#4CAF50", fg="white", width=5).grid(row=0, column=0, padx=10)
        tk.Button(btn_frame, text="Update", command=self.update_record, font=("Arial", 14), bg="#2196F3", fg="white", width=5).grid(row=0, column=1, padx=10)
        tk.Button(btn_frame, text="Delete", command=self.delete_record, font=("Arial", 14), bg="#F44336", fg="white", width=5).grid(row=0, column=2, padx=10)

        table_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE, bg="#ECEFF1")
        table_frame.place(x=450, y=100, width=700, height=400)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Age", "Gender", "Course", "Contact"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Course", text="Course")
        self.tree.heading("Contact", text="Contact")

        self.tree.column("ID", width=50, anchor=tk.CENTER)
        self.tree.column("Name", width=150)
        self.tree.column("Age", width=50, anchor=tk.CENTER)
        self.tree.column("Gender", width=100, anchor=tk.CENTER)
        self.tree.column("Course", width=150)
        self.tree.column("Contact", width=150)

        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_record)

        self.load_data()

    def load_data(self):
        self.tree.delete(*self.tree.get_children())
        students = fetch_students()
        for student in students:
            self.tree.insert("", tk.END, values=student)

    def add_record(self):
        name, age, gender, course, contact = self.name_var.get(), self.age_var.get(), self.gender_var.get(), self.course_var.get(), self.contact_var.get()
        if name and age and gender != "Select Gender" and course != "Select Course" and contact:
            add_student(name, age, gender, course, contact)
            self.load_data()
            self.clear_form()
        else:
            messagebox.showerror("Error", "All fields are required!")

    def update_record(self):
        if self.selected_id:
            name, age, gender, course, contact = self.name_var.get(), self.age_var.get(), self.gender_var.get(), self.course_var.get(), self.contact_var.get()
            if name and age and gender != "Select Gender" and course != "Select Course" and contact:
                update_student(self.selected_id, name, age, gender, course, contact)
                self.load_data()
                self.clear_form()
            else:
                messagebox.showerror("Error", "All fields are required!")
        else:
            messagebox.showerror("Error", "No record selected!")

    def delete_record(self):
        if self.selected_id:
            delete_student(self.selected_id)
            self.load_data()
            self.clear_form()
        else:
            messagebox.showerror("Error", "No record selected!")

    def select_record(self, event):
        selected = self.tree.selection()
        if selected:
            data = self.tree.item(selected, "values")
            self.selected_id = data[0]
            self.name_var.set(data[1])
            self.age_var.set(data[2])
            self.gender_var.set(data[3])
            self.course_var.set(data[4])
            self.contact_var.set(data[5])

    def clear_form(self):
        self.name_var.set("")
        self.age_var.set(0)
        self.gender_var.set("Select Gender")
        self.course_var.set("Select Course")
        self.contact_var.set("")
        self.selected_id = None

if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    app = LoginApp(root)
    root.mainloop()
