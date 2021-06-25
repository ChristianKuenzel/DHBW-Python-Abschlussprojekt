# Copyright 2021
# DHBW Lörrach, Python Projekt: Lernbox/Merkbox
# Christian Künzel, Matr.Nr.: 3889521, <chriskuenzel@web.de>, https://github.com/ChristianKuenzel
#
# Content undergoes the terms of chosen licenses. See GitHub for more:
# https://github.com/ChristianKuenzel/...
#
# ______________________________________________________________________________________________________________________
# Imports
from tkinter import *
from localStoragePy import localStoragePy
import json


# # ______________________________________________________________________________________________________________________
# Classes
# Graphical User Interface
class Application(object):
    def __init__(self):
        # Create Window
        self.root = Tk()
        self.root.title('Training cards')
        self.root.geometry('1280x800')

        # Frames
        self.headline_fm = Frame(master=self.root, bg='#d1bc8a')
        self.headline_fm.pack(side='top', fill='x')

        # self.main_fm = Frame(master=self.root, bg='red')
        # self.main_fm.pack(side='bottom', fill='both')

        # self.question_fm = Frame()
        # self.response_fm = Frame()

        # Menu.
        # Menu bar
        self.menu_bar = Menu(self.root)

        # Box menu
        self.box_menu = Menu(self.menu_bar, tearoff=0)
        self.box_menu.add_command(label="Create new", command=self.create_box_window)
        self.box_menu.add_command(label="Load")
        self.box_menu.add_command(label="Search")
        self.box_menu.add_command(label="Remove", command=self.remove_box_window)
        self.menu_bar.add_cascade(label="Box", menu=self.box_menu)

        # Card menu
        self.card_menu = Menu(self.menu_bar, tearoff=0)
        self.card_menu.add_command(label="Create new", command=self.create_card_window)
        self.card_menu.add_command(label="Search")
        self.card_menu.add_checkbutton(label="Remove")
        self.menu_bar.add_cascade(label="Card", menu=self.card_menu)

        # Options menu
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.options_menu.add_command(label="Reset storage", command=self.reset_window)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)

        self.root.config(menu=self.menu_bar)

        # Labels
        self.headline_lb = Label(master=self.headline_fm, font=("Courier", 28),
                                 text="Learning with training cards!", bg='#d1bc8a', fg="black", height=3)
        self.headline_lb.pack()

        # Buttons
        self.skipQuestion_bt = Button(master=self.root, text="Skip", command=self.skip_question)
        self.skipQuestion_bt.pack()

        self.test_bt = Button(master=self.root, text="test", command=self.test)
        self.test_bt.pack()

        # Input field
        # User response to the given question.
        self.response_if = StringVar()
        self.response_if.set("Enter your suggestion ...")
        self.userResponse_if = Entry(master=self.root, textvariable=self.response_if)
        self.userResponse_if.pack()

        # Start WindowManager.
        self.root.mainloop()

    # Create a new top level window containing all inputs for box creation.
    def create_box_window(self):
        # New window
        box_window = Toplevel(self.root)
        box_window.title("Create new box")
        box_window.geometry("400x600")

        # Labels.
        # Introduction
        task = Label(master=box_window, text="Insert the boxs new name below and click on Create:")
        task.pack()

        # Input fields.
        # Name of a box.
        box_name_if = StringVar()
        box_name_if.set("Enter box name ...")
        create_box_if = Entry(master=box_window, textvariable=box_name_if)
        create_box_if.pack()

        # Buttons.
        # Create a new box
        create_box_bt = Button(master=box_window, text="Create", command=lambda: self.create_new_box(box_name_if))
        create_box_bt.pack()

        # Cancel box creation
        cancel_task_bt = Button(master=box_window, text="Cancel", command=self.test2)
        cancel_task_bt.pack()

    # Create a new top level window containing all inputs for card creation.
    def create_card_window(self):
        # New window.
        card_window = Toplevel(self.root)
        card_window.title("Create new card")
        card_window.geometry("400x600")

        # Labels.
        # Introduction
        task = Label(master=card_window, text="Insert the cards name, question and solution below and click on Create:")
        task.pack()

        # Input fields.
        # Name of a card.
        card_name_if = StringVar()
        card_name_if.set("Enter card name ...")
        create_name_if = Entry(master=card_window, textvariable=card_name_if)
        create_name_if.pack()

        # Question of a card.
        card_question_if = StringVar()
        card_question_if.set("Enter question ...")
        create_question_if = Entry(master=card_window, textvariable=card_question_if)
        create_question_if.pack()

        # Solution of the card.
        card_solution_if = StringVar()
        card_solution_if.set("Enter solution ...")
        create_solution_if = Entry(master=card_window, textvariable=card_solution_if)
        create_solution_if.pack()

        # Buttons.
        # Create a new card.
        create_card_bt = Button(master=card_window, text="Create",
                                command=self.create_card(card_name_if, card_question_if, card_solution_if))
        create_card_bt.pack()

        # Cancel box creation
        cancel_task_bt = Button(master=card_window, text="Cancel", command=self.test3)
        cancel_task_bt.pack()

    # Safety warning before resetting the storage. All data will be lost.
    def reset_window(self):
        # New window.
        reset_window = Toplevel(self.root)
        reset_window.title("WARNING: Data loss!")
        reset_window.geometry("400x100")

        # Labels.
        # Warning message
        warning_msg = Label(master=reset_window, text="Are you sure about deleting all data stored?")
        warning_msg.pack()
        warning2_msg = Label(master=reset_window, text="You wont be able to restore any data after this process.")
        warning2_msg.pack()

        # Buttons.
        # Delete all data.
        clear_storage_bt = Button(master=reset_window, text="Delete", command=self.shutdown_application_window)
        clear_storage_bt.pack()

        # Abort process.
        abort_process_bt = Button(master=reset_window, text="Abort", command=self.test3)
        abort_process_bt.pack()

    # Create a new top level window containing all inputs for box creation.
    def remove_box_window(self):
        # New window
        box_window = Toplevel(self.root)
        box_window.title("Delete box")
        box_window.geometry("400x600")

        # Labels.
        # Introduction
        task = Label(master=box_window, text="Insert the boxs name below and click on Delete:")
        task.pack()

        # Input fields.
        # Name of a box.
        box_name_if = StringVar()
        box_name_if.set("Enter box name ...")
        remove_box_if = Entry(master=box_window, textvariable=box_name_if)
        remove_box_if.pack()

        # Buttons.
        # Create a new box
        remove_box_bt = Button(master=box_window, text="Remove", command=lambda: remove_box_from_storage(self, box_name_if))
        remove_box_bt.pack()

        # Cancel box creation
        cancel_task_bt = Button(master=box_window, text="Cancel", command=self.test2)
        cancel_task_bt.pack()

    # Reset storage and close application.
    def shutdown_application_window(self):
        # Close old reset window.
        # reset_window.quit()
        # reset_window.destroy()

        # Create shut down window.
        self.pop_up_info_window("Program shutdown", "400x100", "The application will be shut down in the process.",
                                "Close", self.reset_and_close_application)

    def reset_and_close_application(self):
        reset_storage()
        self.root.quit()
        self.root.destroy()


    """
    # Close the window by cancel button
    def cancel_window(self, window):
        try:
            window.quit()
            window.destroy()

        except:
            # Error response.
            error_msg = "We are sorry to inform you canceling caused an error."
            self.error_occured("400x80", error_msg)

    def error_occured(self, resolution, error_msg):
        # Create error window
        error_cancel_window = Toplevel(self.root)
        error_cancel_window.title("Error occured!")
        error_cancel_window.geometry(resolution)

        # Print Message
        error_msg_lb = Label(master=error_cancel_window, text=error_msg)
        error_msg_lb.pack()

        # Close application
        close_application_bt = Button(master=error_cancel_window, text="Close Application", command=self.close_application)
        close_application_bt.pack()

    def close_application(self):
        self.root.quit()
        self.root.destroy()"""

    # Create a new box and add itself to storage
    def create_new_box(self, box_name):
        # Create the box object itself.
        box = Box()

        # Read in the values.
        box.name = box_name.get()

        # Store the box.
        add_box_to_storage(self, box.name, box.__dict__)

    def pop_up_info_window(self, title, resolution, text_msg, text_button, cmd):
        # New window.
        info_wd = Toplevel(self.root)
        info_wd.title(title)
        info_wd.geometry(resolution)

        # Labels.
        # User Information
        info_wd_msg = Label(master=info_wd, text=text_msg)
        info_wd_msg.pack()

        # Buttons.
        # Delete all data.
        confirm_bt = Button(master=info_wd, text=text_button, command=cmd) # command=info_wd.destroy()
        confirm_bt.pack()

    # Create a new card and add itself into a box.
    def create_card(self, card_name, card_question, card_solution):
        # Create the card object itself
        card = Card()

        # Read in the values
        card.name = card_name.get()
        card.question = card_question.get()
        card.solution = card_solution.get()

        # Store the card
        #

    def next_card(self):
        return

    def skip_question(self):
        return

    def number_of_cards(self):
        return

    def test(self):
        print("test")

    def test2(self):
        print("test2")

    def test3(self):
        print("test3")


