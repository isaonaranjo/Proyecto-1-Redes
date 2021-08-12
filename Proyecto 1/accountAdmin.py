# Maria Isabel Ortiz Naranjo 
# Carne: 18176
# Proyecto 1 - Redes

import sys
import asyncio
import slixmpp
from getpass import getpass
from argparse import ArgumentParser
from slixmpp.exceptions import IqError, IqTimeout
from optparse import OptionParser
import logging
import getpass
from re import sub
import threading
from tabulate import tabulate


""" Codigo implementado y guiado por documentacion tomada de: https://slixmpp.readthedocs.io/en/latest - DOCUMENTATION"""

# Implementacion de registro de cuenta en servidor

class Register(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.user = jid
        self.add_event_handler("session_start", self.session_start)
        self.add_event_handler("register", self.register)

    def session_start(self, event):
        self.send_presence()
        self.get_roster()

    def register(self, iq):
        iq = self.Iq()
        iq['type'] = 'set'
        iq['register']['username'] = self.boundjid.user
        iq['register']['password'] = self.password

        try:
            iq.send()
            print("Account created succesfully with jid ->", self.boundjid,"\n")
            self.disconnect()
        except IqError as e:
            print("Couldn't register, please check your credentials", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("Server took too long to respond \n")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()

# Gestion de los clientes

class ClientHandler(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.user = jid
        self.add_event_handler("session_start", self.start)

    def start(self, event):
        try:
            self.send_presence()
            self.get_roster()
            self.disconnect()
        except IqError as e:
            print("Couldn't log in, please check your credentials", e,"\n")
            self.disconnect()
        except IqTimeout:
            print("Server took too long to respond \n")
            self.disconnect()
        except Exception as e:
            print(e)
            self.disconnect()

# Borrar usuario 

class UserDelete(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("unregister", self.unregister)

    async def start(self,event):
        self.send_presence()
        await self.get_roster()
        await self.unregister()

        self.disconnect()

    async def unregister(self,iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['from'] = self.boundjid.user
        resp['password'] = self.password
        resp['register']['remove'] = 'remove'
        try:
            await resp.send()
            print("Success! Account Deleted"+str(self.boundjid))
        except IqError as e:
            print("IQ Error:Account Not Deleted")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect() 
            
# Mostrar usuarios disponibles
          
class AvailableUsers(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.presences_received = asyncio.Event()
        self.recieved=set()        
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("changed_status",self.wait_for_presences)
        
    async def start(self,event):    
        try:
            await self.get_roster()
        except IqError as e:
            print("IQ Error")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect()
        self.send_presence()

        print('Roster  for %s'% self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s} [%s]'% (name,jid,sub))
                else:
                    print(' %s (%s} [%s]'% (jid,sub))
                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])
        self.disconnect()


    def wait_for_presences(self,pres):
        self.received.add(pres['from'].bare)
        if len(self.recieved)>=len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()

# Agregar usuario

class AddUser(slixmpp.ClientXMPP):

    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.presences_received = asyncio.Event()
        self.recieved=set()        
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("changed_status",self.wait_for_presences)
        
    async def start(self,event):
        
        try:
            await self.get_roster()
        except IqError as e:
            print("IQ Error")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect()
        self.send_presence()

        print('Roster  for %s'% self.boundjid.bare)
        groups = self.client_roster.groups()
        for group in groups:
            for jid in groups[group]:
                sub = self.client_roster[jid]['subscription']
                name = self.client_roster[jid]['name']
                if self.client_roster[jid]['name']:
                    print(' %s (%s} [%s]'% (name,jid,sub))
                else:
                    print(' %s (%s} [%s]'% (jid,sub))
                connections = self.client_roster.presence(jid)
                for res, pres in connections.items():
                    show = 'available'
                    if pres['show']:
                        show = pres['show']
                    print('   - %s (%s)' % (res, show))
                    if pres['status']:
                        print('       %s' % pres['status'])
        self.disconnect()

    def wait_for_presences(self,pres):
        self.received.add(pres['from'].bare)
        if len(self.recieved)>=len(self.client_roster.keys()):
            self.presences_received.set()
        else:
            self.presences_received.clear()
    
    def send_request(self,to):
        try:
            self.send_presence_subscription(to, self.local_jid, 'subscribe')
        except:
            print("Couldn't add Friend")

# https://slixmpp.readthedocs.io/en/latest/getting_started/muc.html

class GroupChat(slixmpp.ClientXMPP):
    def __init__(self, jid, password, room, nick):
        slixmpp.ClientXMPP.__init__(self, jid, password)

        self.jid = jid
        self.room = room
        self.nick = nick

        self.add_event_handler("session_start", self.start)
        self.add_event_handler("groupchat_message", self.group_chat_message)
        self.add_event_handler("muc::%s::got_online" % self.room, self.group_chat_welcome)

    async def start(self, event):
        await self.get_roster()
        self.send_presence()
        self.plugin['xep_0045'].join_muc(self.room, self.nick)

    def group_chat_message(self, msg):
        sender = str(msg['from']).split('/')[1]

        if(sender != self.nick):
            print(sender + ": " + msg['body'])
            broadcast = input("Write your broadcast: ")
            self.send_message(mto=msg['from'].bare,
                              mbody=broadcast,
                              mtype='groupchat')

    def group_chat_welcome(self, presence):
        if presence['muc']['nick'] != self.nick:
            self.send_message(mto=presence['from'].bare,
                              mbody="Hello, %s %s" % (presence['muc']['role'],
                                                      presence['muc']['nick']),
                              mtype='groupchat')

class Fetch(slixmpp.ClientXMPP):
    def __init__(self, jid, password, user_jid=None):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.session_start)

        self.contacts = []
        self.user_jid = user_jid
        self.presences = threading.Event()
        
    async def session_start(self, event):
        self.send_presence()
        await self.get_roster()

        try:
            self.get_roster()
        except IqError as e:
            print("Couldn't fetch contact(s) \n", e)
        except IqTimeout:
            print("Server took too long to respond \n")
        
        self.presences.wait(3)

        for group in self.client_roster.groups():
            for user in self.client_roster.groups()[group]:
                print("user", user)
                status = "Offline" #pending
                subscription_type = self.client_roster[user]['subscription']
                self.contacts.append([user, status, subscription_type])
    
        if(self.user_jid != None):
            print("\n******Contact Detalis******\n")
            for contact in self.contacts:
                if(contact[0]==self.user_jid):
                    print(tabulate([contact], headers=["JID", "Status", "Subscription"]))
        else:
            print("\n******Your Contacts******\n")
            if (len(self.contacts)!=0):
                contacts_temp = []
                for contact in self.contacts:
                    if contact[0] != self.jid:
                        contacts_temp.append(contact)
                
                print(tabulate(contacts_temp, headers=["JID", "Status", "Subscription"]))
        print('\n')
        self.disconnect()
