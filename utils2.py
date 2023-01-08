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

chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'

matcher = PhraseMatcher(nlp.vocab)

ruler = nlp.add_pipe("entity_ruler", before='ner').from_disk(skills_list)

version_num = 0.10

jobs = []

class Skill:
    def __init__(self, parent_job, desc) -> None:
        self.parent = parent_job
        self.desc = desc[0]
    def __repr__(self) -> str:
        return f'{self.desc} a skill for {self.parent.title} at {self.parent.company}'

class Task:
    def __init__(self, parent_job, desc) -> None:
        self.parent = parent_job
        self.desc = desc
        self.parent.task_complete_dict[self.desc] = 0
        self.status = IntVar() ### BROKEN!! TODO fix the saving system
        self.status.set(self.parent.task_complete_dict[self.desc])
        self.parent.task_values[self.desc] = self.status
        # self.status = 0
    def __repr__(self) -> str:
        return f'{self.desc} a task for {self.parent.title} at {self.parent.company}'
    def pack_it_up(self):
        self.status = self.status.get()
        self.parent.task_values[self.desc] = self.status
    def unpack_it_down(self):
        # self.parent.task_complete_dict[self.desc] = loaded_data
        self.status = IntVar() ### BROKEN!! TODO fix the saving system
        self.status.set(self.parent.task_complete_dict[self.desc])
        self.parent.task_values[self.desc] = self.status

