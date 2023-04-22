from Frames import *


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

    Frames.big_font = font.Font(family="Helvetica", size=18, weight="bold")
    Frames.small_font = font.Font(family="Helvetica", size=10)

    init_log_in()
    init_register()

    frames["log_in"].tkraise()
    frames["log_in"].place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()
