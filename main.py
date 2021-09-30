import sys  # To exit the program and for it's write and flush functions.
import time  # For delay
import click  # For inputs
import random  # To pick a random function
import inquirer  # For inputs
# To customize inquirer inputs
from inquirer.render.console import ConsoleRender
from inquirer.render.console._list import List


# This function creates cool "animated" text
# by putting a delay between each character in a string.
def delay_print(string):
    for i in string:  # Does the following for each character in a string
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.04)  # Used to set the delay between the characters/
        # sets the animation speed


# Here the function is being used to print the program title.
delay_print("Waikato Air Email Generator\n\n".title())


# These classes are used to customize the inquirer inputs
# I decided to create a custom inquirer theme because the two
# default themes weren't that great
class ColorList(List):
    def get_options(self):
        choices = self.question.choices

        for choice in choices:
            selected = choice == choices[self.current]

            if selected:
                color = self.terminal.cyan
                symbol = '>'
            else:
                color = self.terminal.grey
                symbol = ''
            yield choice, symbol, color


# This subclass will be instantiated in prompt()
class ListConsoleRender(ConsoleRender):
    def render_factory(self, question):
        if question != 'list':
            return ConsoleRender, self.render_factory(question)
        return ColorList


# This class lets me add colours to text
class Colour:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


cursor_up_one = '\x1b[1A'  # ANSI escape code to move cursor
erase_line = '\x1b[2K'  # ANSI escape code to remove text


# These functions clear the console when the user decides to
# enter infomation again.
def Remove_Cabin_Class_Lines(n=16):
    for _ in range(n):
        sys.stdout.write(cursor_up_one)
        sys.stdout.write(erase_line)


def Remove_Discount_Lines(n=8):
    for _ in range(n):
        sys.stdout.write(cursor_up_one)
        sys.stdout.write(erase_line)


def Remove_Lines(n=57):
    for _ in range(n):
        sys.stdout.write(cursor_up_one)
        sys.stdout.write(erase_line)


# Destination function
def Destinations():
    global destination  # To use it in formatting the email text
    destination_choices = [
        inquirer.List(
            'destination',
            message="Enter travel destination, use arrow keys to select",
            choices=['Auckland', 'Wellington', 'Rotorua']),
    ]
    destination = inquirer.prompt(destination_choices,
                                  render=ListConsoleRender())


def Flight_Confirmation():
    flight_confirmation = click.confirm(
        "Can the customer fly tomorrow",
        prompt_suffix='? [y/n]: ',
        show_default=False,
    )

    print("\n==============================================================")

    # Because the click.confirm function returns a boolean
    # value I am able to use it like this:
    if flight_confirmation is True:
        Original_Price()
        delay_print('\n')
        Cabin_Class()

    elif flight_confirmation is False:
        delay_print(
            Colour.RED +
            "\nSorry, this program is only for users flying the next day.\n" +
            Colour.END)
        sys.exit()
    # Otherwise I would have to use lists


def Original_Price():
    global original_price
    original_price = click.prompt(
        '\nPlease enter the flight fare to {}'.format(
            destination['destination']),
        prompt_suffix=": $",
        type=int)

    if original_price < 0:
        delay_print(Colour.RED +
                    "\nSorry, please enter positive numbers only\n" +
                    Colour.END)
        Original_Price()


def Cabin_Class():
    global class_type
    global discounted_fare
    cabin_classes = [
        inquirer.List(
            'class',
            message="Please enter the cabin class",
            choices=[
                'Economy Class', 'Premium Economy', 'Business Class',
                'First Class'
            ],
        ),
    ]
    class_type = inquirer.prompt(cabin_classes, render=ListConsoleRender())

    # Depending on what cabin class the user picks the original_price
    # will be mulitiplied by a number
    if class_type['class'] == 'Economy Class':
        discounted_fare = original_price * 1

    elif class_type['class'] == 'Premium Economy':
        discounted_fare = original_price * 1.4

    elif class_type['class'] == 'Business Class':
        discounted_fare = original_price * 1.6

    elif class_type['class'] == 'First Class':
        discounted_fare = original_price * 2

    print("==============================================================")

    delay_print("\nThe flight fare to {} in {} is ${:.2f}".format(
        destination['destination'], class_type['class'], discounted_fare))

    confirmation_message = click.confirm(
        "\n\nAre you sure",
        prompt_suffix='? [y/n]: ',
        show_default=False,
    )

    if confirmation_message is True:
        print(
            "\n==============================================================")

    elif confirmation_message is False:
        confirm = click.confirm(
            "\nWould you like to enter the flight fare and cabin class again",
            prompt_suffix='? [y/n]: ',
            show_default=False)
        if confirm is True:
            Remove_Cabin_Class_Lines()
            Original_Price()
            delay_print('\n')
            Cabin_Class()
        else:
            delay_print("Ok, see you next time!\n")
            sys.exit()


