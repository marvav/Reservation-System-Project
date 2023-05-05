from DB_Methods import *

"""
This file contains functions generating all frames of the application.
Each function generates its frame upon entering to ensure synchronization 
of data with database.
"""

# Dictionary of all frames in the application to ensure quick access
frames = {"log_in": None, "register": None, "main_menu": None,
          "your_tickets": None, "show_tickets": None, "profile": None,
          "tours": None, "admin_menu": None, "modify_tour_type": None,
          "add_tour_type": None, "change_rules": None, "purchase": None,
          "ticket": None, "coordinator_menu": None, "set_schedule": None,
          "enter_refund": None}

# Type aliases for better readability
Tour = Dict[str, str]
Ticket = Dict[str, str]
Entries = Dict[Entry, str]
User = Dict[str, str]

user = None
tours = dict()
schedules = dict()
tour_types = dict()


# Initial admin menu providing options to add / modify tour,
# set global rules and log off
def admin_menu() -> None:
    print(tour_types)
    frame = hide_all_frames("admin_menu")
    Label(frame, text='Admin Menu', font=big_font, width=20, height=2).pack()
    NavButton(frame, 'Add new tour', lambda: add_tour_type())
    tour_name = ttk.Combobox(frame, values=get_tours_params("Name"), width=20,
                             justify='center')
    tour_name.current(0)
    tour_name.pack()
    NavButton(frame, 'Modify tour', lambda: modify_tour_type(tour_name.get()))
    NavButton(frame, 'Set Rules', lambda: change_rules())
    NavButton(frame, 'Log Off', lambda: log_in())


# Displays layout of entries to configure new tour type
def add_tour_type() -> None:
    frame = hide_all_frames("add_tour_type")
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

    NavButtonGrid(frame, 'Go Back', lambda: admin_menu(), row=8, column=0)
    NavButtonGrid(frame, 'Confirm', lambda: insert_tour_type(frame, tour),
                  row=8, column=1)


# Creates layout of entries with prefilled tour
# information from database to modify it.
def modify_tour_type(tour_name: str) -> None:
    frame = hide_all_frames("modify_tour_type")
    tour = get_tours_with_param("Name", tour_name)
    if not tour:
        return add_tour_type()
    tour = tour[0]

    new_tour = dict()

    Label(frame, text='Name:', font=small_font).grid(row=0, column=0)
    new_tour["Name"] = Entry(frame)
    new_tour["Name"].insert(END, tour["Name"])
    new_tour["Name"].grid(row=0, column=1)

    Label(frame, text='Location:', font=small_font, fg="white",
          bg="blue").grid(row=1, column=0)
    new_tour["Location"] = Entry(frame)
    new_tour["Location"].insert(END, tour["Location"])
    new_tour["Location"].grid(row=1, column=1)

    Label(frame, text='Capacity:', font=small_font).grid(row=2, column=0)
    new_tour["Capacity"] = Entry(frame)
    new_tour["Capacity"].insert(END, tour["Capacity"])
    new_tour["Capacity"].grid(row=2, column=1)

    Label(frame, text='Duration:', font=small_font).grid(row=3, column=0)
    new_tour["Duration"] = Entry(frame)
    new_tour["Duration"].insert(END, tour["Duration"])
    new_tour["Duration"].grid(row=3, column=1)

    Label(frame, text='Description:', font=small_font).grid(row=4, column=1)
    new_tour["Description"] = Text(frame, width=20, height=10)
    new_tour["Description"].insert(END, tour["Description"])
    new_tour["Description"].grid(row=5, column=1)

    Label(frame, text='Ticket Price:', font=small_font).grid(row=6, column=0)
    new_tour["TicketPrice"] = Entry(frame)
    new_tour["TicketPrice"].insert(END, tour["TicketPrice"])
    new_tour["TicketPrice"].grid(row=6, column=1)

    Label(frame, text='Discount Price:', font=small_font).grid(row=7, column=0)
    new_tour["DiscountPrice"] = Entry(frame)
    new_tour["DiscountPrice"].insert(END, tour["DiscountPrice"])
    new_tour["DiscountPrice"].grid(row=7, column=1)

    NavButtonGrid(frame, 'Go Back', lambda: admin_menu(), row=9, column=0)
    NavButtonGrid(frame, 'Confirm', lambda: update_tour_type(frame, new_tour),
                  row=9, column=1)
    NavButtonGrid(frame, 'Delete tour', lambda: delete_tour(tour),
                  row=8, column=0)


