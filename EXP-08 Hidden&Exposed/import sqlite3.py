import sqlite3
import tkinter as tk
from tkinter import messagebox

def connect_db():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY,
            title TEXT,
            author TEXT,
            year INTEGER,
            isbn TEXT
        )
    """)
    conn.commit()
    
    # Insert initial book data if the table is empty
    cur.execute("SELECT COUNT(*) FROM books")
    if cur.fetchone()[0] == 0:
        books = [
            ("The Great Gatsby", "F. Scott Fitzgerald", 1925, "9780743273565"),
            ("To Kill a Mockingbird", "Harper Lee", 1960, "9780061120084"),
            ("1984", "George Orwell", 1949, "9780451524935"),
            ("The Catcher in the Rye", "J.D. Salinger", 1951, "9780316769488"),
            ("Pride and Prejudice", "Jane Austen", 1813, "9780141439518")
        ]
        cur.executemany("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)", books)
        conn.commit()
    
    conn.close()

def insert_book(title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO books (title, author, year, isbn) VALUES (?, ?, ?, ?)", (title, author, year, isbn))
    conn.commit()
    conn.close()

def view_books():
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_books(title="", author="", year="", isbn=""):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM books WHERE title=? OR author=? OR year=? OR isbn=?", (title, author, year, isbn))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_book(book_id):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM books WHERE id=?", (book_id,))
    conn.commit()
    conn.close()

def update_book(book_id, title, author, year, isbn):
    conn = sqlite3.connect("books.db")
    cur = conn.cursor()
    cur.execute("UPDATE books SET title=?, author=?, year=?, isbn=? WHERE id=?", (title, author, year, isbn, book_id))
    conn.commit()
    conn.close()

def on_view():
    listbox.delete(0, tk.END)
    for book in view_books():
        listbox.insert(tk.END, book)

def on_search():
    listbox.delete(0, tk.END)
    for book in search_books(title_var.get(), author_var.get(), year_var.get(), isbn_var.get()):
        listbox.insert(tk.END, book)

def on_add():
    insert_book(title_var.get(), author_var.get(), year_var.get(), isbn_var.get())
    on_view()

def on_delete():
    selected = listbox.curselection()
    if selected:
        book_id = listbox.get(selected[0])[0]
        delete_book(book_id)
        on_view()

def on_update():
    selected = listbox.curselection()
    if selected:
        book_id = listbox.get(selected[0])[0]
        update_book(book_id, title_var.get(), author_var.get(), year_var.get(), isbn_var.get())
        on_view()

connect_db()

# GUI Setup
root = tk.Tk()
root.title("Bookstore Management System")

title_var = tk.StringVar()
author_var = tk.StringVar()
year_var = tk.StringVar()
isbn_var = tk.StringVar()

tk.Label(root, text="Title").grid(row=0, column=0)
tk.Entry(root, textvariable=title_var).grid(row=0, column=1)

tk.Label(root, text="Author").grid(row=0, column=2)
tk.Entry(root, textvariable=author_var).grid(row=0, column=3)

tk.Label(root, text="Year").grid(row=1, column=0)
tk.Entry(root, textvariable=year_var).grid(row=1, column=1)

tk.Label(root, text="ISBN").grid(row=1, column=2)
tk.Entry(root, textvariable=isbn_var).grid(row=1, column=3)

listbox = tk.Listbox(root, height=10, width=50)
listbox.grid(row=2, column=0, columnspan=4)

btn_view = tk.Button(root, text="View All", command=on_view)
btn_view.grid(row=3, column=0)

btn_search = tk.Button(root, text="Search", command=on_search)
btn_search.grid(row=3, column=1)

btn_add = tk.Button(root, text="Add", command=on_add)
btn_add.grid(row=3, column=2)

btn_update = tk.Button(root, text="Update", command=on_update)
btn_update.grid(row=3, column=3)

btn_delete = tk.Button(root, text="Delete", command=on_delete)
btn_delete.grid(row=4, column=1, columnspan=2)

root.mainloop()