class Job:
    def __init__(self, title, desc, company, site, salary, skills) -> None:
        self.id = len(jobs)
        self.title = title
        self.desc = desc
        self.company = company
        self.site = site
        self.salary = salary
        self.skills = [Skill(self, skill) for skill in skills]
        tasks = [
            'Finish Applying',
            'Contact Hireing Manager',
            'Phone Screen',
            'Interview',
            'Technical Assessments',
            'Additional Interview',
            'Offer Extension',
            'Acceptance!'
        ]
        self.task_complete_dict = {}
        self.task_values = {} # task_values messes with the saving system TODO fix BUG
        self.tasks = [Task(self, task) for task in tasks]
        self.notes = ''
        jobs.append(self)
    def __repr__(self) -> str:
        return f'{self.title} at {self.company}'
    def remove_job(self):
        jobs.remove(jobs[self.id])
    def add_task(self, desc):
        self.tasks.append(Task(self, desc=desc))
    def add_skill(self, desc):
        self.skills.append(Skill(self, desc=desc))
    def add_notes(self, notes):
        self.notes = notes
    def pack_up(self):
        for i in self.tasks:
            i.pack_it_up()
        self.task_complete_dict = self.task_values
    def load_in(self):
        for i in range(len(self.tasks)):
            self.tasks[i].unpack_it_down()


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
        self.company_site_var = StringVar()
        self.company_site_disp = ttk.Label(self.title_w_links, textvariable=self.company_site_var)
        self.company_site_disp.grid(column=1, row=1, sticky=NSEW)
        self.company_site_btn = ttk.Button(self.title_w_links, text='Company Site', command=lambda: webbrowser.get(chrome_path).open_new_tab(self.company_site_var.get()))
        self.company_site_btn.grid(column=1, row=2, sticky=NSEW)

        # JOBS APPLIED TO LISTBOX # Column 0, row 1

        self.jobs_var = StringVar(value=jobs)
        self.jobs_listbox_frame = ttk.Labelframe(self.main_frame, text='Jobs Applied To')
        self.jobs_listbox_frame.grid(column=0, row=1, sticky=NSEW, rowspan=2)
        self.jobs_listbox = Listbox(self.jobs_listbox_frame, height=30, listvariable=self.jobs_var)
        self.jobs_listbox.grid(column=0, row=0, sticky=NSEW)
        self.jobs_listbox.bind('<<ListboxSelect>>', lambda e: self.listbox_updater())

        # NEXT STEPS SECTION # Column 1, row 1

        self.next_steps_frame = ttk.Labelframe(self.main_frame, text="Next Steps (tasks)")
        self.next_steps_frame.grid(column=1, row=1, sticky=(N, S, E, W), rowspan=2)
        
        # JOB DESCRIPTION OF SEARCH # Column 2, Row 1

        self.job_desc_search_frame = ttk.Labelframe(self.main_frame, text="Job Description")
        self.job_desc_search_frame.grid(column=2, row=1, sticky=(N, S, E, W))
        self.job_desc_disp = Text(self.job_desc_search_frame, width=70, height=30)
        self.job_desc_disp.grid(column=0, row=0, sticky=(N, S, E, W))
        self.job_desc_disp.insert('1.0', 'Something')
        self.job_desc_scroll_bar = ttk.Scrollbar(self.job_desc_search_frame, orient='vertical', command=self.job_desc_disp.yview)
        self.job_desc_scroll_bar.grid(column=1, row=0, sticky=NSEW)
        self.job_desc_disp['yscrollcommand'] = self.job_desc_scroll_bar.set

        # JOB SKILLS # Column 2, Row 2

        self.skills_frame = ttk.Labelframe(self.main_frame, text="Job Skills")
        self.skills_frame.grid(column=2, row=2, sticky=NSEW, columnspan=2)

        # NOTE ADD # Column 3, row 1

        self.note_frame = ttk.Labelframe(self.main_frame, text='Notes:')
        self.note_frame.grid(column=3, row=1, sticky=NSEW)

        self.note_entry = Text(self.note_frame, width=35, height=30)
        self.note_entry.grid(column=0, row=0, sticky=NSEW)

        test_job_1 = Job('Developer', 'Be a coder', 'apple', 'www.apple.com', '50000', [('yoga', 'skill'), ('putting up with shit', 'SKILL')])
        test_job_2 = Job('Developer', 'Be a coder', 'apple', 'www.apple.com', '50000', [('yoga', 'skill'), ('putting up with shit', 'SKILL')])
        test_job_3 = Job('Developer', 'Be a coder', 'apple', 'www.apple.com', '50000', [('yoga', 'skill'), ('putting up with shit', 'SKILL')])

        root.option_add('*tearOff', FALSE)
        menubar = Menu(root)
        root['menu'] = menubar
        menu_file = Menu(menubar)
        menu_edit = Menu(menubar)
        menubar.add_cascade(menu=menu_file, label='File')
        menubar.add_cascade(menu=menu_edit, label='Edit')
        menu_file.add_command(label='New', command=placeholder_command)
        menu_file.add_command(label='Open...', command=load_data)
        menu_file.add_command(label='Save', command=lambda: save_data(self))
        menu_file.add_command(label='Add Jobs', command=self.job_add_window)
        menu_file.add_command(label='Remove Jobs', command=lambda: JobRemoveWindow(self))
        
        menu_edit.add_command(label='Add Task', command=self.task_add_btn)
        menu_edit.add_command(label='Remove Task', command=lambda: RemoveTaskWindow(self, self.jobs_listbox.curselection()))

        self.popup_menu = Menu(self.main_frame, tearoff=0)
        self.popup_menu.add_command(label="Paste", command=self.paste)
        self.popup_menu.add_command(label="Select All", command=self.select_all)
        self.note_entry.bind('<Button-3>', self.right_click_menu)
    
        self.jobs_listbox.selection_set(0)
        self.update((0, 1))

    def paste(self):
        self.note_entry.insert(INSERT, self.root.clipboard_get())
    def select_all(self):
        self.note_entry.tag_add('sel','1.0', 'end')
    
    def right_click_menu(self, event):
        try:
            self.popup_menu.tk_popup(event.x_root, event.y_root, 0)
        finally:
            self.popup_menu.grab_release()

    def listbox_updater(self):
        try:
            jobs[self.previous_selection].add_notes(self.note_entry.get('1.0', 'end'))
        finally:
            self.update(self.jobs_listbox.curselection())

    def populate_listbox(self):
        self.jobs_var.set(jobs)
        stripe(self.jobs_listbox)


    def weight_assign(self, object, x=1, y=1):
        size = object.grid_size()
        for i in range(size[0]):
            object.columnconfigure(i, weight=x)
        for j in range(size[1]):
            object.rowconfigure(j, weight=y)
    def update(self, index):
        indx = index[0]
        self.job_desc_disp['state'] = 'normal'
        self.job_desc_disp.delete('1.0', 'end')
        self.job_desc_disp.insert('1.0', jobs[indx].desc)
        self.job_desc_disp['state'] = 'disabled'
        self.title_disp_var.set(jobs[indx].title)
        self.company_name_var.set(jobs[indx].company)
        self.company_site_var.set(jobs[indx].site)
        self.salary_disp_var.set(jobs[indx].salary)
        self.note_entry.delete('1.0', 'end')
        self.note_entry.insert('1.0', jobs[indx].notes)
        try:
            self.task_check_box_frame.destroy()
            self.task_check_box_frame = ttk.Frame(self.next_steps_frame)
        except:
            self.task_check_box_frame = ttk.Frame(self.next_steps_frame)
        finally:
            self.task_check_box_frame.grid(column=0, row=0, sticky=NSEW)
        for i in jobs[indx].tasks:
            self.task_check_box = ttk.Checkbutton(self.task_check_box_frame, text=i.desc, variable=i.status)
            self.task_check_box.grid(column=0, row=jobs[indx].tasks.index(i), sticky=(E, W))
        try:
            self.skill_disp_frame.destroy()
            self.skill_disp_frame = ttk.Frame(self.skills_frame)
        except:
            self.skill_disp_frame = ttk.Frame(self.skills_frame)
        finally:
            self.skill_disp_frame.grid(column=0, row=0, sticky=NSEW)
        for j in jobs[indx].skills:
            self.skill_disp = ttk.Label(self.skill_disp_frame, text=j.desc)
            self.skill_disp.pack(side="left")
        self.previous_selection = indx

    def job_add_window(self):
        JobAddWindow(self)
    
    def task_add_btn(self):
        TaskAddWindow(momma=self, job=self.jobs_listbox.curselection())

