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

""" Codigo implementado y guiado por documentacion tomada de: https://slixmpp.readthedocs.io/en/latest - DOCUMENTATION"""

# Implementacion de registro de cuenta en servidor

class Register(slixmpp.ClientXMPP):

    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("register", self.register)
        
    async def start(self,event):
        self.send_presence()
        await self.get_roster()
        self.disconnect()

    async def register(self,iq):
        resp = self.Iq()
        resp['type'] = 'set'
        resp['register']['user'] = self.boundjid.user
        resp['register']['password'] = self.password

        try:
            await resp.send()
            print("Account Created"+str(self.boundjid))
        except IqError as e:
            print("Account Not Created")
            self.disconnect()
        except IqTimeout:
            print("----Disconect----")
            self.disconnect()

class ClientHandler(slixmpp.ClientXMPP):
    def __init__(self, jid,password):
        slixmpp.ClientXMPP.__init__(self,jid,password)
        self.success_login=False
        self.add_event_handler("session_start", self.start)
        
    async def start(self,event):
        self.send_presence()
        try:
            await self.get_roster()
            self.success_login=True
            print(self.success_login)
            print("Succesful! Welcome back!"+str(self.boundjid))
            self.disconnect()
        except IqError as e:
            print("IQ Error")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect()

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
            print("Success! Acount Deleted"+str(self.boundjid))
        except IqError as e:
            print("IQ Error:Account Not Deleted")
            self.disconnect()
        except IqTimeout:
            print("Timeout")
            self.disconnect() 

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