import sqlite3
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import csv

FILENAME = r"C:\Users\levig\OneDrive\Documents\Coding\book_database.db"

# ========== Database Functions ==========
def init_db():
    with sqlite3.connect(FILENAME) as conn:
        c = conn.cursor()
        c.execute('''
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY, 
                title TEXT, 
                author TEXT, 
                location TEXT, 
                readBefore BOOLEAN, 
                rating INTEGER
            )
        ''')

def log_book(title, author, location, read_before=False, rating=None):
    with sqlite3.connect(FILENAME) as conn:
        c = conn.cursor()
        c.execute('''
            INSERT INTO books (title, author, location, readBefore, rating)
            VALUES (?, ?, ?, ?, ?)
        ''', (title, author, location, read_before, rating))

def get_all_books():
    with sqlite3.connect(FILENAME) as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM books')
        return c.fetchall()

def get_books_by_keyword(keyword, read_filter=None):
    with sqlite3.connect(FILENAME) as conn:
        c = conn.cursor()
        query = 'SELECT * FROM books WHERE title LIKE ? OR author LIKE ? OR location LIKE ?'
        if read_filter == "Yes":
            query += ' AND readBefore=1'
        elif read_filter == "No":
            query += ' AND readBefore=0'
        c.execute(query, (f'%{keyword}%', f'%{keyword}%', f'%{keyword}%'))
        return c.fetchall()

def update_book(book_id, title, author, location, read_before, rating):
    with sqlite3.connect(FILENAME) as conn:
        c = conn.cursor()
        c.execute('''
            UPDATE books SET title=?, author=?, location=?, readBefore=?, rating=? 
            WHERE id=?
        ''', (title, author, location, read_before, rating, book_id))

def remove_book(book_id):
    with sqlite3.connect(FILENAME) as conn:
        c = conn.cursor()
        c.execute('DELETE FROM books WHERE id=?', (book_id,))