class JobAddWindow():
    def __init__(self, momma) -> None:
        self.ja = Toplevel()
        self.ja.title(f"Py Job Coach {version_num} (JOB ADD)")
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
        Job(self.ja_title.get(), self.job_desc_input_text.get('1.0', 'end'), self.ja_job_company_entry.get(), skills=skills, site=self.ja_job_site_entry.get(), salary=self.ja_job_salary_entry.get())
        self.momma.populate_listbox()
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

class TaskAddWindow():
    def __init__(self, momma, job) -> None:  
        self.taw = Toplevel()
        self.taw.title(f"Py Job Coach {version_num} (TASK ADD)")
        # self.taw.minsize(500, 300)
        self.taw.columnconfigure(0, weight=1)
        self.taw.rowconfigure(0, weight=1)

        self.momma = momma
        self.indx = job[0]
        self.job = jobs[self.indx]

        self.taw_frame = ttk.Frame(self.taw)
        self.taw_frame.grid(column=0, row=0, sticky=NSEW)

        self.taw_task_add_label = ttk.Label(self.taw_frame, text="Add Task:")
        self.taw_task_add_label.grid(column=0, row=0, sticky=NSEW)

        self.task_to_add = StringVar()

        self.taw_task_add_entry = ttk.Entry(self.taw_frame, textvariable=self.task_to_add)
        self.taw_task_add_entry.grid(column=1, row=0, sticky=NSEW)

        self.taw_task_add_btn = ttk.Button(self.taw_frame, text='Add', command=self.add_task)
        self.taw_task_add_btn.grid(column=2, row=0, sticky=NSEW)

        self.taw_cancel_button = ttk.Button(self.taw_frame, text='Cancel', command=self.close_taw)
        self.taw_cancel_button.grid(column=3, row=0, sticky=NSEW)

    def close_taw(self):
        self.taw.destroy()
    def add_task(self):
        self.job.add_task(self.task_to_add.get())
        self.momma.update([self.indx, 'blank'])

class JobRemoveWindow:
    def __init__(self, momma) -> None:
        self.jrw = Toplevel()
        self.jrw.title(f"Py Job Coach {version_num} (JOB REMOVE)")
        self.jrw.minsize(900, 500)
        self.jrw.columnconfigure(0, weight=1)
        self.jrw.rowconfigure(0, weight=1)
        
        self.momma = momma

        self.jrw_frame = ttk.Frame(self.jrw)
        self.jrw_frame.grid(column=0, row=0, sticky=NSEW)

        for i in jobs:
            ttk.Button(self.jrw_frame, text=i, command=lambda: self.job_remover(i)).pack(side='bottom')
    def job_remover(self, job):
        job.remove_job()
        self.momma.populate_listbox()

class RemoveTaskWindow:
    def __init__(self, momma, job) -> None:
        self.rtw = Toplevel()
        self.rtw.title(f"Py Job Coach {version_num} (TASK REMOVE)")
        self.rtw.minsize(900, 500)
        self.rtw.columnconfigure(0, weight=1)
        self.rtw.rowconfigure(0, weight=1)

        self.momma = momma
        self.indx = job[0]
        self.job = jobs[self.indx]

        self.rtw_frame = ttk.Frame(self.rtw)
        self.rtw_frame.grid(column=0, row=0, sticky=NSEW)

        self.rtw_task_list_var = StringVar(value=self.job.tasks)

        self.rtw_listbox = Listbox(self.rtw_frame, height=30, listvariable=self.rtw_task_list_var)
        self.rtw_listbox.grid(column=0, row=0, sticky=NSEW)

        self.rtw_remove_btn = ttk.Button(self.rtw_frame, text='Remove', command=placeholder_command)
        self.rtw_remove_btn.grid(column=1, row=0, sticky=NSEW)

        self.rtw_cancel_btn = ttk.Button(self.rtw_frame, text='Cancel', command=self.close)
        self.rtw_cancel_btn.grid(column=2, row=0, sticky=NSEW)

    def close(self):
        self.rtw.destroy()

def placeholder_command():
    pass

def stripe(listbox):
    for i in range(0, len(jobs), 2):
        listbox.itemconfigure(i, background='#f0f0ff')

def load_data(**kwargs):
    global jobs
    file_name = kwargs.get('filename', None)
    if file_name:
        with open(file_name, 'rb') as f:
            jobs = pickle.load(f)
        for i in jobs:
            i.load_in()
    else:
        filename = filedialog.askopenfilename(initialfile='job_search.pysav', defaultextension=".pysav",filetypes=[("All Files","*.*"),("Py Save","*.pysav")])
        with open(filename, 'rb') as f:
            jobs = pickle.load(f)
        for i in jobs:
            i.load_in()

    

def save_data(parent):
    filename = filedialog.asksaveasfilename(initialfile='job_search.pysav', defaultextension=".pysav",filetypes=[("All Files","*.*"),("Py Save","*.pysav")])
    for i in jobs:
        i.pack_up()

    with open(filename, 'wb') as f:
        pickle.dump(jobs, f, pickle.HIGHEST_PROTOCOL)
    
    load_data(filename=filename)
    parent.update((0, 0))