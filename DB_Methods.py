import Frames
from Widgets import *
import harperdb
import hashlib
import tkcalendar as tkcalendar

db = harperdb.HarperDB(url="https://pb175-marvav.harperdbcloud.com",
                       username="marvav", password="muniprojekt123")


def update_schedule(hours: List[Entry], minutes: List[Entry], daily):
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


def update_rules(new_rules: str) -> None:
    db.update("database", "general_data", [{"name": "general_rules",
                                            "data": new_rules}])
    return Frames.admin_menu()


def get_tour_types() -> List[Tour]:
    return db.sql("SELECT * FROM `database`.`tour_types`")


def get_schedules():
    schedules = dict()
    for record in db.sql("SELECT * FROM `database`.`DailyTours`"):
        schedules[record["Name"]] = record["schedule"]
    return schedules


def delete_tour(tour):
    db.delete("database", "tour_types", [tour["Name"]])
    db.delete("database", "DailyTours", [tour["Name"]])
    Frames.admin_menu()


def purchase(frame: Frame, ticket, tickets, discount):
    try:
        if tickets.get() != "" and int(tickets.get()) < 0:
            return ErrorLabel(frame, "Invalid ticket count")
        if discount.get() != "" and int(discount.get()) < 0:
            return ErrorLabel(frame, "Invalid discount count")
        if tickets.get() != "" and discount.get() != "" \
                and int(tickets.get()) + int(discount.get()) == 0:
            return ErrorLabel(frame, "No tickets selected")
    except:
        return ErrorLabel(frame, "Please enter number")

    ticket["TicketsNumber"] = str(tickets.get())
    ticket["DiscountNumber"] = str(discount.get())
    Frames.user["tickets"].append(ticket)
    db.update("database", "users", [Frames.user])
    Frames.main_menu()


def insert_tour_type(frame: Frame, entries: Dict[str, Entry]) -> None:
    tour = get_tour(entries)
    if not is_valid_tour(tour):
        return ErrorLabelGrid(frame, "Invalid tour", 10, 1)

    db.insert("database", "tour_types", [tour])
    db.insert("database", "DailyTours",
              [{"Name": tour["Name"], "schedule": []}])
    Frames.schedules = get_schedules()
    Frames.tour_types = get_tour_types()
    return Frames.admin_menu()


def update_tour_type(frame: Frame, entries: Dict[str, Entry]) -> None:
    tour = get_tour(entries)
    if not is_valid_tour(tour):
        return ErrorLabelGrid(frame, "Invalid tour", 10, 1)

    db.update("database", "tour_types", [tour])
    Frames.tour_types = get_tour_types()
    return Frames.admin_menu()


def register_user(username: str, password: str) -> None:
    frame = Frames.frames["register"]

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
