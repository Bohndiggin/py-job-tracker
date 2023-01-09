from tkinter import *
from tkinter import ttk
from utils2 import *

version_num = 0.10

root = Tk()
root.title(f"Py Job Coach {version_num} (DASHBOARD)")
root.minsize(900, 700)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)



def setup():

    main_window = MainWindow(root=root)

    main_window.weight_assign(main_window.main_frame)
    main_window.weight_assign(main_window.title_w_links)
    main_window.weight_assign(main_window.welcome_frame)
    main_window.weight_assign(main_window.next_steps_frame)
    main_window.weight_assign(main_window.job_desc_search_frame)
    main_window.weight_assign(main_window.note_frame)
    main_window.populate_listbox()

if __name__ == "__main__":
    setup()
    root.mainloop()


