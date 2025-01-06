import tkinter as tk
from tkinter import messagebox
import sqlite3

# Database setup
def setup_database():
    conn = sqlite3.connect("calculator.db")
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS calculations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        expression TEXT NOT NULL,
        result TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

# Save calculation to the database
def save_to_database(expression, result):
    conn = sqlite3.connect("calculator.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO calculations (expression, result) VALUES (?, ?)", (expression, result))
    conn.commit()
    conn.close()

# View previous calculations
def view_history():
    conn = sqlite3.connect("calculator.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM calculations ORDER BY id DESC LIMIT 10")
    rows = cur.fetchall()
    conn.close()
    
    history_window = tk.Toplevel(root)
    history_window.title("Calculation History")
    history_window.geometry("400x300")
    for row in rows:
        tk.Label(history_window, text=f"{row[1]} = {row[2]}", font="Arial 14").pack(anchor="w", padx=10, pady=5)

# Calculator functionality
def click(event):
    text = event.widget.cget("text")
    if text == "=":
        try:
            expression = screen.get()
            result = eval(expression)
            screen.set(result)
            save_to_database(expression, result)  # Save to the database
        except Exception as e:
            messagebox.showerror("Error", "Invalid Input")
            screen.set("")
    elif text == "C":
        screen.set("")
    else:
        screen.set(screen.get() + text)

# Main window
root = tk.Tk()
root.title("Calculator with History")
root.geometry("400x600")
root.resizable(False, False)

# Input screen
screen = tk.StringVar()
entry = tk.Entry(root, textvar=screen, font="Arial 24", justify="right", bd=8, relief=tk.SUNKEN)
entry.pack(fill=tk.BOTH, padx=10, pady=10, ipady=10)

# Button layout
buttons = [
    ["7", "8", "9", "/"],
    ["4", "5", "6", "*"],
    ["1", "2", "3", "-"],
    ["C", "0", "=", "+"],
]

# Create buttons
for row in buttons:
    frame = tk.Frame(root)
    frame.pack(expand=True, fill="both")
    for btn in row:
        button = tk.Button(frame, text=btn, font="Arial 20", relief=tk.RAISED, bd=2)
        button.pack(side="left", expand=True, fill="both")
        button.bind("<Button-1>", click)

# History button
history_button = tk.Button(root, text="View History", font="Arial 16", bg="lightblue", command=view_history)
history_button.pack(fill="both", padx=10, pady=10)

# Initialize database
setup_database()

# Run the application
root.mainloop()
