from DB_Methods import *

frames = {"log_in": None, "register": None, "main_menu": None,
          "your_tickets": None, "profile": None, "tours": None,
          "admin_menu": None, "modify_tour_type": None, "add_tour_type": None,
          "change_rules": None, "purchase": None, "ticket": None,
          "coordinator_menu": None, "set_schedule": None}

tour_order = ["Name", "Location", "Date", "Time", "Duration", "Description"]
ticket_order = ["Name", "Location", "Date", "Time", "Duration",
                "Description", "TicketsNumber", "DiscountNumber"]

user = None


def init_admin_menu() -> None:
    frame = frames["admin_menu"]
    Label(frame, text='Admin Menu', font=big_font, width=20, height=2).pack()
    NavButton(frame, 'Add new tour', lambda: hide_all_frames("add_tour_type"))
    tour = ttk.Combobox(frame, values=tour_types("Name"), width=20,
                        justify='center')
    tour.current(0)
    tour.pack()
    NavButton(frame, 'Modify tour', lambda: modify_tour_type(tour.get()))
    NavButton(frame, 'Set Rules', lambda: hide_all_frames("change_rules"))
    NavButton(frame, 'Log Off', lambda: hide_all_frames("log_in"))


def init_add_tour_type() -> None:
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

    NavButtonGrid(frame, 'Go Back',
                  lambda: hide_all_frames("admin_menu", frame),
                  row=8, column=0)
    NavButtonGrid(frame, 'Confirm', lambda: insert_tour_type(frame, tour),
                  row=8, column=1)


def modify_tour_type(tour):
    frame = hide_all_frames("modify_tour_type")
    tour = db.search_by_value("database", "tour_types", "Name", tour)
    if not tour:
        return hide_all_frames("add_tour_type")
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

    new_tour["TourRules"] = ""

    NavButtonGrid(frame, 'Go Back', lambda: hide_all_frames("admin_menu"),
                  row=9, column=0)
    NavButtonGrid(frame, 'Confirm', lambda: insert_tour_type(frame, new_tour),
                  row=9, column=1)
    NavButtonGrid(frame, 'Delete tour', lambda: delete_tour(frame, tour),
                  row=8, column=0)


# Creates the layout for coordinator menu
def init_coordinator_menu():
    frame = frames["coordinator_menu"]
    Label(frame, text='Coordinator Menu', font=big_font, width=20,
          height=2).pack()
    Label(frame, text='Choose Location:', width=20, height=2).pack()
    location = ttk.Combobox(frame, values=tour_types("Location"), width=20,
                            justify='center')
    location.current(0)
    location.pack()
    NavButton(frame, 'Set Schedule', lambda: set_schedule(location.get()))
    NavButton(frame, 'Set Tour Date', lambda: change_rules())
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


def change_rules():
    frame = hide_all_frames("change_rules")
    Label(frame, text='General Tour Rules', font=big_font, width=20,
          height=2).pack()
    new_rules = Text(frame, width=30, height=15)
    current_rules = db.search_by_value("database", "general_data",
                                       "name", "general_rules")[0]["data"]
    new_rules.insert(END, current_rules)
    new_rules.pack()
    NavButton(frame, 'Confirm',
              lambda: update_rules(new_rules.get("1.0", END)))
    NavButton(frame, 'Go Back', lambda: hide_all_frames("admin_menu"))


def init_profile():
    frame = frames["profile"]
    Label(frame, text='Your Profile').pack()
    NavButton(frame, 'Log off', lambda: hide_all_frames("log_in", frame))


def load_tours(date, location):
    frame = hide_all_frames("tours")
    schedule = get_schedules()[location]
    Label(frame, text='Upcoming Tours').pack()

    if date >= get_date():
        for tour in get_tours_at_location(location):
            for time in schedule:
                if date == get_date() and time < get_time():
                    continue
                label = tour["Name"] + " | " + time + " | " + tour[
                    "Duration"] + " minutes | "
                SmallButton(frames["tours"], label,
                            lambda: purchase_ticket(date, time, tour))
    NavButton(frame, 'Go back', lambda: hide_all_frames("main_menu", frame))


