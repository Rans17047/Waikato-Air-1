import sys
import time
import click
import random
import inquirer


def delay_print(string):
    for i in string:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(0.05)


delay_print("Waikato Air Email Text Generator\n\n".title())


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


def Destinations():
    global destination
    destination_choices = [
        inquirer.List('destination',
                      message="Enter travel destination",
                      choices=['Auckland', 'Wellington', 'Rotorua']),
    ]
    destination = inquirer.prompt(destination_choices)


def Flight_Confirmation():
    flight_confirmation = click.confirm(
        "Can the customer fly tomorrow",
        prompt_suffix='? [y/n]: ',
        show_default=False,
    )

    if flight_confirmation is True:
        Original_Price()
        delay_print('\n')
        Cabin_Class()

    elif flight_confirmation is False:
        delay_print(
            "\nSorry, this program is only for users flying the next day.\n")
        sys.exit()


def Original_Price():
    global original_price
    original_price = click.prompt(
        '\nPlease enter the flight fare to {}'.format(
            destination['destination']),
        prompt_suffix=": $",
        type=int)


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
    class_type = inquirer.prompt(cabin_classes)

    if class_type['class'] == 'Economy Class':
        discounted_fare = original_price * 1

    elif class_type['class'] == 'Premium Economy':
        discounted_fare = original_price * 1.4

    elif class_type['class'] == 'Business Class':
        discounted_fare = original_price * 1.6

    elif class_type['class'] == 'First Class':
        discounted_fare = original_price * 2

    delay_print("\nThe flight fare to {} in {} is ${:.2f}".format(
        destination['destination'], class_type['class'], discounted_fare))

    confirmation_message = click.confirm(
        "\n\nAre you sure",
        prompt_suffix='? [y/n]: ',
        show_default=False,
    )

    if confirmation_message is True:
        delay_print('\n')
    elif confirmation_message is False:
        confirm = click.confirm(
            "\nWould you like to enter the cabin class again",
            prompt_suffix='? [y/n]: ',
            show_default=False)
        if confirm is True:
            Original_Price()
            delay_print('\n')
            Cabin_Class()
        else:
            delay_print("Ok, see you next time!\n")
            sys.exit()


def Discount():
    global discounted_price
    global discount

    discount = click.prompt("\nPlease enter the discount percentage",
                            prompt_suffix=': %',
                            type=int)

    discounted_price = discounted_fare - (discounted_fare * discount / 100)

    delay_print(Colour.BOLD +
                "\nThe discounted price to {} in {} is ${:.2f}".format(
                    destination['destination'], class_type['class'],
                    discounted_price) + Colour.END)

    confirmation_message = click.confirm("\n\nAre you sure",
                                         prompt_suffix='? [y/n]: ',
                                         show_default=False)

    if confirmation_message is True:
        delay_print('\n\n')

    elif confirmation_message is False:
        confirm = click.confirm(
            "\nWould you like to enter the discount percentage again",
            prompt_suffix='? [y/n]: ',
            show_default=False)

        if confirm is True:
            Discount()
        else:
            delay_print("Ok, see you next time!\n")
            sys.exit()


def Email():
    global customer_name
    global events
    customer_name = click.prompt("\nPlease enter the customers first name",
                                 type=str)

    email_subject = delay_print("\nSubject:\n" +
                                "{}%! discount on Waikato Air {} flights\n".
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

    email_text_1 = delay_print(
        "\nText:\n" + "Dear {},\n\n".format(customer_name.title()) +
        "Whether you're looking for the lowest price,\n"
        "the most amount of flexibility or extra benefits,\n"
        "waikato air has the best fares for you.\n\n"
        "We are currently introducing a {}% discount\n"
        "on all {} flights to {}.\n"
        "Book now while seats last!\n\n".format(discount, class_type['class'],
                                                destination['destination']))


def Text_2():
    email_text_2 = delay_print(
        "\nText:\n" + "Hi {},\n\n".format(customer_name.title()) +
        "{} has something for everyone from {}\n".format(
            destination['destination'], events) +
        "Waikato air is currently having a {}% off sale on all {}\n"
        "flights to {}. Book now while seats last!\n\n".format(
            discount, class_type['class'], destination['destination']))


seats = 168


def Seats():
    global seats
    delay_print(Colour.BOLD +
                "The current seating capacity is {}\n\n".format(seats) +
                Colour.END)


def Restart():
    global seats
    global discounted_price
    global discount

    restart = [
        inquirer.List(
            'option',
            message=
            "Would you like to generate another email or enter new infomation?",
            choices=["Generate new email", "Exit program"],
        ),
    ]

    option = inquirer.prompt(restart)

    if option['option'] == "Generate new email":
        seats -= 1
        Seats()
        discounted_price -= 0.2
        delay_print(
            "The current flight fare is {:.2f}\n".format(discounted_price))
        Email()
        x = [Text_1, Text_2]
        random.choice(x)()
        Restart()

    elif option['option'] == "Exit program":
        delay_print("Thanks for using the waikato air email text generator")
        delay_print("\nSee you next time!\n")
        sys.exit()


Destinations()
Flight_Confirmation()
Discount()
Seats()
Email()
x = [Text_1, Text_2]
random.choice(x)()
Restart()