# ========== GUI Application ==========
class BookCatalogApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Book Catalog")
        self.geometry("950x600")
        self.resizable(True, True)
        self.start_menu()

    def clear_frame(self):
        for widget in self.winfo_children():
            widget.destroy()

    # ===== Auto-resize columns =====
    def auto_resize_columns(self, tree):
        def resize(event):
            total_width = event.width
            col_width = max(int(total_width / len(tree["columns"])) - 1, 50)
            for col in tree["columns"]:
                tree.column(col, width=col_width)
        tree.bind("<Configure>", resize)

    # ========== Start Menu ==========
    def start_menu(self):
        self.clear_frame()
        tk.Label(self, text="Book Catalog", font=("Arial", 28, "bold")).pack(pady=20)
        tk.Button(self, text="Find Books", width=20, command=self.find_books_menu).pack(pady=10)
        tk.Button(self, text="Add Book", width=20, command=self.add_book_menu).pack(pady=10)
        tk.Button(self, text="Exit", width=20, command=self.destroy).pack(pady=10)

    # ========== Add Book ==========
    def add_book_menu(self):
        self.clear_frame()
        tk.Label(self, text="Add Book", font=("Arial", 20)).pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Title").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        title_entry = tk.Entry(frame, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame, text="Author").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        author_entry = tk.Entry(frame, width=40)
        author_entry.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(frame, text="Location").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        location_entry = tk.Entry(frame, width=40)
        location_entry.grid(row=2, column=1, padx=5, pady=5)

        read_var = tk.BooleanVar()
        tk.Checkbutton(frame, text="Read Before", variable=read_var).grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Rating (1-10)").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        rating_entry = tk.Entry(frame, width=10)
        rating_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)

        def add_book_action():
            title = title_entry.get()
            author = author_entry.get()
            location = location_entry.get()
            read_before = read_var.get()
            try:
                rating = int(rating_entry.get())
                if rating < 1 or rating > 10:
                    rating = None
            except ValueError:
                rating = None
            if not title or not author or not location:
                messagebox.showerror("Error", "Title, Author, and Location are required!")
                return
            log_book(title, author, location, read_before, rating)
            messagebox.showinfo("Success", "Book added!")
            self.start_menu()

        tk.Button(self, text="Add Book", command=add_book_action, width=15).pack(pady=10)
        tk.Button(self, text="Back", command=self.start_menu, width=15).pack()

    # ========== Find Books ==========
    def find_books_menu(self):
        self.clear_frame()
        tk.Label(self, text="Find Books", font=("Arial", 20)).pack(pady=10)

        search_frame = tk.Frame(self)
        search_frame.pack(pady=5, fill=tk.X)

        tk.Label(search_frame, text="Keyword:").grid(row=0, column=0, padx=5)
        keyword_var = tk.StringVar()
        keyword_entry = tk.Entry(search_frame, width=30, textvariable=keyword_var)
        keyword_entry.grid(row=0, column=1, padx=5)

        tk.Label(search_frame, text="Filter by Read:").grid(row=0, column=2, padx=5)
        read_filter = ttk.Combobox(search_frame, values=["All", "Yes", "No"], state="readonly", width=8)
        read_filter.current(0)
        read_filter.grid(row=0, column=3, padx=5)

        columns = ("ID", "Title", "Author", "Location", "ReadBefore", "Rating")
        tree_frame = tk.Frame(self)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        tree.tag_configure('evenrow', background='#f2f2f2')
        tree.tag_configure('oddrow', background='#ffffff')
        for col in columns:
            tree.heading(col, text=col, command=lambda _col=col: sort_tree(_col))
            tree.column(col, width=100 if col=="ID" else 130, anchor="center")
        tree.grid(row=0, column=0, sticky="nsew")

        vsb = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)
        vsb.grid(row=0, column=1, sticky="ns")

        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)

        self.auto_resize_columns(tree)

        current_sort = {"column": None, "reverse": False}

        def sort_tree(col):
            data = [(tree.set(child, col), child) for child in tree.get_children('')]
            if col in ["ID", "Rating"]:
                data = [(int(d[0]) if d[0] != "N/A" else 0, d[1]) for d in data]
            data.sort(reverse=current_sort["reverse"])
            for index, (_, iid) in enumerate(data):
                tree.move(iid, '', index)
            if current_sort["column"] == col:
                current_sort["reverse"] = not current_sort["reverse"]
            else:
                current_sort["column"] = col
                current_sort["reverse"] = False

        def update_tree(*args):
            keyword = keyword_var.get()
            read_value = read_filter.get()
            books = get_books_by_keyword(keyword, read_filter=read_value)
            tree.delete(*tree.get_children())
            for idx, b in enumerate(books):
                tag = 'evenrow' if idx % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=(b[0], b[1], b[2], b[3], "Yes" if b[4] else "No", b[5] if b[5] else "N/A"), tags=(tag,))

        keyword_var.trace_add("write", update_tree)
        read_filter.bind("<<ComboboxSelected>>", lambda e: update_tree())

        # ===== Button Functions =====
        def edit_selected():
            selected = tree.selection()
            if not selected:
                messagebox.showwarning("Warning", "No book selected!")
                return
            book_id = tree.item(selected[0])["values"][0]
            self.edit_book_menu(book_id)

        def export_books():
            books = [tree.item(child)["values"] for child in tree.get_children()]
            if not books:
                messagebox.showinfo("Info", "No books to export.")
                return
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")],
                title="Save as"
            )
            if file_path:
                with open(file_path, mode='w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(columns)
                    writer.writerows(books)
                messagebox.showinfo("Success", f"Exported {len(books)} books to {file_path}")

        def import_books():
            file_path = filedialog.askopenfilename(
                filetypes=[("CSV files", "*.csv")],
                title="Select CSV to import"
            )
            if not file_path:
                return
            imported = 0
            with open(file_path, newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        title = row.get("Title") or row.get("title")
                        author = row.get("Author") or row.get("author")
                        location = row.get("Location") or row.get("location")
                        read_before = row.get("ReadBefore","No").strip().lower() in ["yes", "true", "1"]
                        rating_raw = row.get("Rating") or row.get("rating")
                        rating = int(rating_raw) if rating_raw and rating_raw.isdigit() else None
                        if title and author and location:
                            log_book(title, author, location, read_before, rating)
                            imported += 1
                    except:
                        continue
            messagebox.showinfo("Import Complete", f"Imported {imported} books from CSV.")
            update_tree()

        # ===== Buttons =====
        tk.Button(search_frame, text="Edit Selected", command=edit_selected, width=12).grid(row=1, column=0, pady=5)
        tk.Button(search_frame, text="Import CSV", command=import_books, width=12).grid(row=1, column=1, pady=5)
        tk.Button(search_frame, text="Export", command=export_books, width=12).grid(row=1, column=2, pady=5)
        tk.Button(search_frame, text="Back", command=self.start_menu, width=12).grid(row=1, column=3, pady=5)

        update_tree()  # initial population

    # ========== Edit Book ==========
    def edit_book_menu(self, book_id):
        self.clear_frame()
        book_list = get_all_books()
        book_data = next((b for b in book_list if b[0] == book_id), None)
        if not book_data:
            messagebox.showerror("Error", "Book not found")
            self.find_books_menu()
            return

        tk.Label(self, text="Edit Book", font=("Arial", 20)).pack(pady=10)
        frame = tk.Frame(self)
        frame.pack(pady=10)

        tk.Label(frame, text="Title").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        title_entry = tk.Entry(frame, width=40)
        title_entry.grid(row=0, column=1, padx=5, pady=5)
        title_entry.insert(0, book_data[1])

        tk.Label(frame, text="Author").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        author_entry = tk.Entry(frame, width=40)
        author_entry.grid(row=1, column=1, padx=5, pady=5)
        author_entry.insert(0, book_data[2])

        tk.Label(frame, text="Location").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        location_entry = tk.Entry(frame, width=40)
        location_entry.grid(row=2, column=1, padx=5, pady=5)
        location_entry.insert(0, book_data[3])

        read_var = tk.BooleanVar(value=book_data[4])
        tk.Checkbutton(frame, text="Read Before", variable=read_var).grid(row=3, column=1, sticky="w", pady=5)

        tk.Label(frame, text="Rating (1-10)").grid(row=4, column=0, padx=5, pady=5, sticky="e")
        rating_entry = tk.Entry(frame, width=10)
        rating_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
        rating_entry.insert(0, book_data[5] if book_data[5] else "")

        def save_changes():
            try:
                rating = int(rating_entry.get())
                if rating < 1 or rating > 10:
                    rating = None
            except ValueError:
                rating = None
            update_book(book_id, title_entry.get(), author_entry.get(), location_entry.get(), read_var.get(), rating)
            messagebox.showinfo("Success", "Book updated!")
            self.find_books_menu()

        def delete_book():
            if messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this book?"):
                remove_book(book_id)
                messagebox.showinfo("Deleted", "Book deleted")
                self.find_books_menu()

        tk.Button(self, text="Save Changes", command=save_changes, width=15).pack(pady=5)
        tk.Button(self, text="Delete Book", command=delete_book, width=15).pack(pady=5)
        tk.Button(self, text="Back", command=self.find_books_menu, width=15).pack(pady=5)

# ========== Run App ==========
if __name__ == "__main__":
    init_db()
    app = BookCatalogApp()
    app.mainloop()
