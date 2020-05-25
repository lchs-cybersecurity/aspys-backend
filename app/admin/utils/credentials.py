from hashlib import md5
from string import ascii_letters
from random import randint, choice as random_choose
from json import load as json_load, dumps as json_dumps
from pickle import dump as pkl_dump, load as pkl_load
import os.path

def gen_salt():
    charselect = ascii_letters+"0123456789!@#$%^&*"
    salt = ""
    for i in range(randint(5, 10)):
        salt += charselect[randint(0, len(charselect)-1)]
    return salt

class CredentialsManager:
    salt_start = ""
    salt_end = ""

    def __init__(self):
        # generate random-length random salt strings
        self.salt_start = gen_salt()
        self.salt_end = gen_salt()

    def sh_pw(self, pw: str):
        """Salt and hash password"""
        salted_pw = self.salt_start+pw+self.salt_end
        return md5(salted_pw.encode()).hexdigest()

    def check_credentials(self, user: str, raw_pw: str, logins: list):
        """Check validity of login attempt credentials"""
        hpw = self.sh_pw(raw_pw)
        for i in logins:
            if (user, hpw) == i:
                return True
        return False

def load_credentialsmanager():
    path = rel_path("../data/credman.pkl")
    try:
        with open(path, "rb") as credman_file:
            credman = pkl_load(credman_file)
    except FileNotFoundError:
        credman = CredentialsManager()
        with open(path, "wb+") as credman_file:
            pkl_dump(credman, credman_file)
    return credman

def gen_org_id(already_taken: list):
    while True:
        identifier = ""
        for i in range(10):
            identifier += random_choose(ascii_letters)
        if identifier not in already_taken:
            break
    return identifier

def load_organizations():
    path = rel_path("../data/organizations.json")
    try:
        with open(path, "r") as orgs_file:
            orgs = json_load(orgs_file)
        return orgs

    except FileNotFoundError:
        with open(path, "w+") as orgs_file:
            orgs_file.write("[]")
        print("Created new organizations file. Run add_organization.py to add new organizations.")
        return []


def rel_path(string):
    return os.path.join(os.path.dirname(__file__), string)