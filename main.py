import tkinter as tk
from tkinter import messagebox, simpledialog ,ttk
import pickle
from datetime import datetime


class RegistrationWindow:
    def __init__(self, root, login_window):
        self.root = root
        self.login_window = login_window
        self.root.title("Register")

        self.new_username_var = tk.StringVar()
        self.new_password_var = tk.StringVar()

        tk.Label(root, text="New Username:").pack(pady=5)
        tk.Entry(root, textvariable=self.new_username_var).pack(pady=5)
        tk.Label(root, text="New Password:").pack(pady=5)
        tk.Entry(root, textvariable=self.new_password_var, show="*").pack(pady=5)
        tk.Button(root, text="Register", command=self.register, bg="skyblue").pack(pady=10)

    def register(self):
        new_username = self.new_username_var.get()
        new_password = self.new_password_var.get()

        # Check if username already exists
        if new_username in self.login_window.users:
            self.show_error("Username already exists! Please choose a different username.")
        else:
            # Add new user to the user system
            self.login_window.users[new_username] = new_password
            self.show_info("Registration successful! You can now log in.")
            self.root.destroy()  # Close the registration window


class LoginWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("Login")

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        tk.Label(root, text="Username:").pack(pady=5)
        tk.Entry(root, textvariable=self.username_var).pack(pady=5)
        tk.Label(root, text="Password:").pack(pady=5)
        tk.Entry(root, textvariable=self.password_var, show="*").pack(pady=5)
        tk.Button(root, text="Login", command=self.login, bg="red", foreground="black").pack(pady=10)

        # Button to open the registration window
        tk.Button(root, text="Register", command=self.open_registration, bg="skyblue").pack(pady=5)

    def login(self):
        username = self.username_var.get()
        password = self.password_var.get()

        users = {'nishant': 'password'}  # Simple user system for demo

        if username in users and users[username] == password:
            self.root.destroy()
            app = TodoApp(username)
            app.run()
        else:
            self.show_error("Invalid credentials! Please try again.")

    def open_registration(self):
        registration_root = tk.Tk()
        registration_window = RegistrationWindow(registration_root, self)
        registration_root.mainloop()

    def show_error(self, message):
        style = ttk.Style()
        style.configure("TButton", foreground="red", background="#F88")
        messagebox.showerror("Error", message)


