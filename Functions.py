from tkinter import *
from tkinter import font, ttk
import hashlib
import harperdb
import tkcalendar as tkcalendar

from db_methods import *
from Predicate_functions import *
from datetime import datetime

db = harperdb.HarperDB(url="https://pb175-marvav.harperdbcloud.com",
                       username="marvav", password="muniprojekt123")

frames = {"log_in": None, "register": None, "main_menu": None,
          "your_tickets": None, "profile": None, "tours": None,
          "admin_menu": None, "admin_tours": None, "add_tour_type": None,
          "change_rules": None, "purchase": None, "ticket": None,
          "coordinator_menu": None, "set_schedule": None}

tour_order = ["Name", "Location", "Date", "Time", "Duration", "Description"]
ticket_order = ["Name", "Location", "Date", "Time", "Duration",
                "Description", "TicketsNumber", "DiscountNumber"]

user = None
big_font = None
small_font = None
errorLabel = None
upcoming_tours = db.sql("SELECT * FROM `database`.`tour_types`")
locations = get_locations()
schedules = get_schedules()


def init_add_tour_type():
    frame = frames["add_tour_type"]
    tour = dict()
    Label(frame, text='Name:', font=small_font).grid(row=0, column=0)
    tour["Name"] = Entry(frame)
    tour["Name"].grid(row=0, column=1)

    Label(frame, text='Location:', font=small_font, fg="white",
          bg="blue").grid(row=1, column=0)
    tour["Location"] = Entry(frame)
    tour["Location"].grid(row=1, column=1)

    Label(frame, text='Capacity:', font=small_font).grid(row=2, column=0)
    tour["Capacity"] = Entry(frame)
    tour["Capacity"].grid(row=2, column=1)

    Label(frame, text='Duration:', font=small_font).grid(row=3, column=0)
    tour["Duration"] = Entry(frame)
    tour["Duration"].grid(row=3, column=1)

    Label(frame, text='Description:', font=small_font).grid(row=4, column=1)
    tour["Description"] = Text(frame, width=20, height=10)
    tour["Description"].grid(row=5, column=1)

    Label(frame, text='Ticket Price:', font=small_font).grid(row=6, column=0)
    tour["TicketPrice"] = Entry(frame)
    tour["TicketPrice"].grid(row=6, column=1)

    Label(frame, text='Discount Price:', font=small_font).grid(row=7, column=0)
    tour["DiscountPrice"] = Entry(frame)
    tour["DiscountPrice"].grid(row=7, column=1)

    tour["TourRules"] = ""

    NavButtonGrid(frame, 'Go Back', lambda: hide_all_frames("admin_menu"),
                  row=8,
                  column=0)
    NavButtonGrid(frame, 'Confirm', lambda: insert_tour_type(tour), row=8,
                  column=1)


def init_coordinator_menu():
    frame = frames["coordinator_menu"]
    Label(frame, text='Coordinator Menu', font=big_font, width=20,
          height=2).pack()
    Label(frame, text='Choose Location:', width=20, height=2).pack()
    location = ttk.Combobox(frame, values=locations, width=20,
                            justify='center')
    location.current(0)
    location.pack()
    NavButton(frame, 'Set Schedule', lambda: set_schedule(location.get()))
    NavButton(frame, 'Set Tour Date', lambda: hide_all_frames("change_rules"))
    NavButton(frame, 'Log Off', lambda: hide_all_frames("log_in"))


def set_schedule(location):
    frame = hide_all_frames("set_schedule")
    daily = db.search_by_value("database", "DailyTours", "Name", location)[0]
    schedule = daily["schedule"]
    Label(frame, text='Hours', font=small_font, width=10, height=2).grid(
        row=2, column=0)
    Label(frame, text='Minutes', font=small_font, width=10, height=2).grid(
        row=2, column=1)
    hours, minutes = [], []
    for index in range(10):
        hours.append(Entry(frame, justify='center', validate='key'))
        hours[-1].grid(row=3 + index, column=0)
        minutes.append(Entry(frame, justify='center', validate='key'))
        minutes[-1].grid(row=3 + index, column=1)
        if index < len(schedule):
            hours[-1].insert(0, schedule[index].split(":")[0])
            minutes[-1].insert(0, schedule[index].split(":")[1])

    NavButtonGrid(frame, 'Go back',
                  lambda: hide_all_frames("coordinator_menu"),
                  row=14, column=0)
    NavButtonGrid(frame, 'Confirm',
                  lambda: update_schedule(hours, minutes, daily),
                  row=14, column=1)


