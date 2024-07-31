import json
import os
import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

# File to store tasks
TASKS_FILE = "tasks.json"

class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("To-Do List Application")
        self.tasks = self.load_tasks()
        
        # Create the GUI
        self.create_widgets()

    def create_widgets(self):
        # Frame for tasks list
        self.frame_tasks = tk.Frame(self.root)
        self.frame_tasks.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

        # Listbox to show tasks
        self.listbox_tasks = tk.Listbox(self.frame_tasks, selectmode=tk.SINGLE, activestyle="none")
        self.listbox_tasks.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox_tasks.bind('<Double-1>', self.edit_task)
        
        # Scrollbar for the Listbox
        self.scrollbar = tk.Scrollbar(self.frame_tasks)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox_tasks.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.config(command=self.listbox_tasks.yview)

        # Frame for buttons
        self.frame_buttons = tk.Frame(self.root)
        self.frame_buttons.pack(padx=10, pady=10, fill=tk.X)

        # Add task button
        self.button_add = tk.Button(self.frame_buttons, text="Add Task", command=self.add_task)
        self.button_add.pack(side=tk.LEFT, padx=5)

        # Edit task button
        self.button_edit = tk.Button(self.frame_buttons, text="Edit Task", command=self.edit_task)
        self.button_edit.pack(side=tk.LEFT, padx=5)

        # Delete task button
        self.button_delete = tk.Button(self.frame_buttons, text="Delete Task", command=self.delete_task)
        self.button_delete.pack(side=tk.LEFT, padx=5)

        # Mark as completed button
        self.button_complete = tk.Button(self.frame_buttons, text="Mark as Completed", command=self.mark_completed)
        self.button_complete.pack(side=tk.LEFT, padx=5)

        # Filter options
        self.filter_var = tk.StringVar(value="All")
        self.filter_options = ["All", "Completed", "Incomplete"]
        self.filter_menu = ttk.Combobox(self.frame_buttons, textvariable=self.filter_var, values=self.filter_options, state="readonly")
        self.filter_menu.pack(side=tk.LEFT, padx=5)
        self.filter_menu.bind("<<ComboboxSelected>>", self.filter_tasks)

        # Load tasks into the Listbox
        self.refresh_task_list()

    def add_task(self):
        task = simpledialog.askstring("Add Task", "Enter task description:")
        if task:
            self.tasks.append({"description": task, "completed": False})
            self.save_tasks()
            self.refresh_task_list()

    def edit_task(self, event=None):
        selected_index = self.listbox_tasks.curselection()
        if selected_index:
            index = selected_index[0]
            old_task = self.tasks[index]["description"]
            new_task = simpledialog.askstring("Edit Task", "Edit task description:", initialvalue=old_task)
            if new_task:
                self.tasks[index]["description"] = new_task
                self.save_tasks()
                self.refresh_task_list()

    def delete_task(self):
        selected_index = self.listbox_tasks.curselection()
        if selected_index:
            index = selected_index[0]
            if messagebox.askyesno("Delete Task", "Are you sure you want to delete this task?"):
                del self.tasks[index]
                self.save_tasks()
                self.refresh_task_list()

    def mark_completed(self):
        selected_index = self.listbox_tasks.curselection()
        if selected_index:
            index = selected_index[0]
            self.tasks[index]["completed"] = not self.tasks[index]["completed"]
            self.save_tasks()
            self.refresh_task_list()

    def filter_tasks(self, event=None):
        filter_status = self.filter_var.get()
        self.refresh_task_list(filter_status)

    def refresh_task_list(self, filter_status="All"):
        self.listbox_tasks.delete(0, tk.END)
        for task in self.tasks:
            if filter_status == "All" or (filter_status == "Completed" and task["completed"]) or (filter_status == "Incomplete" and not task["completed"]):
                display_text = f"{task['description']} {'(Completed)' if task['completed'] else '(Incomplete)'}"
                self.listbox_tasks.insert(tk.END, display_text)

    def save_tasks(self):
        with open(TASKS_FILE, 'w') as file:
            json.dump(self.tasks, file)

    def load_tasks(self):
        if os.path.exists(TASKS_FILE):
            with open(TASKS_FILE, 'r') as file:
                return json.load(file)
        return []

if __name__ == "__main__":
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()
