import tkinter as tk
from tkinter import messagebox

from database import student_records, users_db, find_student


class RegistrationForm(tk.Frame):
    """Registration screen. Replaces the login screen; calls on_back() to return to it."""

    FIELDS = ["Student ID", "Full Name", "Age", "Course", "Year Level", "Email",
              "Username", "Password"]

    def __init__(self, parent, on_back):
        super().__init__(parent, bg="#f0f0f0")
        self.on_back = on_back
        self.build()

    def build(self):
        header = tk.Frame(self, bg="#2c3e50", height=50)
        header.pack(fill="x")
        tk.Label(header, text="🎓 Register New Student", bg="#2c3e50",
                 fg="white", font=("Arial", 20, "bold")).pack(pady=10)

        form = tk.Frame(self, bg="#f0f0f0", pady=10)
        form.pack(expand=True)

        self.entries = {}
        for row, field in enumerate(self.FIELDS):
            tk.Label(form, text=f"{field}:", bg="#f0f0f0", font=("Arial", 10),
                     anchor="w", width=12).grid(row=row, column=0, sticky="w", pady=4)
            entry = tk.Entry(form, width=30, show="*" if field == "Password" else "")
            entry.grid(row=row, column=1, pady=4)
            self.entries[field] = entry

        btns = tk.Frame(form, bg="#f0f0f0")
        btns.grid(row=len(self.FIELDS), column=0, columnspan=2, pady=15)
        tk.Button(btns, text="Register", bg="#2ecc71", fg="white", width=12,
                  command=self.submit).pack(side="left", padx=5)
        tk.Button(btns, text="Back to Login", bg="#3498db", fg="white", width=12,
                  command=self.on_back).pack(side="left", padx=5)

        self.entries["Student ID"].focus_set()

    def submit(self):
        data = {k: v.get().strip() for k, v in self.entries.items()}

        if not all(data.values()):
            messagebox.showerror("Error", "All fields are required!")
            return
        if not data["Age"].isdigit():
            messagebox.showerror("Error", "Age must be a number.")
            return
        if "@" not in data["Email"]:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        if find_student(data["Student ID"]):
            messagebox.showerror("Error", "Student ID already exists.")
            return
        if data["Username"] in users_db:
            messagebox.showerror("Error", "Username is already taken.")
            return

        student_records.append({
            "id": data["Student ID"],
            "name": data["Full Name"],
            "age": data["Age"],
            "course": data["Course"],
            "year": data["Year Level"],
            "email": data["Email"],
        })
        users_db[data["Username"]] = {
            "password": data["Password"],
            "role": "student",
            "student_id": data["Student ID"],
        }

        messagebox.showinfo("Success", "Student registered successfully! You can now log in.")
        self.on_back()