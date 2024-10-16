import tkinter as tk
from tkinter import messagebox
import psycopg2
from psycopg2 import sql


class DatabaseApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Database App")

        # Database connection fields
        self.db_name = tk.StringVar(value='danhsach')
        self.user = tk.StringVar(value='postgres')
        self.password = tk.StringVar(value='phattan112')
        self.host = tk.StringVar(value='localhost')
        self.port = tk.StringVar(value='5432')
        self.table_name = tk.StringVar(value='danhsach')
        
    



        # Create GUI elements
        self.create_widgets()
        self.create_menu()  # Create the menu
    
    def create_widgets(self):
        # Connection section
        connection_frame = tk.Frame(self.root)
        connection_frame.pack(pady=10)

        tk.Label(connection_frame, text="DB Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.db_name).grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(connection_frame, text="User:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.user).grid(row=1, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Password:").grid(row=2, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.password, show="*").grid(row=2, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Host:").grid(row=3, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.host).grid(row=3, column=1, padx=5, pady=5)

        tk.Label(connection_frame, text="Port:").grid(row=4, column=0, padx=5, pady=5)
        tk.Entry(connection_frame, textvariable=self.port).grid(row=4, column=1, padx=5, pady=5)

        tk.Button(connection_frame, text="Connect", command=self.connect_db).grid(row=5, columnspan=2, pady=10)

        # Query section
        query_frame = tk.Frame(self.root)
        query_frame.pack(pady=10)

        tk.Label(query_frame, text="Table Name:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(query_frame, textvariable=self.table_name).grid(row=0, column=1, padx=5, pady=5)

        tk.Button(query_frame, text="Load Data", command=self.load_data).grid(row=1, columnspan=2, pady=10)

        self.data_display = tk.Text(self.root, height=10, width=50)
        self.data_display.pack(pady=10)

        # Insert section
        insert_frame = tk.Frame(self.root)
        insert_frame.pack(pady=10)

        self.column1 = tk.StringVar()
        self.column2 = tk.StringVar()

        tk.Label(insert_frame, text="Ho ten:").grid(row=0, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column1).grid(row=0, column=1, padx=5, pady=5)

        tk.Label(insert_frame, text="Dia chi:").grid(row=1, column=0, padx=5, pady=5)
        tk.Entry(insert_frame, textvariable=self.column2).grid(row=1, column=1, padx=5, pady=5)

        tk.Button(insert_frame, text="Insert Data", command=self.insert_data).grid(row=2, columnspan=2, pady=10)
    
    def create_menu(self):
        menubar = tk.Menu(self.root)
        
        # Create Database menu
        database_menu = tk.Menu(menubar, tearoff=0)
        database_menu.add_command(label="Connect", command=self.connect_db)
        database_menu.add_command(label="Load Data", command=self.load_data)
        database_menu.add_command(label="Insert Data", command=self.insert_data)
        menubar.add_cascade(label="Database", menu=database_menu)
        
        # Create Search menu
        search_menu = tk.Menu(menubar, tearoff=0)
        search_menu.add_command(label="Search Data", command=self.search_data)
        menubar.add_cascade(label="Search", menu=search_menu)

        # Create Delete menu
        delete_menu = tk.Menu(menubar, tearoff=0)
        delete_menu.add_command(label="Delete Data", command=self.delete_data)
        menubar.add_cascade(label="Delete", menu=delete_menu)

        self.root.config(menu=menubar)
    
    

    def connect_db(self):
        try:
            self.conn = psycopg2.connect(
                dbname=self.db_name.get(),
                user=self.user.get(),
                password=self.password.get(),
                host=self.host.get(),
                port=self.port.get()
            )
            self.cur = self.conn.cursor()
            messagebox.showinfo("Success", "Connected to the database successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error connecting to the database: {e}")

    def load_data(self):
        try:
            query = sql.SQL("SELECT * FROM {}").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(query)
            rows = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            for row in rows:
                self.data_display.insert(tk.END, f"{row}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error loading data: {e}")

    def insert_data(self):
        try:
            insert_query = sql.SQL("INSERT INTO {} (hoten, diachi) VALUES (%s, %s)").format(sql.Identifier(self.table_name.get()))
            data_to_insert = (self.column1.get(), self.column2.get())
            self.cur.execute(insert_query, data_to_insert)
            self.conn.commit()
            messagebox.showinfo("Success", "Data inserted successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Error inserting data: {e}")

    def search_data(self):
        search_window = tk.Toplevel(self.root)
        search_window.title("Search Data")
        
        tk.Label(search_window, text="Search by Name:").pack(pady=5)
        search_term = tk.StringVar()
        tk.Entry(search_window, textvariable=search_term).pack(pady=5)
        
        tk.Button(search_window, text="Search", command=lambda: self.perform_search(search_term.get())).pack(pady=5)

    def perform_search(self, term):
        try:
            search_query = sql.SQL("SELECT * FROM {} WHERE hoten ILIKE %s OR diachi ILIKE %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(search_query, (f'%{term}%', f'%{term}%'))
            results = self.cur.fetchall()
            self.data_display.delete(1.0, tk.END)
            for row in results:
                self.data_display.insert(tk.END, f"{row}\n")
        except Exception as e:
            messagebox.showerror("Error", f"Error searching data: {e}")

    def delete_data(self):
        delete_window = tk.Toplevel(self.root)
        delete_window.title("Delete Data")
        
        tk.Label(delete_window, text="Enter ID to Delete:").pack(pady=5)
        delete_id = tk.StringVar()
        tk.Entry(delete_window, textvariable=delete_id).pack(pady=5)
        
        tk.Button(delete_window, text="Delete", command=lambda: self.perform_delete(delete_id.get())).pack(pady=5)

    def perform_delete(self, id_value):
        try:
            delete_query = sql.SQL("DELETE FROM {} WHERE id = %s").format(sql.Identifier(self.table_name.get()))
            self.cur.execute(delete_query, (id_value,))
            self.conn.commit()
            messagebox.showinfo("Success", "Data deleted successfully!")
            
            self.load_data()
        except Exception as e:
            messagebox.showerror("Error", f"Error deleting data: {e}")
def connect_db(self):
    try:
        # Đoạn code bạn cần sửa để kết nối tới database
        self.conn = psycopg2.connect(
            dbname=self.db_name.get(),
            user=self.user.get(),
            password=self.password.get(),
            host=self.host.get(),
            port='5432'  # Cập nhật cổng về 5432 hoặc bất kỳ cổng nào PostgreSQL đang sử dụng
        )
        self.cur = self.conn.cursor()
        messagebox.showinfo("Success", "Connected to the database successfully!")
    except Exception as e:
        messagebox.showerror("Error", f"Error connecting to the database: {e}")


if __name__ == "__main__":
    root = tk.Tk()
    app = DatabaseApp(root)
    root.mainloop()