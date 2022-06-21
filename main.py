
from tkinter import *
import json
import os
from datetime import date

def get_data_form_file():
    if os.path.exists("todo_dict.json"):
        with open("todo_dict.json", "r") as file:
            dict_todo = json.load(file)
    else:
        dict_todo = {}

    todo_number = 1 if not dict_todo else int(max(dict_todo.keys())) + 1
    return dict_todo, todo_number

# This window pops up to create a new task (called with the button "+ Add a task"
def open_new_task_window(main_window):  # Create the pop up window
    task_definition_window = Toplevel()
    task_definition_window.geometry("500x300")
    task_definition_window.title("New task")
    task_definition_window.configure(bg="lightgreen")
    task_definition_window.iconbitmap("todo.ico")

    new_task_frame = Frame(task_definition_window,
                                width=100,
                                height=100,
                                bg="skyblue")
    new_task_frame.pack()

    task_name_label = Label(new_task_frame,
                                    text="New task : ",
                                    bg="darkgreen",
                                    fg="white",
                                    width=10)
    task_name_label.grid(row=0, column=0)

    task_name_entry = Entry(new_task_frame, width=40)
    task_name_entry.grid(row=0, column=1, columnspan=3)

    task_deadline_label = Label(new_task_frame,
                                        text="Deadline : ",
                                        bg="darkgreen",
                                        fg="white")
    task_deadline_label.grid(row=1, column=0)

    # START OPTION MENU TO SELECT THE DEADLINE -----------------------------------------------
    option_list_year = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010,
                        2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020,
                        2021, 2022, 2023, 2024, 2025, 2026, 2027, 2028, 2029, 2030,
                        2031, 2032, 2033, 2034, 2035, 2036, 2037, 2038, 2039, 2040]

    year_variable = IntVar(new_task_frame)
    year_variable.set(date.today().year)
    year_option_menu = OptionMenu(new_task_frame, year_variable, *option_list_year)
    year_option_menu.grid(row=1, column=1)

    option_list_month = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12]
    month_variable = IntVar(new_task_frame)
    month_variable.set(date.today().month)
    month_option_menu = OptionMenu(new_task_frame, month_variable, *option_list_month)
    month_option_menu.grid(row=1, column=2)

    option_list_day = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17,
                        18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
    day_variable = IntVar(new_task_frame)
    day_variable.set(date.today().day)
    day_option_menu = OptionMenu(new_task_frame, day_variable, *option_list_day)
    day_option_menu.grid(row=1, column=3)

    # END OF OPTION MENU TO SELECT THE DEADLINE -----------------------------------------------

    validation_button = Button(new_task_frame, text="Create", command=lambda: create_new_task(task_name_entry.get(), date(year_variable.get(), month_variable.get(), day_variable.get()), task_definition_window), width=20)
    validation_button.grid(row=2, column=0, columnspan=5)

    task_definition_window.mainloop()

def create_new_task(description, deadline, task_definition_window):  # add the created new task to the mapping and save it into json file
    dict_todo, todo_number = get_data_form_file()
    if description:
        dict_todo[todo_number] = {
            "description": description,
            "deadline": deadline.isoformat(),
            "priority": "important",
            "status": "active",
        }
    print(dict_todo)
    with open("todo_dict.json", "w") as file:
        json.dump(dict_todo, file, indent=4)
    task_definition_window.destroy()



# This is the main window of the app where :
# - the todos are displayed and
# - some buttons lead to other actions
# Each todo has a unique todo_number. This number is incremented everytime a new task is created

# GETTING A MAPPING OF EXISTING TODOS OR CREATING A NEW ONE :
# (I made it a class attribute because it is easier to reach it after)


FILTER = "important"

# create the main window
root = Tk()
root.title("Todo application")
root.iconbitmap("todo.ico")
root.configure(bg="lightgreen")

# CREATE A TOP FRAME TO PACK THE MAIN OPTIONS -----------------------------
options_frame = Frame(root, bg="lightgreen")
options_frame.pack()

filter_label = Label(options_frame,
                        text=FILTER,
                        font=14,
                        width=50,
                        bg= "lightgreen")
filter_label.grid(row=0, column=1)

new_task_button = Button(options_frame,
                            text="+ Add a task",
                            font=14,
                            width=15,
                            height=2,
                            command=lambda: open_new_task_window(root))
new_task_button.grid(row=0, column=3)

# CREATE A FRAME TO DISPLAY THE TASKS TO DO ------------------------------------------
tasks_list_frame = LabelFrame(root, text="Task to do", bg="skyblue")
tasks_list_frame.pack()
dict_todo, todo_number = get_data_form_file()

for task_number, task_parameters in dict_todo.items():
    if task_parameters["priority"] == FILTER:
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
root.mainloop()




def todo_modification(self):
    pass


# class Todo:
#     def __init__(self):
#         self.description = ""
#         self.deadline = date(1978, 3, 30)
#         self.priority = "important"
#         self.status = "active"



