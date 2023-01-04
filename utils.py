from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import seaborn as sns
from matplotlib.backend_bases import key_press_handler
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import pickle
import spacy
from spacy.matcher import PhraseMatcher
import webbrowser

spacy.prefer_gpu()
nlp = spacy.load("en_core_web_sm")
skills_list = 'jz_skill_patterns.jsonl'

matcher = PhraseMatcher(nlp.vocab)

ruler = nlp.add_pipe("entity_ruler", before='ner').from_disk(skills_list)

version_num = 0.01

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
        self.task_check_box = ttk.Checkbutton(self.parent_frame, text=self.name, variable=self.completed)
        self.task_check_box.grid(column=0, row=(len(self.parent_job.task_list)), sticky=(E, W))
    def complete_task(self):
        self.completed = 1
    def show(self):
        self.task_check_box = ttk.Checkbutton(self.parent_frame, text=self.name, variable=self.completed)
        self.task_check_box.grid(column=0, row=self.parent_job.task_list.index(self), sticky=(E, W))
    def hide(self):
        self.task_check_box.destroy()
    def __repr__(self) -> str:
        return f'{self.name}. A task associated with {self.parent_job}'

jobs = []
jobs_data = []

class Job:
    def __init__(self, title, description, company, skills, frame, jobs_var, jobs_listbox, job_skill_box,  **kwargs) -> None:
        self.id = len(jobs)
        self.title = title
        self.description = description
        self.company = company
        self.salary = kwargs.get('salary', None)
        self.frame = frame
        self.skills = [Skill(len(jobs), ent[0], job_skill_box, self) for ent in skills]
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
        jobs.append(self)
        # jobs2.append(f'{self.title} at {self.company}')
        jobs_var.set(jobs)
        self.saveable = [self.title, self.description, self.company, self.salary, self.skills]
        if len(jobs) % 2 == 0:
            jobs_listbox.itemconfigure(len(jobs)-1, background='#f0f0ff')
    def show_tasks(self):
        for i in self.task_list:
            i.show()
        for i in self.skills:
            i.show()
    def hide_tasks(self):
        for i in self.task_list:
            i.hide()
        for i in self.skills:
            i.hide()
    def add_task(self, desc):
        atw = Toplevel()
        atw.title(f'Py Job Search {version_num} (ADD TASK)')
        Task(desc, self.frame, self)
    def __repr__(self) -> str:
        return f'{self.title} at {self.company}'
    def wrap_data(self):
        job_data_wrapped = {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'company': self.company,
            'skills': [i for i in self.skills],
            'tasks': [i for i in self.task_list]
        }
        return job_data_wrapped


class Skill:
    def __init__(self, job_id, name, parent_frame, parent_obj) -> None:
        self.job_id = job_id
        self.skill_id = 0
        self.name = name
        self.parent_frame = parent_frame
        # self.skill_disp = ttk.Label(self.parent_frame, text=self.name)
        # self.skill_disp.pack(side=LEFT)

    def __repr__(self) -> str:
        return f'{self.name} is a skill needed for Job {self.job_id}'
    
    def show(self):
        self.skill_disp = ttk.Label(self.parent_frame, text=self.name)
        self.skill_disp.pack(side=LEFT)
    def hide(self):
        try:
            self.skill_disp.destroy()
        except:
            pass

def update_info(id, job_desc_disp, title_disp_var, company_name_var, salary_disp_var):
    indx = id[0]
    for i in jobs:
        i.hide_tasks()
    jobs[indx].show_tasks()
    job_desc_disp['state'] = 'normal'
    job_desc_disp.delete('1.0', 'end')
    job_desc_disp.insert('1.0', jobs[indx].description)
    job_desc_disp['state'] = 'disabled'
    title_disp_var.set(jobs[indx].title)
    company_name_var.set(jobs[indx].company)

    if jobs[indx]:
        salary_disp_var.set(jobs[indx].salary)
    else:
        pass

def weight_assign(object, x=1, y=1):
    size = object.grid_size()
    for i in range(size[0]):
        object.columnconfigure(i, weight=x)
    for j in range(size[1]):
        object.rowconfigure(j, weight=y)
        
