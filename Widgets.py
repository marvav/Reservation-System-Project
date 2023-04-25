from Auxilary_Functions import *

errLabel = None
big_font = None
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