# Creates the layout for coordinator menu.
# Provides option to set schedule at chosen location or set tour date
def coordinator_menu() -> None:
    frame = hide_all_frames("coordinator_menu")
    Label(frame, text='Coordinator Menu', font=big_font, width=20,
          height=2).pack()
    Label(frame, text='Choose Location:', width=20, height=2).pack()
    tours = ttk.Combobox(frame, values=get_tours_params("Name"),
                         width=20, justify='center')
    tours.current(0)
    tours.pack()
    NavButton(frame, 'Set Schedule', lambda: set_schedule(tours.get()))
    NavButton(frame, 'Set Tour Date', lambda: change_rules())
    NavButton(frame, 'Log Off', lambda: log_in())


# Creates the layout of entries to modify tour schedule times
def set_schedule(name: str) -> None:
    frame = hide_all_frames("set_schedule")
    tour = tours[name]
    schedule = tour["schedule"]
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

    NavButtonGrid(frame, 'Go back', lambda: coordinator_menu(), row=14,
                  column=0)
    NavButtonGrid(frame, 'Confirm',
                  lambda: update_schedule(hours, minutes, tour),
                  row=14, column=1)


# Creates layout with entry to change global tour rules
def change_rules() -> None:
    frame = hide_all_frames("change_rules")
    BigLabel(frame, text='General Tour Rules').pack()
    new_rules = Text(frame, width=30, height=15)
    current_rules = db.search_by_value("database", "general_data",
                                       "name", "general_rules")[0]["data"]
    new_rules.insert(END, current_rules)
    new_rules.pack()
    NavButton(frame, 'Confirm',
              lambda: update_rules(new_rules.get("1.0", END)))
    NavButton(frame, 'Go Back', lambda: admin_menu())


# Displays user account information and provides log off option
def profile() -> None:
    frame = hide_all_frames("profile")
    MediumLabel(frame, text='Your Profile').pack()
    SmallLabel(frame, text='Username: ' + user["username"]).pack()
    spacer = Label(frame, height=1, highlightthickness=0, borderwidth=0)
    spacer.pack()

    NavButton(frame, 'Log off', lambda: log_in())


# Creates button for tour ticket purchase
def tour_button(date: str, time: str, tour: Tour, name: str) -> None:
    if date == get_date() and time < get_time():
        return
    label = tour["Name"] + " | " + time + " | " + tour[
        "Duration"] + " minutes | "
    if (date + time) in tours[name]["dates"]:
        label += "Capacity: " + str(
            tours[name]["dates"][date + time])
    else:
        label += "Capacity: " + tour["Capacity"]
    SmallButton(frames["tours"], label,
                lambda: purchase_ticket(date, time, tour))


# Displays available tour times at the specific location
def load_tours(date: str, name: str) -> None:
    frame = hide_all_frames("tours")
    Label(frame, text='Upcoming Tours').pack()
    schedule = tours[name]["schedule"]
    if date >= get_date():
        for tour in get_tours_with_param("Name", name):
            for time in schedule:
                tour_button(date, time, tour, name)
    NavButton(frame, 'Go back', lambda: main_menu())


# Displays tour information and entries for user to initiate the purchase
def purchase_ticket(date: str, time: str, tour: Tour, tickets_count: str = 0,
                    discount_count: str = 0, price: int = 0) -> None:
    ticket = tour_to_ticket(tour, time, date)
    frame = hide_all_frames("purchase")

    listbox = Listbox(frame)
    for key in tour_order:
        listbox.insert(END, key + ": " + ticket[key])
    listbox.pack()

    Label(frame, text='Ticket number', font=small_font).pack()

    tickets = Entry(frame)
    tickets.pack()
    tickets.insert(END, tickets_count)
    Label(frame, text='Discount Tickets number', font=small_font).pack()
    discount = Entry(frame)
    discount.pack()
    discount.insert(END, discount_count)

    price = Label(frames["purchase"], text="Price: " + str(price) + " CZK")
    price.pack()

    SmallButton(frame, "Calculate price",
                lambda: purchase_ticket(date, time, tour, tickets.get(),
                                        discount.get(),
                                        calculate_price(tickets, discount,
                                                        tour)))
    NavButton(frame, 'Purchase',
              lambda: purchase(frame, ticket, tickets, discount))
    NavButton(frame, 'Go Back', lambda: load_tours(date, ticket["Name"]))


