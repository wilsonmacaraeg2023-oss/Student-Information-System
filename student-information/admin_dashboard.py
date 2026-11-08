import tkinter as tk
from tkinter import messagebox, ttk

import database
from database import student_records, find_student


class AdminDashboard(tk.Frame):
    """Admin screen with full Create / Read / Update / Delete on student records."""

    def __init__(self, parent, on_logout):
        super().__init__(parent, bg="#f0f0f0")
        self.on_logout = on_logout
        self.build()
        self.refresh_table()

    def build(self):
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill="x")
        tk.Label(header, text="🎓 Student Information System - Admin", bg="#2c3e50",
                 fg="white", font=("Arial", 18, "bold")).pack(side="left", padx=20, pady=15)
        tk.Button(header, text="Logout", bg="#e74c3c", fg="white", width=10,
                  command=self.on_logout).pack(side="right", padx=20)

        # --- Form ---
        form = tk.Frame(self, bg="#f0f0f0", pady=15)
        form.pack(fill="x", padx=20)

        def label(text, r, c):
            tk.Label(form, text=text, bg="#f0f0f0", font=("Arial", 10, "bold")).grid(
                row=r, column=c, sticky="w", padx=5, pady=5)

        label("Student ID:", 0, 0)
        self.admin_id = tk.Entry(form, width=20)
        self.admin_id.grid(row=0, column=1, padx=5)

        label("Full Name:", 0, 2)
        self.admin_name = tk.Entry(form, width=25)
        self.admin_name.grid(row=0, column=3, padx=5)

        label("Age:", 0, 4)
        self.admin_age = tk.Entry(form, width=10)
        self.admin_age.grid(row=0, column=5, padx=5)

        label("Course:", 1, 0)
        self.admin_course = tk.Entry(form, width=20)
        self.admin_course.grid(row=1, column=1, padx=5)

        label("Year Level:", 1, 2)
        self.admin_year = tk.Entry(form, width=25)
        self.admin_year.grid(row=1, column=3, padx=5)

        label("Email:", 1, 4)
        self.admin_email = tk.Entry(form, width=25)
        self.admin_email.grid(row=1, column=5, padx=5)

        # --- Table ---
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        columns = ("ID", "Name", "Age", "Course", "Year", "Email")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.tree.pack(side="left", fill="both", expand=True)
        self.tree.bind("<<TreeviewSelect>>", self.on_select)

        # --- Buttons ---
        btns = tk.Frame(self, bg="#f0f0f0", pady=15)
        btns.pack(fill="x", padx=20)
        font = ("Arial", 10, "bold")
        tk.Button(btns, text="➕ Create", bg="#2ecc71", fg="white", font=font, width=12,
                  command=self.add_student).pack(side="left", padx=5)
        tk.Button(btns, text="✏️ Update", bg="#f39c12", fg="white", font=font, width=12,
                  command=self.update_student).pack(side="left", padx=5)
        tk.Button(btns, text="🗑️ Delete", bg="#e74c3c", fg="white", font=font, width=12,
                  command=self.delete_student).pack(side="left", padx=5)
        tk.Button(btns, text="🧹 Clear", bg="#3498db", fg="white", font=font, width=12,
                  command=self.clear_fields).pack(side="left", padx=5)

    # ---------- helpers ----------
    def refresh_table(self):
        self.tree.delete(*self.tree.get_children())
        for r in student_records:
            self.tree.insert("", "end", values=(r["id"], r["name"], r["age"],
                                                r["course"], r["year"], r["email"]))

    def on_select(self, _event=None):
        """Fill the form with the selected row so it can be edited."""
        selected = self.tree.selection()
        if not selected:
            return
        values = self.tree.item(selected[0], "values")
        self.set_fields(values)

    def set_fields(self, values):
        entries = [self.admin_id, self.admin_name, self.admin_age,
                   self.admin_course, self.admin_year, self.admin_email]
        for entry, value in zip(entries, values):
            entry.delete(0, tk.END)
            entry.insert(0, value)

    def clear_fields(self):
        for entry in (self.admin_id, self.admin_name, self.admin_age,
                      self.admin_course, self.admin_year, self.admin_email):
            entry.delete(0, tk.END)
        self.tree.selection_remove(self.tree.selection())

    # ---------- CRUD ----------
    def add_student(self):
        new_student = {
            "id": self.admin_id.get().strip(),
            "name": self.admin_name.get().strip(),
            "age": self.admin_age.get().strip(),
            "course": self.admin_course.get().strip(),
            "year": self.admin_year.get().strip(),
            "email": self.admin_email.get().strip(),
        }
        if not all(new_student.values()):
            messagebox.showerror("Error", "All fields are required.")
            return
        if not new_student["age"].isdigit():
            messagebox.showerror("Error", "Age must be a number.")
            return
        if find_student(new_student["id"]):
            messagebox.showerror("Error", "Student ID already exists.")
            return

        student_records.append(new_student)
        self.refresh_table()
        self.clear_fields()
        messagebox.showinfo("Success", "Student added successfully.")

    def update_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to update.")
            return

        student_id = self.tree.item(selected[0], "values")[0]
        record = find_student(student_id)
        if record is None:
            return

        age = self.admin_age.get().strip()
        if age and not age.isdigit():
            messagebox.showerror("Error", "Age must be a number.")
            return

        record["name"] = self.admin_name.get().strip() or record["name"]
        record["age"] = age or record["age"]
        record["course"] = self.admin_course.get().strip() or record["course"]
        record["year"] = self.admin_year.get().strip() or record["year"]
        record["email"] = self.admin_email.get().strip() or record["email"]

        self.refresh_table()
        self.clear_fields()
        messagebox.showinfo("Success", "Student updated successfully.")

    def delete_student(self):
        selected = self.tree.selection()
        if not selected:
            messagebox.showerror("Error", "Please select a student to delete.")
            return

        student_id = self.tree.item(selected[0], "values")[0]
        if not messagebox.askyesno("Confirm", f"Delete student {student_id}?"):
            return

        # Modify in place so every module keeps seeing the same list.
        student_records[:] = [r for r in student_records if r["id"] != student_id]

        self.refresh_table()
        self.clear_fields()
        messagebox.showinfo("Success", "Student deleted successfully.")