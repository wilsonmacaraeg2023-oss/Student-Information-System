import tkinter as tk
from tkinter import messagebox

from database import users_db, find_student


class UserDashboard(tk.Frame):
    """Student screen: shows the student's own record and lets them edit age/email."""

    def __init__(self, parent, username, on_logout):
        super().__init__(parent, bg="#f0f0f0")
        self.username = username
        self.on_logout = on_logout

        student_id = users_db.get(username, {}).get("student_id")
        self.record = find_student(student_id) if student_id else None
        self.build()

    def build(self):
        header = tk.Frame(self, bg="#2c3e50", height=60)
        header.pack(fill="x")
        tk.Label(header, text="🎓 Student Portal", bg="#2c3e50", fg="white",
                 font=("Arial", 18, "bold")).pack(side="left", padx=20, pady=15)
        tk.Button(header, text="Logout", bg="#e74c3c", fg="white", width=10,
                  command=self.on_logout).pack(side="right", padx=20)

        body = tk.Frame(self, bg="#f0f0f0", padx=30, pady=30)
        body.pack(expand=True)

        if self.record is None:
            tk.Label(body, text="No student record is linked to this account.",
                     bg="#f0f0f0", font=("Arial", 12)).pack()
            return

        tk.Label(body, text=f"Welcome, {self.record['name']}!", bg="#f0f0f0",
                 font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Read-only details
        for i, (label, key) in enumerate([("Student ID", "id"), ("Full Name", "name"),
                                          ("Course", "course"), ("Year Level", "year")], start=1):
            tk.Label(body, text=f"{label}:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(
                row=i, column=0, sticky="w", pady=6, padx=(0, 15))
            tk.Label(body, text=self.record[key], bg="#f0f0f0", font=("Arial", 10)).grid(
                row=i, column=1, sticky="w", pady=6)

        # Editable details
        tk.Label(body, text="Age:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(
            row=5, column=0, sticky="w", pady=6)
        self.age_entry = tk.Entry(body, width=30)
        self.age_entry.insert(0, self.record["age"])
        self.age_entry.grid(row=5, column=1, sticky="w")

        tk.Label(body, text="Email:", bg="#f0f0f0", font=("Arial", 10, "bold")).grid(
            row=6, column=0, sticky="w", pady=6)
        self.email_entry = tk.Entry(body, width=30)
        self.email_entry.insert(0, self.record["email"])
        self.email_entry.grid(row=6, column=1, sticky="w")

        tk.Button(body, text="💾 Save Changes", bg="#f39c12", fg="white",
                  font=("Arial", 10, "bold"), width=16,
                  command=self.save).grid(row=7, column=0, columnspan=2, pady=20)

    def save(self):
        age = self.age_entry.get().strip()
        email = self.email_entry.get().strip()
        if not age.isdigit():
            messagebox.showerror("Error", "Age must be a number.")
            return
        if "@" not in email:
            messagebox.showerror("Error", "Please enter a valid email address.")
            return
        self.record["age"] = age
        self.record["email"] = email
        messagebox.showinfo("Success", "Your information was updated.")