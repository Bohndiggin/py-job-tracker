import nltk
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
from utils import *


root = Tk()
root.title("py-j-search 0.0")
root.minsize(900, 500)



def main():
    main_frame = ttk.Frame(root)
    main_frame['padding'] = 5
    main_frame.grid(column=0, row=0, sticky=(N, S, E, W))



    welcome_frame = ttk.Frame(main_frame)
    welcome_frame.grid(column=0, row=0, sticky=(N, W))
    ttk.Label(welcome_frame, text='WELCOME, NAME').grid(column=2, row=2, sticky=(N, S, E, W))
    
    
    search_frame = ttk.Frame(main_frame)
    search_frame.grid(column=1, row=0, sticky=(N, S, E, W))
    search_frame.columnconfigure(0, weight=1)
    search_frame.columnconfigure(1, weight=1)
    search_text = ttk.Label(search_frame, text="Search:")
    search_text.grid(column=0, row=0, sticky=(E))
    search_query = StringVar()
    search_bar = ttk.Entry(search_frame, textvariable=search_query)
    search_bar.grid(column=1, row=0, sticky=(E, W))


    next_steps_frame = ttk.Labelframe(main_frame, text="Next Steps")
    next_steps_frame.grid(column=0, row=1, sticky=(N, S, E, W))

    job_desc_paste_frame = ttk.Labelframe(main_frame, text="Job Description Input")
    job_desc_paste_frame.grid(column=1, row=1, sticky=(N, S, E, W))
    job_desc_text = Text(job_desc_paste_frame, width=70, height=30)
    job_desc_text.grid(column=0, row=0, sticky=(N, S, E, W))
    


    upcoming_controls_frame = ttk.Frame(main_frame)
    upcoming_controls_frame.grid(column=0, row=2, sticky=(N, S, E, W))
    
    search_controls_frame = ttk.Frame(main_frame)
    search_controls_frame.grid(column=1, row=2, sticky=(N, S, E, W))
    
    weight_assign(main_frame)
    weight_assign(welcome_frame)
    weight_assign(search_frame)
    weight_assign(next_steps_frame)
    weight_assign(job_desc_paste_frame)
    weight_assign(upcoming_controls_frame)
    weight_assign(search_controls_frame)
    root.mainloop()

if __name__ == "__main__":
    main()
    