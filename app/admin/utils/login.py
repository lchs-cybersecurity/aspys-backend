from flask_login import LoginManager, UserMixin, login_manager, login_user
from .credentials import load_credentialsmanager, load_organizations

login_manager = LoginManager()
login_manager.session_protection = "strong"
login_manager.login_view = "/"

active_users = []
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
            return True
    return False