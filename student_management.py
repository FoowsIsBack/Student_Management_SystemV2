import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3

def initialize_db():
    with sqlite3.connect("student_management.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                age INTEGER NOT NULL,
                gender TEXT NOT NULL,
                course TEXT NOT NULL
            )
        """)
        conn.commit()

def add_student(name, age, gender, course):
    with sqlite3.connect("student_management.db") as conn:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO students (name, age, gender, course) VALUES (?, ?, ?, ?)", 
                       (name, age, gender, course))
        conn.commit()

def fetch_students():
    with sqlite3.connect("student_management.db") as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM students")
        rows = cursor.fetchall()
    return rows

def update_student(student_id, name, age, gender, course):
    with sqlite3.connect("student_management.db") as conn:
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE students
            SET name = ?, age = ?, gender = ?, course = ?
            WHERE id = ?
        """, (name, age, gender, course, student_id))
        conn.commit()

def delete_student(student_id):
    with sqlite3.connect("student_management.db") as conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM students WHERE id = ?", (student_id,))
        conn.commit()

class StudentManagementApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Student Management System")
        self.root.geometry("800x500")

        self.name_var = tk.StringVar()
        self.age_var = tk.IntVar()
        self.gender_var = tk.StringVar()
        self.course_var = tk.StringVar()
        self.selected_id = None

        self.setup_ui()

    def setup_ui(self):
        title = tk.Label(self.root, text="EVSU Student Management System", font=("Arial", 20, "bold"))
        title.pack(side=tk.TOP, fill=tk.X)

        input_frame = tk.LabelFrame(self.root, text="Student Registration", font=("Arial", 12, "bold"), padx=10, pady=10)
        input_frame.place(x=10, y=50, width=300, height=400)

        tk.Label(input_frame, text="Name:", font=("Arial", 10)).grid(row=0, column=0, pady=5, sticky=tk.W)
        tk.Entry(input_frame, textvariable=self.name_var, font=("Arial", 10)).grid(row=0, column=1, pady=5)

        tk.Label(input_frame, text="Age:", font=("Arial", 10)).grid(row=1, column=0, pady=5, sticky=tk.W)
        tk.Entry(input_frame, textvariable=self.age_var, font=("Arial", 10)).grid(row=1, column=1, pady=5)

        tk.Label(input_frame, text="Gender:", font=("Arial", 10)).grid(row=2, column=0, pady=5, sticky=tk.W)
        gender_combo = ttk.Combobox(input_frame, textvariable=self.gender_var, values=("Male", "Female"), state="readonly", font=("Arial", 10))
        gender_combo.grid(row=2, column=1, pady=5)
        gender_combo.set("Select Gender")

        tk.Label(input_frame, text="Course:", font=("Arial", 10)).grid(row=3, column=0, pady=5, sticky=tk.W)
        course_combo = ttk.Combobox(input_frame, textvariable=self.course_var, 
                                    values=("BS in Information Technology (BSIT)", "BS in Industrial Technology (Electronics)", "BS in Civil Engineering (BSCE)", "BS in Mechanical Engineering (BSME)", 
                                            "BS in Industrial Technology (Culinary Arts)"), state="readonly", font=("Arial", 10))
        course_combo.grid(row=3, column=1, pady=5)
        course_combo.set("Select Course")

        btn_frame = tk.Frame(input_frame)
        btn_frame.grid(row=4, column=0, columnspan=2, pady=10)

        tk.Button(btn_frame, text="Add", command=self.add_record, font=("Arial", 10), width=5).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Update", command=self.update_record, font=("Arial", 10), width=5).pack(side=tk.LEFT, padx=10)
        tk.Button(btn_frame, text="Delete", command=self.delete_record, font=("Arial", 10), width=5).pack(side=tk.LEFT, padx=10)

        table_frame = tk.Frame(self.root, bd=2, relief=tk.RIDGE)
        table_frame.place(x=320, y=50, width=1000, height=400)

        self.tree = ttk.Treeview(table_frame, columns=("ID", "Name", "Age", "Gender", "Course"), show="headings")
        self.tree.heading("ID", text="ID")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Age", text="Age")
        self.tree.heading("Gender", text="Gender")
        self.tree.heading("Course", text="Course")

        self.tree.column("ID", width=50)
        self.tree.column("Name", width=100)
        self.tree.column("Age", width=50)
        self.tree.column("Gender", width=100)
        self.tree.column("Course", width=150)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        self.tree.bind("<ButtonRelease-1>", self.select_record)

        self.load_data()

    def load_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for row in fetch_students():
            self.tree.insert("", tk.END, values=row)

    def select_record(self, event):
        selected = self.tree.focus()
        data = self.tree.item(selected, "values")
        if data:
            self.name_var.set(data[1])
            self.age_var.set(data[2])
            self.gender_var.set(data[3])
            self.course_var.set(data[4])
            self.selected_id = data[0]

    def add_record(self):
        if not self.name_var.get():
            messagebox.showerror("Error", "Name is required")
            return
        if self.gender_var.get() == "Select Gender":
            messagebox.showerror("Error", "Please select a gender")
            return
        if self.course_var.get() == "Select Course":
            messagebox.showerror("Error", "Please select a course")
            return
        add_student(self.name_var.get(), self.age_var.get(), self.gender_var.get(), self.course_var.get())
        self.load_data()
        messagebox.showinfo("Success", "Student added successfully")

    def update_record(self):
        if self.selected_id is None:
            messagebox.showerror("Error", "No student selected")
            return
        update_student(self.selected_id, self.name_var.get(), self.age_var.get(), self.gender_var.get(), self.course_var.get())
        self.load_data()
        messagebox.showinfo("Success", "Student updated successfully")

    def delete_record(self):
        if self.selected_id is None:
            messagebox.showerror("Error", "No student selected")
            return
        delete_student(self.selected_id)
        self.load_data()
        messagebox.showinfo("Success", "Student deleted successfully")

if __name__ == "__main__":
    initialize_db()
    root = tk.Tk()
    root.attributes("-zoomed", True)
    app = StudentManagementApp(root)
    root.mainloop()
