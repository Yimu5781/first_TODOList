import datetime
from tkinter import messagebox


def format_time(time):
    return time.strftime("%Y/%m/%d %H:%M")


def validate_datetime(datetime_str):
    try:
        datetime.datetime.strptime(datetime_str, "%Y/%m/%d %H:%M")
        return True
    except ValueError:
        return False


def validate_priority(priority):
    return priority in range(1, 6)


class Task:
    def __init__(self):
        self.description = " "
        self.status = "Pending"
        self.planned_completion_time = None
        self.actual_completion_time = None
        self.priority = 3

    def mark_as_completed(self):
        self.status = "Completed"
        self.actual_completion_time = datetime.datetime.now()

    def __str__(self):
        return f"Task: {self.description}\n" \
               f"Status: {self.status}\n" \
               f"Planned Completion Time: {format_time:(self.planned_completion_time)}\n" \
               f"Actual Completion Time: {format_time:(self.actual_completion_time)}\n" \
               f"Priority: {self.priority}"


def create_task(description, completion_time, priority):
    task = Task()
    task.description = description

    if not validate_datetime(completion_time):
            messagebox.showerror("Invalid Input", "Invalid datetime format. Please enter in YYYY/MM/DD HH:MM format.")
            return None

    planned_completion_datetime = datetime.datetime.strptime(completion_time, "%Y/%m/%d %H:%M")

    if planned_completion_datetime < datetime.datetime.now():
        confirm =messagebox.askyesno("Confirmation", "The specified time is in the past. Do you want to continue?")
        if not confirm:
            messagebox.showerror("Invalid Input", "Please re-enter the completion time.")
            return None

    task.planned_completion_time = planned_completion_datetime

    if not priority.isdigit() or not validate_priority(int(priority)):
        messagebox.showerror("Invalid Input", "Priority must be an integer between 1 and 5.")
        return None

    task.priority = int(priority)
    return task
