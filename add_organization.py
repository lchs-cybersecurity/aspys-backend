from getpass import getpass
from app.admin.utils.credentials import load_credentialsmanager, gen_org_id, load_organizations
from json import load as json_load, dumps as json_dumps

"""
I'd like to get rid of this file.
We shouldn't have to do this.
- Trinity

I know, it's definitely not ideal. :P
We'll eventually replace the crappy CLI version with a proper web form 
once we start taking customers (That is, unless we find an even better way).
- Michael
"""

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
    
domains_str = input("Enter all user domains, separated by commas: ")
domains = [i.strip() for i in domains_str.split(",")]

orgs.append({
    "user": username,
    "sh_pw": credman.sh_pw(password), 
    "id": gen_org_id([i["id"] for i in orgs]),
    "domains": domains
})

print(f"Adding {username}.")

with open("./app/admin/data/organizations.json", "w+") as logins_file:
    logins_file.write(json_dumps(orgs))

print('Done!')
