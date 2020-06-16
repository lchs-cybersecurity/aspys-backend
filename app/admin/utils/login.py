from flask_login import LoginManager, UserMixin, login_manager, login_user
from pickle import load as pickle_load, dump as pickle_dump
import os.path
from .credentials import load_credentialsmanager, load_organizations

def rel_path(string):
    return os.path.join(os.path.dirname(__file__), string)

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "/"

logins = load_organizations()
credman = load_credentialsmanager()

class User(UserMixin):
    userid = ""
    org_id = ""

    def __init__(self, new_id: str):
        self.userid = new_id

    def get_id(self):
        return self.userid

    def set_org_id(self, new_org_id):
        self.org_id = new_org_id


active_users_bak = rel_path("../data/active_users_bak.pkl")

try:
    with open(active_users_bak, "rb") as bak_file:
        active_users = pickle_load(bak_file)
except FileNotFoundError:
    active_users = []

def write_bak():
    with open(active_users_bak, "wb+") as bak_file:
        pickle_dump(active_users, bak_file)

@login_manager.user_loader
def load_user(userid: str):
    try:
        return active_users[int(userid)]
    except IndexError:
        return User(userid)


def try_login(username, password):
    for login in logins:
        if username == login["user"] and credman.sh_pw(password) == login["sh_pw"]:
            user = User(str(len(active_users)))
            user.set_org_id(login["id"])
            active_users.append(user)
            login_user(user)
            write_bak()
            return True
    return False

def logout_bak_sync(user: UserMixin):
    active_users.remove(user)
    write_bak()