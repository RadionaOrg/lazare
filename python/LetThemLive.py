#############################################################################
# Let them live again by Lazarus
# 
# pygame
# sql
# gpio
#
#############################################################################

import sys
import os
import threading
#import sqlite3

import mysql.connector
from mysql.connector import errorcode

from datetime import datetime, date

#import RPi.GPIO as GPIO
import time
#GPIO.setmode(GPIO.BCM)

import pygame
from time import gmtime, strftime
import time
#from serial import Serial
import struct
from pygame.locals import *

try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

from pygame.compat import unicode_

pygame.init()

#open text file, and write message to log
def sendToText(text):
    text_file = open("lazar.log", "a")
    text_file.write(str(text))

sendToText("Started" + '\n')

sendToText("Init pygame" + '\n')
pygame.init()

sendToText("Connect to sql" + '\n')

try:
  cnx = mysql.connector.connect(user='dprizmic_lazare', password='cxfuKhZ9uhw9',
                                host='185.58.73.37',
                                database='dprizmic_lazare',
)
except mysql.connector.Error as err:
  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
    print("Something is wrong with your user name or password")
  elif err.errno == errorcode.ER_BAD_DB_ERROR:
    print("Database does not exist")
  else:
    print(err)
else:
  cnx.close()


size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
sendToText("Getting screen size" + '\n')
screen = pygame.display.set_mode((640, 480))
#screen = pygame.display.set_mode(size, pygame.FULLSCREEN)


sendToText("Screen is set" + '\n')

#Turn off mouse cursor
sendToText("Set mouse visible" + '\n')
pygame.mouse.set_visible(0)
sendToText("Mixer quit" + '\n')
pygame.mixer.quit()
sendToText("Loading images" + '\n')
leftTalk = pygame.image.load("/home/mistery/lazare//pics/leftTalk.png")
rightTalk = pygame.image.load("/home/mistery/lazare/pics/rightTalk.png")

#pygame.mixer.init(44100, -16,2,2048)
#sendToText("Loading sounds" + '\n')
#CowSound= pygame.mixer.Sound("/home/pi/automat/cow.wav")

font=pygame.font.SysFont("freesansbold", 20)
#font=pygame.font.SysFont("verdana", 70)

sendToText("check Keyboard function" + '\n')
def checkKeyboard():
    for event in pygame.event.get():
        #sendToText(event.type)
        if (event.type == QUIT):
            pygame.quit()
            sys.exit()
            done = True
        if (event.type == KEYDOWN):
            if (event.key == K_ESCAPE):
                pygame.quit()
                sys.exit()
                done = True
#setting score numbers that will change on screen
def applyText(textToAdd,x,y,LeftRight):
	if(LeftRight):
   		screen.blit(leftTalk,(x,y))
   		pygame.display.flip()
   		scoretext=font.render(str(textToAdd), 1,(255,255,255))
   		screen.blit(scoretext, (x, y-100))
   		pygame.display.flip()
   	else:
   	   	screen.blit(rightTalk,(x,y))
   		pygame.display.flip()
   		scoretext=font.render(str(textToAdd), 1,(255,255,255))
   		screen.blit(scoretext, (x-100, y-100))
   		pygame.display.flip()

newText=True
done=False

while not done:
    #sendToText("In loop" + '\n')
    checkKeyboard()
    if(newText):
    	applyText("Left Text skdjhaksjhdkajhskdjhs",100,100,True)
    	sendToText("Left Text applied" + '\n')
	applyText("Right Text skdjhaksjhdkajhskdjhs",300,300,False)
	sendToText("Right Text applied" + '\n')
	newText = False
