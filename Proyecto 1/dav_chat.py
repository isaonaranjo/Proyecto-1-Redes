# Maria Isabel Ortiz Naranjo 
# Carne: 18176
# Proyecto 1 - Redes

from re import X
from accountAdmin import *

def menu_ad():
    print("-----------CHAT MENU REGISTER----------")
    print("1. Register a new account on the server")
    print("2. Log in with an account")
    print("3. Log out with an account")
    print("4. Delete account from server")
    answer =input("Choose: ")
    return answer
    
def log_register(username,password):
    xmpp = Register(username,password)
    xmpp.register_plugin('xep_0030') ### Service Discovery
    xmpp.register_plugin('xep_0004') ### Data Forms
    xmpp.register_plugin('xep_0066') ### Band Data
    xmpp.register_plugin('xep_0077') ### Band Registration
    xmpp.connect()
    xmpp.process(forever=False)

def menu_us():
    print("""-----------CHAT MENU----------""")
    print(""" 1. Show Available Users""")
    print(""" 2.  Contacts   """)
    print(""" 3. Show status  """)
    print(""" 4. Talk!    """)
    print(""" 5. Group Chat! """)
    print(""" 6. check Notifications""")
    print(""" 7. Log Out  """)
    answer=input("Choose: ")
    return answer
    
    
def delete_user(username,password):
    xmpp = UserDelete(username,password)
    xmpp.register_plugin('xep_0030') 
    xmpp.register_plugin('xep_0004') 
    xmpp.register_plugin('xep_0066') 
    xmpp.register_plugin('xep_0077') 
    xmpp.connect()
    xmpp.process(forever=False)

def login(username,password):
    xmpp = ClientHandler(username,password)
    xmpp.register_plugin('xep_0030') # Service Discovery
    xmpp.register_plugin('xep_0199') # XMPP Ping
    xmpp.register_plugin('xep_0096') # Jabber Search
    xmpp.connect()
    xmpp.process(forever=False)
    print("Welcome" + username)

def show_available(username,password):
    xmpp = AvailableUsers(username,password)
    xmpp.connect()
    xmpp.process(forever=False)

def add_friend(username,password,friend):
    xmpp = AvailableUsers(username,password)
    xmpp.connect()
    xmpp.send_request(friend)
    xmpp.process(forever=False)
