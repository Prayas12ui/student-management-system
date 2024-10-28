from tkinter import *
import time
import ttkthemes
from tkinter import ttk, messagebox
import pymysql

# Global variables for the connection and cursor
con = None
mycursor = None

def show_student():
    query = 'SELECT * FROM studentmgt'
    mycursor.execute(query)
    fetched_data = mycursor.fetchall()
    studentTable.delete(*studentTable.get_children())
    for data in fetched_data:
        studentTable.insert('', END, values=data)
    print("Current Students:")
    for data in fetched_data:
        print(data)  # Output to terminal

def delete_student():
    indexing = studentTable.focus()
    if not indexing:
        messagebox.showerror('Error', 'Please select a student to delete.')
        return

    content = studentTable.item(indexing)
    content_id = content['values'][0]
    query = 'DELETE FROM studentmgt WHERE id=%s'
    mycursor.execute(query, (content_id,))
    con.commit()
    messagebox.showinfo('Deleted', f'Id {content_id} is deleted successfully')
    print(f"Deleted Student ID: {content_id}")  # Output to terminal
    show_student()

def add_student():
    def add_data():
        global mycursor, con
        if con is None or mycursor is None:
            messagebox.showerror('Error', 'Database connection not established', parent=add_window)
            return
        
        if (idEntry.get() == '' or nameEntry.get() == '' or PhoneEntry.get() == '' or 
            EmailEntry.get() == '' or addressEntry.get() == '' or genderEntry.get() == '' or 
            dobEntry.get() == ''):
            messagebox.showerror('Error', 'All Fields are required', parent=add_window)
        else:
            try:
                currenttime = time.strftime('%H:%M:%S')
                query = 'INSERT INTO studentmgt (id, name, mobile, email, address, gender, dob, time) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
                mycursor.execute(query, (idEntry.get(), nameEntry.get(), PhoneEntry.get(), 
                                          EmailEntry.get(), addressEntry.get(), genderEntry.get(), 
                                          dobEntry.get(), currenttime))

                con.commit()
                print(f"Added Student: {idEntry.get()}, {nameEntry.get()}, {PhoneEntry.get()}, {EmailEntry.get()},{addressEntry.get()}, {genderEntry.get()}, {dobEntry.get()}")  # Output to terminal

                result = messagebox.askyesno('Confirm', 'Data added successfully. Do you want to clear the form?', parent=add_window)
                if result:
                    idEntry.delete(0, END)
                    nameEntry.delete(0, END)
                    PhoneEntry.delete(0, END)
                    EmailEntry.delete(0, END)
                    addressEntry.delete(0, END)
                    genderEntry.delete(0, END)
                    dobEntry.delete(0, END)
            except pymysql.IntegrityError:
                messagebox.showerror('Error', 'Id cannot be repeated', parent=add_window)
            except Exception as e:
                messagebox.showerror('Error', f'Failed to add data: {e}', parent=add_window)

            show_student()

    add_window = Toplevel()
    add_window.title('Add Student')
    add_window.geometry('400x400')

    # Create Entry Labels and Fields
    fields = [
        ('Id', 0), ('Name', 1), ('Mobile', 2), ('Email', 3),
        ('Address', 4), ('Gender', 5), ('D.O.B', 6)
    ]
    
    entries = {}
    for field, row in fields:
        label = Label(add_window, text=field, font=('times new roman', 20, 'bold'))
        label.grid(row=row, column=0, padx=30, pady=15)
        entry = Entry(add_window, font=('roman', 15, 'bold'))
        entry.grid(row=row, column=1, pady=15, padx=10)
        entries[field] = entry

    idEntry = entries['Id']
    nameEntry = entries['Name']
    PhoneEntry = entries['Mobile']
    EmailEntry = entries['Email']
    addressEntry = entries['Address']
    genderEntry = entries['Gender']
    dobEntry = entries['D.O.B']

    add_student_button = ttk.Button(add_window, text='ADD STUDENT', command=add_data)
    add_student_button.grid(row=7, columnspan=2)

