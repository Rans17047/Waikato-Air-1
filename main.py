import sys
import click
import inquirer

print("Waikato Air Email Text Generator\n\n")


def Destinations():
    global destination
    destination_choices = [
        inquirer.List('destination',
                      message="Enter travel destination",
                      choices=['Auckland', 'Wellington', 'Rotorua']),
    ]
    destination = inquirer.prompt(destination_choices)


def Flight_Confirmation():
    flight_confirmation = click.confirm("Can the customer fly tomorrow")

    if flight_confirmation is True:
        Original_Price()
        print(" ")
        Cabin_Class()

    elif flight_confirmation is False:
        print("\nSorry, this program is only for users flying the next day.\n")
        sys.exit()


def Original_Price():
    global original_price
    original_price = click.prompt(
        '\nPlease enter the flight fare to {}'.format(
            destination['destination']),
        type=int)


def Cabin_Class():
    global class_type
    global discounted_fare
    cabin_classes = [
        inquirer.List(
            'class',
            message="Please enter the cabin class",
            choices=['Economy Class', 'Business Class', 'First Class'],
        ),
    ]
    class_type = inquirer.prompt(cabin_classes)

    if class_type['class'] == 'Economy Class':
        discounted_fare = original_price * 1

    elif class_type['class'] == 'Business Class':
        discounted_fare = original_price * 1.6

    elif class_type['class'] == 'First Class':
        discounted_fare = original_price * 2

    print("The flight fare to {} in {} is ${}".format(
        destination['destination'], class_type['class'], discounted_fare))

    confirmation_message = click.confirm("\nAre you sure")

    if confirmation_message is True:
        print(" ")

    elif confirmation_message is False:
        confirm = click.confirm(
            "\nWould you like to enter the cabin class again")
        if confirm is True:
            Original_Price()
            print('\n')
            Cabin_Class()
        else:
            print("Ok, see you next time!\n")
            sys.exit()


def Discount():
    global discounted_price
    global discount
    discount = click.prompt("\nPlease enter the discount percentage",
                            prompt_suffix=': %',
                            type=int)
    discounted_price = discounted_fare - (discounted_fare * discount / 100)

    print("\nThe discounted price to {} in {} is ${:.2f}".format(
        destination['destination'], class_type['class'], discounted_price))

    confirmation_message = click.confirm("\nAre you sure")

    if confirmation_message is True:
        print(" ")

    elif confirmation_message is False:
        confirm = click.confirm(
            "\nWould you like to enter the discount percentage again")

        if confirm is True:
            Discount()
        else:
            print("Ok, see you next time!\n")
            sys.exit()


def Email():
    global customer_name
    global events
    customer_name = click.prompt("\nPlease enter the customers first name",
                                 type=str)

    email_subject = print(
        "\nSubject: {}%! discount on Waikato Air {} flights".format(
            discount, class_type['class']))

    email_text = print(
        "\nText: Hi {},\n\n".format(customer_name) +
        "Thanks for choosing waikato air, we are"
        " currently having a {}% off sale on all {}\n"
        "flights to {}. Book now! There are only {} seats left!\n\n".format(
            discount, class_type['class'], destination['destination'], seats))


seats = 168


def Seats():
    global seats
    seats -= 1
    print("The current seating capacity is {}\n".format(seats))


Destinations()
Flight_Confirmation()
Discount()
Seats()
Email()
