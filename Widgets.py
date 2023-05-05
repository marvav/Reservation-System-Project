from Auxilary_Functions import *

"""
This file define screen elements aliases used across the application to ensure
cohesive look, which can be effortlessly configured here.
"""
errLabel = None
big_font = None
medium_font = None
small_font = None


def ErrorLabel(frame: Frame, text: str) -> None:
    global errLabel
    if errLabel is not None:
        errLabel.destroy()
    errLabel = Label(frame, text=text, width=25, height=1, font=small_font)
    errLabel.pack()


def ErrorLabelGrid(frame: Frame, text: str, row: int, column: int) -> None:
    global errLabel
    if errLabel is not None:
        errLabel.destroy()
    errLabel = Label(frame, text=text, width=25, height=1)
    errLabel.grid(row=row, column=column)


def SmallButton(frame: Frame, text: str, command: Callable) -> None:
    Button(frame, text=text, font=small_font, width=40, height=1,
           activebackground="blue", command=command).pack()


def NavButton(frame: Frame, text: str, command: Callable) -> None:
    Button(frame, text=text, font=big_font, width=20, height=2,
           activebackground="#cdfffc", command=command).pack()


def NavButtonGrid(frame: Frame, text: str, command: Callable,
                  row: int, column: int) -> None:
    Button(frame, text=text, height=2, width=14, activebackground="blue",
           font=small_font, command=command).grid(row=row, column=column)


def SmallLabel(frame: Frame, text: str) -> Label:
    return Label(frame, text=text, font=small_font, width=20, height=1)


def MediumLabel(frame: Frame, text: str) -> Label:
    return Label(frame, text=text, font=medium_font, width=20, height=2)


def BigLabel(frame: Frame, text: str) -> Label:
    return Label(frame, text=text, font=big_font, width=20, height=2)


def ShowValidTickets(frame: Frame, listbox: Listbox) -> None:
    MediumLabel(frame, "Your Tickets").pack()
    for ticket in Frames.user["tickets"]:
        if not is_expired(ticket["Date"], ticket["Time"]):
            listbox.insert(END, ticket["Name"] + " | " + ticket["Location"])
            listbox.insert(END, ticket["Date"] + " | " + ticket["Time"])
            listbox.insert(END, "Ticket Identification Code:")
            listbox.insert(END, ticket["Code"])
            listbox.insert(END, "Full tickets: " + ticket["TicketsNumber"])
            listbox.insert(END,
                           "Discounted tickets: " + ticket["DiscountNumber"])
            listbox.insert(END, "\n")


def ShowExpiredTickets(frame: Frame, listbox: Listbox) -> None:
    MediumLabel(frame, "Expired Tickets").pack()
    for ticket in Frames.user["tickets"]:
        if is_expired(ticket["Date"], ticket["Time"]):
            listbox.insert(END, ticket["Name"] + " | " + ticket["Location"])
            listbox.insert(END, ticket["Date"] + " | " + ticket["Time"])
            listbox.insert(END, "Ticket Code: " + ticket["Code"])
            listbox.insert(END, "Full tickets: " + ticket["TicketsNumber"])
            listbox.insert(END,
                           "Discounted tickets: " + ticket["DiscountNumber"])
            listbox.insert(END, "\n")

