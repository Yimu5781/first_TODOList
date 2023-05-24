# TODOlist
from gui import TodoListApp

app = TodoListApp()
app.protocol("WM_DELETE_WINDOW", app.on_closing)
app.tasks = app.load_tasks() or []
app.mainloop()
