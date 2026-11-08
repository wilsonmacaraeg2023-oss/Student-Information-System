"""Student Information System - main entry point.

Run this file:  python STUDENT_INFORMATION_GROUP_FERNANDEZ.py

Modules:
    database.py         shared users and student records
    loginform.py        login screen
    registration.py     student registration screen
    admin_dashboard.py  admin CRUD screen
    user_dashboard.py   student portal

Only one screen is shown at a time: opening one closes the previous one.
"""
import tkinter as tk

from loginform import LoginForm
from registration import RegistrationForm
from admin_dashboard import AdminDashboard
from user_dashboard import UserDashboard


class StudentInfoSystem:
    def __init__(self, root):
        self.root = root
        self.current = None
        self.show_login()

    def switch(self, frame, title, size):
        if self.current is not None:
            self.current.destroy()
        self.current = frame
        self.root.title(title)
        self.root.geometry(size)
        self.current.pack(fill="both", expand=True)

    def show_login(self):
        frame = LoginForm(self.root, on_admin=self.show_admin,
                          on_student=self.show_student,
                          on_register=self.show_registration)
        self.switch(frame, "Student Information System - Login", "800x500")

    def show_registration(self):
        frame = RegistrationForm(self.root, on_back=self.show_login)
        self.switch(frame, "Student Information System - Registration", "800x560")

    def show_admin(self, username):
        frame = AdminDashboard(self.root, on_logout=self.show_login)
        self.switch(frame, "Student Information System - Admin", "1100x600")

    def show_student(self, username):
        frame = UserDashboard(self.root, username, on_logout=self.show_login)
        self.switch(frame, "Student Information System - Student", "800x500")


if __name__ == "__main__":
    root = tk.Tk()
    app = StudentInfoSystem(root)
    root.mainloop()