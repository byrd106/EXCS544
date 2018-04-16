#Author: Mike Jacobi
#Test and Update: Xu Zhang
#Virtual Werewolf Game
#Collaborators: Roya Ensafi, Jed Crandall
#This is an example client for players to connect to the Mafia server

#Copyright (c) 2012 Mike Jacobi, Xu Zhang, Roya Ensafi, Jed Crandall
#This file is part of Virtual Werewolf Game.

#Virtual werewolf is free software: you can redistribute it and/or modify
#it under the terms of the GNU General Public License as published by
#the Free Software Foundation, either version 3 of the License, or
#(at your option) any later version.
#Virtual werewolf is distributed in the hope that it will be useful,
#but WITHOUT ANY WARRANTY; without even the implied warranty of
#MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#GNU General Public License for more details.

#You should have received a copy of the GNU General Public License
#along with Virtual werewolf.  If not, see <http://www.gnu.org/licenses/>.

import signal
import sys
import os
import pwd
import getpass

sys.path.append('/home/moderator/')
import communication as c
from threading import Thread


uid=pwd.getpwuid(os.getuid())[0].split('p')[1]
inPipe='sto'+uid
outPipe=uid+'tos'

def sayWolf():
    c.send(getpass.getUser()+' IS VERY MUCH A WOLF - says EggMcMuffin, the words most notorius hacker',outPipe)    
def sayWitch():
    c.send(getpass.getUser()+' IS VERY MUCH A WITCH - says EggMcMuffin, the words most notorius hacker',outPipe)    
def sayPerson():
    c.send(getpass.getUser()+' IS A PRETY REGULAR HUMAN - says EggMcMuffin, the words most notorius hacker',outPipe)    


def listen():
        isListening=1
        sendThread = Thread(target=send,args=[])
        sendThread.setDaemon(True)
        sendThread.start()

        while isListening:
                try: data=c.recv(inPipe)#receive data from moderator
                except:continue
                try:#process received data
                        # here we'd begin a non blocking timer which will send weird messages                        
                        import threading
                        
                        if "YOU ARE A wolf" in data[2]: 
                            timer = threading.Timer(20.0, sayWolf)
                            timer.start()
                        if "YOU ARE A witch" in data[2]: 
                            timer = threading.Timer(20.0, sayWitch)
                            timer.start()
                        if "YOU ARE A wolf" in data[2]: 
                            timer = threading.Timer(20.0, sayPerson)
                            timer.start()

                        
                        if data[2]=="close":
                                print "Connection closed."
                                isListening=0
                                sendThread._Thread__stop()
                                exit()
                        else: print data[2]
                except Exception, p: pass
                #https://www.thegeekstuff.com/2013/02/stack-smashing-attacks-gcc/

def send():
    c.send('connect',outPipe)
    while 1:
                try:
                        msg=raw_input()#listen for user input
                        c.send(msg,outPipe)
                except: pass

if __name__=='__main__':
        listen()