def update_student():
    indexing = studentTable.focus()
    if not indexing:
        messagebox.showerror('Error', 'Please select a student to update.')
        return

    content = studentTable.item(indexing)
    current_data = content['values']
    
    def save_update():
        if (nameEntry.get() == '' or PhoneEntry.get() == '' or 
            EmailEntry.get() == '' or addressEntry.get() == '' or 
            genderEntry.get() == '' or dobEntry.get() == ''):
            messagebox.showerror('Error', 'All Fields are required', parent=update_window)
            return
        
        query = '''UPDATE studentmgt SET name=%s, mobile=%s, email=%s, address=%s, gender=%s, dob=%s WHERE id=%s'''
        mycursor.execute(query, (nameEntry.get(), PhoneEntry.get(), EmailEntry.get(), 
                                  addressEntry.get(), genderEntry.get(), dobEntry.get(), current_data[0]))
        con.commit()
        print(f"Updated Student ID: {current_data[0]} to {nameEntry.get()},{PhoneEntry.get()}, {EmailEntry.get()}, {addressEntry.get()},{genderEntry.get()}, {dobEntry.get()}")  # Output to terminal
        messagebox.showinfo('Updated', 'Data updated successfully')
        show_student()
        update_window.destroy()

    update_window = Toplevel()
    update_window.title('Update Student')
    update_window.geometry('400x400')

    # Create Entry Labels and Fields
    fields = [
        ('Id', 0), ('Name', 1), ('Mobile', 2), ('Email', 3),
        ('Address', 4), ('Gender', 5), ('D.O.B', 6)
    ]
    
    entries = {}
    for field, row in fields:
        label = Label(update_window, text=field, font=('times new roman', 20, 'bold'))
        label.grid(row=row, column=0, padx=30, pady=15)
        entry = Entry(update_window, font=('roman', 15, 'bold'))
        entry.grid(row=row, column=1, pady=15, padx=10)
        entries[field] = entry

    idEntry = entries['Id']
    nameEntry = entries['Name']
    PhoneEntry = entries['Mobile']
    EmailEntry = entries['Email']
    addressEntry = entries['Address']
    genderEntry = entries['Gender']
    dobEntry = entries['D.O.B']

    # Pre-fill with current student data
    idEntry.insert(0, current_data[0])
    nameEntry.insert(0, current_data[1])
    PhoneEntry.insert(0, current_data[2])
    EmailEntry.insert(0, current_data[3])
    addressEntry.insert(0, current_data[4])
    genderEntry.insert(0, current_data[5])
    dobEntry.insert(0, current_data[6])

    update_student_button = ttk.Button(update_window, text='UPDATE STUDENT', command=save_update)
    update_student_button.grid(row=7, columnspan=2)

def connect_database():
    global mycursor, con
    def connect():
        global mycursor, con
        try:
            con = pymysql.connect(host=hostEntry.get(), user=userEntry.get(), password=passwordEntry.get())
            mycursor = con.cursor()
            mycursor.execute('CREATE DATABASE IF NOT EXISTS `student_management_system`')
            mycursor.execute('USE `student_management_system`')
            mycursor.execute('''CREATE TABLE IF NOT EXISTS studentmgt (
                id INT NOT NULL PRIMARY KEY,
                name VARCHAR(30),
                mobile VARCHAR(10),
                email VARCHAR(30),
                address VARCHAR(100),
                gender VARCHAR(20),
                dob VARCHAR(50),
                time VARCHAR(50))''')
            messagebox.showinfo('Success', 'Database and Table Created Successfully', parent=connectWindow)
        except Exception as e:
            messagebox.showerror('Error', f'Invalid Detail: {e}', parent=connectWindow)
        finally:
            connectWindow.grab_release()
            connectWindow.destroy()

    connectWindow = Toplevel()
    connectWindow.grab_set()
    connectWindow.geometry('470x250+730+230')
    connectWindow.title('Database Connection')
    connectWindow.resizable(0, 0)

    # Entry Labels and Fields for Database Connection
    labels = ['Host Name', 'User Name', 'Password']
    entries = {}
    for i, label in enumerate(labels):
        Label(connectWindow, text=label, font=('arial', 20, 'bold')).grid(row=i, column=0)
        entry = Entry(connectWindow, font=('roman', 15, 'bold'), show='*' if label == 'Password' else '')
        entry.grid(row=i, column=1, padx=40, pady=20)
        entries[label] = entry

    hostEntry = entries['Host Name']
    userEntry = entries['User Name']
    passwordEntry = entries['Password']

    connectButton = ttk.Button(connectWindow, text='Connect', command=connect)
    connectButton.grid(row=3, columnspan=2)

