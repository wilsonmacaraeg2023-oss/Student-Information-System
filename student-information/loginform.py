import tkinter as tk
from tkinter import messagebox
from database import users_db


class LoginForm(tk.Frame):
    """Login screen. Calls on_admin(username) / on_student(username) on success."""

    def __init__(self, parent, on_admin, on_student, on_register):
        super().__init__(parent, bg="#f0f0f0")
        self.on_admin = on_admin
        self.on_student = on_student
        self.on_register = on_register
        self.build()

    def build(self):
        header = tk.Frame(self, bg="#2c3e50", height=50)
        header.pack(fill="x")
        tk.Label(header, text="🎓 Student Information System", bg="#2c3e50",
                 fg="white", font=("Arial", 20, "bold")).pack(pady=10)

        frame = tk.Frame(self, bg="#f0f0f0", padx=20, pady=20)
        frame.pack(expand=True)

        tk.Label(frame, text="Username:", bg="#f0f0f0", font=("Arial", 10)).grid(row=0, column=0, sticky="w", pady=5)
        self.username_entry = tk.Entry(frame, width=25)
        self.username_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password:", bg="#f0f0f0", font=("Arial", 10)).grid(row=1, column=0, sticky="w", pady=5)
        self.password_entry = tk.Entry(frame, width=25, show="*")
        self.password_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="Login As:", bg="#f0f0f0", font=("Arial", 10)).grid(row=2, column=0, sticky="w", pady=5)
        self.role_var = tk.StringVar(value="admin")
        tk.Radiobutton(frame, text="Admin", variable=self.role_var, value="admin", bg="#f0f0f0").grid(row=2, column=1, sticky="w")
        tk.Radiobutton(frame, text="Student", variable=self.role_var, value="student", bg="#f0f0f0").grid(row=2, column=1, sticky="e")

        btn_frame = tk.Frame(frame, bg="#f0f0f0")
        btn_frame.grid(row=3, column=0, columnspan=2, pady=20)

        tk.Button(btn_frame, text="Login", bg="#3498db", fg="white", width=10,
                  command=self.login).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Register", bg="#2ecc71", fg="white", width=10,
                  command=self.on_register).pack(side="left", padx=5)

        self.username_entry.focus_set()
        self.password_entry.bind("<Return>", lambda e: self.login())

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        role = self.role_var.get()

        user = users_db.get(username)
        if not user or user["password"] != password:
            messagebox.showerror("Error", "Invalid username or password.")
            return
        if user["role"] != role:
            messagebox.showerror("Error", "Incorrect role selected for this user.")
            return

        if role == "admin":
            self.on_admin(username)
        else:
            self.on_student(username)