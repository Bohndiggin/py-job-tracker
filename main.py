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

root = Tk()
root.title("Py Job Search 0.01 (DASHBOARD)")
root.minsize(900, 500)
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)



def main():
    main_frame = ttk.Frame(root)
    main_frame['padding'] = 5
    main_frame.grid(column=0, row=0, sticky=(N, S, E, W))

    #  WELCOME SECTION # Column 0, Row 0

    welcome_frame = ttk.Frame(main_frame)
    welcome_frame.grid(column=0, row=0, sticky=(N, W))
    ttk.Label(welcome_frame, text='WELCOME, NAME').grid(column=2, row=2, sticky=(N, S, E, W))
    
    # SEARCH BAR # Column 1, row 0

    search_frame = ttk.Frame(main_frame)
    search_frame.grid(column=1, row=0, sticky=(N, S, E, W))
    search_text = ttk.Label(search_frame, text="Search:")
    search_text.grid(column=0, row=0, sticky=(E))
    search_query = StringVar()
    search_bar = ttk.Entry(search_frame, textvariable=search_query)
    search_bar.grid(column=1, row=0, sticky=(E, W))
    search_btn = ttk.Button(search_frame, text='Search')
    search_btn.grid(column=2, row=0, sticky=(N, S, E, W))

    # Results AREA # TODO Column 2, Row 0

    title_w_links = ttk.Frame(main_frame)
    title_w_links.grid(column=2, row=0, sticky=(N, S, E, W))
    title_disp_var = StringVar()
    title_disp = ttk.Label(title_w_links, textvariable=title_disp_var)
    title_disp.grid(column=0, row=0, sticky=(N, S, E, W))
    title_disp_var.set('JOB TITLE HERE')
    company_name_var = StringVar()
    company_name_label = ttk.Label(title_w_links, textvariable=company_name_var)
    company_name_label.grid(column=0, row=1, sticky=NSEW)
    company_name_var.set('COMPANY NAME HERE')
    company_btn_label = ttk.Label(title_w_links, text='Company:')
    company_btn_label.grid(column=0, row=2, sticky=NSEW)
    company_site_btn = ttk.Button(title_w_links, text='Company Site', command=placeholder_command)
    company_site_btn.grid(column=1, row=2, sticky=NSEW)



    # NEXT STEPS SECTION # Column 0, row 1

    next_steps_frame = ttk.Labelframe(main_frame, text="Next Steps")
    next_steps_frame.grid(column=0, row=1, sticky=(N, S, E, W))

    # dummy_task_1 = Task('james', next_steps_frame, 1)
    # dummy_task_2 = Task('james', next_steps_frame, 2)
    # dummy_task_3 = Task('james', next_steps_frame, 2)
    # dummy_task_4 = Task('james', next_steps_frame, 2)
    # dummy_task_5 = Task('james', next_steps_frame, 3)
    # dummy_task_6 = Task('james', next_steps_frame, 3)

    
    # JOB DESCRIPTION OF SEARCH # Column 2, Row 1

    job_desc_search_frame = ttk.Labelframe(main_frame, text="Searched Job Description")
    job_desc_search_frame.grid(column=2, row=1, sticky=(N, S, E, W))
    searched_desc = StringVar()
    job_desc_disp = ttk.Label(job_desc_search_frame, textvariable=searched_desc)
    job_desc_disp.grid(column=0, row=0, sticky=(N, S, E, W))
    searched_desc.set('Something')

    # CONTROLS FOR UPCOMING SECTION # Column 0, Row 2

    upcoming_controls_frame = ttk.Labelframe(main_frame, text='Upcoming Controls')
    upcoming_controls_frame.grid(column=0, row=2, sticky=(N, S, E, W))
    
    # CONTROLS FOR INPUT # Column 1, Row 2

    input_controls_frame = ttk.Labelframe(main_frame, text='Search Controls')
    input_controls_frame.grid(column=1, row=2, sticky=(N, S, E, W))
    input_next_btn = ttk.Button(input_controls_frame, text='Huh?', command=job_add_window)
    input_next_btn.grid(column=0, row=0, sticky=(N, S, E, W))

    # SEARCHED JOB SKILLS # Column 2, Row 2

    searched_skills_frame = ttk.Labelframe(main_frame, text="Searched Job Skills")
    searched_skills_frame.grid(column=2, row=2, sticky=NSEW)

    new_job = Job('coder', 'be coder boiiii', 'apple', ['yoga', 'putting up with crap'], next_steps_frame)

    
    weight_assign(main_frame)
    weight_assign(title_w_links)
    weight_assign(welcome_frame)
    weight_assign(search_frame)
    weight_assign(next_steps_frame) 
    weight_assign(job_desc_search_frame)
    weight_assign(upcoming_controls_frame)
    weight_assign(input_controls_frame)
    
    root.mainloop()

if __name__ == "__main__":
    main()
    