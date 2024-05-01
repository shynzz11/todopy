from tkinter import Tk, Label, Entry, Button, Text, messagebox
import requests

def login():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password.")
        return
    response = requests.post('http://localhost:5000/login', json={'username': username, 'password': password})
    if response.status_code == 200:
        messagebox.showinfo("Success", "Login successful.")
        get_todos()
    else:
        messagebox.showerror("Error", "Login failed. Please check your username and password.")

def signup():
    username = username_entry.get()
    password = password_entry.get()
    if not username or not password:
        messagebox.showerror("Error", "Please enter username and password.")
        return
    response = requests.post('http://localhost:5000/signup', json={'username': username, 'password': password})
    if response.status_code == 200:
        messagebox.showinfo("Success", "Signup successful. Please login.")
    else:
        messagebox.showerror("Error", "Signup failed. Please try again.")

def get_todos():
    username = username_entry.get()
    if not username:
        # Handle empty username (optional: show error message)
        return
    #headers = {'Authorization': f'Bearer {auth_token}'}
    response = requests.get(f'http://localhost:5000/users/{username}/todos')
    if response.status_code == 200:
        data = response.json()
        todos_text.delete(1.0, 'end')  # Clear existing todo list
        for todo in data:
            todos_text.insert('end', f"- {todo}\n")  # Add each todo with a new line
    else:
        messagebox.showerror("Error", "Failed to fetch todos.")

def add_todo():
    username = username_entry.get()
    if not username:
        # Handle empty username (optional: show error message)
        return
    todo_text = todo_entry.get()
    if not todo_text:
        messagebox.showerror("Error", "Please enter a todo.")
        return
    #headers = {'Authorization': f'Bearer {auth_token}'}
    data = {'todo': todo_text}
    response = requests.post(f'http://localhost:5000/users/{username}/todos', json=data)
    if response.status_code == 200:
        messagebox.showinfo("Success", "Todo added successfully.")
        get_todos()  # Call get_todos to refresh the list after adding
    else:
        messagebox.showerror("Error", "Failed to add todo.")

root = Tk()
root.title('Todo App')

# Username Label and Entry
username_label = Label(root, text='Username:')
username_label.pack()

username_entry = Entry(root)
username_entry.pack()

# Password Label and Entry
password_label = Label(root, text='Password:')
password_label.pack()

password_entry = Entry(root, show='*')  # Show * for password
password_entry.pack()

# Login Button
login_button = Button(root, text='Login', command=login)
login_button.pack()

# Signup Button
signup_button = Button(root, text='Signup', command=signup)
signup_button.pack()

# Todo Label and Entry
todo_label = Label(root, text='New Todo:')
todo_label.pack()

todo_entry = Entry(root)
todo_entry.pack()

# Text widget to display todos
todos_text = Text(root, height=10)
todos_text.pack()

# Buttons
get_todos_button = Button(root, text='Get Todos', command=get_todos)
get_todos_button.pack()

add_todo_button = Button(root, text='Add Todo', command=add_todo)
add_todo_button.pack()

root.mainloop()
