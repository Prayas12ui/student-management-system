from tkinter import *
from PIL import Image, ImageTk
from tkinter import messagebox

def login():
    if usernameEntry.get() == '' or passwordEntry.get() == '':
        messagebox.showerror('Error', 'Fields cannot be empty')
    elif usernameEntry.get() == 'Prayas' and passwordEntry.get() == '1235':
        messagebox.showinfo('Success', 'Welcome')
        window.destroy()
        import sms
    else:
        messagebox.showerror('Error', 'Please enter correct details')

window = Tk()

window.title('Login Of Student Managment System')

# Background Image
backgroundImage = Image.open('bg.jpg')
backgroundImage = ImageTk.PhotoImage(backgroundImage)
bgLabel = Label(window, image=backgroundImage)
bgLabel.place(x=1, y=1, relwidth=1, relheight=1)

# Frame for login
loginFrame = Frame(window)
loginFrame.place(relx=0.5, rely=0.5, anchor=CENTER)  # Center the frame

# Logo Image
logoImage = Image.open('logo.png')
logoImage = ImageTk.PhotoImage(logoImage)
logoLabel = Label(loginFrame, image=logoImage)
logoLabel.grid(row=0, column=0, columnspan=2)  # Span across two columns
logoLabel.image = logoImage

# Username Image and Label
usernameImage = PhotoImage(file='user.png')
usernameLabel = Label(loginFrame, image=usernameImage, text='Username', compound=LEFT, font=('times new roman', 20, 'bold'))
usernameLabel.grid(row=1, column=0, padx=10, pady=10)

# Username Entry
usernameEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'))
usernameEntry.grid(row=1, column=1, padx=10, pady=10)

# Password Image and Label
passwordImage = PhotoImage(file='password.png')
passwordLabel = Label(loginFrame, image=passwordImage, text='Password', compound=LEFT, font=('times new roman', 20, 'bold'))
passwordLabel.grid(row=2, column=0, padx=10, pady=10)

# Password Entry
passwordEntry = Entry(loginFrame, font=('times new roman', 20, 'bold'), show='*')
passwordEntry.grid(row=2, column=1, padx=10, pady=10)

# Login Button
loginButton = Button(loginFrame, text="Login", font=('times new roman', 14, 'bold'), bg="blue", fg="white", command=login)
loginButton.grid(row=3, column=0, columnspan=2, pady=20)

window.mainloop()