class MainWindow:
    def __init__(self, root) -> None:
        self.main_frame = ttk.Frame(root)
        self.main_frame['padding'] = 5
        self.main_frame.grid(column=0, row=0, sticky=(N, S, E, W))

        self.root = root

        #  WELCOME SECTION # Column 0, Row 0

        self.welcome_frame = ttk.Frame(self.main_frame)
        self.welcome_frame.grid(column=0, row=0, sticky=(N, W))
        ttk.Label(self.welcome_frame, text='WELCOME, NAME').grid(column=2, row=2, sticky=(N, S, E, W))

        # Results AREA # TODO Column 2, Row 0

        self.title_w_links = ttk.Frame(self.main_frame)
        self.title_w_links.grid(column=2, row=0, sticky=(N, S, E, W))
        self.title_disp_var = StringVar()
        self.title_disp = ttk.Label(self.title_w_links, textvariable=self.title_disp_var)
        self.title_disp.grid(column=0, row=0, sticky=(N, S, E, W))
        self.title_disp_var.set('JOB TITLE HERE')
        self.company_name_var = StringVar()
        self.company_name_label = ttk.Label(self.title_w_links, textvariable=self.company_name_var)
        self.company_name_label.grid(column=0, row=1, sticky=NSEW)
        self.company_name_var.set('COMPANY NAME HERE')
        self.salary_disp_var = StringVar()
        self.salary_disp = ttk.Label(self.title_w_links, textvariable=self.salary_disp_var)
        self.salary_disp.grid(column=0, row=2, sticky=NSEW)
        self.company_site_btn = ttk.Button(self.title_w_links, text='Company Site', command=placeholder_command)
        self.company_site_btn.grid(column=1, row=2, sticky=NSEW)

        # JOBS APPLIED TO LISTBOX # Column 0, row 1

        self.jobs_var = StringVar(value=jobs)
        self.jobs_listbox_frame = ttk.Labelframe(self.main_frame, text='Jobs Applied To')
        self.jobs_listbox_frame.grid(column=0, row=1, sticky=NSEW)
        self.jobs_listbox = Listbox(self.jobs_listbox_frame, height=15, listvariable=self.jobs_var)
        self.jobs_listbox.grid(column=0, row=0, sticky=NSEW)
        self.jobs_listbox.bind('<<ListboxSelect>>', lambda e: update_info(self.jobs_listbox.curselection(), self.job_desc_disp, self.title_disp_var, self.company_name_var, self.salary_disp_var))

        # NEXT STEPS SECTION # Column 1, row 1

        self.next_steps_frame = ttk.Labelframe(self.main_frame, text="Next Steps (tasks)")
        self.next_steps_frame.grid(column=1, row=1, sticky=(N, S, E, W))
        
        # JOB DESCRIPTION OF SEARCH # Column 2, Row 1

        self.job_desc_search_frame = ttk.Labelframe(self.main_frame, text="Job Description")
        self.job_desc_search_frame.grid(column=2, row=1, sticky=(N, S, E, W))
        # self.searched_desc = StringVar()
        self.job_desc_disp = Text(self.job_desc_search_frame, width=70, height=30)
        self.job_desc_disp.grid(column=0, row=0, sticky=(N, S, E, W))
        self.job_desc_disp.insert('1.0', 'Something')
        self.job_desc_scroll_bar = ttk.Scrollbar(self.job_desc_search_frame, orient='vertical', command=self.job_desc_disp.yview)
        self.job_desc_scroll_bar.grid(column=1, row=0, sticky=NSEW)
        self.job_desc_disp['yscrollcommand'] = self.job_desc_scroll_bar.set
        # self.job_desc_disp['state'] = 'disabled'


        # CONTROLS FOR INPUT # Column 0, Row 2

        self.add_jobs_btn_frame = ttk.Labelframe(self.main_frame, text='Add Jobs')
        self.add_jobs_btn_frame.grid(column=0, row=2, sticky=(N, S, E, W))
        self.add_jobs_btn = ttk.Button(self.add_jobs_btn_frame, text='Add Jobs', command=self.job_add_window)
        self.add_jobs_btn.grid(column=0, row=0, sticky=(N, S, E, W))

        # CONTROLS FOR NEXT STEPS SECTION # Column 1, Row 2

        self.next_steps_controls_frame = ttk.Labelframe(self.main_frame, text='Next Steps Controls')
        self.next_steps_controls_frame.grid(column=1, row=2, sticky=(N, S, E, W))
        self.next_steps_controls_add_task_btn = ttk.Button(self.next_steps_controls_frame, text='Add Task', command=self.task_add_btn)
        self.next_steps_controls_add_task_btn.grid(column=0, row=0, sticky=NSEW)
        self.next_steps_controls_remove_task_btn = ttk.Button(self.next_steps_controls_frame, text='Remove Task', command=placeholder_command)
        self.next_steps_controls_remove_task_btn.grid(column=1, row=0, sticky=NSEW)


        # JOB SKILLS # Column 2, Row 2

        self.skills_frame = ttk.Labelframe(self.main_frame, text="Job Skills")
        self.skills_frame.grid(column=2, row=2, sticky=NSEW)

        new_job = Job('coder', 'be coder boiiii', 'apple', [('yoga', 'x'), ('putting up with crap', 'x')], self.next_steps_frame, self.jobs_var, self.jobs_listbox, self.skills_frame)
        new_job2 = Job('coder', 'be coder boiiii', 'apple', [('yoga', 'x'), ('putting up with crap', 'x')], self.next_steps_frame, self.jobs_var, self.jobs_listbox, self.skills_frame, salary=250000)
        new_job3 = Job('coder', 'be coder boiiii', 'apple', [('yoga', 'x'), ('putting up with crap', 'x')], self.next_steps_frame, self.jobs_var, self.jobs_listbox, self.skills_frame)

        root.option_add('*tearOff', FALSE)
        menubar = Menu(root)
        root['menu'] = menubar
        menu_file = Menu(menubar)
        menu_edit = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_edit, label='Edit')
        menu_file.add_command(label='New', command=placeholder_command)
        menu_file.add_command(label='Open...', command=placeholder_command)
        menu_file.add_command(label='Save', command=save_data)

    def weight_assign(self, object, x=1, y=1):
        size = object.grid_size()
        for i in range(size[0]):
            object.columnconfigure(i, weight=x)
        for j in range(size[1]):
            object.rowconfigure(j, weight=y)
    def job_add_window(self):
        ja_window = JobAddWindow(self)
    def task_add_btn(self):
        TaskAddWindow(momma=self)