def insert_tour_type(tour):
    if not is_valid_tour(tour):
        global errorLabel
        if errorLabel is not None:
            errorLabel.destroy()
        errorLabel = Label(frames["add_tour_type"], text="Invalid tour",
                           width=25, height=1, font=small_font)
        return errorLabel.grid(row=10, column=0)

    db.insert("database", "tour_types",
              [{"Name": tour["Name"].get(), "Location": tour["Location"].get(),
                "Duration": tour["Duration"].get(),
                "Capacity": tour["Capacity"].get(),
                "Description": tour["Description"].get("1.0", END),
                "TicketPrice": tour["TicketPrice"].get(),
                "DiscountPrice": tour["DiscountPrice"].get(),
                "TourRules": tour["TourRules"]}])
    db.insert("database", "DailyTours",
              [{"Name": "Ostrov u Macochy", "schedule": []}])

    return hide_all_frames("admin_menu")


def init_change_rules():
    frame = frames["change_rules"]
    Label(frame, text='General Tour Rules', font=big_font, width=20,
          height=2).pack()
    new_rules = Text(frame, width=30, height=15)
    current_rules = db.search_by_value("database", "general_data",
                                       "name", "general_rules")[0]["data"]
    new_rules.insert(END, current_rules)
    new_rules.pack()
    NavButton(frame, 'Confirm',
              lambda: change_rules(new_rules.get("1.0", END)))
    NavButton(frame, 'Go Back', lambda: hide_all_frames("admin_menu"))


def init_admin_menu():
    frame = frames["admin_menu"]
    Label(frame, text='Admin Menu', font=big_font, width=20, height=2).pack()
    NavButton(frame, 'Manage Tours', lambda: hide_all_frames("admin_tours"))
    NavButton(frame, 'Set Rules', lambda: hide_all_frames("change_rules"))
    NavButton(frame, 'Log Off', lambda: hide_all_frames("log_in"))


def init_admin_tours():
    frame = frames["admin_tours"]
    Label(frame, text='Tour Menu', font=big_font, width=20, height=2).pack()
    NavButton(frame, 'Add tour', lambda: hide_all_frames("add_tour_type"))
    NavButton(frame, 'Go back', lambda: hide_all_frames("admin_menu"))


def init_profile():
    frame = frames["profile"]
    Label(frame, text='Your Profile').pack()
    NavButton(frame, 'Log off', lambda: hide_all_frames("log_in"))


def load_tours(date, location):
    frame = hide_all_frames("tours")
    schedule = schedules[location]
    Label(frame, text='Upcoming Tours').pack()
    for tour in upcoming_tours:
        if tour["Location"] != location:
            continue
        for time in schedule:
            label = tour["Name"] + " | " + time + " | " + tour[
                "Duration"] + " minutes | "
            SmallButton(frames["tours"], label,
                        lambda: purchase_ticket(date, time, tour))
    NavButton(frame, 'Go back', lambda: hide_all_frames("main_menu", frame))


def purchase_ticket(date, time, tour, price=0):
    ticket = {"Name": tour["Name"], "Location": tour["Location"], "Date": date,
              "Time": time, "Duration": tour["Duration"],
              "Description": tour["Description"]}
    frame = hide_all_frames("purchase")

    listbox = Listbox(frame)
    for key in ticket_order:
        if key in tour:
            listbox.insert(END, key + ": " + tour[key])
    listbox.pack()

    Label(frame, text='Ticket number', font=small_font).pack()

    tickets = Entry(frame)
    tickets.pack()
    Label(frame, text='Discount Tickets number', font=small_font).pack()
    discount = Entry(frame)
    discount.pack()

    price = Label(frames[("purchase")], text="Price: 0 CZK")
    price.pack()

    SmallButton(frame, "Calculate price",
                lambda: price.config(text="Price: " + str(
                    calculate_price(tickets, discount, tour)) + " CZK"))
    NavButton(frame, 'Purchase', lambda: purchase(ticket, tickets, discount))
    NavButton(frame, 'Go Back', lambda: hide_all_frames("tours", frame))


def calculate_price(tickets, discount, tour):
    return int(tickets.get()) * int(tour["DiscountPrice"]) + \
           int(discount.get()) * int(tour["TicketPrice"])


def purchase(ticket, tickets, discount):
    try:
        if tickets.get()!="" and int(tickets.get()) < 0:
            return ErrorLabel(frames["tours"], "Invalid ticket count")
        if discount.get()!="" and int(discount.get()) < 0:
            return ErrorLabel(frames["tours"], "Invalid discount count")
        if tickets.get()!="" and discount.get()!="" \
                and int(tickets.get()) + int(discount.get()) == 0:
            return ErrorLabel(frames["tours"], "No tickets selected")
    except:
        return ErrorLabel(frames["tours"], "Please enter number")

    ticket["TicketsNumber"] = str(tickets.get())
    ticket["DiscountNumber"] = str(discount.get())
    user["tickets"].append(ticket)
    db.update("database", "users", [user])