def slider():
    global text, count
    if count >= len(s):
        count = 0
        text = ''
    else:
        text += s[count]
        count += 1
    sliderLabel.config(text=text)
    sliderLabel.after(300, slider)

def clock():
    date = time.strftime('%d/%m/%Y')
    currenttime = time.strftime('%H:%M:%S')
    datetimeLabel.config(text=f'Date: {date}\nTime: {currenttime}')
    datetimeLabel.after(1000, clock)

def exit_application():
    if messagebox.askokcancel("Quit", "Do you really want to quit?"):
        root.destroy()

root = ttkthemes.ThemedTk()
root.get_themes()
root.set_theme('radiance')
root.title('Student Management System')

# Date and Time Label
datetimeLabel = Label(root, font=('times new roman', 18, 'bold'))
datetimeLabel.place(x=10, y=10)
clock()

# Title Slider
s = 'Student Management System'
text = ''
count = 0
sliderLabel = Label(root, text=s, font=('arial', 28, 'italic bold'))
sliderLabel.place(relx=0.5, rely=0, anchor=N)
slider()

# Connect Database Button
ttk.Button(root, text='Connect Database', command=connect_database).place(relx=1, x=-10, y=10, anchor=NE)

# Left Frame
leftFrame = Frame(root)
leftFrame.place(x=10, y=100, width=300, height=600)

# Logo Image
logo_image = PhotoImage(file='student.png')  # Ensure this image path is correct
Label(leftFrame, image=logo_image).grid(row=0, column=0, padx=10, pady=10)

# Action Buttons
buttons = [
    ('Add Student', 1, add_student),
    ('Update Student', 2, update_student),
    ('Delete Student', 3, delete_student),
    ('Show Student', 4, show_student),
    ('Exit', 5, exit_application)
]

for text, row, command in buttons:
    ttk.Button(leftFrame, text=text, command=command, width=20).grid(row=row, column=0, pady=15)

# Right Frame
RIGHTFrame = Frame(root, bg='yellow')
RIGHTFrame.place(x=350, y=100, width=930, height=700)

# Scrollbars
scrollBarX = Scrollbar(RIGHTFrame, orient=HORIZONTAL)
scrollBarY = Scrollbar(RIGHTFrame, orient=VERTICAL)

# Student Table
studentTable = ttk.Treeview(RIGHTFrame, columns=('Id', 'Name', 'Mobile No', 'Email', 'Gender', 'DOB'),
                             xscrollcommand=scrollBarX.set, yscrollcommand=scrollBarY.set)
for col in ('Id', 'Name', 'Mobile No', 'Email', 'Gender', 'DOB'):
    studentTable.heading(col, text=col)
studentTable['show'] = 'headings'
scrollBarX.pack(side=BOTTOM, fill=X)
scrollBarY.pack(side=RIGHT, fill=Y)
scrollBarX.config(command=studentTable.xview)
scrollBarY.config(command=studentTable.yview)

studentTable.pack(fill=BOTH, expand=True)

root.mainloop()
