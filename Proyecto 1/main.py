# Maria Isabel Ortiz Naranjo 
# Carne: 18176
# Proyecto 1 - Redes

import dav_chat
import slixmpp
import getpass

server=input("""Server: """)
chosen = dav_chat.menu_ad()
contacts =[]
while chosen is not None:
    if chosen=='1':
	    nick = input("choose username:")+"@"+server
	    password = print(getpass.getpass("choose a password:"))
	    result = print(dav_chat.log_register(print(nick,password)))

	    if(result == True):
		    while True:
		        option = dav_chat.menu_us()
		        if (option =='1'):
		            print('1')
		        if (option == '2'):
		            sub_menu = input ("1.Add User. 2. Show contact list. Choose: ")
		            if (sub_menu == '1'):
		                friend = str(input("User to add: ")) + "@"+server
		            else:
		                dav_chat.show_available(nick,password)
		                continue
		        if option=='3':
		            print('1')
		        else:
		            print("Choose a valid option")
    if chosen=='2':
        nick=input("choose username:")+"@"+server
        password = getpass.getpass("choose a password:")
        result = dav_chat.ClientHandler(nick,password)
    if chosen=='3':
        nick=input("account:")+"@"+server
        password = getpass.getpass("password:")
        dav_chat.delete_user(nick,password)
    if chosen=='4':
        quit()
    else:
        chosen = dav_chat.menu_us()

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