def Discount_Input():
    global discount
    global discounted_price

    discount = click.prompt("\nPlease enter the discount percentage",
                            prompt_suffix=': %',
                            type=int)

    discounted_price = discounted_fare - (discounted_fare * discount / 100)

    if discounted_price < 0:
        delay_print(Colour.RED + "\nThe number you entered is too high!,"
                    " please enter a lower discount.\n" + Colour.END)
        Discount_Input()


def Discount():
    delay_print(Colour.BOLD +
                "\nThe discounted price to {} in {} is ${:.2f}".format(
                    destination['destination'], class_type['class'],
                    discounted_price) + Colour.END)

    confirmation_message = click.confirm("\n\nAre you sure",
                                         prompt_suffix='? [y/n]: ',
                                         show_default=False)

    if confirmation_message is True:
        print(
            "\n==============================================================")

    elif confirmation_message is False:
        confirm = click.confirm(
            "\nWould you like to enter the discount percentage again",
            prompt_suffix='? [y/n]: ',
            show_default=False)

        if confirm is True:
            Remove_Discount_Lines()
            Discount_Input()
            Discount()
        else:
            delay_print("Ok, see you next time!\n")
            sys.exit()


def Seats():
    global seats
    seats = 168
    delay_print(Colour.BOLD +
                "The current seating capacity is {}\n\n".format(seats) +
                Colour.END)


def User_Name():
    global customer_name  # For formatting the email text
    customer_name = click.prompt("\nPlease enter the customers first name")

    if not customer_name.isalpha():
        delay_print(Colour.RED + "\nPlease input letters only\n" + Colour.END)
        User_Name()


def Email():
    global events
    print("\n==============================================================\n"
          "##############################################################\n"
          "==============================================================")

    email_subject = delay_print("\nSubject:\n" +
                                "{}%! discount on Waikato Air {} flights".
                                format(discount, class_type['class']).title())

    if destination['destination'] == 'Wellington':
        events = (
            "Te Papa mueseum to\n"
            "hunderds of different restaraunts and everything in between!\n")

    elif destination['destination'] == 'Auckland':
        events = ("events such as the Auckland Lantern Festival\n"
                  "to asb classic and activities such as the Sky Tower"
                  " bungee jump or the Auckland art gallery.\n")

    elif destination['destination'] == 'Rotorua':
        events = ("the Skyline luge cart and gondala to \n"
                  "Crankworx mountain biking compitition\n"
                  "Rotorua has a place for you!\n")


def Text_1():
    delay_print("\n\nText:\n" + "Dear {},\n\n".format(customer_name.title()) +
                "Whether you're looking for the lowest price,\n"
                "the most amount of flexibility or extra benefits,\n"
                "waikato air has the best fares for you.\n\n"
                "We are currently introducing a {}% discount\n"
                "on all {} flights to {}.\n"
                "Book now while seats last!\n\n".format(
                    discount, class_type['class'], destination['destination']))


def Text_2():
    delay_print("\n\nText:\n" + "Hi {},\n\n".format(customer_name.title()) +
                "{} has something for everyone from {}\n".format(
                    destination['destination'], events) +
                "Waikato air is currently having a {}% off sale on all {}\n"
                "flights to {}. Book now while seats last!\n\n".format(
                    discount, class_type['class'], destination['destination']))


def Text_3():
    delay_print(
        "\n\nText:\n" + "Hi {},\n\n".format(customer_name.title()) +
        "Thanks for choosing waikato air, we are "
        "currently having a {}% off sale on all {}\n"
        "flights to {}. Book now! There are only {} seats left!\n\n".format(
            discount, class_type['class'], destination['destination'], seats))


seats = 168


def Restart():
    global seats
    global discounted_price
    global discount

    print("==============================================================\n"
          "##############################################################\n"
          "==============================================================\n")

    restart = [
        inquirer.List(
            'option',
            message="Would you like to generate another"
            " email or enter new infomation?",
            choices=[
                "Generate new email", "Enter new infomation", "Exit program"
            ],
        ),
    ]

    option = inquirer.prompt(restart, render=ListConsoleRender())

    if option['option'] == "Generate new email":
        print("==============================================================")
        seats -= 1
        delay_print("\nThe current seating capacity is {}\n".format(seats))
        discounted_price += 0.4
        delay_print("\nThe current fare is {:.2f}\n".format(discounted_price))
        User_Name()
        Email()
        x = [Text_1, Text_2, Text_3]
        random.choice(x)()
        Restart()

    elif option['option'] == "Enter new infomation":
        Remove_Lines()
        functions()

    elif option['option'] == "Exit program":
        print(
            "==============================================================\n")
        delay_print("Thanks for using the waikato air email generator")
        delay_print("\nSee you next time!\n")
        sys.exit()


# Calling functions
def functions():
    Destinations()
    Flight_Confirmation()
    Discount_Input()
    Discount()
    delay_print(Colour.BOLD +
                "\nThe current seating capacity is {}\n".format(seats) +
                Colour.END)
    User_Name()
    Email()
    x = [Text_1, Text_2, Text_3]  # This bit of code picks a random function
    random.choice(x)()  # containing the email that will be printed
    # I did this so that the program will print
    # out different text each time.
    Restart()


functions()