# Vocabulary Card containing question, solution, tier and attempts.
class Card(object):
    def __init__(self):
        self.id = id(self)
        self.tier = 1

        self.name = "default"
        self.question = "default"
        self.solution = "default"

        self.attempts = 0
        self.success = 0

    def increase_attempts(self):
        self.attempts += 1

    def reset_attempts(self):
        self.attempts = 0

    def increase_tier(self):
        self.tier += 1


# Box containing cards
class Box(object):
    def __init__(self):
        self.name = "default"
        self.card_dict = dict()
        self.amount_of_cards = 0

    def amount_of_cards(self):
        self.amount_of_cards = len(self.card_dict)
        return self.amount_of_cards


# ______________________________________________________________________________________________________________________
# Storage functions with localStorage. Converting with json included.
# Add new item to storage system by get, add and set.
# List of boxes need to be updated and overwritten.
# Object need to be stored by its name.
def add_box_to_storage(app_obj, item_name, item):
    # Get list of boxes as dictionary.
    lob = get_item_convert_json_to_py("list_of_boxes")

    # Check if item already exists.
    if item_name in lob:
        app_obj.pop_up_info_window("Item already exists!", "400x100",
                                   "The box you are trying to create already exists.", "Ok", app_obj.test)

    else:
        # Add key-value pair.
        lob[item_name] = item

        # Set dictionary into storage.
        set_item_convert_py_to_json("list_of_boxes", lob)

        # Check if item got stored correctly.
        new_lob = get_item_convert_json_to_py("list_of_boxes")
        if item_name in new_lob:
            app_obj.pop_up_info_window("Info Message", "400x100", "Creating box successfully!", "Ok", app_obj.test)

        else:
            # Failure
            app_obj.pop_up_info_window("Info Message", "400x100", "WARNING: Creating box failed!", "Ok", app_obj.test2)


