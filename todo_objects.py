
import json
import os
from tkinter import *
from datetime import date


class TodoMainWindow:

    # This is the main window of the app where :
    # - the todos are displayed and
    # - some buttons lead to other actions
    # Each todo has a unique todo_number. This number is incremented everytime a new task is created

    # GETTING A MAPPING OF EXISTING TODOS OR CREATING A NEW ONE :
    # (I made it a class attribute because it is easier to reach it after)

    if os.path.exists("todo_dict.json"):
        with open("todo_dict.json", "r") as file:
            DICT_TODO = json.load(file)
    else:
        DICT_TODO = {}

    TODO_NUMBER = 1 if not DICT_TODO else int(max(DICT_TODO.keys())) + 1
    FILTER = "important"

    def __init__(self):  # create the main window
        self.root = Tk()
        self.root.title("Todo application")
        self.root.iconbitmap("todo.ico")
        self.root.configure(bg="lightgreen")
        self.new_task_registration = None
        self.display_tasks()

        self.root.mainloop()

    def display_tasks(self):  # create the widgets to display inside the main window

        # CREATE A TOP FRAME TO PACK THE MAIN OPTIONS -----------------------------
        options_frame = Frame(self.root)
        options_frame.pack()

        filter_label = Label(options_frame,
                             text=TodoMainWindow.FILTER,
                             font=14,
                             width=50)
        filter_label.grid(row=0, column=1)

        new_task_button = Button(options_frame,
                                 text="+ Add a task",
                                 font=14,
                                 width=15,
                                 height=2,
                                 command=self.open_new_task_window)
        new_task_button.grid(row=0, column=3)

        # CREATE A FRAME TO DISPLAY THE TASKS TO DO ------------------------------------------

        tasks_list_frame = LabelFrame(self.root, text="Task to do", bg="skyblue")
        tasks_list_frame.pack()
        for task_number, task_parameters in TodoMainWindow.DICT_TODO.items():
            if task_parameters["priority"] == TodoMainWindow.FILTER:
                task_frame = LabelFrame(tasks_list_frame, bg="darkgreen", padx=30, pady=5)
                task_frame.pack(fill="both", expand="yes", padx=10, pady=10)

                var = StringVar()
                check_box = Checkbutton(task_frame,
                                        variable=var,
                                        onvalue="archive",
                                        offvalue="active",
                                        bg="darkgreen")
                check_box.deselect()
                check_box.grid(row=0, column=0)

                description_label = Label(task_frame,
                                          text=task_parameters["description"],
                                          bd=4,
                                          justify=LEFT,
                                          bg="darkgreen",
                                          fg="white",
                                          width=50,
                                          font=("blackarial", 14))
                description_label.grid(row=0, column=1)

                deadline_label = Label(task_frame,
                                       text=task_parameters["deadline"],
                                       bg="darkgreen",
                                       fg="white")
                deadline_label.grid(row=0, column=2)

    def open_new_task_window(self):
        self.new_task_registration = NewTaskWindow(self.root)


class NewTaskWindow:  # This window pop up to create a new task (called with the button "+ Add a task"
    def __init__(self, main_window):  # Create the pop up window
        self.main_window = main_window
        self.new_task = Todo()
        print(self.new_task.deadline)
        self.task_definition_window = Toplevel()
        self.task_definition_window.geometry("500x300")
        self.task_definition_window.title("New task")
        self.task_definition_window.configure(bg="lightgreen")
        self.task_definition_window.iconbitmap("todo.ico")

        self.new_task_frame = Frame(self.task_definition_window,
                                    width=100,
                                    height=100,
                                    bg="skyblue")
        self.new_task_frame.pack()

        self.task_name_label = Label(self.new_task_frame,
                                     text="New task : ",
                                     bg="darkgreen",
                                     fg="white",
                                     width=10)
        self.task_name_label.grid(row=0, column=0)

        self.task_name_entry = Entry(self.new_task_frame, width=40)
        self.task_name_entry.grid(row=0, column=1, columnspan=3)

        self.task_deadline_label = Label(self.new_task_frame,
                                         text="Deadline : ",
                                         bg="darkgreen",
                                         fg="white")
        self.task_deadline_label.grid(row=1, column=0)

        # START OPTION MENU TO SELECT THE DEADLINE -----------------------------------------------
        option_list_year = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
                            2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
                            2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030,
                            2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040]

        year_variable = IntVar(self.new_task_frame)
        year_variable.set(date.today().year)
        year_option_menu = OptionMenu(self.new_task_frame, year_variable, *option_list_year)
        year_option_menu.grid(row=1, column=1)

        option_list_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        month_variable = IntVar(self.new_task_frame)
        month_variable.set(date.today().month)
        month_option_menu = OptionMenu(self.new_task_frame, month_variable, *option_list_month)
        month_option_menu.grid(row=1, column=2)

        option_list_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                           18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
        day_variable = IntVar(self.new_task_frame)
        day_variable.set(date.today().day)
        day_option_menu = OptionMenu(self.new_task_frame, day_variable, *option_list_day)
        day_option_menu.grid(row=1, column=3)

        deadline = date(year_variable.get(), month_variable.get(), day_variable.get())
        print(deadline)
        # END OF OPTION MENU TO SELECT THE DEADLINE -----------------------------------------------

        self.validation_button = Button(self.new_task_frame, text="Create", command=self.create_new_task, width=20)
        self.validation_button.grid(row=2, column=0, columnspan=5)

        self.task_definition_window.mainloop()

    def create_new_task(self):  # add the created new task to the mapping and save it into json file
        if self.task_name_entry.get():
            TodoMainWindow.DICT_TODO[TodoMainWindow.TODO_NUMBER] = {
                "description": self.task_name_entry.get(),
                "deadline": self.new_task.deadline.isoformat(),
                "priority": "important",
                "status": "Nothing yet",
            }
            TodoMainWindow.TODO_NUMBER += 1
        with open("todo_dict.json", "w") as file:
            json.dump(TodoMainWindow.DICT_TODO, file, indent=4)
        print(TodoMainWindow.DICT_TODO)
        self.task_definition_window.destroy()

    def todo_modification(self):
        pass


class Todo:
    def __init__(self):
        self.description = ""
        self.deadline = date(1978, 3, 30)
        self.priority = "important"
        self.status = "active"
