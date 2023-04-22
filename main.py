import Functions
from Functions import *

def initialize_window() -> Tk:
    window = Tk()
    window.title("My Window")
    # screen_width = window.winfo_screenwidth()
    # screen_height = window.winfo_screenheight()
    # Set the window size
    window.geometry(f"{450}x{700}")
    window.configure()
    return window


root = initialize_window()
img = PhotoImage(file="Background.png")
background = Label(root, image=img)
# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    for key in frames.keys():
        frames[key] = Frame(root, bg="SystemButtonFace")

    background.pack(side='top', fill=Y, expand=True)

    Functions.big_font = font.Font(family="Helvetica", size=18, weight="bold")
    Functions.small_font = font.Font(family="Helvetica", size=10)
    Functions.upcoming_tours = db.sql("SELECT * FROM `database`.`tour_types`")
    init_log_in()
    init_register()

    init_main_menu()
    init_profile()

    init_coordinator_menu()

    init_admin_menu()
    init_admin_tours()
    init_add_tour_type()
    init_change_rules()

    frames["log_in"].tkraise()
    frames["log_in"].place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()
