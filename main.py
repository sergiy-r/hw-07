# Module 7 Homework
# This is program for a Command Line Interface bot that allows to interact with a contact list
# It allows a user to add, change, and retrieve a contact's phone number, as well as print all contacts
# This module defines the logic.
import cli_ab
from cli_ab import *

# decorator function for error handling
def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except KeyError:
            return "KeyError"
        except ValueError:
            if func.__name__ == 'parse_input':
                print("You did not enter a command. Please enter a command.")
                return parse_input('try_again')
            if func.__name__ == 'add_contact':
                return ("This contact already exists. To view the contact number, please enter 'phone [Name]', e.g., "
                        "phone Alex")
            if func.__name__ == 'phone':
                return ("There is no such contact. To view all contacts, please enter 'all'. \nTo add a contact, "
                        "please enter 'add [Name] [Number]', e.g., add Alex 07770000001")
            if func.__name__ == 'show_all':
                return ("There are no stored contacts. To add a contact, please enter 'add [Name] [Number]', e.g., "
                        "add Alex 07770000001")
            if func.__name__ == 'change_contact':
                return "There is no such contact. To view all contacts enter 'all'."
            return "ValueError"
        except IndexError:
            if func.__name__ in ['add_contact', 'change_contact', 'phone']:
                return "Please enter the argument(s) for the command."
            return "IndexError"
    return inner

@input_error
def parse_input(user_input):
    cmd, *args = user_input.split()
    cmd = cmd.strip().lower()
    return cmd, *args

@input_error
def add_contact(args, book):        # Add name and phone to Address Book
    name = args[0].title()
    phone = args[1]
    rec = cli_ab.Record(name)       # Create a record
    rec.add_phone(phone)            # Add phone number to record
    book.add_record(rec)            # Add record to Address Book
    return "Contact added."


@input_error                        # Return all records from Address Book
def show_all(book):
    if not book:
        raise ValueError
    for name, record in book.data.items():
        print(record)
    # if contacts:
    #     contacts_str = "\n".join(f"{name}: {phone}" for name, phone in contacts.items())
    #     return "Contacts:\n" + contacts_str
    # else:
    #     raise ValueError


def main():
    book = AddressBook()
    print("Welcome to the assistant bot!")
    while True:
        user_input = input("Enter a command: ")
        command, *args = parse_input(user_input)

        if command in ["close", "exit"]:
            print("Good bye!")
            break

        elif command == "hello":
            print("How can I help you?")

        elif command == "add":
            print(add_contact(args, book))

        elif command == "change":
            pass

        elif command == "phone":
            pass

        elif command == "all":
            print(show_all(book))

        elif command == "add-birthday":
            pass

        elif command == "show-birthday":
            pass

        elif command == "birthdays":
            pass

        else:
            print("Invalid command.")

if __name__ == "__main__":
    main()