# Displays tickets purchased by the user.
# Provides option to display either expired or valid tickets
def show_tickets(expired: bool) -> None:
    frame = hide_all_frames("show_tickets")
    scrollbar = ttk.Scrollbar(frame, orient=VERTICAL)
    listbox = Listbox(frame, yscrollcommand=scrollbar.set, justify='center')
    scrollbar.config(command=listbox.yview)
    if expired:
        ShowExpiredTickets(frame, listbox)
    else:
        ShowValidTickets(frame, listbox)
    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(fill=BOTH, expand=1)
    NavButton(frame, 'Go back', lambda: main_menu())


# Displays choice to show valid or expired tickets
def show_your_tickets() -> None:
    frame = hide_all_frames("your_tickets")
    NavButton(frame, 'Valid tickets', lambda: show_tickets(False))
    NavButton(frame, 'Expired tickets', lambda: show_tickets(True))
    NavButton(frame, 'Refunds', lambda: enter_refund())
    NavButton(frame, 'Go back', lambda: main_menu())


def enter_refund():
    frame = hide_all_frames("enter_refund")
    MediumLabel(frame, "Enter ticket code").pack()
    code = Entry(frame)
    code.pack()
    NavButton(frame, 'Confirm', lambda: process_refund(frame, code.get()))
    NavButton(frame, 'Go back', lambda: show_your_tickets())


# Visitor menu providing access to purchasing new tickets.
# Acces to purchased tickets and to user profile
def main_menu() -> None:
    frame = hide_all_frames("main_menu")
    SmallLabel(frame, "Main Menu").pack()
    date = tkcalendar.DateEntry(frame, date_pattern='dd/mm/yyyy',
                                justify='center')
    date.pack()
    combo = ttk.Combobox(frame, values=get_tours_params("Name"),
                         width=20, justify='center')
    combo.current(0)
    combo.pack()
    NavButton(frame, 'Upcoming Tours',
              lambda: load_tours(date.get(), combo.get()))
    NavButton(frame, 'Your Tickets', lambda: show_your_tickets())
    NavButton(frame, 'Profile', lambda: profile())


# Displays layout for new credentials and allows user to create his account
def register() -> None:
    frame = hide_all_frames("register")

    Label(frames["register"], text='Enter username').pack()
    username = Entry(frame)
    username.pack()

    Label(frame, text='Enter password').pack()
    password = Entry(frame, show='*')
    password.pack()

    NavButton(frame, 'Create Account',
              lambda: register_user(username.get(), password.get()))
    NavButton(frame, 'Go Back', lambda: log_in())
    NavButton(frame, 'EXIT', lambda: exit())


# Provides user with entries for his credentials so he can authorize himself,
# or redirect himself to registration
def log_in() -> None:
    frame = hide_all_frames("log_in")

    Label(frame, text='Enter username').pack()
    username = Entry(frame)
    username.pack()

    Label(frame, text='Enter password').pack()
    password = Entry(frame, show='*')
    password.pack()

    NavButton(frame, 'Log In',
              lambda: authorize_log_in(username.get(), password.get()))
    NavButton(frame, 'Register', lambda: register())
    NavButton(frame, 'EXIT', lambda: exit())


# This function is called upon entering each frame. It hides all other frames
# and deletes past contents of the frame to ensure all the data are valid
def hide_all_frames(new_frame: str) -> Frame:
    for widget in frames[new_frame].winfo_children():
        widget.destroy()
    for frame in frames.values():
        frame.place_forget()
    frames[new_frame].pack(fill=BOTH, expand=True)
    frames[new_frame].place(relx=0.5, rely=0.5, anchor=CENTER)
    return frames[new_frame]


# Assigns the successfully logged in user and
# redirects him to the menu corresponding to his role
def assign_user(new_user: User) -> None:
    Frames.user = new_user
    if user["role"] == "Coordinator":
        return coordinator_menu()
    elif user["role"] == "Admin":
        return admin_menu()
    return main_menu()
