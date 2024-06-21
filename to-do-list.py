import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3 as sql

def add_task():
    task_string = task_field.get()
    if len(task_string) == 0:
        messagebox.showinfo('Error', 'Field is Empty.')
    else:
        tasks.append(task_string)
        try:
            the_cursor.execute('insert into tasks (title) values (?)', (task_string,))
            the_connection.commit()
            list_update()
            task_field.delete(0, 'end')
        except sql.Error as e:
            messagebox.showerror('Database Error', f'Error inserting task: {e}')

def list_update():
    clear_list()
    for task in tasks:
        task_listbox.insert('end', task)

def delete_task():
    try:
        the_value = task_listbox.get(task_listbox.curselection())
        if the_value in tasks:
            tasks.remove(the_value)
            list_update()
            try:
                the_cursor.execute('delete from tasks where title = ?', (the_value,))
                the_connection.commit()
            except sql.Error as e:
                messagebox.showerror('Database Error', f'Error deleting task: {e}')
    except tk.TclError:
        messagebox.showinfo('Error', 'No Task Selected. Cannot Delete.')

def delete_all_tasks():
    message_box = messagebox.askyesno('Delete All', 'Are you sure?')
    if message_box:
        tasks.clear()
        try:
            the_cursor.execute('delete from tasks')
            the_connection.commit()
            list_update()
        except sql.Error as e:
            messagebox.showerror('Database Error', f'Error deleting all tasks: {e}')

def clear_list():
    task_listbox.delete(0, 'end')

def close():
    print(tasks)
    guiWindow.destroy()

def retrieve_database():
    tasks.clear()
    try:
        for row in the_cursor.execute('select title from tasks'):
            tasks.append(row[0])
    except sql.Error as e:
        messagebox.showerror('Database Error', f'Error retrieving tasks: {e}')

if __name__ == "__main__":
    guiWindow = tk.Tk()
    guiWindow.title("To-Do List Manager")
    guiWindow.geometry("500x450+750+250")
    guiWindow.resizable(0, 0)
    guiWindow.configure(bg="#2E2E2E")

    try:
        the_connection = sql.connect('listOfTasks.db')
        the_cursor = the_connection.cursor()
        the_cursor.execute('create table if not exists tasks (title text)')
    except sql.Error as e:
        messagebox.showerror('Database Error', f'Error connecting to database: {e}')
        guiWindow.destroy()

    tasks = []

    header_frame = tk.Frame(guiWindow, bg="#FFD700")
    functions_frame = tk.Frame(guiWindow, bg="#2E2E2E")
    listbox_frame = tk.Frame(guiWindow, bg="#2E2E2E")

    header_frame.pack(fill="both")
    functions_frame.pack(side="left", expand=True, fill="both")
    listbox_frame.pack(side="right", expand=True, fill="both")

    header_label = ttk.Label(
        header_frame,
        text="To-Do List",
        font=("Helvetica", 30, "bold"),
        background="#FFD700",
        foreground="#2E2E2E"
    )
    header_label.pack(padx=10, pady=10)

    task_label = ttk.Label(
        functions_frame,
        text="Enter the Task:",
        font=("Helvetica", 11, "bold"),
        background="#2E2E2E",
        foreground="#FFFFFF"
    )
    task_label.place(x=30, y=40)

    task_field = ttk.Entry(
        functions_frame,
        font=("Consolas", 12),
        width=18
    )
    task_field.place(x=30, y=80)

    add_button = ttk.Button(
        functions_frame,
        text="Add Task",
        width=24,
        command=add_task
    )
    del_button = ttk.Button(
        functions_frame,
        text="Delete Task",
        width=24,
        command=delete_task
    )
    del_all_button = ttk.Button(
        functions_frame,
        text="Delete All Tasks",
        width=24,
        command=delete_all_tasks
    )
    exit_button = ttk.Button(
        functions_frame,
        text="Exit",
        width=24,
        command=close
    )
    add_button.place(x=30, y=120)
    del_button.place(x=30, y=160)
    del_all_button.place(x=30, y=200)
    exit_button.place(x=30, y=240)

    task_listbox = tk.Listbox(
        listbox_frame,
        width=26,
        height=13,
        selectmode='SINGLE',
        background="#FFFFFF",
        foreground="#000000",
        selectbackground="#CD853F",
        selectforeground="#FFFFFF",
        font=("Consolas", 12)
    )
    task_listbox.place(x=10, y=20)

    retrieve_database()
    list_update()
    guiWindow.mainloop()

    the_connection.commit()
    the_cursor.close()
    the_connection.close()
