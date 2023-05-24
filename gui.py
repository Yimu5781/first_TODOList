import json
from datetime import datetime
import tkinter as tk
from tkinter import messagebox
import task
from task import Task


class DateTimeEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime("%Y/%m/%d %H:%M")
        return super().default(obj)


class TodoListApp(tk.Tk):  # tk为Tkinter的别名，Tk为Tkinter模块中的Tk类
    def __init__(self):
        super().__init__()
        self.title("Todo List App")
        window_width = 800
        window_height = 600
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

        self.tasks = []

        self.add_button = tk.Button(self, text="Add", command=self.add_task)
        self.add_button.pack()

        self.task_table = tk.Listbox(self)
        self.task_table.config(width=60, height=20)
        self.task_table.pack()

        self.task_table.bind("<<ListboxSelect>>", self.show_task_details)

        self.delete_button = tk.Button(self, text="Delete", command=self.delete_task)
        self.delete_button.pack()

        self.load_tasks()

    def add_task(self):
        add_window = tk.Toplevel(self)
        add_window.title("Add Task")
        window_width = 300
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        add_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        description_label = tk.Label(add_window, text="Description:")
        description_label.pack()
        description_entry = tk.Entry(add_window)
        description_entry.pack()

        completion_label = tk.Label(add_window, text="Completion Time (YYYY/MM/DD HH:MM):")
        completion_label.pack()
        completion_entry = tk.Entry(add_window)
        completion_entry.pack()

        priority_label = tk.Label(add_window, text="Priority (1-5):")
        priority_label.pack()
        priority_entry = tk.Entry(add_window)
        priority_entry.pack()

        save_button = tk.Button(add_window, text="Save",
                                command=lambda: self.save_task(add_window, description_entry.get(),
                                                               completion_entry.get(), priority_entry.get()))

        save_button.pack()

    def save_task(self, add_window, description, completion_time, priority):
        task_obj = task.create_task(description, completion_time, priority)
        if task_obj is None:
            return

        self.tasks.append(task_obj)
        self.update_task_table()
        self.save_tasks()

        add_window.destroy()

    def update_task_table(self):
        self.task_table.delete(0, tk.END)  # 清空任务列表

        # 添加任务到任务列表
        for task_obj in self.tasks:
            self.task_table.insert(tk.END,
                                   f"{task_obj.description}| {task_obj.planned_completion_time} | {task_obj.priority} | ")

    def show_task_details(self, event):
        selected_row = self.task_table.curselection()
        if selected_row:
            task_index = int(selected_row[0])
            task = self.tasks[task_index]
            self.show_task_details_dialog(task)

    def show_task_details_dialog(self, task):
        details_window = tk.Toplevel()
        details_window.title("Task Details")
        window_width = 300
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        details_window.geometry(f"{window_width}x{window_height}+{x}+{y}")

        description_label = tk.Label(details_window, text="Description:")
        description_label.grid(row=0, column=0, sticky="w")
        description_value = tk.Label(details_window, text=task.description)
        description_value.grid(row=0, column=1, sticky="w")

        status_label = tk.Label(details_window, text="Status:")
        status_label.grid(row=1, column=0, sticky="w")
        status_value = tk.Label(details_window, text=task.status)
        status_value.grid(row=1, column=1, sticky="w")

        planned_completion_label = tk.Label(details_window, text="Planned Completion Time:")
        planned_completion_label.grid(row=2, column=0, sticky="w")
        planned_completion_value = tk.Label(details_window, text=task.planned_completion_time)
        planned_completion_value.grid(row=2, column=1, sticky="w")

        priority_label = tk.Label(details_window, text="Priority:")
        priority_label.grid(row=4, column=0, sticky="w")
        priority_value = tk.Label(details_window, text=task.priority)
        priority_value.grid(row=4, column=1, sticky="w")

        close_button = tk.Button(details_window, text="Close", command=details_window.destroy)
        close_button.grid(row=5, column=0, columnspan=2, pady=10)

    def delete_task(self):
        selected_index = self.task_table.curselection()
        if selected_index:
            confirm = messagebox.askyesno("Confirmation", "Are you sure you want to delete the task?")
            if confirm:
                del self.tasks[selected_index[0]]
                self.update_task_table()
                self.save_tasks()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                tasks_data = json.load(file)
                self.tasks = []
                for task_data in tasks_data:
                    task = Task()
                    task.description = task_data["description"]
                    task.status = task_data["status"]
                    if task_data["planned_completion_time"]:
                        task.planned_completion_time = datetime.strptime(task_data["planned_completion_time"],
                                                                         "%Y/%m/%d %H:%M")
                    if task_data["actual_completion_time"]:
                        task.actual_completion_time = datetime.strptime(task_data["actual_completion_time"],
                                                                        "%Y/%m/%d %H:%M")
                    task.priority = task_data["priority"]
                    self.tasks.append(task)

                self.update_task_table()  # 更新任务列表的显示(排查了两个小时，我是笨蛋)

                return self.tasks if self.tasks else None
        except FileNotFoundError:
            return None

    def save_tasks(self):
        tasks_data = []

        for task in self.tasks:
            task_data = {
                "description": task.description,
                "status": task.status,
                "planned_completion_time": task.planned_completion_time.strftime("%Y/%m/%d %H:%M") if task.planned_completion_time else None,
                "actual_completion_time": task.actual_completion_time.strftime("%Y/%m/%d %H:%M") if task.actual_completion_time else None,
                "priority": task.priority
            }
            tasks_data.append(task_data)

        with open('tasks.json', 'w') as file:
            json.dump(tasks_data, file, cls=DateTimeEncoder, indent=1)

    def on_closing(self):
        self.save_tasks()
        self.destroy()
