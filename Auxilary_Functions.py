from Modules import *

import Frames

Tour = Dict[str, str]
Ticket = Dict[str, str]
Entries = Dict[Entry, str]
User = Dict[str, str]

TOUR_PARAMS = ["Name", "Capacity", "Description", "DiscountPrice",
               "Duration", "Location", "TicketPrice"]

tour_order = ["Name", "Location", "Date", "Time", "Duration", "Description"]
ticket_order = ["Name", "Location", "Date", "Time", "Duration",
                "Description", "TicketsNumber", "DiscountNumber", "Code"]


def strip_entry(entry) -> str:
    return entry.replace(' ', '')


def get_tour(entries):
    tour = dict()
    for parameter in TOUR_PARAMS:
        if parameter == "Description":
            tour[parameter] = entries[parameter].get("1.0", END)
        else:
            tour[parameter] = entries[parameter].get()
    return tour


def tour_to_ticket(ticket: Tour, time: str, date: str) -> Ticket:
    ticket = ticket.copy()
    ticket["Date"] = date
    ticket["Time"] = time
    ticket.pop("DiscountPrice")
    ticket.pop("TicketPrice")
    return ticket


def is_valid_tour(tour):
    for param in TOUR_PARAMS:
        if param not in tour:
            return False

    if not tour["Name"].replace(' ', '').isalpha():
        return False

    if not tour["Location"].replace(' ', '').isalpha():
        return False

    if not tour["Capacity"].replace(' ', '').isnumeric():
        return False

    if not tour["Duration"].replace(' ', '').isnumeric():
        return False

    if not tour["TicketPrice"].replace(' ', '').isnumeric():
        return False

    if not tour["DiscountPrice"].replace(' ', '').isnumeric():
        return False

    if int(tour["TicketPrice"]) < int(tour["DiscountPrice"]):
        return False

    return True


def calculate_price(tickets, discount, tour):
    return int(tickets.get()) * int(tour["DiscountPrice"]) + \
           int(discount.get()) * int(tour["TicketPrice"])


def get_date():
    today = date.today()
    day = "0"+str(today.day) if len(str(today.day))==1 else str(today.day)
    month = "0"+str(today.month) if len(str(today.month))==1 else str(today.month)
    return day + "/" + month + "/" + str(today.year)


def get_time():
    today = datetime.time(datetime.now())
    return str(today.hour) + ":" + str(today.minute)


def is_expired(date, time):
    return date < get_date() or (date == get_date() and time < get_time())


def get_tours_with_param(key, value) -> List[Tour]:
    return [tour for tour in Frames.tour_types if tour[key] == value]


def get_tours_params(param) -> List[str]:
    return [tour[param] for tour in Frames.tour_types]

