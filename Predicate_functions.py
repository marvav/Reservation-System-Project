
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