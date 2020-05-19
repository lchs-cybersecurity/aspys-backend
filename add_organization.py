from getpass import getpass
from login_utils import load_credentialsmanager, gen_org_id, load_organizations
from json import load as json_load, dumps as json_dumps

credman = load_credentialsmanager()

orgs = load_organizations()

print("No users found. Please create a user.")
username = input("Username: ")
while True:
    password = getpass("Password: ")
    password_confirm = getpass("Confirm password: ")
    if password == password_confirm:
        break
    else:
        print("Passwords did not match. Please try again.")
# orgs.append((username, credman.sh_pw(password)))
orgs.append(
    {"user": username, "sh_pw": credman.sh_pw(password), 
    "id": gen_org_id([i["id"] for i in orgs])})
print(f"User {username} added.")
with open("data/organizations.json", "w+") as logins_file:
    logins_file.write(json_dumps(orgs))