class TodoApp:
    def __init__(self, master):
        self.master = master
        self.master.title("To-Do List App")

        # Initialize tasks
        self.tasks = []
        self.load_tasks()

        # Create GUI elements
        self.task_label = tk.Label(master, text="Task:")
        self.task_entry = tk.Entry(master, width=30)

        self.label_label = tk.Label(master, text="Label:")
        self.label_entry = tk.Entry(master, width=30)

        self.due_date_label = tk.Label(master, text="Due Date (YYYY-MM-DD):")
        self.due_date_entry = tk.Entry(master, width=15)

        self.target_date_label = tk.Label(master, text="Target Date (YYYY-MM-DD):")
        self.target_date_entry = tk.Entry(master, width=15)

        self.add_button = tk.Button(master, text="Add Task", command=self.add_task)
        self.listbox = tk.Listbox(master, selectmode=tk.SINGLE, width=100, height=10)
        self.edit_button = tk.Button(master, text="Edit Task", command=self.edit_task)
        self.complete_button = tk.Button(master, text="Complete Task", command=self.complete_task)
        self.delete_button = tk.Button(master, text="Delete Task", command=self.delete_task)
        self.save_button = tk.Button(master, text="Save Tasks", command=self.save_tasks)
        self.logout_button = tk.Button(master, text="Logout", command=self.logout)


        # Place GUI elements
        self.task_label.grid(row=0, column=0, padx=10, pady=5, sticky=tk.E)
        self.task_entry.grid(row=0, column=1, padx=10, pady=5, sticky=tk.W)
        self.label_label.grid(row=1, column=0, padx=10, pady=5, sticky=tk.E)
        self.label_entry.grid(row=1, column=1, padx=10, pady=5, sticky=tk.W)
        self.due_date_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)
        self.due_date_entry.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)
        self.target_date_label.grid(row=3, column=0, padx=10, pady=5, sticky=tk.E)
        self.target_date_entry.grid(row=3, column=1, padx=10, pady=5, sticky=tk.W)
        self.add_button.grid(row=4, column=0, columnspan=2, pady=10)
        self.listbox.grid(row=5, column=0, columnspan=2, padx=10, pady=5)
        self.edit_button.grid(row=6, column=0, pady=10)
        self.complete_button.grid(row=6, column=1, pady=10)
        self.delete_button.grid(row=7, column=0, columnspan=2, pady=10)
        self.save_button.grid(row=8, column=0, columnspan=2, pady=10)
        self.logout_button.grid(row=9, column=0, columnspan=2, pady=10)


        # Load tasks into listbox
        self.refresh_listbox()

    def add_task(self):
        task_description = self.task_entry.get()
        task_label = self.label_entry.get()
        due_date = self.due_date_entry.get()
        target_date = self.target_date_entry.get()

        if task_description:
            try:
                datetime.strptime(due_date, "%Y-%m-%d")
                datetime.strptime(target_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date format. Use YYYY-MM-DD.")
                return

            self.tasks.append({
                "description": task_description,
                "label": task_label,
                "due_date": due_date,
                "target_date": target_date,
                "completed": False
            })
            self.save_tasks()
            self.refresh_listbox()
            self.task_entry.delete(0, tk.END)
            self.label_entry.delete(0, tk.END)
            self.due_date_entry.delete(0, tk.END)
            self.target_date_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Warning", "Task description cannot be empty!")

    def edit_task(self):
        selected_index = self.listbox.curselection()

        if selected_index:
            selected_task = self.tasks[selected_index[0]]
            new_description = simpledialog.askstring("Edit Task", "New Task Description:", initialvalue=selected_task["description"])
            new_label = simpledialog.askstring("Edit Task", "New Task Label:", initialvalue=selected_task["label"])
            new_due_date = simpledialog.askstring("Edit Task", "New Due Date (YYYY-MM-DD):", initialvalue=selected_task["due_date"])
            new_target_date = simpledialog.askstring("Edit Task", "New Target Date (YYYY-MM-DD):", initialvalue=selected_task["target_date"])

            try:
                datetime.strptime(new_due_date, "%Y-%m-%d")
                datetime.strptime(new_target_date, "%Y-%m-%d")
            except ValueError:
                messagebox.showwarning("Warning", "Invalid date format. Use YYYY-MM-DD.")
                return

            if new_description is not None and new_label is not None and new_due_date is not None and new_target_date is not None:
                self.tasks[selected_index[0]]["description"] = new_description
                self.tasks[selected_index[0]]["label"] = new_label
                self.tasks[selected_index[0]]["due_date"] = new_due_date
                self.tasks[selected_index[0]]["target_date"] = new_target_date
                self.save_tasks()
                self.refresh_listbox()

    def complete_task(self):
        selected_index = self.listbox.curselection()

        if selected_index:
            self.tasks[selected_index[0]]["completed"] = True
            self.save_tasks()
            self.refresh_listbox()

    def delete_task(self):
        selected_index = self.listbox.curselection()

        if selected_index:
            self.tasks.pop(selected_index[0])
            self.save_tasks()
            self.refresh_listbox()

    def refresh_listbox(self):
        self.listbox.delete(0, tk.END)
        for i, task in enumerate(self.tasks, start=1):
            description = task["description"]
            label = task["label"]
            due_date = task["due_date"]
            target_date = task["target_date"]
            completed = task["completed"]

            if completed:
                self.listbox.insert(tk.END,
                                    f"{i}. [Done] {description} ({label}) - Due: {due_date} - Target: {target_date}")
                self.listbox.itemconfig(i - 1, {'fg': 'gray'})
            else:
                self.listbox.insert(tk.END, f"{i}. {description} ({label}) - Due: {due_date} - Target: {target_date}")

    def load_tasks(self):
        try:
            with open('tasks.pkl', 'rb') as file:
                self.tasks = pickle.load(file)
        except FileNotFoundError:
            self.tasks = []

    def save_tasks(self):
        with open('tasks.pkl', 'wb') as file:
            pickle.dump(self.tasks, file)

    def logout(self):
        self.master.destroy()

if __name__ == "__main__":
    login_root = tk.Tk()
    login_app = LoginWindow(login_root)
    login_root.mainloop()
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


