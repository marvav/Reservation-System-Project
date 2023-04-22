from Auxilary_Functions import *
from Widgets import *
import harperdb
import hashlib
import tkcalendar as tkcalendar

db = harperdb.HarperDB(url="https://pb175-marvav.harperdbcloud.com",
                       username="marvav", password="muniprojekt123")


def update_schedule(hours, minutes, daily):
    new_schedule = []
    for i in range(len(hours)):
        if hours[i].get() != "":
            if minutes[i].get() == "":
                new_schedule.append(hours[i].get() + ":00")
            else:
                new_schedule.append(hours[i].get() + ":" + minutes[i].get())
    daily["schedule"] = new_schedule
    db.update("database", "DailyTours", [daily])
    Frames.hide_all_frames("coordinator_menu")


def change_rules(new_rules):
    db.update("database", "general_data", [{"name": "general_rules",
                                            "data": new_rules}])
    return Frames.hide_all_frames("admin_menu")


def tour_types(param):
    if not param:
        return db.sql("SELECT * FROM `database`.`tour_types`")
    return [x[param] for x in db.sql("SELECT * FROM `database`.`tour_types`")]


def get_tours_at_location(location):
    tours = db.search_by_value("database", "tour_types", "Location", location)
    return tours


def get_schedules():
    schedules = dict()
    for location in tour_types("Location"):
        schedules[location] = \
            schedule = db.search_by_value("database", "DailyTours",
                                          "Name", location)
        if schedule:
            schedules[location] = schedule[0]["schedule"]
    return schedules


def purchase(frame, ticket, tickets, discount):
    try:
        if tickets.get() != "" and int(tickets.get()) < 0:
            return errorLabel(frame, "Invalid ticket count")
        if discount.get() != "" and int(discount.get()) < 0:
            return errorLabel(frame, "Invalid discount count")
        if tickets.get() != "" and discount.get() != "" \
                and int(tickets.get()) + int(discount.get()) == 0:
            return errorLabel(frame, "No tickets selected")
    except:
        return errorLabel(frame, "Please enter number")

    ticket["TicketsNumber"] = str(tickets.get())
    ticket["DiscountNumber"] = str(discount.get())
    Frames.user["tickets"].append(ticket)
    db.update("database", "users", [Frames.user])
    Frames.hide_all_frames("main_menu", frame)


def calculate_price(tickets, discount, tour):
    return int(tickets.get()) * int(tour["DiscountPrice"]) + \
           int(discount.get()) * int(tour["TicketPrice"])


def insert_tour_type(frame, tour):
    if not is_valid_tour(tour):
        return ErrorLabelGrid(frame, "Invalid tour", 10, 1)

    db.insert("database", "tour_types",
              [{"Name": tour["Name"].get(), "Location": tour["Location"].get(),
                "Duration": tour["Duration"].get(),
                "Capacity": tour["Capacity"].get(),
                "Description": tour["Description"].get("1.0", END),
                "TicketPrice": tour["TicketPrice"].get(),
                "DiscountPrice": tour["DiscountPrice"].get(),
                "TourRules": tour["TourRules"]}])
    db.insert("database", "DailyTours",
              [{"Name": tour["Name"].get(), "schedule": []}])

    return Frames.hide_all_frames("admin_menu")


def register_user(username, password):
    frame = Frames.frames["register"]

    if username == "" or password == "":
        return errorLabel(frame, 'Credentials have to be filled')

    if db.search_by_value("database", "users", "username", username):
        return errorLabel(frame, 'This username is already taken')

    try:
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        db.insert("database", "users",
                  [{"role": "Visitor", "username": username,
                    "password": hashed_password, "tickets": []}])
        Frames.user = db.search_by_value("database", "users", "username",
                                         username)
        Frames.hide_all_frames("main_menu")

    except harperdb.exceptions.HarperDBError:
        errorLabel(frame, 'Error is on our side. Try again')


def authorize_log_in(username, password):
    frame = Frames.frames["log_in"]
    if username == "" or password == "":
        return errorLabel(frame, 'Credentials have to be filled')

    new_user = db.search_by_value("database", "users", "username", username)

    if not new_user:
        return errorLabel(frame, 'Username does not exist')

    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    if new_user[0]["password"] != hashed_password:
        return errorLabel(frame, 'Wrong password')

    return Frames.init_ui(new_user[0])
