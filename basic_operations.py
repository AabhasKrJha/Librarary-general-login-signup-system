import re
import hashlib
import string
import secrets
import pickle
import random
import os

# string.punctuation - this returns all the special chars

alphabet_number_symbol = string.ascii_letters + string.digits

try:
    File = open('libID.dat', 'x')
    File.close()
except:
    pass


def make_list(obj):
    row = []
    for i in obj:
        for j in i:
            row.append(j)
    return row


def gen_code():
    code = ''
    for i in range(4):
        code += random.choice(alphabet_number_symbol)
    return code


def hash(password):
    hashed_passwd = hashlib.md5(password.encode()).hexdigest()
    return hashed_passwd


def check_email(email):

    def check_username(username):
        if username:
            for i in username:
                if i not in alphabet_number_symbol:
                    return False
        else:
            return False

    def check_domain(domain):
        if domain:
            if domain.count('.') == 1:
                domain_parts = domain.partition('.')
                if domain_parts[0] and domain_parts[2]:
                    return True
                else:
                    return False
            else:
                return False
        else:
            return False

    if email.count('@') == 1:
        username, symbol, domain = email.partition('@')
        username = username.lower()
        domain = domain.lower()
        if check_username(username) != False and check_domain(domain) == True:
            return True
        else:
            return False
    else:
        return False


def validate_signup(name, email, phone, password):

    if not name.isspace():
        if check_email(email):
            try:
                int(phone)
                if len(phone) == 10:
                    if password and not password.isspace():
                        return True
                    else:
                        return 'password'
                else:
                    return 'phone'
            except:
                return 'phone'
        else:
            return 'email'
    else:
        return 'name'


def check_job_application(email, phone):

    try:
        int(phone)
        if check_email(email) and len(phone) == 10:
            return True
        else:
            return False
    except:
        return False


def check_reset_password_form(email, password, conf_password):

    if check_email(email):
        if password == conf_password:
            return True
        else:
            return False
    else:
        return False


def create_libID_file():

    code_file = 'libID.dat'

    readers = ['rd100']
    authors = ['at100']
    authority = ['auth00']

    users = {'reader': readers, 'author': authors, 'authority': authority}

    with open(code_file, 'wb') as f:
        pickle.dump(users, f)


def gen_libID(designation):

    code_file = 'libID.dat'

    readers = ['rd100']
    authors = ['at100']
    authority = ['auth00']

    def read():

        with open(code_file, 'rb') as f:
            try:
                data = pickle.load(f)
            except:
                data = []

        return data

    def write(users):
        with open(code_file, 'wb') as f:
            pickle.dump(users, f)

    data = read()
    print(data)

    if data:

        readers = data['reader']
        authors = data['author']
        authority = data['authority']

        last_ID = data.get(designation)[-1]

        for i in last_ID:
            if i.isdigit():
                if int(i) != 0:
                    index = last_ID.index(i)
                    break
                else:
                    index = last_ID.index(i)+1

        last_ID_number = int(last_ID[index:])
        new_ID = last_ID[0:index] + str(last_ID_number+1)

        if designation == 'reader':
            readers.append(new_ID)
        elif designation == 'author':
            authors.append(new_ID)
        else:
            authority.append(new_ID)

        users = {'reader': readers, 'author': authors, 'authority': authority}
        write(users)

        return new_ID

    else:
        users = {'reader': readers, 'author': authors, 'authority': authority}
        write(users)

        return users
