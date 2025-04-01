import tkinter as tk
from tkinter import ttk, messagebox
import sqlite3
from datetime import datetime

class Library:
    def __init__(self, root):
        self.root = root
        self.root.title("Library Management System")
        
        # Connect to SQLite database and create table
        self.conn = sqlite3.connect("LibraryData.db")
        self.cursor = self.conn.cursor()
        self.create_table()
        
        # Frame Setup
        self.frame1 = tk.Frame(self.root)
        self.frame1.pack(side=tk.TOP, fill=tk.X)
        
        self.frame2 = tk.Frame(self.root)
        self.frame2.pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)
        
        # Input Fields
        self.book_label = tk.Label(self.frame1, text="Book Name:", font=("Arial", 14))
        self.book_label.grid(row=0, column=0, pady=5, padx=5)
        self.book_input = tk.Entry(self.frame1, font=("Arial", 14))
        self.book_input.grid(row=0, column=1, pady=5, padx=5)
        
        self.rollno_label = tk.Label(self.frame1, text="Roll No:", font=("Arial", 14))
        self.rollno_label.grid(row=0, column=2, pady=5, padx=5)
        self.rollno_input = tk.Entry(self.frame1, font=("Arial", 14))
        self.rollno_input.grid(row=0, column=3, pady=5, padx=5)

        # Additional Fields
        self.student_name_label = tk.Label(self.frame1, text="Student Name:", font=("Arial", 14))
        self.student_name_label.grid(row=1, column=0, pady=5, padx=5)
        self.student_name_input = tk.Entry(self.frame1, font=("Arial", 14))
        self.student_name_input.grid(row=1, column=1, pady=5, padx=5)

        self.course_label = tk.Label(self.frame1, text="Course Name:", font=("Arial", 14))
        self.course_label.grid(row=1, column=2, pady=5, padx=5)
        self.course_input = tk.Entry(self.frame1, font=("Arial", 14))
        self.course_input.grid(row=1, column=3, pady=5, padx=5)

        self.branch_label = tk.Label(self.frame1, text="Branch Name:", font=("Arial", 14))
        self.branch_label.grid(row=2, column=0, pady=5, padx=5)
        self.branch_input = tk.Entry(self.frame1, font=("Arial", 14))
        self.branch_input.grid(row=2, column=1, pady=5, padx=5)

        self.mobile_label = tk.Label(self.frame1, text="Mobile Number:", font=("Arial", 14))
        self.mobile_label.grid(row=2, column=2, pady=5, padx=5)
        self.mobile_input = tk.Entry(self.frame1, font=("Arial", 14))
        self.mobile_input.grid(row=2, column=3, pady=5, padx=5)

        self.date_label = tk.Label(self.frame1, text="Date of Issue (YYYY-MM-DD):", font=("Arial", 14))
        self.date_label.grid(row=3, column=0, pady=5, padx=5)
        self.date_input = tk.Entry(self.frame1, font=("Arial", 14))
        self.date_input.grid(row=3, column=1, pady=5, padx=5)
        
        # Allocate Book Button
        self.allocate_button = tk.Button(self.frame1, text="Allocate Book", font=("Arial", 14), command=self.allocate_book)
        self.allocate_button.grid(row=4, column=0, columnspan=4, pady=15)
        
        # Treeview for displaying allocated books
        self.tree = ttk.Treeview(self.frame2, columns=("Book Name", "Roll No", "Student Name", "Course Name", "Branch Name", "Mobile Number", "Date of Issue"), show="headings", height=15)
        
        # Define column headings
        self.tree.heading("Book Name", text="Book Name")
        self.tree.heading("Roll No", text="Roll No")
        self.tree.heading("Student Name", text="Student Name")
        self.tree.heading("Course Name", text="Course Name")
        self.tree.heading("Branch Name", text="Branch Name")
        self.tree.heading("Mobile Number", text="Mobile Number")
        self.tree.heading("Date of Issue", text="Date of Issue")
        
        # Define column widths
        self.tree.column("Book Name", width=100)
        self.tree.column("Roll No", width=100)
        self.tree.column("Student Name", width=150)
        self.tree.column("Course Name", width=100)
        self.tree.column("Branch Name", width=100)
        self.tree.column("Mobile Number", width=120)
        self.tree.column("Date of Issue", width=120)
        
        self.tree.pack(fill=tk.BOTH, expand=True)
        
        # Sample Books List
        self.books = [
            "Data Structures and Algorithms in C", "Operating System Concepts", 
            "Database Management Systems", "Computer Networks", "Discrete Mathematics", 
            "Programming in C", "Software Engineering", "Artificial Intelligence", 
            "Data Structures and Algorithms", "Compiler Design"
        ]
        
        # Sample Student Data
        self.students = [str(roll) for roll in range(100, 201)]

    def create_table(self):
        # Create table if it does not exist
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS allocations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_name TEXT,
                roll_no TEXT,
                student_name TEXT,
                course_name TEXT,
                branch_name TEXT,
                mobile_number TEXT,
                date_of_issue TEXT
            )
        """)
        self.conn.commit()

    def allocate_book(self):
        # Get input values
        book_name = self.book_input.get().strip()
        roll_no = self.rollno_input.get().strip()
        student_name = self.student_name_input.get().strip()
        course_name = self.course_input.get().strip()
        branch_name = self.branch_input.get().strip()
        mobile_number = self.mobile_input.get().strip()
        date_of_issue = self.date_input.get().strip()

        # Check if the book and roll number are valid
        book_found = book_name in self.books
        rollno_found = roll_no in self.students
        
        if book_found and rollno_found:
            # Insert new record in database and Treeview
            self.cursor.execute("""
                INSERT INTO allocations (book_name, roll_no, student_name, course_name, branch_name, mobile_number, date_of_issue)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (book_name, roll_no, student_name, course_name, branch_name, mobile_number, date_of_issue))
            self.conn.commit()
            self.tree.insert("", tk.END, values=(book_name, roll_no, student_name, course_name, branch_name, mobile_number, date_of_issue))
        else:
            if not book_found:
                messagebox.showerror("Error", "Book Not Found")
            if not rollno_found:
                messagebox.showerror("Error", "Invalid Roll No")
        
        # Clear input fields after allocation
        self.clear_inputs()

    def clear_inputs(self):
        # Clear all input fields
        self.book_input.delete(0, tk.END)
        self.rollno_input.delete(0, tk.END)
        self.student_name_input.delete(0, tk.END)
        self.course_input.delete(0, tk.END)
        self.branch_input.delete(0, tk.END)
        self.mobile_input.delete(0, tk.END)
        self.date_input.delete(0, tk.END)

# Run Application
root = tk.Tk()
app = Library(root)
root.mainloop()