class TaskAddWindow():
    def __init__(self, momma) -> None:  
        self.taw = Toplevel()
        self.taw.title(f"Py Job Search {version_num} (TASK ADD)")
        # self.taw.minsize(500, 300)
        self.taw.columnconfigure(0, weight=1)
        self.taw.rowconfigure(0, weight=1)

        self.momma = momma

        self.taw_frame = ttk.Frame(self.taw)
        self.taw_frame.grid(column=0, row=0, sticky=NSEW)

        self.taw_task_add_label = ttk.Label(self.taw_frame, text="Add Task:")
        self.taw_task_add_label.grid(column=0, row=0, sticky=NSEW)

        self.task_to_add = StringVar()

        self.taw_task_add_entry = ttk.Entry(self.taw_frame, textvariable=self.task_to_add)
        self.taw_task_add_entry.grid(column=1, row=0, sticky=NSEW)

        self.taw_task_add_btn = ttk.Button(self.taw_frame, text='Add', command=placeholder_command)
        self.taw_task_add_btn.grid(column=2, row=0, sticky=NSEW)

        self.taw_cancel_button = ttk.Button(self.taw_frame, text='Cancel', command=self.close_taw)
        self.taw_cancel_button.grid(column=3, row=0, sticky=NSEW)

    def close_taw(self):
        self.taw.destroy()



def placeholder_command():
    pass

