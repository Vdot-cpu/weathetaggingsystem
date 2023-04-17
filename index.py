import tkinter.messagebox as tkMessageBox
import sqlite3
from tkinter import *
from tkinter import ttk, messagebox
from main import *
import datetime
import matplotlib.pyplot as plt
import yfinance as yf
from meteostat import Point, Daily, Monthly, Hourly
from datetime import datetime
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pytz
import json

global canvas
canvas = None

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
    btn_login = Button(LoginFrame, text="Login", font=('arial', 18), width=35, command=postLogin)
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


def postLogin(root=None):
    global graph_frame, canvas, graphs
    graphs = []  #list of all generated graphs
    # Remove the LoginFrame from the root window
    #LoginFrame.pack_forget()
    # Create a new frame to hold the graph canvas
    graph_frame2 = Frame(root)
    graph_frame2.pack(side=TOP, pady=5, padx=5, fill=BOTH, expand=True)
    # create the canvas widget and add it to the new frame
    canvas = FigureCanvasTkAgg(plt.gcf(), master=graph_frame2)
    canvas.get_tk_widget().pack(padx=0, pady=0)
    graphs.append(canvas) # add the canvas to the list of graphs
    # update the canvas widget with the initial graph
    canvas.draw()
    # Update the global graph_frame variable to the new frame
    graph_frame = graph_frame2



    Database()
    if USERNAME.get == "" or PASSWORD.get() == "":
        lbl_result1.config(text="Please complete the required field!", fg="orange")
    else:
        cursor.execute("SELECT * FROM `member` WHERE `username` = ? and `password` = ?",
                       (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:

            # object creation, name & layout
            root = Tk()
            root.title('Weather Tagging System')
            root.geometry("1000x1000")

            # dropdowns and search bar
            stock_label = Label(root, text="Enter Stock Ticker:").grid(row=0, column=0, sticky=W)
            stock_entry = Entry(root)
            stock_entry.grid(row=0, column=1, padx=5, pady=5, sticky=W)

            weather_label = Label(root, text="Select Weather Variable:").grid(row=1, column=0, sticky=W)
            weather_options = ["Temperature", "Precipitation", "Pressure"]
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

            def validate_date(date_str):
                try:
                    datetime.strptime(date_str, '%Y-%m-%d')
                    return True
                except ValueError:
                    return False
            # clears fields
            def clear():
                stock_entry.delete(0, END)
                weather_dropdown.set('')
                region_dropdown.set('')
                start_date_entry.delete(0, END)
                end_date_entry.delete(0, END)

            def clear_graphs():
                global graphs
                for graph in graphs:
                    graph.get_tk_widget().destroy()
                graphs = []
                plt.close('all')



            def generate_graph_clicked(stock_ticker, weather_variable, region, start_date, end_date, lbl_result=None):
                global canvas, graphs
                try:
                    # Get stock data
                    stock_data = get_stock_data(start_date, end_date, '1d', yf.Ticker(stock_ticker))

                    # Check if the stock data is valid
                    if stock_data is None:
                        return

                    if stock_ticker == '':
                        messagebox.showerror("Error", "Please enter a Stock ticker")

                    if start_date == '' or end_date == '':
                        messagebox.showerror("Error", "Please enter start and end dates.")
                    elif not validate_date(start_date) or not validate_date(end_date):
                        messagebox.showerror("Error", "Invalid date format. Please use the format 'YYYY-MM-DD'.")
                    else:
                        start_datetime = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=None)
                        end_datetime = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=None)
                        set_start_date_time(start_datetime.year, start_datetime.month, start_datetime.day)
                        set_end_date_time(end_datetime.year, end_datetime.month, end_datetime.day)

                    # Convert date strings to datetime objects with timezone information
                    start_datetime = datetime.strptime(start_date, '%Y-%m-%d').replace(tzinfo=None)
                    end_datetime = datetime.strptime(end_date, '%Y-%m-%d').replace(tzinfo=None)

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
                    elif weather_variable == "Pressure":
                        weather_parameter = "pres"

                    # Call plot_data() function

                    try:
                        createdGraph = plot_data(ticker, weather_parameter, location, root)
                    except AttributeError:
                        # Code to handle the error
                        messagebox.showerror("Please check your input",
                                             "The stock data could not be retrieved due to an attribute error.")

                    canvas = FigureCanvasTkAgg(createdGraph, master=root)
                    canvas.draw()
                    canvas_row = 5
                    canvas_col = 0
                    max_columns = 2
                    max_rows = 6

                    for i, graph in enumerate(graphs):
                        # Check if the number of rows exceeds the maximum
                        if canvas_row == max_rows:
                            messagebox.showerror("Error", "Cannot add more than 3 graphs.")
                            break
                        if canvas_col >= max_columns:
                            canvas_row += 1
                            canvas_col = 0
                        # Check if the maximum number of columns has been reached
                        if canvas_col == max_columns:
                            canvas_row += 1
                            canvas_col = 0

                        canvas.get_tk_widget().grid(row=canvas_row, column=canvas_col)
                        canvas_col += 1

                    # Add the canvas to the list of graphs
                    graphs.append(canvas)

                    # Update the canvas widget with the new graph
                    plt.show()
                    # Create canvas from figure and add to window



                except ValueError as e:
                    if lbl_result is not None:
                        lbl_result.config(text=str(e), fg="red")
                    else:
                        print(str(e))



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
            clear_display_button = Button(root, text="Clear Graphs", bd='5', command=clear_graphs).grid(row=4, column=3, pady=10)


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