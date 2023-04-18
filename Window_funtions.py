from tkinter import *
from tkinter import font
import hashlib
import harperdb
from datetime import datetime

db = harperdb.HarperDB(url="https://pb175-marvav.harperdbcloud.com",
                       username="marvav", password="muniprojekt123")
frames = {"log_in": None, "register": None, "main_menu": None,
          "your_tickets": None, "profile": None, "tours": None}
user = None


def hide_all_frames(new_frame):
    for frame in frames.values():
        frame.place_forget()
    frames[new_frame].pack()
    frames[new_frame].place(relx=0.5, rely=0.5, anchor=CENTER)


def initialize_window() -> Tk:
    window = Tk()
    window.title("My Window")
    # screen_width = window.winfo_screenwidth()
    # screen_height = window.winfo_screenheight()
    width_percent = 450
    height_percent = 700
    # Set the window size
    window.geometry(f"{width_percent}x{height_percent}")
    return window


def init_profile():
    profile = frames["profile"]
    Label(profile, text='Your Profile').pack()

    Button(profile, text='Log offk',
           command=lambda: hide_all_frames("log_in")).pack()


def show_your_tickets():
    print(user)
    hide_all_frames("your_tickets")


def load_tours():
    upcoming_tours = []
    index = 10
    current_time = datetime.now()
    while index > 10:
        tour = db.search_by_value("database", "tour_dates", "start_time",
                                  get_attributes=['*'])


def init_tours():
    tours = frames["tours"]
    Label(tours, text='Upcoming Tours').pack()
    Button(tours, text='Go back',
           command=lambda: hide_all_frames("main_menu")).pack()


def init_your_tickets():
    your_tickets = frames["your_tickets"]
    Label(your_tickets, text='Your Tickets').pack()

    Button(your_tickets, text='Go back',
           command=lambda: hide_all_frames("main_menu")).pack()


def init_main_menu():
    main_menu = frames["main_menu"]
    Label(main_menu, text='Main Menu', font=big_font, width=20,
          height=2).pack()

    Button(main_menu, text='Upcoming Tours', font=big_font, width=20, height=2,
           command=lambda: hide_all_frames("tours")).pack()
    Button(main_menu, text='Your Tickets', font=big_font, width=20, height=2,
           command=lambda: show_your_tickets()).pack()
    Button(main_menu, text='Profile', font=big_font, width=20, height=2,
           command=lambda: hide_all_frames("profile")).pack()


def init_register():
    frame = frames["register"]
    Label(frames["register"], text='Register').pack()

    Label(frame, text='Enter username', font=small_font).pack()
    username = Entry(frame)
    username.pack()

    Label(frame, text='Enter password', font=small_font).pack()
    password = Entry(frame)
    password.pack()

    Button(frame, text='Confirm', font=big_font, width=20, height=2,
           command=lambda: register_user(username, password)).pack()
    Button(frame, text='Go back', font=big_font, width=20, height=2,
           command=lambda: hide_all_frames("log_in")).pack()
    Button(frame, text='EXIT', font=big_font, width=20, height=2,
           command=lambda: exit()).pack()


def init_fonts():
    global big_font
    big_font = font.Font(family="Helvetica", size=18, weight="bold")
    global small_font
    small_font = font.Font(family="Helvetica", size=14)


def init_log_in() -> None:
    frame = frames["log_in"]

    Label(frame, text='Log In page', width=20, height=2, font=big_font).pack()
    Label(frame, text='Enter username', font=small_font).pack()

    username = Entry(frame)
    username.pack()

    Label(frame, text='Enter password', font=small_font).pack()
    password = Entry(frame)
    password.pack()

    Button(frame, text='Log In', font=big_font, width=20, height=2,
           command=lambda: authorize_credentials(username, password)).pack()
    Button(frame, text='Register', font=big_font, width=20, height=2,
           command=lambda: hide_all_frames("register")).pack()
    Button(frame, text='EXIT', font=big_font, width=20, height=2,
           command=lambda: exit()).pack()


def authorize_credentials(username, password):
    if username.get() == "" or password.get() == "":
        Label(frames["log_in"], text='Credentials have to be filled',
              width=40, height=1).pack()
        return
    new_user = db.search_by_value("database", "users", "username",
                                  username.get())
    hashed_password = hashlib.sha256(password.get().encode()).hexdigest()
    if new_user != [] and new_user[0]["password"] == hashed_password:
        global user
        user = new_user
        hide_all_frames("main_menu")
    else:
        Label(frames["log_in"], text='User already exists', width=20,
              height=2,
              font=big_font).pack()


def register_user(username, password):
    if username.get() == "" or password.get() == "":
        Label(frames["register"], text='Credentials have to be filled',
              width=10, height=1,
              font=big_font).pack()
        return
    new_user = db.search_by_value("database", "users", "username",
                                  username.get())
    hashed_password = hashlib.sha256(password.get().encode()).hexdigest()
    if new_user:
        Label(frames["register"], text='This username is already taken',
              width=10, height=1,
              font=big_font).pack()
        return
    try:
        db.insert("database", "users",
                  [{"role": "Visitor", "username": username.get(),
                    "password": hashed_password,
                    "tickets": []}])
        global user
        user = new_user
        hide_all_frames("main_menu")
    except harperdb.exceptions.HarperDBError:
        Label(frames["register"], text='User already exists', width=10,
              height=1,
              font=big_font).pack()
