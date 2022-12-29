import nltk
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from utils import *
import seaborn as sns
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

sns.set()

version_num = 0.01

root = Tk()
root.title(f"Py Job Search {version_num} (DASHBOARD)")
root.minsize(900, 500)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)



def setup():

    main_window = MainWindow(root=root)

    main_window.weight_assign(main_window.main_frame)
    main_window.weight_assign(main_window.title_w_links)
    main_window.weight_assign(main_window.welcome_frame)
    # weight_assign(search_frame)
    main_window.weight_assign(main_window.next_steps_frame) 
    main_window.weight_assign(main_window.job_desc_search_frame)
    main_window.weight_assign(main_window.next_steps_controls_frame)
    main_window.weight_assign(main_window.add_jobs_btn_frame)
    
    
# def job_add_reply(title, desc, company, skills):
#     new_boi = Job(title=title, description=desc, company=company, skills=skills, frame=next_steps_frame, jobs_var=jobs_var, jobs_listbox=jobs_listbox)

if __name__ == "__main__":
    setup()
    root.mainloop()


