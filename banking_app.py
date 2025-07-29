import tkinter as tk
from tkinter import messagebox
import mysql.connector
import random
from datetime import datetime


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="DIVYA@123",
    database="bank_db"   
)
cursor = conn.cursor()

class BankingApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Divya Bank Management System")
        self.geometry("1000x500")

        self.current_frame = None

        
        self.show_frame(LoginForm)

    def show_frame(self, frame_class):
        if self.current_frame is not None:
            self.current_frame.destroy()

        self.current_frame = frame_class(parent=self, controller=self)
        self.current_frame.pack(fill="both", expand=True)

#Login Form 
class LoginForm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        tk.Label(self, text="Enter URD (User ID):").pack(pady=5)
        self.E1 = tk.Entry(self)
        self.E1.pack()

        tk.Label(self, text="Enter PWD (Password):").pack(pady=5)
        self.E2 = tk.Entry(self, show='*')
        self.E2.pack()

        tk.Button(self, text="OK", command=self.login).pack(pady=5)
        tk.Button(self, text="Cancel", command=self.cancel).pack(pady=5)
        tk.Button(self, text="Register", command=lambda: controller.show_frame(RegistrationForm)).pack(pady=5)
        tk.Button(self, text="Find", command=self.find_user).pack(pady=5)

    def login(self):
        user = self.E1.get().strip()
        pwd = self.E2.get().strip()

        if not user or not pwd:
            messagebox.showerror("Error", "Please enter User ID and Password")
            return

        cursor.execute("SELECT * FROM users WHERE login_id=%s AND login_password=%s", (user, pwd))
        if cursor.fetchone():
            messagebox.showinfo("Success", "Login successful")
            self.controller.show_frame(DivyaBankForm)
            self.E1.delete(0, tk.END)
            self.E2.delete(0, tk.END)
        else:
            messagebox.showerror("Error", "Invalid User ID or Password")

    def cancel(self):
        self.E1.delete(0, tk.END)
        self.E2.delete(0, tk.END)

    def find_user(self):
        user = self.E1.get().strip()
        pwd = self.E2.get().strip()
        if not user or not pwd:
            messagebox.showerror("Error", "Please enter User ID and Password")
            return
        cursor.execute("SELECT * FROM users WHERE login_id=%s AND login_password=%s", (user, pwd))
        if cursor.fetchone():
            messagebox.showinfo("Info", "User exists in database")
        else:
            messagebox.showerror("Error", "User does not exist")

#Registration Form
class RegistrationForm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        fields = ["Name", "Email", "Phone", "UID", "Password"]
        self.entries = {}
        for field in fields:
            tk.Label(self, text=f"Enter {field}").pack()
            entry = tk.Entry(self, show="*" if field == "Password" else None)
            entry.pack()
            self.entries[field] = entry

        tk.Button(self, text="Register", command=self.register_user).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: controller.show_frame(LoginForm)).pack(pady=5)

    def register_user(self):
        full_name = self.entries["Name"].get().strip()
        email = self.entries["Email"].get().strip()
        phone = self.entries["Phone"].get().strip()
        login_id = self.entries["UID"].get().strip()
        password = self.entries["Password"].get().strip()

        if not (full_name and email and phone and login_id and password):
            messagebox.showerror("Error", "Please fill all fields")
            return
        if not email.endswith("@gmail.com"):
            messagebox.showerror("Error", "Email must end with @gmail.com")
            return
        if not (phone.isdigit() and len(phone) == 10):
            messagebox.showerror("Error", "Phone number must be 10 digits")
            return

        try:
            cursor.execute("INSERT INTO users (full_name1, email1, phone1, login_id, login_password) VALUES (%s, %s, %s, %s, %s)",
                           (full_name, email, phone, login_id, password))
            conn.commit()
            messagebox.showinfo("Success", "Registered successfully")
            for entry in self.entries.values():
                entry.delete(0, tk.END)
        except mysql.connector.IntegrityError:
            messagebox.showerror("Error", "User ID already exists")
        except Exception as e:
            messagebox.showerror("Error", f"Database error: {e}")

#Dashboard
class DivyaBankForm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Divya Bank Dashboard", font=("Arial", 16)).pack(pady=10)

        options = [
            ("Account Open", AccountOpenForm),
            ("Account Information", AccountInfoForm),
            ("Deposit", DepositForm),
            ("Withdraw", WithdrawForm),
            ("Account Close", AccountCloseForm),
            ("Logout", LoginForm)
        ]
        for text, frame_class in options:
            if text == "Logout":
                tk.Button(self, text=text, width=20, command=lambda: controller.show_frame(LoginForm)).pack(pady=5)
            else:
                tk.Button(self, text=text, width=20, command=lambda f=frame_class: controller.show_frame(f)).pack(pady=5)

        tk.Button(self, text="Exit", width=20, command=self.controller.destroy).pack(pady=5)

