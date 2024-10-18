import tkinter as tk
from tkinter import ttk
import psycopg2
from psycopg2 import sql

# Function to connect to the PostgreSQL database
def connect_db():
    try:
        conn = psycopg2.connect(
            database="qlsv",  # Đổi thành chữ thường không có dấu ngoặc kép
            user="postgres",
            password="phattan112",
            host="localhost",
            port="5432"
)

        return conn
    except Exception as e:
        print("Error connecting to the database:", e)
        return None

# Function to load data into Treeview
def load_data():
    for row in tree.get_children():
        tree.delete(row)
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM students")
            rows = cursor.fetchall()
            for row in rows:
                tree.insert('', tk.END, values=row)
        except Exception as e:
            print("Error loading data:", e)
        finally:
            conn.close()

# Adding a new student
def add_student():
    conn = connect_db()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO students (name, age, gender, major) VALUES (%s, %s, %s, %s)",
                           (entry_name.get(), entry_age.get(), entry_gender.get(), entry_major.get()))
            conn.commit()
        except Exception as e:
            print("Error adding student:", e)
        finally:
            conn.close()
            load_data()

# Update selected student
def update_student():
    selected = tree.selection()
    if selected:
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                student_id = tree.item(selected[0])['values'][0]
                cursor.execute("""
                    UPDATE students
                    SET name=%s, age=%s, gender=%s, major=%s
                    WHERE id=%s
                """, (entry_name.get(), entry_age.get(), entry_gender.get(), entry_major.get(), student_id))
                conn.commit()
            except Exception as e:
                print("Error updating student:", e)
            finally:
                conn.close()
                load_data()

# Delete selected student
def delete_student():
    selected = tree.selection()
    if selected:
        conn = connect_db()
        if conn:
            try:
                cursor = conn.cursor()
                student_id = tree.item(selected[0])['values'][0]
                cursor.execute("DELETE FROM students WHERE id=%s", (student_id,))
                conn.commit()
            except Exception as e:
                print("Error deleting student:", e)
            finally:
                conn.close()
                load_data()

# Initialize main window
root = tk.Tk()
root.title("Student Management System")

# Top Frame (for input fields)
top_frame = tk.Frame(root)
top_frame.pack(pady=10)

tk.Label(top_frame, text="Tên:").grid(row=0, column=0)
entry_name = tk.Entry(top_frame)
entry_name.grid(row=0, column=1)

tk.Label(top_frame, text="Tuổi:").grid(row=0, column=2)
entry_age = tk.Entry(top_frame)
entry_age.grid(row=0, column=3)

tk.Label(top_frame, text="Giới tính:").grid(row=1, column=0)
entry_gender = tk.Entry(top_frame)
entry_gender.grid(row=1, column=1)

tk.Label(top_frame, text="Ngành học:").grid(row=1, column=2)
entry_major = tk.Entry(top_frame)
entry_major.grid(row=1, column=3)

# Middle Frame (for buttons)
middle_frame = tk.Frame(root)
middle_frame.pack(pady=10)

btn_add = tk.Button(middle_frame, text="Thêm sinh viên", command=add_student)
btn_add.grid(row=0, column=0, padx=10)

btn_update = tk.Button(middle_frame, text="Cập nhật thông tin", command=update_student)
btn_update.grid(row=0, column=1, padx=10)

btn_delete = tk.Button(middle_frame, text="Xóa sinh viên", command=delete_student)
btn_delete.grid(row=0, column=2, padx=10)

btn_reload = tk.Button(middle_frame, text="Tải lại danh sách", command=load_data)
btn_reload.grid(row=0, column=3, padx=10)

# Bottom Frame (for Treeview displaying student list)
bottom_frame = tk.Frame(root)
bottom_frame.pack(pady=10)

columns = ("id", "name", "age", "gender", "major")
tree = ttk.Treeview(bottom_frame, columns=columns, show="headings")
tree.heading("id", text="ID")
tree.heading("name", text="Tên")
tree.heading("age", text="Tuổi")
tree.heading("gender", text="Giới tính")
tree.heading("major", text="Ngành học")
tree.pack()

# Load data on startup
load_data()

# Start the main event loop
root.mainloop()

