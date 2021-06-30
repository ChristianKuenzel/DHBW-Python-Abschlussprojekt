# Copyright 2021
# DHBW Lörrach, Python Projekt: Lernbox/Merkbox
# Christian Künzel, Matr.Nr.: 3889521, <chriskuenzel@web.de>, https://github.com/ChristianKuenzel
#
# Content undergoes the terms of chosen licenses. See GitHub for more:
# https://github.com/ChristianKuenzel/DHBW-Python-Abschlussprojekt
#
# ______________________________________________________________________________________________________________________
# Imports
from tkinter import *
from localStoragePy import localStoragePy
# WARNING: Install Pillow instead of PIL!
from PIL import ImageTk, Image
import json


# ______________________________________________________________________________________________________________________
# Classes
# Graphical User Interface
class Application(object):
    def __init__(self):
        # Active objects.
        self.active_box = Box().__dict__
        self.active_card = Card().__dict__

        # Switches: De-/Activating functionality.
        # Toggle next button.
        # Change status if result got checked: Press Start -> false, Next -> false, Skip -> false, Check -> true.
        self.next_button_switch = False
        # Toggle skip button.
        # Change status if check was used: Press Start -> true, Next -> true, Skip -> true, Check -> False.
        self.skip_button_switch = True
        # -> Exact opposite
        # -> Next Button usable/active if Skip Button not usable/active and other way around.
        # -> Implementation due to overview and in case of changes in different situations.

        """Callbackfunktionen zur Farbänderung ? disabled -> grau/transparent ?"""

        # Create master window.
        self.root = Tk()
        self.root.title('Training cards')
        # Resolution: Width x Height.
        self.root.geometry('800x1000')

        # Frames -> GUI structure.
        # Master: Headline and main interaction.
        self.headline_fm = Frame(master=self.root, bg='#d1bc8a')
        self.headline_fm.place(x=0, y=0, width=800, height=95)

        self.main_interaction_fm = Frame(master=self.root, bg='#5e5e5e')
        self.main_interaction_fm.place(x=150, y=120, width=500, height=600)

        # Main interaction: Select active box and main activity
        self.select_box_fm = Frame(master=self.main_interaction_fm, bg='#FE2E2E')
        self.select_box_fm.place(x=0, y=0, width=500, height=60)

        self.activity_fm = Frame(master=self.main_interaction_fm, bg='#AC58FA')
        self.activity_fm.place(x=0, y=60, width=500, height=540)

        # Activity: All activities beside selecting active box.
        self.card_frame_fm = Frame(master=self.activity_fm, bg='#2EFEC8')
        self.card_frame_fm.place(x=20, y=20, width=460, height=470)

        self.button_frame_fm = Frame(master=self.activity_fm, bg='#D7DF01')
        self.button_frame_fm.place(x=20, y=490, width=460, height=50)

        # Card: Title, question, solution and user input.
        self.card_frame_title_fm = Frame(master=self.card_frame_fm, bg='#FF00BF')
        self.card_frame_title_fm.place(x=0, y=0, width=460, height=60)

        self.card_frame_question_fm = Frame(master=self.card_frame_fm, bg='#0101DF')
        self.card_frame_question_fm.place(x=0, y=60, width=460, height=140)

        self.card_frame_solution_fm = Frame(master=self.card_frame_fm, bg='#FF8000')
        self.card_frame_solution_fm.place(x=0, y=200, width=460, height=140)

        self.card_frame_input_fm = Frame(master=self.card_frame_fm, bg='#00FF00')
        self.card_frame_input_fm.place(x=0, y=340, width=460, height=130)

        # Card frame input:
        self.check_result_image_fm = Frame(master=self.card_frame_input_fm, bg='white')
        self.check_result_image_fm.place(relx=0.15, rely=0.5, width=40, height=40, anchor=CENTER)

        # Labels
        # Main title of GUI
        self.headline_lb = Label(master=self.headline_fm, font=("Courier", 28),
                                 text="Learning with training cards!", bg='#d1bc8a', fg="black", height=3)
        self.headline_lb.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Card frame title.
        self.visualize_card_name_lb = Label(master=self.card_frame_title_fm, text="Name")
        self.visualize_card_name_lb.place(relx=0.5, rely=0.5, width=250, height=30, anchor=CENTER)

        # Cards question.
        self.visualize_card_question_lb = Label(master=self.card_frame_question_fm, text="Question")
        self.visualize_card_question_lb.place(relx=0.5, rely=0.5, width=300, height=100, anchor=CENTER)

        # Cards solution.
        self.visualize_card_solution_lb = Label(master=self.card_frame_solution_fm, text="Solution")
        self.visualize_card_solution_lb.place(relx=0.5, rely=0.5, width=300, height=100, anchor=CENTER)

        # Result info image.
        self.green_checkmark_src = Image.open("green_checkmark.png")
        self.green_checkmark_src = self.green_checkmark_src.resize((40, 40), Image.ANTIALIAS)
        self.green_checkmark_img = ImageTk.PhotoImage(self.green_checkmark_src)
        self.red_cross_src = Image.open("red_x.png")
        self.red_cross_src = self.red_cross_src.resize((40, 40), Image.ANTIALIAS)
        self.red_cross_img = ImageTk.PhotoImage(self.red_cross_src)
        self.check_result_img = Label(master=self.check_result_image_fm, image="")
        self.check_result_img.place(relx=0.5, rely=0.5, anchor=CENTER)

        # Input field
        # User response to the given question.
        self.response_if = StringVar()
        self.response_if.set("Enter your suggestion ...")
        self.userResponse_if = Entry(master=self.card_frame_input_fm, textvariable=self.response_if)
        self.userResponse_if.place(relx=0.5, rely=0.5, width=200, height=40, anchor=CENTER)

        # Buttons.
        # Start the exercise by loading in the first card.
        self.card_num = 0
        self.start_exercise_bt = Button(master=self.button_frame_fm, text="Start",
                                        command=lambda: self.start_exercise(self.active_box))
        self.start_exercise_bt.place(relx=0.25, rely=0.5, width=60, height=30, anchor=CENTER)

        # Skip the given question.
        self.skipQuestion_bt = Button(master=self.button_frame_fm, text="Skip", command=self.skip_question)
        self.skipQuestion_bt.place(relx=0.5, rely=0.5, width=60, height=30, anchor=CENTER)

        # Load in the next card.
        self.next_card_bt = Button(master=self.button_frame_fm, text="Next",
                                   command=lambda: self.next_card(self.active_box))
        self.next_card_bt.place(relx=0.75, rely=0.5, width=60, height=30, anchor=CENTER)

        # Compare the user input/suggestion and the cards solution.
        self.check_result_bt = Button(master=self.card_frame_input_fm, text="Check",
                                      command=lambda: self.check_result(self.active_box, self.response_if))
        self.check_result_bt.place(relx=0.85, rely=0.5, width=60, height=30, anchor=CENTER)

        # OptionsMenu.
        # Select box you wanna work with (as active box).
        # Cast dict keys into list.
        self.box_option_list = list(get_item_convert_json_to_py("list_of_boxes").keys())
        self.select_box = StringVar()
        self.select_box.set(self.box_option_list[0])
        self.select_box_om = OptionMenu(self.select_box_fm, self.select_box, *self.box_option_list)
        self.select_box_om.config(width=20, font=('helvetica', 12))
        self.select_box_om.place(relx=0.5, rely=0.5, anchor=CENTER)
        # Add trace and callback method.
        self.select_box.trace("w", self.load_box_cb)

        # Menu.
        # Menu bar with various functions.
        self.menu_bar = Menu(self.root)

        # Box menu: Create, remove.
        self.box_menu = Menu(self.menu_bar, tearoff=0)
        self.box_menu.add_command(label="Create new", command=self.create_box_window)
        """self.box_menu.add_command(label="Search")"""
        self.box_menu.add_command(label="Remove", command=self.remove_box_window)
        self.menu_bar.add_cascade(label="Box", menu=self.box_menu)

        # Card menu: Create, Add to box, Remove.
        self.card_menu = Menu(self.menu_bar, tearoff=0)
        self.card_menu.add_command(label="Create new", command=self.create_card_window)
        self.card_menu.add_command(label="Add to box", command=self.add_card_to_box_window)
        """self.card_menu.add_command(label="Search")"""
        self.card_menu.add_checkbutton(label="Remove")
        self.menu_bar.add_cascade(label="Card", menu=self.card_menu)

        # Options menu: Reset storage.
        self.options_menu = Menu(self.menu_bar, tearoff=0)
        self.options_menu.add_command(label="Reset storage", command=self.reset_window)
        self.menu_bar.add_cascade(label="Options", menu=self.options_menu)

        self.root.config(menu=self.menu_bar)

        # Developer tools:
        """DevTools"""

        # Update widgets and keep the application running.
        self.root.mainloop()

    # Functions.
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
        cancel_task_bt = Button(master=box_window, text="Cancel", command=lambda: self.cancel_window(box_window))
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
                                command=lambda: self.create_new_card(card_name_if, card_question_if, card_solution_if))
        create_card_bt.pack()

        # Cancel box creation
        cancel_task_bt = Button(master=card_window, text="Cancel", command=lambda: self.cancel_window(card_window))
        cancel_task_bt.pack()

    # Callback function. Load box for active usage.
    def load_box_cb(self, *args):
        # Get list of boxes.
        lob = get_item_convert_json_to_py("list_of_boxes")
        # Change active box to chosen box.
        self.active_box = lob[self.select_box.get()]

    # Safety warning before resetting the storage. All data will be lost.
    def reset_window(self):
        # New window.
        reset_window = Toplevel(self.root)
        reset_window.title("WARNING: Data loss!")
        reset_window.geometry("400x120")

        # Labels.
        # Warning message
        warning_msg = Label(master=reset_window, text="Are you sure about deleting all data stored?")
        warning_msg.pack()
        warning2_msg = Label(master=reset_window, text="You wont be able to restore any data after this process.")
        warning2_msg.pack()
        warning3_msg = Label(master=reset_window, text="The application will be shut down in the process.")
        warning3_msg.pack()

        # Buttons.
        # Delete all data.
        clear_storage_bt = Button(master=reset_window, text="Delete", command=self.reset_storage)
        clear_storage_bt.pack()

        # Abort process.
        abort_process_bt = Button(master=reset_window, text="Abort", command=lambda: self.cancel_window(reset_window))
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
        remove_box_bt = Button(master=box_window, text="Remove",
                               command=lambda: remove_box_from_storage(self, box_name_if))
        remove_box_bt.pack()

        # Cancel box creation
        cancel_task_bt = Button(master=box_window, text="Cancel", command=lambda: self.cancel_window(box_window))
        cancel_task_bt.pack()

    # Reset storage and close application.
    def reset_storage(self):
        localStorage.clear()
        self.root.quit()
        self.root.destroy()

    # Close the window by cancel button.
    def cancel_window(self, window):
        try:
            window.destroy()

        except:
            # Error response.
            error_msg = "We are sorry to inform you 'Cancel' caused an error."
            self.error_occurred("400x80", error_msg)

    # Error window. Closing application.
    def error_occurred(self, resolution, error_msg):
        # Create error window
        error_cancel_window = Toplevel(self.root)
        error_cancel_window.title("Error occurred!")
        error_cancel_window.geometry(resolution)

        # Print Message
        error_msg_lb = Label(master=error_cancel_window, text=error_msg)
        error_msg_lb.pack()

        # Close application
        close_application_bt = Button(master=error_cancel_window, text="Close Application",
                                      command=lambda: [self.root.destroy(), self.root.quit()])
        close_application_bt.pack()

    # Create a new box and add itself to storage
    def create_new_box(self, box_name):
        # Create the box object itself.
        box = Box()

        # Read in the values.
        box.name = box_name.get()

        # Store the box.
        add_box_to_storage(self, box.name, box.__dict__)

    def pop_up_info_window(self, title, resolution, text_msg, text_button):
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
        confirm_bt = Button(master=info_wd, text=text_button, command=lambda: info_wd.destroy())
        confirm_bt.pack()

    # Create a new card and add itself into a box.
    def create_new_card(self, card_name, card_question, card_solution):
        # Create the card object itself
        card = Card()

        # Read in the values
        card.name = card_name.get()
        card.question = card_question.get()
        card.solution = card_solution.get()

        # Store the card
        add_card_to_storage(self, card.name, card.__dict__)

    # Start visualizing cards if available.
    def start_exercise(self, box):
        # Check if enough cards exist to start.
        # Hint: len(list(element1)) starts with 1 and list(element1) starts with pos. 0. (-> '>' instead of '>=')
        if len(list(box["card_dict"].items())) == 0:
            # As boxes can have a lot of cards i don't wanna iterate over the dict.
            # But to get the cards content by index instead of key-value i need to change the dict.
            # List cast gives me the possibility to use card_num as index, but messes up the  dicts within:
            # self.visualize_card_lb.configure(text=list(box["card_dict"].items())[0].question) -> Doesnt exist
            # self.visualize_card_lb.configure(text=list(box["card_dict"].items())[0][0][4]) -> Gives a letter ('s')
            # So i will call the card_dict, list cast its keys to grab the card_num-nth cards content by index.
            self.visualize_card_name_lb.configure(text="Empty")
            self.visualize_card_question_lb.configure(text="Empty")
            self.visualize_card_solution_lb.configure(text="Empty")

        elif len(list(box["card_dict"].items())) > 0:
            # As boxes can have a lot of cards i don't wanna iterate over the dict.
            # But to get the cards content by index instead of key-value i need to change the dict.
            # List cast gives me the possibility to use card_num as index, but messes up the  dicts within:
            # self.visualize_card_lb.configure(text=list(box["card_dict"].items())[0].question) -> Doesnt exist
            # self.visualize_card_lb.configure(text=list(box["card_dict"].items())[0][0][4]) -> Gives a letter ('s')
            # So i will call the card_dict, list cast its keys to grab the card_num-nth cards content by index.
            # Reset card_num to zero.
            self.card_num = 0
            # Set active card values.
            card = Card()
            card.name = box["card_dict"][list(box["card_dict"].keys())[self.card_num]]["name"]
            card.question = box["card_dict"][list(box["card_dict"].keys())[self.card_num]]["question"]
            card.solution = box["card_dict"][list(box["card_dict"].keys())[self.card_num]]["solution"]
            self.active_card = card.__dict__
            # Visualize card content. Show only name and question. Show solution later.
            self.visualize_card_name_lb.configure(text=self.active_card["name"])
            self.visualize_card_question_lb.configure(text=self.active_card["question"])
            self.visualize_card_solution_lb.configure(text="")
            # .

            # Toggle button functionality.
            self.next_button_switch = False
            self.skip_button_switch = True

        else:
            self.error_occurred("400x100", "Error: Invalid card number.")

    # Visualize next card if available.
    def next_card(self, box):
        # Check if enough cards exist to continue. Precalculate before increasing the card number value. (-> +1)
        # Hint: len(list(element1)) starts with 1 and list(element1) starts with pos. 0. (-> '>' instead of '>=')
        # No card exists at all.
        if len(list(box["card_dict"].items())) == 0:
            # As boxes can have a lot of cards i don't wanna iterate over the dict.
            # But to get the cards content by index instead of key-value i need to change the dict.
            # List cast gives me the possibility to use card_num as index, but messes up the  dicts within:
            # self.visualize_card_lb.configure(text=list(box["card_dict"].items())[0].question) -> Doesnt exist
            # self.visualize_card_lb.configure(text=list(box["card_dict"].items())[0][0][4]) -> Gives a letter ('s')
            # So i will call the card_dict, list cast its keys to grab the card_num-nth cards content by index.
            self.visualize_card_name_lb.configure(text="Empty")
            self.visualize_card_question_lb.configure(text="Empty")
            self.visualize_card_solution_lb.configure(text="Empty")

        # Check if enough cards exist to continue. Precalculate before increasing the card number value. (-> +1)
        # Enough cards exist.
        elif len(list(box["card_dict"].items())) > self.card_num + 1:
            if self.next_button_switch is True:
                self.card_num += 1
                # As boxes can have a lot of cards i don't wanna iterate over the dict.
                # But to get the cards content by index instead of key-value i need to change the dict.
                # List cast gives me the possibility to use card_num as index, but messes up the  dicts within:
                # self.visualize_card_lb.configure(text=list(box["card_dict"].items())[0].question) -> Doesnt exist
                # self.visualize_card_lb.configure(text=list(box["card_dict"].items())[0][0][4]) -> Gives a letter ('s')
                # So i will call the card_dict, list cast its keys to grab the card_num-nth cards content by index.
                # Set active card values.
                card = Card()
                card.name = box["card_dict"][list(box["card_dict"].keys())[self.card_num]]["name"]
                card.question = box["card_dict"][list(box["card_dict"].keys())[self.card_num]]["question"]
                card.solution = box["card_dict"][list(box["card_dict"].keys())[self.card_num]]["solution"]
                self.active_card = card.__dict__
                # Visualize card content. Show only name and question. Show solution later.
                self.visualize_card_name_lb.configure(text=self.active_card["name"])
                self.visualize_card_question_lb.configure(text=self.active_card["question"])
                self.visualize_card_solution_lb.configure(text="")
                #.

                # Toggle button functionality.
                self.next_button_switch = False
                self.skip_button_switch = True

            elif self.next_button_switch is False:
                # Do nothing.
                pass

            else:
                self.error_occurred("400x100", "Error: Invalid value.")

        # Check if enough cards exist to continue. Precalculate before increasing the card number value. (-> +1)
        # No more cards exist. Maximum / End of card-dict is reached.
        elif len(list(box["card_dict"].items())) == self.card_num + 1 and len(list(box["card_dict"].items())) != 0:
            pass

        # Negative card number or invalid value.
        else:
            self.error_occurred("400x100", "Error: Invalid card number.")

    # Skip current question without comparing to solution.
    def skip_question(self):
        if self.skip_button_switch is True:
            self.next_button_switch = True
            # Load next card.
            self.next_card(self.active_box)
            # Toggle button functionality.
            self.next_button_switch = False
            self.skip_button_switch = True

        elif self.skip_button_switch is False:
            # Do nothing.
            pass

        else:
            self.error_occurred("400x100", "Error: Invalid value.")

    # Return number of cards a box contains.
    def number_of_cards(self):
        return

    # Compare the user input/suggestion and the cards solution.
    def check_result(self, box, user_input):
        # Toggle button functionality.
        self.next_button_switch = True
        self.skip_button_switch = False

        if len(list(box["card_dict"].items())) > 0:
            user_input = user_input.get()

            # Compare values. Equal, unequal, error.
            # Equal result
            if user_input == self.active_card["solution"]:
                self.result_equal()

            # Unequal result.
            elif user_input != self.active_card["solution"]:
                self.result_unequal()

            # Error occurred.
            else:
                self.error_occurred("400x100", "Error: Comparison failed.")

        else:
            self.pop_up_info_window("Empty box", "400x100", "There is no active card usage.", "Ok")

    # .
    def result_equal(self):
        # User feedback via image.
        self.check_result_img.config(image=self.green_checkmark_img)

    # .
    def result_unequal(self):
        # User feedback via image.
        self.check_result_img.config(image=self.red_cross_img)

    def test(self):
        print("test")

    # Input card name and add card to named box.
    def add_card_to_box_window(self):
        # New window
        add_card_to_box_window = Toplevel(self.root)
        add_card_to_box_window.title("Add card to box")
        add_card_to_box_window.geometry("400x600")

        # Labels.
        # Introduction.
        task = Label(master=add_card_to_box_window, text="Insert the boxs name, the card's name you wanna"
                                                         " add to it and click on 'Add' below:")
        task.pack()

        # Input fields.
        # Name of a box.
        box_name_if = StringVar()
        box_name_if.set("Enter box name ...")
        get_box_name_if = Entry(master=add_card_to_box_window, textvariable=box_name_if)
        get_box_name_if.pack()

        # Input fields.
        # Name of a box.
        card_name_if = StringVar()
        card_name_if.set("Enter card name ...")
        get_card_name_if = Entry(master=add_card_to_box_window, textvariable=card_name_if)
        get_card_name_if.pack()

        # Buttons.
        # Add card to box.
        add_card_to_box_bt = Button(master=add_card_to_box_window, text="Add",
                                    command=lambda: add_card_to_box(self, box_name_if, card_name_if))
        add_card_to_box_bt.pack()

        # Cancel box creation
        cancel_task_bt = Button(master=add_card_to_box_window, text="Cancel", command=lambda: self.cancel_window(add_card_to_box_window))
        cancel_task_bt.pack()


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
                                   "The box you are trying to create already exists.", "Ok")

    else:
        # Add key-value pair.
        lob[item_name] = item

        # Set dictionary into storage.
        set_item_convert_py_to_json("list_of_boxes", lob)

        # Check if item got stored correctly.
        new_lob = get_item_convert_json_to_py("list_of_boxes")
        if item_name in new_lob:
            app_obj.pop_up_info_window("Info Message", "400x100", "Creating box successfully!", "Ok")

        else:
            # Failure
            app_obj.pop_up_info_window("Info Message", "400x100", "WARNING: Creating box failed!", "Ok")


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
            app_obj.pop_up_info_window("Info Message", "400x100", "Deleting box successfully!", "Ok")

        else:
            # Failure
            app_obj.pop_up_info_window("Info Message", "400x100", "WARNING: Deleting box failed!", "Ok")

    else:
        app_obj.pop_up_info_window("Item doesnt exist!", "400x100",
                                   "The item you are trying to delete doesnt exist.", "Ok")