# Remove box item by item name and update list of boxes.
def remove_box_from_storage(app_obj, item_name):
    # Get list of boxes as dictionary
    item_name = item_name.get()
    lob = get_item_convert_json_to_py("list_of_boxes")

    if item_name in lob:
        # Delete item in dictionary. Dictionary mutates.
        del lob[item_name]
        set_item_convert_py_to_json("list_of_boxes", lob)

        # Check if item got deleted correctly.
        new_lob = get_item_convert_json_to_py("list_of_boxes")
        if item_name not in new_lob:
            app_obj.pop_up_info_window("Info Message", "400x100", "Deleting box successfully!", "Ok", app_obj.test)

        else:
            # Failure
            app_obj.pop_up_info_window("Info Message", "400x100", "WARNING: Deleting box failed!", "Ok", app_obj.test2)

    else:
        app_obj.pop_up_info_window("Item doesnt exist!", "400x100",
                                   "The item you are trying to delete doesnt exist.", "Ok", app_obj.test)


# Empty the whole storage. All data will be lost.
def reset_storage():
    localStorage.clear()


# ______________________________________________________________________________________________________________________
# JSON converter functions. Get/Set with localStorage included.
# Get any item from storage and convert it from json to py.
def get_item_convert_json_to_py(item_name):
    return json.loads(localStorage.getItem(item_name))


# Convert any item from py to json and set it into storage.
def set_item_convert_py_to_json(item_name, item):
    localStorage.setItem(item_name, json.dumps(item))


# # ______________________________________________________________________________________________________________________
# Main
if __name__ == '__main__':
    # Initialize storage.
    localStorage = localStoragePy("python.merkbox", "sqlite")

    # Check if list of all boxes exists, otherwise create new dict.
    if localStorage.getItem("list_of_boxes") is None:
        set_item_convert_py_to_json("list_of_boxes", dict())

    # Run application.
    app = Application()

    print(localStorage.getItem("list_of_boxes"))
