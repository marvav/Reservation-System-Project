from Window_funtions import *

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    root = initialize_window()
    root.configure(bg="blue")

    for key in frames.keys():
        frames[key] = Frame(root, bg="green")

    init_fonts()
    init_log_in()
    init_register()
    init_main_menu()
    init_your_tickets()
    init_profile()
    init_tours()

    frames["log_in"].tkraise()
    frames["log_in"].place(relx=0.5, rely=0.5, anchor=CENTER)
    root.mainloop()
