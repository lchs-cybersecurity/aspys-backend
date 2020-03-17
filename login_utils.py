from hashlib import md5
from string import ascii_letters
from random import randint

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