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

  