from typing import Any

import Widgets
from Modules import *

import Frames

"""
This file contains auxiliary functions providing functionality such as 
conversion, validity checks, formatting and extra type annotations.
Functions here should not require comments as they should be easy to 
understand and self-commenting
"""

# Type annotations
TourRecord = Dict[str, Any]
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


def get_tour(entries: Dict[str, Any]) -> Tour:
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


def is_purchase_valid(frame: Frame, tickets: Entry, discount: Entry) -> bool:
    try:
        if tickets.get() != "" and int(tickets.get()) < 0:
            Widgets.ErrorLabel(frame, "Invalid ticket count")
            return False
        if discount.get() != "" and int(discount.get()) < 0:
            Widgets.ErrorLabel(frame, "Invalid discount count")
            return False
        if tickets.get() != "" and discount.get() != "" \
                and int(tickets.get()) + int(discount.get()) == 0:
            Widgets.ErrorLabel(frame, "No tickets selected")
            return False
    except:
        Widgets.ErrorLabel(frame, "Please enter number")
        return False
    return True


def is_valid_tour(tour: Tour) -> bool:
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


def calculate_price(tickets: Entry, discount: Entry, tour: Tour) -> int:
    price = 0
    price += int(discount.get()) * int(tour["DiscountPrice"])
    price += int(tickets.get()) * int(tour["TicketPrice"])
    return price


def get_date() -> str:
    today = date.today()
    day = "0" + str(today.day) if len(str(today.day)) == 1 else str(today.day)
    month = "0" + str(today.month) if len(str(today.month)) == 1 else str(
        today.month)
    return day + "/" + month + "/" + str(today.year)


def get_time() -> str:
    today = datetime.time(datetime.now())
    hour = "0" + str(today.hour) if len(str(today.hour)) == 1 else str(
        today.hour)
    minute = "0" + str(today.minute) if len(str(today.minute)) == 1 else str(
        today.minute)
    return hour + ":" + minute


def is_expired(date: str, time: str) -> bool:
    return date < get_date() or (date == get_date() and time < get_time())


def get_tours_with_param(key: str, value: str) -> List[Tour]:
    return [tour for tour in Frames.tour_types if tour[key] == value]


def get_tours_params(param: str) -> List[str]:
    return [tour[param] for tour in Frames.tour_types]
