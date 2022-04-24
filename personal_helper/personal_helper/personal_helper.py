from collections import UserDict
import os.path
import pickle
import re

class CustomException(Exception):
    def __init__(self, text):
        self.txt = text


class AddressBook(UserDict):

    def get_record(self, name):
        if self.data.get(name):
            return self.data.get(name)
        else:
            raise CustomException('Such contacts name doesn\'t exist')

    def load_from_file(self, file_name):
        if os.path.exists(file_name):
            with open(file_name, 'rb') as fh:
                self.data = pickle.load(fh)
                if len(self.data):
                    return f'The contacts book is loaded from the file "{file_name}".'
                else:
                    return 'This is empty contacts book. Add contacts to it.'
        else:
            return 'This is empty contacts book. Add contacts into it.'

    def save_to_file(self, file_name):
        with open(file_name, 'wb') as fh:
            pickle.dump(self.data, fh)
        return f'The contacts book is saved in the file "{file_name}".'


contacts = AddressBook()


class Record:

    def __init__(self, name, address=None, phones_list=[], email=None, birthday=None):
        self.name = name
        self._address = address
        self._phones_list = phones_list
        self._email = email
        self._birthday = birthday

    def append_phone(self, phone):
        if re.search('[+]?\d+', phone):
            self._phones_list.append(phone)
        else:
            raise CustomException('Wrong phone number format')

    @property
    def address(self):
        return self._address
    
    @address.setter
    def address(self, address):
        self._address = address

    @property
    def phones_list(self):
        return self._phones_list

    @property
    def email(self):
        return self._email
    
    @email.setter
    def email(self, email):
        if re.search('[a-zA-Z][\w.]+@[a-zA-z]+\.[a-zA-Z]{2,}', email):
            self._email = email
        else:
            raise CustomException('Wrong email format. Should be as same as: aaaa@ddd.cc')
        
    @property
    def birthday(self):
        return self._email
    

    @birthday.setter
    def birthday(self, birthday):
        if re.search('\d{2}\.\d{2}.\d{4}', birthday):
            self._birthday = birthday
        else:
            raise CustomException('Wrong date format. Should be as same as: dd.mm.yyyy') 


def input_error(func):

    def inner(command_line):

        try:
            result = func(command_line)

        except CustomException as warning_text:
            result = warning_text
            
        except:
            if func.__name__ == 'save_func':
                result = f'Error while saving.'
        return result

    return inner


@input_error
def exit_func(command_line):

    return 'Good bye!'


@input_error
def save_func(command_line):

    return contacts.save_to_file('contacts.bin')

@input_error
def prepare_value(command_line):#если нет имени, будет ошибка Such contacts name doesn't exist
    if command_line:
        key = command_line.pop(0).lower()
        value = ' '.join(command_line)
        return key, value
    else:
        raise CustomException('With command must to be INFORMATION you want to add(Format: command Name information)')

@input_error
def add_name(command_line):#если имя уже существует?
    if command_line:
        name = ' '.join(command_line).lower()
        record = Record(name = name)
        contacts[record.name] = record
    else:
        raise CustomException('With command must to be NAME you want to add (Format: add Name)')

@input_error
def add_address(command_line):
    key, address = prepare_value(command_line)
    contacts.get_record(key).address = address

@input_error
def add_birthday(command_line):
    key, birthday = prepare_value(command_line)
    contacts.get_record(key).birthday = birthday

@input_error
def add_email(command_line):
    key, email = prepare_value(command_line)
    contacts.get_record(key).email = email

@input_error
def add_phone(command_line):
    key, phone = prepare_value(command_line)
    if not phone in contacts.get_record(key).phones_list:
        contacts.get_record(key).append_phone(phone)


COMMANDS = {
    'close': exit_func,
    'exit': exit_func,
    'good bye': exit_func,
    'save': save_func,
    'add': add_name,
    'add address': add_address,
    'add birthday': add_birthday,
    'add email': add_email,
    'add phone': add_phone
}

ONE_WORD_COMMANDS = ['add', 'close', 'exit', 'save']
TWO_WORDS_COMMANDS = ['add address', 'add birthday', 'add email', 'add phone', 'good bye']


def get_handler(command):
    return COMMANDS[command]


def main():

    print(contacts.load_from_file('contacts.bin'))

    while True:
        command_line = []
        while not command_line:
            command_line = input('>>> ').split()

        right_command = False

        if len(command_line) > 1 and \
           f'{command_line[0].lower()} {command_line[1].lower()}' in TWO_WORDS_COMMANDS:
            command = f'{command_line.pop(0).lower()} {command_line.pop(0).lower()}'
            right_command = True

        if not right_command:
            command = command_line.pop(0).lower()
            right_command = command in ONE_WORD_COMMANDS

        if not right_command:
            print(
                f'The "{command}" command is wrong! The allowable commands are {", ".join(ONE_WORD_COMMANDS + TWO_WORDS_COMMANDS)}.')
            continue

        handler = get_handler(command)
        print(handler(command_line))
        if handler is exit_func:
            print(contacts.save_to_file('contacts.bin'))
            break


if __name__ == '__main__':
    main()