def show_your_tickets():
    frame = hide_all_frames("your_tickets")
    tickets = user["tickets"]
    Label(frame, text='Your Tickets').pack()

    scrollbar = ttk.Scrollbar(frames["your_tickets"], orient=VERTICAL)
    listbox = Listbox(frames["your_tickets"], yscrollcommand=scrollbar.set)
    scrollbar.config(command=listbox.yview)

    for ticket in tickets:
        for key in ticket_order:
            listbox.insert(END, key + ": " + ticket[key])

    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(fill=BOTH, expand=1)
    NavButton(frame, 'Go back', lambda: hide_all_frames("main_menu", frame))


def init_main_menu():
    frame = frames["main_menu"]
    Label(frame, text='Main Menu', font=big_font, width=20, height=2).pack()
    date = tkcalendar.DateEntry(frame, date_pattern='dd/mm/yyyy',
                                justify='center')
    date.pack()
    combo = ttk.Combobox(frame, values=locations, width=20, justify='center')
    combo.current(0)
    combo.pack()
    NavButton(frame, 'Upcoming Tours',
              lambda: load_tours(date.get(), combo.get()))
    NavButton(frame, 'Your Tickets', lambda: show_your_tickets())
    NavButton(frame, 'Profile', lambda: hide_all_frames("profile"))


def init_register():
    frame = frames["register"]

    Label(frames["register"], text='Enter username').pack()
    username = Entry(frame)
    username.pack()

    Label(frame, text='Enter password').pack()
    password = Entry(frame)
    password.pack()

    NavButton(frame, 'Create Account',
              lambda: register_user(username.get(), password.get()))
    NavButton(frame, 'Go Back', lambda: hide_all_frames("log_in"))
    NavButton(frame, 'EXIT', lambda: exit())


def init_log_in() -> None:
    frame = frames["log_in"]

    Label(frame, text='Enter username').pack()
    username = Entry(frame)
    username.pack()

    Label(frame, text='Enter password').pack()
    password = Entry(frame)
    password.pack()

    NavButton(frame, 'Log In',
              lambda: authorize_credentials(username.get(), password.get()))
    NavButton(frame, 'Register', lambda: hide_all_frames("register"))
    NavButton(frame, 'EXIT', lambda: exit())


def authorize_credentials(username, password):
    if username == "" or password == "":
        return ErrorLabel(frames["log_in"], 'Credentials have to be filled')

    new_user = db.search_by_value("database", "users", "username", username)
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if new_user[0]["password"] != hashed_password:
        return ErrorLabel(frames["log_in"], 'Wrong password')

    if new_user:
        global user
        user = new_user[0]
        if user["role"] == "Visitor":
            return hide_all_frames("main_menu")
        if user["role"] == "Coordinator":
            return hide_all_frames("coordinator_menu")
        elif user["role"] == "Admin":
            return hide_all_frames("admin_menu")


def register_user(username, password):
    global user

    if username == "" or password == "":
        return ErrorLabel(frames["register"], 'Credentials have to be filled')

    if db.search_by_value("database", "users", "username", username):
        return ErrorLabel(frames["register"], 'This username is already taken')

    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        db.insert("database", "users",
                  [{"role": "Visitor", "username": username,
                    "password": hashed_password, "tickets": []}])
        user = db.search_by_value("database", "users", "username", username)
        hide_all_frames("main_menu")

    except harperdb.exceptions.HarperDBError:
        ErrorLabel(frames["register"], 'Error is on our side. Try again')


def ErrorLabel(frame, text):
    global errorLabel
    if errorLabel is not None:
        errorLabel.destroy()
    errorLabel = Label(frame, text=text, width=25, height=1, font=small_font)
    errorLabel.pack()


def SmallButton(frame, text, command):
    Button(frame, text=text, font=small_font, width=40, height=1,
           activebackground="blue", command=command).pack()


def NavButton(frame, text, command):
    Button(frame, text=text, font=big_font, width=20, height=2,
           activebackground="#cdfffc", command=command).pack()


def NavButtonGrid(frame, text, command, row, column):
    Button(frame, text=text, height=2, width=14, activebackground="blue",
           font=small_font, command=command).grid(row=row, column=column)


def hide_all_frames(new_frame, reset_frame=None):
    if reset_frame:
        for widget in reset_frame.winfo_children():
            widget.destroy()
    for frame in frames.values():
        frame.place_forget()
    frames[new_frame].pack(fill=BOTH, expand=True)
    frames[new_frame].place(relx=0.5, rely=0.5, anchor=CENTER)
    return frames[new_frame]