#Account Open
class AccountOpenForm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        self.account_no_var = tk.StringVar()
        tk.Label(self, text="Account Number (Auto):").pack()
        tk.Entry(self, textvariable=self.account_no_var, state='readonly').pack()

        self.fields = {}
        labels = ["Holder Name", "Address 1", "Address 2", "Email", "DOB (YYYY-MM-DD)", "Deposit Amount"]
        for label in labels:
            tk.Label(self, text=label).pack()
            entry = tk.Entry(self)
            entry.pack()
            self.fields[label] = entry

        tk.Button(self, text="Account Open", command=self.open_account).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: controller.show_frame(DivyaBankForm)).pack(pady=5)

        self.generate_account_no()

    def generate_account_no(self):
        while True:
            acc_no = random.randint(100000, 999999)
            cursor.execute("SELECT account_no FROM accounts WHERE account_no=%s", (acc_no,))
            if not cursor.fetchone():
                self.account_no_var.set(str(acc_no))
                break

    def open_account(self):
        acc_no = self.account_no_var.get()
        values = [self.fields[label].get().strip() for label in self.fields]
        if "" in values:
            messagebox.showerror("Error", "Please fill all fields")
            return
        try:
            datetime.strptime(values[4], "%Y-%m-%d")
            deposit = float(values[5])
        except:
            messagebox.showerror("Error", "Invalid date or amount")
            return

        cursor.execute("INSERT INTO accounts (account_no, account_holder1, address1, address2, email1, dob1, balance1) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                       (acc_no, values[0], values[1], values[2], values[3], values[4], deposit))
        conn.commit()
        messagebox.showinfo("Success", f"Account Opened: {acc_no}")
        self.controller.show_frame(DivyaBankForm)

#Account Info
class AccountInfoForm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Enter Account Number:").pack()
        self.E1 = tk.Entry(self)
        self.E1.pack()
        tk.Button(self, text="Submit", command=self.get_info).pack(pady=5)
        self.text = tk.Text(self, height=10, width=50)
        self.text.pack()
        tk.Button(self, text="Back", command=lambda: controller.show_frame(DivyaBankForm)).pack(pady=5)

    def get_info(self):
        acc_no = self.E1.get().strip()
        cursor.execute("SELECT account_holder1, email1, dob1, balance1 FROM accounts WHERE account_no=%s", (acc_no,))
        result = cursor.fetchone()
        self.text.delete("1.0", tk.END)
        if result:
            info = f"Name: {result[0]}\nEmail: {result[1]}\nDOB: {result[2]}\nBalance: ₹{result[3]}"
            self.text.insert(tk.END, info)
        else:
            messagebox.showerror("Error", "Account not found")

#Deposit / Withdraw
class DepositForm(tk.Frame):
    def __init__(self, parent, controller, action="Deposit"):
        super().__init__(parent)
        self.controller = controller
        self.create_form(action)

    def create_form(self, action):
        self.action = action
        tk.Label(self, text=f"Enter Account Number:").pack()
        self.E1 = tk.Entry(self)
        self.E1.pack()
        tk.Button(self, text="Submit", command=self.get_details).pack()
        self.text = tk.Text(self, height=5, width=50)
        self.text.pack()
        tk.Label(self, text=f"Amount to {action}:").pack()
        self.E2 = tk.Entry(self)
        self.E2.pack()
        tk.Button(self, text=action, command=self.process).pack()
        tk.Button(self, text="Back", command=lambda: self.controller.show_frame(DivyaBankForm)).pack()

    def get_details(self):
        acc_no = self.E1.get().strip()
        cursor.execute("SELECT account_holder1, balance1 FROM accounts WHERE account_no=%s", (acc_no,))
        result = cursor.fetchone()
        self.text.delete("1.0", tk.END)
        if result:
            self.text.insert(tk.END, f"Name: {result[0]}\nCurrent Balance: ₹{result[1]}")
        else:
            messagebox.showerror("Error", "Account not found")

    def process(self):
        acc_no = self.E1.get().strip()
        try:
            amount = float(self.E2.get().strip())
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror("Error", "Invalid amount")
            return

        cursor.execute("SELECT balance1 FROM accounts WHERE account_no=%s", (acc_no,))
        result = cursor.fetchone()
        if not result:
            messagebox.showerror("Error", "Account not found")
            return

        balance = result[0]
        if self.action == "Withdraw":
            if amount > balance:
                messagebox.showerror("Error", "Insufficient balance")
                return
            balance -= amount
        else:
            balance += amount

        cursor.execute("UPDATE accounts SET balance1=%s WHERE account_no=%s", (balance, acc_no))
        conn.commit()
        messagebox.showinfo("Success", f"{self.action} successful. New balance: ₹{balance}")
        self.text.delete("1.0", tk.END)
        self.E2.delete(0, tk.END)

class WithdrawForm(DepositForm):
    def __init__(self, parent, controller):
        super().__init__(parent, controller, action="Withdraw")

#Account Close 
class AccountCloseForm(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        tk.Label(self, text="Enter Account Number to Close:").pack()
        self.E1 = tk.Entry(self)
        self.E1.pack()
        tk.Button(self, text="Close Account", command=self.close_account).pack(pady=5)
        tk.Button(self, text="Back", command=lambda: controller.show_frame(DivyaBankForm)).pack()

    def close_account(self):
        acc_no = self.E1.get().strip()
        cursor.execute("SELECT * FROM accounts WHERE account_no=%s", (acc_no,))
        if not cursor.fetchone():
            messagebox.showerror("Error", "Account not found")
            return
        confirm = messagebox.askyesno("Confirm", "Are you sure to close this account?")
        if confirm:
            cursor.execute("DELETE FROM accounts WHERE account_no=%s", (acc_no,))
            conn.commit()
            messagebox.showinfo("Success", "Account permanently closed.")
            self.E1.delete(0, tk.END)

if __name__ == "__main__":
    app = BankingApp()
    app.mainloop()
