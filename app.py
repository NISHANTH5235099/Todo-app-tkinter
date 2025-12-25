import tkinter as tk
from tkinter import *
import json
from datetime import date

# -------------------------------------------------
# CONFIGURATION
# -------------------------------------------------
WIDTH, HEIGHT = 400, 650
DATA_FILE = "tasks.json"

# -------------------------------------------------
# WINDOW SETUP
# -------------------------------------------------
root = tk.Tk()
root.title("To-Do App")
root.geometry(f"{WIDTH}x{HEIGHT}+400+100")
root.resizable(False, False)

# -------------------------------------------------
# DATA STORAGE
# -------------------------------------------------
tasks = []
visible_tasks = []

# -------------------------------------------------
# FILE HANDLING FUNCTIONS
# -------------------------------------------------
def save_tasks():
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def load_tasks():
    try:
        with open(DATA_FILE, "r") as f:
            tasks.extend(json.load(f))
    except:
        save_tasks()
    refresh_list()

# -------------------------------------------------
# UI LOGIC FUNCTIONS
# -------------------------------------------------
def refresh_list(data=None):
    listbox.delete(0, END)
    visible_tasks.clear()

    source = data if data else tasks
    for t in source:
        status = "✔ " if t["completed"] else ""
        listbox.insert(END, f"{status}{t['task']} | {t['due']}")
        visible_tasks.append(t)

    update_counter()

def add_task():
    text = task_var.get().strip()
    due = due_var.get().strip()

    if text and due:
        tasks.append({
            "task": text,
            "due": due,
            "completed": False
        })
        task_var.set("")
        due_var.set(str(date.today()))
        save_tasks()
        refresh_list()

def delete_task():
    sel = listbox.curselection()
    if not sel:
        return
    task = visible_tasks[sel[0]]
    tasks.remove(task)
    save_tasks()
    refresh_list()

def edit_task():
    sel = listbox.curselection()
    if not sel:
        return
    task = visible_tasks[sel[0]]
    task_var.set(task["task"])
    due_var.set(task["due"])
    tasks.remove(task)
    save_tasks()
    refresh_list()

def toggle_complete(event):
    sel = listbox.curselection()
    if not sel:
        return
    task = visible_tasks[sel[0]]
    task["completed"] = not task["completed"]
    save_tasks()
    refresh_list()

def search_task(*args):
    query = search_var.get().lower()
    if query == "" or query == "search tasks...":
        refresh_list()
    else:
        filtered = [t for t in tasks if query in t["task"].lower()]
        refresh_list(filtered)

def clear_all():
    tasks.clear()
    save_tasks()
    refresh_list()

def update_counter():
    total = len(tasks)
    done = sum(t["completed"] for t in tasks)
    counter.config(text=f"Total: {total} | ✔ {done} | ⏳ {total-done}")

# -------------------------------------------------
# PLACEHOLDER FUNCTION
# -------------------------------------------------
def add_placeholder(entry, text):
    entry.insert(0, text)
    entry.config(fg="grey")

    def on_focus_in(event):
        if entry.get() == text:
            entry.delete(0, END)
            entry.config(fg="black")

    def on_focus_out(event):
        if entry.get() == "":
            entry.insert(0, text)
            entry.config(fg="grey")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)

# -------------------------------------------------
# ICONS / HEADER
# -------------------------------------------------
app_icon = PhotoImage(file="images/to2.png")
root.iconphoto(False, app_icon)

top_img = PhotoImage(file="images/topbar.png")
Label(root, image=top_img).pack()

dock_img = PhotoImage(file="images/dock.png")
Label(root, image=dock_img, bg="#32405b").place(x=30, y=25)

task_img = PhotoImage(file="images/task.png")
Label(root, image=task_img, bg="#32405b").place(x=80, y=25)

Label(root, text="ALL TASKS",
      font=("Segoe UI", 18, "bold"),
      fg="white", bg="#32405b").place(x=140, y=20)

# -------------------------------------------------
# SEARCH BAR (ROUNDED + ICON + PLACEHOLDER)
# -------------------------------------------------
search_var = StringVar()
search_var.trace_add("write", search_task)

search_icon = PhotoImage(file="images/search.png").subsample(3, 3)


canvas = Canvas(root, width=360, height=35, bg="#f0f0f0", highlightthickness=0)
canvas.place(x=20, y=115)

canvas.create_oval(0, 0, 35, 35, fill="white", outline="white")
canvas.create_oval(325, 0, 360, 35, fill="white", outline="white")
canvas.create_rectangle(18, 0, 342, 35, fill="white", outline="white")

Label(root, image=search_icon, bg="white").place(x=30, y=122)

search_entry = Entry(root, textvariable=search_var,
                     font=("Segoe UI", 12), bd=0)
search_entry.place(x=60, y=122, width=300)

add_placeholder(search_entry, "Search tasks...")

# -------------------------------------------------
# INPUT AREA
# -------------------------------------------------
task_var = StringVar()
due_var = StringVar(value=str(date.today()))

Entry(root, textvariable=task_var,
      font=("Segoe UI", 13), bd=0).place(x=20, y=160, width=240)

Entry(root, textvariable=due_var,
      font=("Segoe UI", 11), bd=0).place(x=270, y=160, width=110)

Button(root, text="ADD", bg="#5a95ff", fg="white",
       font=("Segoe UI", 11, "bold"),
       bd=0, command=add_task).place(x=150, y=200, width=100)

# -------------------------------------------------
# TASK LIST
# -------------------------------------------------
frame = Frame(root, bg="#32405b")
frame.place(x=10, y=250, width=380, height=280)

scroll = Scrollbar(frame)
scroll.pack(side=RIGHT, fill=Y)

listbox = Listbox(frame, bg="#32405b", fg="white",
                  font=("Segoe UI", 12),
                  selectbackground="#5a95ff",
                  activestyle="none",
                  yscrollcommand=scroll.set)
listbox.pack(fill=BOTH, expand=True)

scroll.config(command=listbox.yview)
listbox.bind("<Double-Button-1>", toggle_complete)

# -------------------------------------------------
# COUNTER
# -------------------------------------------------
counter = Label(root, font=("Segoe UI", 11))
counter.place(x=20, y=545)

# -------------------------------------------------
# BUTTONS
# -------------------------------------------------
Button(root, text="✏ Edit", bg="#ffa500", fg="white",
       font=("Segoe UI", 11, "bold"),
       bd=0, command=edit_task).place(x=40, y=580, width=80)

Button(root, text="🧹 Clear", bg="#999999", fg="white",
       font=("Segoe UI", 11, "bold"),
       bd=0, command=clear_all).place(x=150, y=580, width=80)

del_img = PhotoImage(file="images/delete.png")
Button(root, image=del_img, bd=0,
       command=delete_task).place(x=270, y=575)

# -------------------------------------------------
# START APP
# -------------------------------------------------
load_tasks()
root.mainloop()
