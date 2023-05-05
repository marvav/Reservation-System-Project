from Widgets import *

"""
This file contains all methods communicating with the online harperdb database
"""

# Instance of the database for unified communication
db = harperdb.HarperDB(url="https://pb175-marvav.harperdbcloud.com",
                       username="marvav", password="muniprojekt123")


# Propagates changes in schedule made by Coordinator into database
def update_schedule(hours: List[Entry], minutes: List[Entry],
                    tour: TourRecord) -> None:
    new_schedule = []
    for i in range(len(hours)):
        if hours[i].get() != "":
            if minutes[i].get() == "":
                new_schedule.append(hours[i].get() + ":00")
            else:
                new_schedule.append(hours[i].get() + ":" + minutes[i].get())
    tour["schedule"] = new_schedule
    db.update("database", "tours", [tour])
    return Frames.coordinator_menu()


# Overwrite rules in database with new ones by Admin
def update_rules(new_rules: str) -> None:
    db.update("database", "general_data", [{"name": "general_rules",
                                            "data": new_rules}])
    return Frames.admin_menu()


# Pulls tour records from database
def get_tours() -> Dict[str, TourRecord]:
    tours = dict()
    for record in db.sql("SELECT * FROM `database`.`tours`"):
        tours[record["Name"]] = record
    return tours


# Pulls all tour types and tour information from database
def get_tour_types() -> List[Tour]:
    return db.sql("SELECT * FROM `database`.`tour_types`")


# Deletes tour from database and updates local copy
def delete_tour(tour: Tour) -> None:
    db.delete("database", "tour_types", [tour["Name"]])
    db.delete("database", "tours", [tour["Name"]])
    Frames.tours = get_tours()
    Frames.tour_types = get_tour_types()
    return Frames.admin_menu()


# Assigns ticket to the users account and updates available capacity
def purchase(frame: Frame, ticket: Ticket, tickets: Entry,
             discount: Entry) -> None:
    if not is_purchase_valid(frame, tickets, discount):
        return

    ticket_count = 0
    if tickets.get() != "":
        ticket_count += int(tickets.get())
    if discount.get() != "":
        ticket_count += int(discount.get())

    tour = db.search_by_value("database", "tours", "Name", ticket["Name"])[0]
    dates = tour["dates"]
    if (ticket["Date"] + ticket["Time"]) in dates:
        new_capacity = dates[ticket["Date"] + ticket["Time"]] - ticket_count
        if new_capacity < 0:
            return ErrorLabel(frame, "The capacity is insufficient")
        dates[ticket["Date"] + ticket["Time"]] = new_capacity
    else:
        dates[ticket["Date"] + ticket["Time"]] = int(
            ticket["Capacity"]) - ticket_count

    db.update("database", "tours", [tour])

    code = (str(time.time()) + Frames.user["username"]).encode()
    ticket["Code"] = hashlib.sha256(code).hexdigest()[0:12]
    ticket["TicketsNumber"] = str(tickets.get())
    ticket["DiscountNumber"] = str(discount.get())
    Frames.user["tickets"].append(ticket)

    Frames.tours = get_tours()
    db.update("database", "users", [Frames.user])

    Frames.main_menu()


# Deletes ticket from users account and restores the freed capacity.
def process_refund(frame: Frame, ticket_code: str) -> None:
    for index, ticket in enumerate(Frames.user["tickets"]):
        if ticket["Code"] == ticket_code:
            count = 0
            if ticket["TicketsNumber"] != "":
                count += int(ticket["TicketsNumber"])
            if ticket["DiscountNumber"] != "":
                count += int(ticket["DiscountNumber"])
            tour = Frames.tours[ticket["Name"]]
            tour["dates"][ticket["Date"] + ticket["Time"]] += count
            db.update("database", "tours", [tour])

            del Frames.user["tickets"][index]
            db.update("database", "users", [Frames.user])
            return Frames.show_your_tickets()
    ErrorLabel(frame, "This code is not valid")


# Inserts new tour type onto the database and updates local values
def insert_tour_type(frame: Frame, entries: Dict[str, Entry]) -> None:
    tour = get_tour(entries)
    if not is_valid_tour(tour):
        return ErrorLabelGrid(frame, "Invalid tour", 10, 1)

    db.insert("database", "tour_types", [tour])
    db.insert("database", "tours",
              [{"Name": tour["Name"], "schedule": [], "dates": {}}])
    Frames.tour_types = get_tour_types()
    Frames.tours = get_tours()
    return Frames.admin_menu()


# Propagates changes in tour type into database and updates local information
def update_tour_type(frame: Frame, entries: Dict[str, Entry]) -> None:
    tour = get_tour(entries)
    if not is_valid_tour(tour):
        return ErrorLabelGrid(frame, "Invalid tour", 10, 1)

    db.update("database", "tour_types", [tour])
    Frames.tour_types = get_tour_types()
    return Frames.admin_menu()


# Adds new user to the database, Password is stored as a hash
def register_user(username: str, password: str) -> None:
    frame = Frames.frames["register"]

    if username == password:
        return ErrorLabel(frame, 'Username and Password need to differ')
    if username == "" or password == "":
        return ErrorLabel(frame, 'Credentials have to be filled')

    if db.search_by_value("database", "users", "username", username):
        return ErrorLabel(frame, 'This username is already taken')

    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        db.insert("database", "users",
                  [{"role": "Visitor", "username": username,
                    "password": hashed_password, "tickets": []}])
        Frames.user = db.search_by_value("database", "users", "username",
                                         username)
        return Frames.main_menu()

    except harperdb.exceptions.HarperDBError:
        ErrorLabel(frame, 'Error is on our side. Try again')


# Authorizes users request to access account in the database
def authorize_log_in(username: str, password: str) -> None:
    frame = Frames.frames["log_in"]
    if username == "" or password == "":
        return ErrorLabel(frame, 'Credentials have to be filled')

    new_user = db.search_by_value("database", "users", "username", username)

    if not new_user:
        return ErrorLabel(frame, 'Username does not exist')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if new_user[0]["password"] != hashed_password:
        return ErrorLabel(frame, 'Wrong password')

    return Frames.assign_user(new_user[0])
