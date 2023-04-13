import tkinter.messagebox as tkMessageBox
import sqlite3
from tkinter import *
from tkinter import ttk
from main import *
import datetime
import matplotlib.pyplot as plt
import yfinance as yf
from meteostat import Point, Daily, Monthly, Hourly
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pytz



root = Tk()
root.title("Weather Tagging System")

width = 640
height = 480
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width / 2) - (width / 2)
y = (screen_height / 2) - (height / 2)
root.geometry("%dx%d+%d+%d" % (width, height, x, y))
root.resizable(0, 0)

def Database():
    global conn, cursor
    conn = sqlite3.connect("db_member.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `member` (mem_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT, firstname TEXT, lastname TEXT)")


USERNAME = StringVar()
PASSWORD = StringVar()
FIRSTNAME = StringVar()
LASTNAME = StringVar()


def LoginForm():
    global LoginFrame, lbl_result1
    LoginFrame = Frame(root)
    LoginFrame.pack(side=TOP, pady=80)
    lbl_username = Label(LoginFrame, text="Username:", font=('arial', 25), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(LoginFrame, text="Password:", font=('arial', 25), bd=18)
    lbl_password.grid(row=2)
    lbl_result1 = Label(LoginFrame, text="", font=('arial', 18))
    lbl_result1.grid(row=3, columnspan=2)
    username = Entry(LoginFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(LoginFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=Login)
    btn_login.grid(row=4, columnspan=2, pady=20)
    lbl_register = Label(LoginFrame, text="Register", fg="Blue", font=('arial', 12))
    lbl_register.grid(row=0, sticky=W)
    lbl_register.bind('<Button-1>', ToggleToRegister)


def RegisterForm():
    global RegisterFrame, lbl_result2
    RegisterFrame = Frame(root)
    RegisterFrame.pack(side=TOP, pady=40)
    lbl_username = Label(RegisterFrame, text="Username:", font=('arial', 18), bd=18)
    lbl_username.grid(row=1)
    lbl_password = Label(RegisterFrame, text="Password:", font=('arial', 18), bd=18)
    lbl_password.grid(row=2)
    lbl_firstname = Label(RegisterFrame, text="Firstname:", font=('arial', 18), bd=18)
    lbl_firstname.grid(row=3)
    lbl_lastname = Label(RegisterFrame, text="Lastname:", font=('arial', 18), bd=18)
    lbl_lastname.grid(row=4)
    lbl_result2 = Label(RegisterFrame, text="", font=('arial', 18))
    lbl_result2.grid(row=5, columnspan=2)
    username = Entry(RegisterFrame, font=('arial', 20), textvariable=USERNAME, width=15)
    username.grid(row=1, column=1)
    password = Entry(RegisterFrame, font=('arial', 20), textvariable=PASSWORD, width=15, show="*")
    password.grid(row=2, column=1)
    firstname = Entry(RegisterFrame, font=('arial', 20), textvariable=FIRSTNAME, width=15)
    firstname.grid(row=3, column=1)
    lastname = Entry(RegisterFrame, font=('arial', 20), textvariable=LASTNAME, width=15)
    lastname.grid(row=4, column=1)
    btn_login = Button(RegisterFrame, text="Register", font=('arial', 18), width=35, command=Register)
    btn_login.grid(row=6, columnspan=2, pady=20)
    lbl_login = Label(RegisterFrame, text="Login", fg="Blue", font=('arial', 12))
    lbl_login.grid(row=0, sticky=W)
    lbl_login.bind('<Button-1>', ToggleToLogin)


# =======================================METHODS=======================================
def Exit():
    result = tkMessageBox.askquestion('System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()


def ToggleToLogin(event=None):
    RegisterFrame.destroy()
    LoginForm()


def ToggleToRegister(event=None):
    LoginFrame.destroy()
    RegisterForm()


def Register():
    Database()
    if USERNAME.get == "" or PASSWORD.get() == "" or FIRSTNAME.get() == "" or LASTNAME.get == "":
        lbl_result2.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ?", (USERNAME.get(),))
        if cursor.fetchone() is not None:
            lbl_result2.config(text="Username is already taken", fg="red")
        else:
            cursor.execute("INSERT INTO `member` (username, password, firstname, lastname) VALUES(?, ?, ?, ?)",
                           (str(USERNAME.get()), str(PASSWORD.get()), str(FIRSTNAME.get()), str(LASTNAME.get())))
            conn.commit()
            USERNAME.set("")
            PASSWORD.set("")
            FIRSTNAME.set("")
            LASTNAME.set("")
            lbl_result2.config(text="Successfully Created!", fg="black")
        cursor.close()
        conn.close()


def Login(root=None):
    graph_frame = Frame(root)
    graph_frame.pack(padx=5, pady=3)

    # create the canvas widget and add it to the frame
    canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_frame)
    canvas.get_tk_widget().pack(padx=0, pady=0)

    # update the canvas widget with the initial graph
    canvas.draw()

    def generate_graph_clicked(stock_ticker, weather_variable, region, start_date, end_date, lbl_result=None):
        try:
            # Convert date strings to datetime objects with timezone information
            start_datetime = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=None)
            end_datetime = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=None)

            #CONVERT DATETIME TO TIMESTAMP


            # Set date range
            set_start_date_time(start_datetime.year, start_datetime.month, start_datetime.day)
            set_end_date_time(end_datetime.year, end_datetime.month, end_datetime.day)

            # Get stock ticker object
            ticker = yf.Ticker(stock_ticker)

            # Get location object based on selected region
            if region == "APAC":
                location = Point(35.6762, 139.6503)  # Tokyo
            elif region == "EMEA":
                location = Point(51.5074, -0.1278)  # London
            elif region == "NA":
                location = Point(40.7128, -74.0060)  # New York

            # Set weather parameter based on selected weather variable
            if weather_variable == "Temperature":
                weather_parameter = "tavg"
            elif weather_variable == "Precipitation":
                weather_parameter = "prcp"
            elif weather_variable == "Humidity":
                weather_parameter = "rh_avg"

            # Call plot_data() function
            plot_data(ticker, weather_parameter, location)

            # Update the canvas widget with the new graph
            canvas.draw()

        except ValueError as e:
            if lbl_result is not None:
                lbl_result.config(text=str(e), fg="red")
            else:
                print(str(e))


    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?",
                       (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:

            # object creation, name & layout
            root = Tk()
            root.title('Put in a snazzy name')
            root.geometry("1000x1000")

            # dropdowns and search bar
            stock_label = Label(root, text="Enter Stock Ticker:").grid(row=0, column=0, sticky=W)
            stock_entry = Entry(root)
            stock_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

            weather_label = Label(root, text="Select Weather Variable:").grid(row=1, column=0, sticky=W)
            weather_options = ["Temperature", "Precipitation", "Humidity"]
            weather_dropdown = ttk.Combobox(root, value=weather_options)
            weather_dropdown.grid(row=1, column=1, padx=5, pady=5, sticky=W)

            region_label = Label(root, text="Select Region:").grid(row=2, column=0, sticky=W)
            region_options = ["APAC", "EMEA", "NA"]
            region_dropdown = ttk.Combobox(root, value=region_options)
            region_dropdown.grid(row=2, column=1, padx=5, pady=5, sticky=W)

            date_label = Label(root, text="Enter Date Range (yyyy-mm-dd):").grid(row=3, column=0, sticky=W)
            start_date_entry = Entry(root)
            start_date_entry.grid(row=3, column=1, padx=5, pady=5, sticky=W)
            end_date_entry = Entry(root)
            end_date_entry.grid(row=3, column=2, padx=5, pady=5, sticky=W)

            # clears fields
            def clear():
                stock_entry.delete(0, END)
                weather_dropdown.set('')
                region_dropdown.set('')
                start_date_entry.delete(0, END)
                end_date_entry.delete(0, END)

            # layout
            stock_entry.grid(row=0, column=1)
            weather_dropdown.grid(row=1, column=1)
            region_dropdown.grid(row=2, column=1)
            start_date_entry.grid(row=3, column=1)
            end_date_entry.grid(row=3, column=2)

            # button creation
            clear = Button(root, text="Clear Selection", bd='5', command=clear).grid(row=4, column=0, pady=10)
            end = Button(root, text="Quit Application", bd='5', command=root.destroy).grid(row=4, column=1, pady=10)
            generate_graph = Button(root, text="Generate Graph", bd='5', command=lambda: generate_graph_clicked(stock_entry.get(), weather_dropdown.get(), region_dropdown.get(), start_date_entry.get(), end_date_entry.get())).grid(row=4, column=2, pady=10)

            # execution
            root.mainloop()




        else:
            lbl_result1.config(text="Invalid Username or password", fg="red")




LoginForm()



menubar = Menu(root)
filemenu = Menu(menubar, tearoff=0)
filemenu.add_command(label="Exit", command=Exit)
menubar.add_cascade(label="File", menu=filemenu)
root.config(menu=menubar)


if __name__ == '__main__':
    root.mainloop()