# Add new card to storage -> see add_box_to_storage fore more info.
def add_card_to_storage(app_obj, item_name, item):
    # Get list of cards as dictionary.
    loc = get_item_convert_json_to_py("list_of_cards")

    # Check if item already exists.
    if item_name in loc:
        app_obj.pop_up_info_window("Item already exists!", "400x100",
                                   "The card you are trying to create already exists.", "Ok")

    else:
        # Add key-value pair.
        loc[item_name] = item

        # Set dictionary into storage.
        set_item_convert_py_to_json("list_of_cards", loc)

        # Check if item got stored correctly.
        new_loc = get_item_convert_json_to_py("list_of_cards")
        if item_name in new_loc:
            app_obj.pop_up_info_window("Info Message", "400x100", "Creating card successfully!", "Ok")

        else:
            # Failure
            app_obj.pop_up_info_window("Info Message", "400x100", "WARNING: Creating card failed!", "Ok")


# Add a card to a box card-dictionary.
def add_card_to_box(app_obj, box_name, card_name):
    # Get values from input field.
    box_name = box_name.get()
    card_name = card_name.get()

    # Get list of boxes as dictionary.
    lob = get_item_convert_json_to_py("list_of_boxes")
    # Get list of cards as dictionary.
    loc = get_item_convert_json_to_py("list_of_cards")

    # Check if box and card exists.
    # Adding card twice will update the value.
    if box_name in lob and card_name in loc:
        # Add card values to card-dict of the box.
        lob[box_name]["card_dict"][card_name] = loc[card_name]

        # Set new values.
        set_item_convert_py_to_json("list_of_boxes", lob)

        # Check if card got stored correctly.
        new_lob = get_item_convert_json_to_py("list_of_boxes")
        if card_name in new_lob[box_name]["card_dict"]:
            app_obj.pop_up_info_window("Info Message", "400x100", "Adding card successfully!", "Ok")

        else:
            # Failure
            app_obj.pop_up_info_window("Info Message", "400x100", "WARNING: Adding card failed!", "Ok")

    else:
        app_obj.pop_up_info_window("Box or card doesnt exist!", "400x100",
                                   "The box/card you are trying to trying to use doesnt exist.", "Ok")


# ______________________________________________________________________________________________________________________
# JSON converter functions. Get/Set with localStorage included.
# Get any item from storage and convert it from json to py.
def get_item_convert_json_to_py(item_name):
    return json.loads(localStorage.getItem(item_name))


# Convert any item from py to json and set it into storage.
def set_item_convert_py_to_json(item_name, item):
    localStorage.setItem(item_name, json.dumps(item))


# ______________________________________________________________________________________________________________________
# Main
if __name__ == '__main__':
    # Initialize storage.
    localStorage = localStoragePy("python.merkbox", "sqlite")

    # Check if list of all boxes exists, otherwise create new dict.
    if localStorage.getItem("list_of_boxes") is None:
        set_item_convert_py_to_json("list_of_boxes", dict())

    # Check if list of all cards exists, otherwise create new dict.
    if localStorage.getItem("list_of_cards") is None:
        set_item_convert_py_to_json("list_of_cards", dict())

    # Run application.
    app = Application()

    print(localStorage.getItem("list_of_boxes"))
    print(localStorage.getItem("list_of_cards"))
    print(app.active_box)
    print(app.active_card)
