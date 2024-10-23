import tkinter as tk
from tkinter import ttk, messagebox
import psycopg2

db_connection = None

def login():
    global db_connection
    try:
        db_connection = psycopg2.connect(
            database="postgres",
            user=entry_user.get(),
            password=entry_password.get(),
            host="localhost",
            port="5432"
        )
        messagebox.showinfo("Thành công", "Đăng nhập thành công!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi đăng nhập: {e}")

def register_user():
    try:
        with psycopg2.connect(
            database="postgres", user="postgres", password="admin", host="localhost", port="5432"
        ) as conn:
            conn.autocommit = True
            cursor = conn.cursor()
            username = entry_new_user.get()
            password = entry_new_password.get()
            cursor.execute(f"CREATE USER {username} WITH PASSWORD %s", (password,))
            cursor.execute(f"GRANT CONNECT ON DATABASE postgres TO {username}")
            messagebox.showinfo("Thành công", f"User '{username}' đã được tạo!")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi tạo user: {e}")

def search_users():
    keyword = entry_search.get().strip()  
    try:
        with psycopg2.connect(
            database="postgres", user="postgres", password="admin", host="localhost", port="5432"
        ) as conn:
            cursor = conn.cursor()
            query = "SELECT usename FROM pg_user WHERE usename ILIKE %s"
            cursor.execute(query, (f"%{keyword}%",))
            users = cursor.fetchall()

            for row in tree.get_children():
                tree.delete(row)

            if users:
                for user in users:
                    tree.insert('', tk.END, values=user)
            else:
                messagebox.showinfo("Kết quả", "Không tìm thấy user nào.")
    except Exception as e:
        messagebox.showerror("Lỗi", f"Lỗi tìm kiếm user: {e}")

def main_window():
    root = tk.Tk()
    root.title("Quản lý User PostgreSQL")

    notebook = ttk.Notebook(root)
    notebook.pack(padx=10, pady=10, expand=True)

    login_tab = ttk.Frame(notebook)
    notebook.add(login_tab, text="Đăng nhập")

    tk.Label(login_tab, text="User:").grid(row=0, column=0, padx=5, pady=5)
    global entry_user
    entry_user = tk.Entry(login_tab)
    entry_user.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(login_tab, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    global entry_password
    entry_password = tk.Entry(login_tab, show="*")
    entry_password.grid(row=1, column=1, padx=5, pady=5)

    btn_login = tk.Button(login_tab, text="Login", command=login)
    btn_login.grid(row=2, column=0, columnspan=2, pady=10)

    register_tab = ttk.Frame(notebook)
    notebook.add(register_tab, text="Đăng ký User")

    tk.Label(register_tab, text="User mới:").grid(row=0, column=0, padx=5, pady=5)
    global entry_new_user
    entry_new_user = tk.Entry(register_tab)
    entry_new_user.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(register_tab, text="Password:").grid(row=1, column=0, padx=5, pady=5)
    global entry_new_password
    entry_new_password = tk.Entry(register_tab, show="*")
    entry_new_password.grid(row=1, column=1, padx=5, pady=5)

    btn_register_user = tk.Button(register_tab, text="Tạo User", command=register_user)
    btn_register_user.grid(row=2, column=0, columnspan=2, pady=10)

    search_tab = ttk.Frame(notebook)
    notebook.add(search_tab, text="Tìm kiếm User")

    tk.Label(search_tab, text="Từ khóa tìm kiếm:").pack(padx=5, pady=5)
    global entry_search
    entry_search = tk.Entry(search_tab)
    entry_search.pack(padx=5, pady=5)

    btn_search_users = tk.Button(search_tab, text="Tìm User", command=search_users)
    btn_search_users.pack(pady=10)

    global tree
    tree = ttk.Treeview(search_tab, columns=("User"), show="headings")
    tree.heading("User", text="Tên User")
    tree.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

    root.mainloop()

if __name__ == "__main__":
    main_window()
