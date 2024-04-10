# Module 7 Homework
# This is program for a Command Line Interface bot that allows to interact with a contact list
# It allows a user to add, change, and retrieve a contact's phone number, as well as print all contacts
# This module defines the logic.

# TO DO: modify 'birthdays', add error handling, finish change_contact

from cli_ab import *
from datetime import datetime, timedelta


# decorator function for error handling
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            if func.__name__ == 'create_contact':
                return "Error creating a contact."
            if func.__name__ == 'phone':
                return "No such contact."
            if func.__name__ == 'show_all':
                return "There are no contacts in the Address Book."
            if func.__name__ == 'change_contact':
                return "There is no such contact."
            return "ValueError"
        except IndexError:
            if func.__name__ in ['add_contact', 'change_contact', 'phone']:
                return "Please enter the argument(s) for the command."
            return "IndexError"
    return inner


@input_error
def parse_input(user_input):                # Parse user input
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args


@input_error
def create_contact(name, book: AddressBook):
    record = book.find(name)
    if record is None:
        record = Record(name)
        book.add_record(record)
        print("Contact created. ", end='')
    return record


@input_error
def add_phone(args, book: AddressBook):   # Add name and phone to Address Book
    name = args[0].title()
    phone_ = args[1]
    record = create_contact(name, book)
    message = "Phone number added."
    # record = book.find(name)
    # message = "Contact updated"
    # if record is None:
    #     record = Record(name)
    #     book.add_record(record)
    #     message = "Contact added"
    if phone_:
        record.add_phone(phone_)
    return message


@input_error
def add_birthday(args, book: AddressBook):  # Create a contact
    name = args[0].title()
    birthday = args[1]
    record = create_contact(name, book)
    message = "Birthday added/updated."
    if birthday:
        record.add_birthday(birthday)
    return message


@input_error
def change_contact(args, book: AddressBook):
    name = args[0].title()
    phone = args[1]
    # NOT IMPLEMENTED - AWAITING CONFIRMATION FROM TUTOR
    # if not book.find(name):
    #     raise ValueError
    # rec = book.find(name)
    # rec.

    # find phone and update it

    # if name in contacts.keys():
    #     contacts.update({name: phone})
    #     debug and print(f"New details: {name}: {contacts.get(name)}")
    #     return "Contact updated."
    # else:
    #     raise ValueError


def hello(args, book:AddressBook):
    return "How can I help you?"


@input_error
def phone(args, book: AddressBook):                  # Return the phone number(s) for a contact
    name = args[0].title()
    record = book.find(name)
    if record.phone is None:
        raise ValueError
    return str(record.phone)

@input_error
def show_birthday(args, book):
    name = args[0].title()
    record = book.find(name)
    if record.birthday is None:
        raise ValueError
    birthday = f"Contact name: {str(record.name)}, birthday: {str(record.birthday)}"
    return birthday


@input_error
def show_all(args, book: AddressBook):      # Return all records from Address Book
    if not book:
        raise ValueError
    return book


functions = {
    "add": add_phone,
    "add-birthday": add_birthday,
    "all": show_all,
    "change": change_contact,
    "hello": hello,
    "hi": hello,
    "phone": phone,
    "show-birthday": show_birthday,
}

def get_upcoming_birthdays(users:list) -> list:
    today = datetime.today().date()
    users_congrats_next_7_days = []

    # iterate through users
    for user in users:
        birthday = datetime.strptime(user["birthday"], "%Y.%m.%d").date()

        # replace year in birthday to current year
        birthday_this_year = birthday.replace(year=today.year)

        # calculate number of days to birthday this year
        days_to_birthday = (birthday_this_year - today).days

        if days_to_birthday >= 0 and days_to_birthday <= 7:
            match birthday_this_year.isoweekday():
                case 6:
                    congratulation_date = birthday_this_year + timedelta(days= 2)
                case 7:
                    congratulation_date = birthday_this_year + timedelta(days= 1)
                case _:
                    congratulation_date = birthday_this_year

            # create a dictionary for a user
            user_congrats = dict(name=user['name'], congratulation_date=congratulation_date.strftime(format="%Y.%m.%d"))

            # add user to list
            users_congrats_next_7_days.append(user_congrats)

    if not users_congrats_next_7_days:
        print('There are no birthdays today or in the next 7 days')

    return users_congrats_next_7_days

def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break
        elif command in functions:
            print(functions[command](args, book))
        else:
            print("Invalid command.")


        # elif command == "birthdays":
        #     pass


if __name__ == "__main__":
    main()
