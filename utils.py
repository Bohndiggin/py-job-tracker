import nltk
import os
import sys
from tkinter import *
from tkinter import ttk
from tkinter import filedialog

task_list = []
task_complete_dict = {}
task_values = {}

class Task:
    def __init__(self, name, desc_id, parent_frame):
        self.name = name
        self.desc_id = desc_id
        task_list.append(self)
        self.task_id = len(task_list)
        task_complete_dict[self.name] = 0
        self.completed = IntVar()
        self.completed.set(task_complete_dict[self.name])
        task_values[self.name] = self.completed
        task_complete_box = ttk.Checkbutton(parent_frame, text=self.name, variable=self.completed)
        task_complete_box.grid(column=0, row=(len(task_list)), sticky=(E, W))
    def complete_task(self):
        self.completed = True

# dummy_task_1 = Task('james', 55)
# dummy_task_2 = Task('james', 55)
# dummy_task_3 = Task('james', 55)
# dummy_task_4 = Task('james', 55)
# dummy_task_5 = Task('james', 55)
# dummy_task_6 = Task('james', 55)

jobs = []

class Job:
    def __init__(self, title, description, company, skills) -> None:
        jobs.append(self)
        self.id = len(jobs)
        self.title = title
        self.description = description
        self.company = company
        self.skills = skills
    def __repr__(self) -> str:
        return f'{self.title} at {self.company}'

def job_add(description):
    # Entity Extraction here
    Job()
    Task() # Need to list out all the tasks of a job search and include custom stages
    Task()

def weight_assign(object, x=1, y=1):
     size = object.grid_size()
     for i in range(size[0]):
          object.columnconfigure(i, weight=x)
     for j in range(size[1]):
          object.rowconfigure(j, weight=y)