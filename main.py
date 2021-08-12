import ui
import slixmpp
import getpass

server=input("""Please insert the server to continue:""")
chosen = ui.starting_menu()
contacts =[]
while chosen is not None:
    if chosen=='1':
        nick=input("choose username:")+"@"+server
        password = getpass.getpass("choose a password:")
        result=ui.login(nick,password)    
      
        if(result== True):
            while True:
                option=ui.user_menu()    
                if(option=='1'):                    
                    print(1)
                if(option=='2'):
                    sub_menu = input("""
                    1. Add User.

                    2. Show Contact List
                    
                    Choose:\n
                    """)
                    if sub_menu=='1':
                        friend = str(input("User  to add: "))+"@"+server
                    else:
                        ui.show_available(nick,password)
                        continue
                if(option==3):
                    print(1)
                if(option==4):
                    print(1)
                if(option==5):
                    print(1)
                if(option==6):
                    print(1)
                if(option==7):
                    print(1)
                else: 
                    print("Choose a Valid Option")
    if chosen=='2':
        nick=input("choose username:")+"@"+server
        password = getpass.getpass("choose a password:")
        ui.register_user(nick,password)
    if chosen=='3':
        nick=input("account:")+"@"+server
        password = getpass.getpass("password:")
        ui.delete_user(nick,password)
    if chosen=='4':
        quit()
    else:
        chosen=ui.starting_menu()
        continue