class JobAddWindow():
    def __init__(self, momma) -> None:
        self.ja = Toplevel()
        self.ja.title(f"Py Job Search {version_num} (JOB ADD)")
        self.ja.minsize(900, 500)
        self.ja.columnconfigure(0, weight=1)
        self.ja.rowconfigure(0, weight=1)
        
        self.momma = momma

        self.ja_title = StringVar()
        self.ja_salary = StringVar()
        self.ja_company = StringVar()
        self.ja_company_site = StringVar()
        
        self.ja_company_details_frame = ttk.Labelframe(self.ja, text='Enter Details')
        self.ja_company_details_frame.grid(column=0, row=0, sticky=NSEW)

        self.ja_job_title = ttk.Label(self.ja_company_details_frame, text="Title:")
        self.ja_job_title.grid(column=0, row=0, sticky=NSEW)
        self.ja_job_title_entry = ttk.Entry(self.ja_company_details_frame, textvariable=self.ja_title)
        self.ja_job_title_entry.grid(column=1, row=0)
        
        self.ja_job_salary = ttk.Label(self.ja_company_details_frame, text="Salary:")
        self.ja_job_salary.grid(column=0, row=1, sticky=NSEW)
        self.ja_job_salary_entry = ttk.Entry(self.ja_company_details_frame, textvariable=self.ja_salary)
        self.ja_job_salary_entry.grid(column=1, row=1, sticky=NSEW)
        
        self.ja_job_company = ttk.Label(self.ja_company_details_frame, text="Company:")
        self.ja_job_company.grid(column=0, row=2, sticky=NSEW)
        self.ja_job_company_entry = ttk.Entry(self.ja_company_details_frame, textvariable=self.ja_company)
        self.ja_job_company_entry.grid(column=1, row=2, sticky=NSEW)
        
        self.ja_job_site = ttk.Label(self.ja_company_details_frame, text="Company Site:")
        self.ja_job_site.grid(column=0, row=3, sticky=NSEW)
        self.ja_job_site_entry = ttk.Entry(self.ja_company_details_frame, textvariable=self.ja_company_site)
        self.ja_job_site_entry.grid(column=1, row=3, sticky=NSEW)
        
        # JOB DESCRIPTION INPUT # Column 0, Row 1
        
        self.ja_frame = ttk.Labelframe(self.ja, text="Paste Job Description:")
        self.ja_frame.grid(column=0, row=1, sticky=NSEW)
        
        self.job_desc_input_paste_frame = ttk.Frame(self.ja_frame)
        self.job_desc_input_paste_frame.grid(column=0, row=0, sticky=(N, S, E, W))
        self.job_desc_input_text = Text(self.job_desc_input_paste_frame, width=70, height=30)
        self.job_desc_input_text.grid(column=0, row=0, sticky=(N, S, E, W))
        self.popup_menu = Menu(self.ja, tearoff=0)
        self.popup_menu.add_command(label="Paste", command=self.paste)
        self.popup_menu.add_command(label="Select All", command=self.select_all)
        self.job_desc_input_text.bind('<Button-3>', self.right_click_menu)
        
        weight_assign(self.job_desc_input_paste_frame)
        
        self.ja_button_frame = ttk.Frame(self.ja)
        self.ja_button_frame.grid(column=1, row=2, sticky=NSEW)
        self.ja_button_add = ttk.Button(self.ja_button_frame, text='Add', command=self.job_add_button_clicked)
        self.ja_button_add.grid(column=0, row=0, sticky=NSEW)
        self.ja_button_close = ttk.Button(self.ja_button_frame, text='Cancel', command=self.close_ja_window)
        self.ja_button_close.grid(column=1, row=0, sticky=NSEW)

    def job_add_button_clicked(self):
        # Entity Extraction here
        desc = self.job_desc_input_text.get('1.0', 'end')
        doc = nlp(text=desc)
        labels = [(ent.text, ent.label_) for ent in doc.ents]
        skills = [ent for ent in labels if ent[1] == 'SKILL']
        # skill_objs = [Skill(len(jobs), ent[0]) for ent in skills]
        # job_add_reply(ja_title.get(), job_desc_input_text.get('1.0', 'end'), ja_job_company.get(), skills=['nothing yet'])
        Job(self.ja_title.get(), self.job_desc_input_text.get('1.0', 'end'), self.ja_job_company_entry.get(), skills=skills, frame=self.momma.next_steps_frame, jobs_var=self.momma.jobs_var, jobs_listbox=self.momma.jobs_listbox, job_skill_box=self.momma.skills_frame)
        print(jobs[len(jobs)-1].skills)

    def close_ja_window(self):
        self.ja.destroy()
    
    def right_click_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()
    def paste(self):
        self.job_desc_input_text.delete('1.0', 'end')
        self.job_desc_input_text.insert('1.0', self.momma.root.clipboard_get())
    def select_all(self):
        self.job_desc_input_text.tag_add('sel','1.0', 'end')


def stripe(listbox):
    for i in range(0, len(jobs), 2):
        listbox.itemconfigure(i, background='#f0f0ff')

class RemoveJobWindow:
    def __init__(self) -> None:
        self.rjw = Toplevel()
        self.rjw.title(f"Py Job Search {version_num} (JOB REMOVE)")
        self.rjw.minsize(900, 500)
        self.rjw.columnconfigure(0, weight=1)
        self.rjw.rowconfigure(0, weight=1)


def save_data():
    filename = filedialog.asksaveasfilename(initialfile='job_search.json', defaultextension=".json",filetypes=[("All Files","*.*"),("JAVASCRIPT OBJECT NOTATION","*.json")])
    with open(filename, 'wb') as f:
        # for i in jobs:
        pickle.dump(jobs[0].wrap_data(), f, pickle.HIGHEST_PROTOCOL)

def load_data():
    pass