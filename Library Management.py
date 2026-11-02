import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox

FILE_NAME = "library.csv"

# ---------------- CSV INIT ----------------
if not os.path.exists(FILE_NAME):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["BookID", "Title", "Author", "Year", "Genre", "Status"])


def load_books():
    with open(FILE_NAME, "r") as f:
        return list(csv.DictReader(f))


def save_books(books):
    with open(FILE_NAME, "w", newline="") as f:
        writer = csv.DictWriter(f,
                                fieldnames=["BookID", "Title", "Author", "Year", "Genre", "Status"])
        writer.writeheader()
        writer.writerows(books)


def format_text(text):
    return text.strip().title()


# ======================================================
#                  MAIN LMS CLASS
# ======================================================
class LMS:
    def __init__(self, root, full_name):
        self.root = root
        self.full_name = full_name

        self.root.title("Library Management System")
        self.root.geometry("1000x550")
        self.root.configure(bg="#1e1e2f")

        self.mode = None
        self.main_menu()

    def clear(self):
        for w in self.root.winfo_children():
            w.destroy()

            # ---------------- MAIN MENU ----------------

    def main_menu(self):
        self.clear()

        tk.Label(self.root,
                 text="Library Management System",
                 font=("Arial", 22, "bold"),
                 bg="#1e1e2f",
                 fg="white").pack(pady=30)

        tk.Label(self.root,
                 text=f"Welcome to our library, {self.full_name}",
                 font=("Arial", 16, "bold"),
                 bg="#1e1e2f",
                 fg="lightgreen").pack(pady=10)

        tk.Button(self.root, text="User Menu",
                  width=25, height=2,
                  bg="green", fg="white",
                  command=self.user_mode, ).pack(pady=10)

        tk.Button(self.root, text="Admin Menu",
                  width=25, height=2,
                  bg="blue", fg="white",
                  command=self.admin_login).pack(pady=10)

        tk.Button(self.root, text="Exit",
                  width=25, height=2,
                  bg="red", fg="white",
                  command=self.root.destroy).pack(pady=10)

        # ---------------- ADMIN LOGIN ----------------

    def admin_login(self):
        win = tk.Toplevel(self.root, height=100, width=100)
        win.title("Admin Login")

        tk.Label(win, text="Enter Password").pack(pady=10)
        tk.Entry(win, show="*").pack()

        tk.Button(win, text="Enter",
                  command=lambda: [win.destroy(), self.admin_mode()]).pack(pady=10)

        # ---------------- MODES ----------------

    def user_mode(self):
        self.mode = "user"
        self.dashboard()

    def admin_mode(self):
        self.mode = "admin"
        self.dashboard()

        # ---------------- DASHBOARD ----------------

    def dashboard(self):
        self.clear()

        tk.Label(self.root,
                 text=f"{self.mode.upper()} DASHBOARD",
                 font=("Arial", 18, "bold"),
                 bg="#1e1e2f",
                 fg="white").pack(pady=10)

        frame = tk.Frame(self.root, bg="#1e1e2f")
        frame.pack()

        self.search_by = ttk.Combobox(frame,
                                      values=["BookID", "Title", "Author", "Genre"],
                                      state="readonly", width=12)
        self.search_by.set("Title")
        self.search_by.grid(row=0, column=0)

        self.search_entry = tk.Entry(frame, width=25)
        self.search_entry.grid(row=0, column=1)

        tk.Button(frame, text="Search", command=self.search).grid(row=0, column=2)

        # -------- SORT OPTION (FIXED) --------
        self.sort_by = ttk.Combobox(frame,
                                    values=["BookID", "Title", "Author", "Year", "Genre"],
                                    state="readonly", width=12)
        self.sort_by.set("Sort By")
        self.sort_by.grid(row=0, column=3)

        tk.Button(frame, text="Sort", command=self.sort_books).grid(row=0, column=4)

        # ---------------- TABLE ----------------
        style = ttk.Style()
        style.theme_use("default")

        style.configure("Treeview",
                        background="white",
                        foreground="black",
                        fieldbackground="white")

        style.configure("Treeview.Heading",
                        background="white",
                        foreground="black")

        cols = ("BookID", "Title", "Author", "Year", "Genre", "Status")

        self.tree = ttk.Treeview(self.root, columns=cols, show="headings")

        for c in cols:
            self.tree.heading(c, text=c)
            self.tree.column(c, width=140, anchor="center")

        self.tree.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        btn = tk.Frame(self.root, bg="#1e1e2f")
        btn.pack(pady=10)

        if self.mode == "user":
            tk.Button(btn, text="All Books", bg="#607D8B", fg="white",
                      command=self.load_all).grid(row=0, column=0, padx=5)

            tk.Button(btn, text="Available Books", bg="#00C853", fg="white",
                      command=self.load_available).grid(row=0, column=1, padx=5)

            tk.Button(btn, text="Borrow", bg="#FF9800", fg="white",
                      command=self.borrow).grid(row=0, column=2, padx=5)

            tk.Button(btn, text="Return", bg="#9C27B0", fg="white",
                      command=self.return_book).grid(row=0, column=3, padx=5)

            tk.Button(btn, text="Main Menu", bg="#555", fg="white",
                      command=self.main_menu).grid(row=0, column=4, padx=5)

        else:
            tk.Button(btn, text="All Books", bg="#607D8B", fg="white",
                      command=self.load_all).grid(row=0, column=0, padx=5)

            tk.Button(btn, text="Add", bg="#2196F3", fg="white",
                      command=self.add_book).grid(row=0, column=1, padx=5)

            tk.Button(btn, text="Update", bg="#FF9800", fg="white",
                      command=self.update_book).grid(row=0, column=2, padx=5)

            tk.Button(btn, text="Delete", bg="#f44336", fg="white",
                      command=self.delete_book).grid(row=0, column=3, padx=5)

            tk.Button(btn, text="Main Menu", bg="#555", fg="white",
                      command=self.main_menu).grid(row=0, column=4, padx=5)

        self.load_all()

        # ---------------- CORE ----------------

    def show(self, books):
        self.tree.delete(*self.tree.get_children())
        for b in books:
            self.tree.insert("", tk.END, values=(
                b["BookID"], b["Title"], b["Author"],
                b["Year"], b["Genre"], b["Status"]
            ))

    def load_all(self):
        self.show(load_books())

    def load_available(self):
        self.show([b for b in load_books() if b["Status"] == "Available"])

    def search(self):
        key = self.search_entry.get().lower()
        field = self.search_by.get()
        self.show([b for b in load_books() if key in b[field].lower()])

        # -------- SORT FUNCTION --------

    def sort_books(self):
        field = self.sort_by.get()
        books = load_books()

        if field in ["Year", "BookID"]:
            books.sort(key=lambda x: int(x[field]))
        else:
            books.sort(key=lambda x: x[field].lower())

        self.show(books)

    def selected(self):
        item = self.tree.focus()
        if not item:
            messagebox.showerror("Error", "Select a book first")
            return None
        return self.tree.item(item)["values"]

        # ---------------- BORROW ----------------

    def borrow(self):
        sel = self.selected()
        if not sel:
            return

        if not messagebox.askyesno("Confirm", "Do you want to borrow this book?"):
            return

        books = load_books()
        for b in books:
            if b["BookID"] == str(sel[0]):
                if b["Status"] == "Borrowed":
                    messagebox.showerror("Error", "Already borrowed")
                    return
                b["Status"] = "Borrowed"

        save_books(books)
        messagebox.showinfo("Success", "Book borrowed successfully")
        self.load_all()

        # ---------------- RETURN ----------------

    def return_book(self):
        win = tk.Toplevel(self.root)
        win.title("Return Book")

        cols = ("BookID", "Title", "Author", "Year", "Genre", "Status")
        tree = ttk.Treeview(win, columns=cols, show="headings")

        for c in cols:
            tree.heading(c, text=c)
            tree.column(c, width=120, anchor="center")

        tree.pack(fill=tk.BOTH, expand=True)

        for b in load_books():
            if b["Status"] == "Borrowed":
                tree.insert("", tk.END, values=(
                    b["BookID"], b["Title"], b["Author"],
                    b["Year"], b["Genre"], b["Status"]
                ))

        def confirm():
            item = tree.focus()
            if not item:
                return

            sel = tree.item(item)["values"]

            if not messagebox.askyesno("Confirm", "Return this book?"):
                return

            books = load_books()
            for b in books:
                if b["BookID"] == str(sel[0]):
                    b["Status"] = "Available"

            save_books(books)
            messagebox.showinfo("Success", "Book returned successfully")
            win.destroy()
            self.load_all()

        tk.Button(win, text="Return", command=confirm).pack()

        # ---------------- ADMIN ----------------

    def add_book(self):
        self.popup()

    def update_book(self):
        sel = self.selected()
        if sel:
            self.popup(sel)

    def delete_book(self):
        sel = self.selected()
        if not sel:
            return

        if not messagebox.askyesno("Confirm", "Delete this book?"):
            return

        books = [b for b in load_books() if b["BookID"] != str(sel[0])]
        save_books(books)
        messagebox.showinfo("Success", "Book deleted successfully")
        self.load_all()

        # ---------------- POPUP ----------------

    def popup(self, selected=None):
        win = tk.Toplevel(self.root)

        labels = ["BookID", "Title", "Author", "Year", "Genre"]
        entries = {}

        for i, l in enumerate(labels):
            tk.Label(win, text=l).grid(row=i, column=0)
            e = tk.Entry(win)
            e.grid(row=i, column=1)

            if selected:
                e.insert(0, selected[i])
                if l == "BookID":
                    e.config(state="readonly")

            entries[l] = e

        def save():
            books = load_books()
            data = [entries[l].get() for l in labels]

            data = [format_text(d) if i in [1, 2, 4] else d for i, d in enumerate(data)]

            if not data[0].isdigit():
                messagebox.showerror("Error", "Book ID must be a number")
                return

            if not data[3].isdigit():
                messagebox.showerror("Error", "Year must be a number")
                return

            year = int(data[3])
            if year < 1500 or year > 2026:
                messagebox.showerror("Error", "Year must be 1500–2026")
                return

            for b in books:
                if selected is None:
                    if b["BookID"] == data[0]:
                        messagebox.showerror("Error", "Book ID must be unique")
                        return
                else:
                    if b["BookID"] == data[0] and data[0] != str(selected[0]):
                        messagebox.showerror("Error", "Book ID must be unique")
                        return

            if not selected:
                books.append({
                    "BookID": data[0],
                    "Title": data[1],
                    "Author": data[2],
                    "Year": data[3],
                    "Genre": data[4],
                    "Status": "Available"
                })
            else:
                for b in books:
                    if b["BookID"] == str(selected[0]):
                        b["BookID"] = data[0]
                        b["Title"] = data[1]
                        b["Author"] = data[2]
                        b["Year"] = data[3]
                        b["Genre"] = data[4]

            save_books(books)
            messagebox.showinfo("Success", "Book saved successfully")
            self.load_all()
            win.destroy()

        tk.Button(win, text="Save", command=save).grid(row=6, columnspan=2, pady=10)

    # ======================================================


# START SCREEN
# ======================================================
def start_screen():
    root = tk.Tk()
    root.title("Welcome")
    root.geometry("350x250")
    root.configure(bg="#1e1e2f")

    tk.Label(root, text="Input your first name", bg="#1e1e2f", fg="white").pack(pady=5)
    first = tk.Entry(root)
    first.pack()

    tk.Label(root, text="Input your last name", bg="#1e1e2f", fg="white").pack(pady=5)
    last = tk.Entry(root)
    last.pack()

    def enter():
        f = format_text(first.get())
        l = format_text(last.get())

        if not f or not l:
            messagebox.showerror("Error", "Enter both names")
            return

        root.destroy()

        main = tk.Tk()
        LMS(main, f"{f} {l}")
        main.mainloop()

    tk.Button(root, text="Enter", bg="green", fg="white", command=enter).pack(pady=20)

    root.mainloop()


# RUN
start_screen()