def purchase_ticket(date: str, time: str, tour: Tour, price: int = 0) -> None:
    ticket = {"Name": tour["Name"], "Location": tour["Location"], "Date": date,
              "Time": time, "Duration": tour["Duration"],
              "Description": tour["Description"]}
    frame = hide_all_frames("purchase")

    listbox = Listbox(frame)
    for key in tour_order:
        listbox.insert(END, key + ": " + ticket[key])
    listbox.pack()

    Label(frame, text='Ticket number', font=small_font).pack()

    tickets = Entry(frame)
    tickets.pack()
    Label(frame, text='Discount Tickets number', font=small_font).pack()
    discount = Entry(frame)
    discount.pack()

    price = Label(frames["purchase"], text="Price: 0 CZK")
    price.pack()

    SmallButton(frame, "Calculate price",
                lambda: price.config(text="Price: " + str(
                    calculate_price(tickets, discount, tour)) + " CZK"))
    NavButton(frame, 'Purchase',
              lambda: purchase(frame, ticket, tickets, discount))
    NavButton(frame, 'Go Back', lambda: hide_all_frames("tours", frame))


def show_your_tickets() -> None:
    frame = hide_all_frames("your_tickets")
    tickets = user["tickets"]

    scrollbar = ttk.Scrollbar(frames["your_tickets"], orient=VERTICAL)
    listbox = Listbox(frames["your_tickets"], yscrollcommand=scrollbar.set)
    listbox.insert(END, "Valid Tickets\n")
    listbox.insert(END, "\n")
    scrollbar.config(command=listbox.yview)

    for ticket in tickets:
        if is_expired(ticket["Date"], ticket["Time"]):
            continue
        for key in ticket_order:
            listbox.insert(END, key + ": " + ticket[key])
        listbox.insert(END, "\n")

    listbox.insert(END, "Expired Tickets")
    listbox.insert(END, "\n")

    for ticket in tickets:
        if not is_expired(ticket["Date"], ticket["Time"]):
            continue
        for key in ticket_order:
            listbox.insert(END, key + ": " + ticket[key])
        listbox.insert(END, "\n")

    scrollbar.pack(side=RIGHT, fill=Y)
    listbox.pack(fill=BOTH, expand=1)
    NavButton(frame, 'Go back', lambda: hide_all_frames("main_menu", frame))


def init_main_menu() -> None:
    frame = frames["main_menu"]
    Label(frame, text='Main Menu', font=big_font, width=20, height=2).pack()
    date = tkcalendar.DateEntry(frame, date_pattern='dd/mm/yyyy',
                                justify='center')
    date.pack()
    combo = ttk.Combobox(frame, values=tour_types("Location"),
                         width=20, justify='center')
    combo.current(0)
    combo.pack()
    NavButton(frame, 'Upcoming Tours',
              lambda: load_tours(date.get(), combo.get()))
    NavButton(frame, 'Your Tickets', lambda: show_your_tickets())
    NavButton(frame, 'Profile', lambda: hide_all_frames("profile"))


def init_register() -> None:
    frame = frames["register"]

    Label(frames["register"], text='Enter username').pack()
    username = Entry(frame)
    username.pack()

    Label(frame, text='Enter password').pack()
    password = Entry(frame, show='*')
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
    password = Entry(frame, show='*')
    password.pack()

    NavButton(frame, 'Log In',
              lambda: authorize_log_in(username.get(), password.get()))
    NavButton(frame, 'Register', lambda: hide_all_frames("register"))
    NavButton(frame, 'EXIT', lambda: exit())


def hide_all_frames(new_frame: str,
                    reset_frame: Optional[Frame] = None) -> Frame:
    if reset_frame:
        for widget in reset_frame.winfo_children():
            widget.destroy()
    for frame in frames.values():
        frame.place_forget()
    frames[new_frame].pack(fill=BOTH, expand=True)
    frames[new_frame].place(relx=0.5, rely=0.5, anchor=CENTER)
    return frames[new_frame]


def init_ui(new_user: User) -> Frame:
    Frames.user = new_user
    if user["role"] == "Coordinator":
        init_coordinator_menu()
        return hide_all_frames("coordinator_menu")
    elif user["role"] == "Admin":
        init_admin_menu()
        init_add_tour_type()
        return hide_all_frames("admin_menu")

    init_main_menu()
    init_profile()
    return hide_all_frames("main_menu")
