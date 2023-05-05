from Frames import *
import Widgets

"""
This is the main file to make the application run. Initiates the program.
"""


def initialize_window() -> Tk:
    window = Tk()
    window.title("My Window")
    window.geometry(f"{450}x{700}")
    window.configure()
    return window


root = initialize_window()
img = PhotoImage(file="Background.png")
background = Label(root, image=img)

if __name__ == '__main__':

    for key in frames.keys():
        frames[key] = Frame(root, bg="SystemButtonFace")

    background.pack(side='top', fill=Y, expand=True)

    Widgets.big_font = font.Font(size=18, weight="bold")
    Widgets.medium_font = font.Font(size=13, weight="bold")
    Widgets.small_font = font.Font(size=10)

    Frames.tour_types = get_tour_types()
    Frames.tours = get_tours()

    log_in()

    frames["log_in"].tkraise()
    frames["log_in"].place(relx=0.5, rely=0.5, anchor=CENTER)

    root.mainloop()
