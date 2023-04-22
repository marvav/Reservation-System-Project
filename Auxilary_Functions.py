from datetime import datetime, date


def strip_entry(entry):
    return entry.get().replace(' ', '')


def is_valid_tour(tour):
    if not strip_entry(tour["Name"]).isalpha():
        return False

    if not strip_entry(tour["Location"]).isalpha():
        return False

    if not tour["Capacity"].get().isnumeric():
        return False

    if not tour["Duration"].get().isnumeric():
        return False

    if not tour["Description"] != "":
        return False

    if not tour["TicketPrice"].get().isnumeric():
        return False

    if not tour["DiscountPrice"].get().isnumeric():
        return False

    if tour["TicketPrice"].get() < tour["DiscountPrice"].get():
        return False

    return True


def get_date():
    today = date.today()
    return str(today.day) + "/" + str(today.month) + "/" + str(today.year)


def get_time():
    today = datetime.time(datetime.now())
    return str(today.hour) + ":" + str(today.minute)


def is_expired(date, time):
    return date < get_date() or (date == get_date() and time < get_time())
