import nltk
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import seaborn as sns
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure

class Task:
    def __init__(self, name, parent_frame, parent_job):
        self.name = name
        self.parent_job = parent_job
        self.parent_job.task_list.append(self)
        self.parent_frame = parent_frame
        self.task_id = len(self.parent_job.task_list)
        self.parent_job.task_complete_dict[self.name] = 0
        self.completed = IntVar()
        self.completed.set(self.parent_job.task_complete_dict[self.name])
        self.parent_job.task_values[self.name] = self.completed
        self.task_complete_box = ttk.Checkbutton(self.parent_frame, text=self.name, variable=self.completed)
        self.task_complete_box.grid(column=0, row=(len(self.parent_job.task_list)), sticky=(E, W))
    def complete_task(self):
        self.completed = 1
    def show(self):
        self.task_complete_box = ttk.Checkbutton(self.parent_frame, text=self.name, variable=self.completed)
        self.task_complete_box.grid(column=0, row=(len(self.parent_job.task_list)), sticky=(E, W))
    def hide(self):
        self.task_complete_box.destroy()
    def __repr__(self) -> str:
        return f'{self.name}. A task associated with {self.parent_job}'

jobs = []

class Job:
    def __init__(self, title, description, company, skills, frame) -> None:
        jobs.append(self)
        self.id = len(jobs)
        self.title = title
        self.description = description
        self.company = company
        self.skills = []
        for i in skills:
            self.skills.append(Skill(self.id, i))
        self.task_list = []
        self.task_complete_dict = {}
        self.task_values = {}
        Task('Finish Applying', frame, self) # Need to list out all the tasks of a job search and include custom stages
        Task('Contact Hireing Manager', frame, self)
        # Task('Contact Hireing Manager', frame, self)
        Task('Phone Screen', frame, self)
        Task('Interview', frame, self)
        Task('Interview', frame, self)
        Task('Technical Assessments', frame, self)
        Task('Additional Interview', frame, self)
        Task('Offer Extension', frame, self)
        Task('Acceptance!', frame, self)
    def show_tasks(self):
        for i in self.task_list:
            i.show()
    def hide_tasks(self):
        for i in self.task_list:
            i.hide()
    def __repr__(self) -> str:
        return f'{self.title} at {self.company}'


class Skill:
    def __init__(self, job_id, name) -> None:
        self.job_id = job_id
        self.name = name
    def __repr__(self) -> str:
        return f'{self.name} is a skill needed for Job {self.job_id}'

    

def weight_assign(object, x=1, y=1):
     size = object.grid_size()
     for i in range(size[0]):
          object.columnconfigure(i, weight=x)
     for j in range(size[1]):
          object.rowconfigure(j, weight=y)

def placeholder_command():
    pass

def job_add_window():
    ja = Toplevel()
    ja.title("Py Job Search 0.01 (JOB ADD)")
    ja.minsize(900, 500)
    ja.columnconfigure(0, weight=1)
    ja.rowconfigure(0, weight=1)

    ja_title = StringVar()
    ja_salary = StringVar()
    ja_company = StringVar()
    ja_company_site = StringVar()

        
    ja_company_details_frame = ttk.Labelframe(ja, text='Enter Details')
    ja_company_details_frame.grid(column=0, row=0, sticky=NSEW)
    
    ja_job_title = ttk.Label(ja_company_details_frame, text="Title:")
    ja_job_title.grid(column=0, row=0, sticky=NSEW)
    ja_job_title_entry = ttk.Entry(ja_company_details_frame, textvariable=ja_title)
    ja_job_title_entry.grid(column=1, row=0)
    
    ja_job_salary = ttk.Label(ja_company_details_frame, text="Salary:")
    ja_job_salary.grid(column=0, row=1, sticky=NSEW)
    ja_job_salary_entry = ttk.Entry(ja_company_details_frame, textvariable=ja_salary)
    ja_job_salary_entry.grid(column=1, row=1, sticky=NSEW)

    ja_job_company = ttk.Label(ja_company_details_frame, text="Company:")
    ja_job_company.grid(column=0, row=2, sticky=NSEW)
    ja_job_company_entry = ttk.Entry(ja_company_details_frame, textvariable=ja_company)
    ja_job_company_entry.grid(column=1, row=2, sticky=NSEW)

    ja_job_site = ttk.Label(ja_company_details_frame, text="Company Site:")
    ja_job_site.grid(column=0, row=3, sticky=NSEW)
    ja_job_site_entry = ttk.Entry(ja_company_details_frame, textvariable=ja_company_site)
    ja_job_site_entry.grid(column=1, row=3, sticky=NSEW)


    # JOB DESCRIPTION INPUT # Column 0, Row 1
    
    ja_frame = ttk.Labelframe(ja, text="Paste Job Description:")
    ja_frame.grid(column=0, row=1, sticky=NSEW)
    job_desc_input_paste_frame = ttk.Frame(ja_frame)
    job_desc_input_paste_frame.grid(column=0, row=0, sticky=(N, S, E, W))
    job_desc_input_text = Text(job_desc_input_paste_frame, width=70, height=30)
    job_desc_input_text.grid(column=0, row=0, sticky=(N, S, E, W))
    weight_assign(job_desc_input_paste_frame)

    def job_add_button():
        # Entity Extraction here
        desc = job_desc_input_text.get('1.0', 'end')
        tokens = nltk.word_tokenize(desc)
        print(tokens)
        tagged = nltk.pos_tag(tokens)
        print(tagged)

    def close_ja_window():
        ja.destroy()

    ja_button_frame = ttk.Frame(ja)
    ja_button_frame.grid(column=1, row=2, sticky=NSEW)
    ja_button_close = ttk.Button(ja_button_frame, text='Cancel', command=close_ja_window)
    ja_button_close.grid(column=1, row=0, sticky=NSEW)
    ja_button_add = ttk.Button(ja_button_frame, text='Add', command=job_add_button)
    ja_button_add.grid(column=0, row=0, sticky=NSEW)
