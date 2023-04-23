from Auxilary_Functions import *
import Frames

errLabel = None
big_font = None
small_font = None


def ErrorLabel(frame, text):
    global errLabel
    if errLabel is not None:
        errLabel.destroy()
    errLabel = Label(frame, text=text, width=25, height=1, font=small_font)
    errLabel.pack()


def ErrorLabelGrid(frame, text, row, column):
    global errLabel
    if errLabel is not None:
        errLabel.destroy()
    errLabel = Label(frame, text=text, width=25, height=1)
    return errLabel.grid(row=row, column=column)


def SmallButton(frame, text, command):
    Button(frame, text=text, font=small_font, width=40, height=1,
           activebackground="blue", command=command).pack()


def NavButton(frame, text, command):
    Button(frame, text=text, font=big_font, width=20, height=2,
           activebackground="#cdfffc", command=command).pack()


def NavButtonGrid(frame, text, command, row, column):
    Button(frame, text=text, height=2, width=14, activebackground="blue",
           font=small_font, command=command).grid(row=row, column=column)
