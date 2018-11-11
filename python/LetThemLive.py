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

#from textrect/textrect.py import render_textrect
from textrect import render_textrect

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

text = []
Character_ID = []


#open text file, and write message to log
def sendToText(text):
    text_file = open("lazar.log", "a")
    text_file.write(str(text))

sendToText("Started" + '\n')

sendToText("Init pygame" + '\n')
pygame.init()

sendToText("Connect to sql" + '\n')

def sqlConnectToDatabase():
	mySQLconnection = mysql.connector.connect(user='your_user', password='your_password',
                                host='your_host',
                                database='your_database',
	)
def sqlDissConnectFromDatabase():
	if(mySQLconnection .is_connected()):
		mySQLconnection.close()
		print("MySQL connection is closed")
	mySQLconnection.close()

def updateEntry(ID,status):
        mySQLconnection = mysql.connector.connect(user='your_user', password='your_password',
                                host='your_host',
                                database='your_database',
        )
        cursor = mySQLconnection .cursor()
        sql_update_Query = "UPDATE lazare_database set DONE=%s where ID=%s" % (status, ID)
        cursor.execute (sql_update_Query)
	mySQLconnection.commit()
        print (sql_update_Query)
        cursor.close()
        if(mySQLconnection .is_connected()):
                mySQLconnection.close()
                print("MySQL connection is closed")
        mySQLconnection.close()

def getLastEntry():
	mySQLconnection = mysql.connector.connect(user='your_user', password='your_user',
                                host='your_host',
                                database='your_database',
        )
	sql_select_Query = "select * from lazare_database where DONE = TRUE"
	cursor = mySQLconnection .cursor()
	cursor.execute(sql_select_Query)
	row = cursor.fetchone()
	print("Total number of rows in lazare_database is - ", cursor.rowcount)
	if(cursor.rowcount > 0):
		text = []
                screen.fill(black)
		pygame.display.flip()
		time.sleep(1)
		print ("Printing each row's column values i.e.  developer record")
  		print("ID = ", row[0])
		currentID = row[0]
		print(currentID)
    		print("TIME = ", row[1])
    		print("PIC_ID = ", row[2])
    		print("ENTRY_ID = ", row[3])
		characterID = row[4]
    		print("CHAR_ID = ", row[4])
   		print("TEXT = ", row[5])
    		text.append(row[5])
    		Character_ID.append(row[4])
    		print("ENABLE = ", row[6])
		print("DONE = ", row[7])
		addCharacterText(characterID,row[5])
		updateEntry(currentID,0)
		time.sleep(2)
		return 1
	else:
		#Clear Screen
    		screen.fill((black))
		pygame.display.flip()
		time.sleep(2)
		updateEntry(1,1)
                updateEntry(2,1)
                updateEntry(3,1)
                updateEntry(4,1)
                updateEntry(5,1)
    		#screen.blit(EmptyImage,(0,0))
	return 0

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
font=pygame.font.SysFont("freesansbold", 20)

sendToText("check Keyboard function" + '\n')

white = (255,255,255)
black = (0,0,0)

def text_objects(text, font):
    textSurface = font.render(text, True, white)
    return textSurface, textSurface.get_rect()

def message_display(text):
    largeText = pygame.font.Font('freesansbold.ttf',30)
    TextSurf, TextRect = text_objects(text, largeText)
    TextRect.center = ((400),(400))
    screen.blit(TextSurf, TextRect)
    pygame.display.update()

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

def addCharacterText(CharID, text):
	if(CharID == 1):
		applyTextBox(text,100,200,True)
	if(CharID == 2):
                applyTextBox(text,300,300,False)
        if(CharID == 3):
                applyTextBox(text,450,250,True)
        if(CharID == 4):
                applyTextBox(text,150,300,False)

def applyTextBox(textToAdd,x,y,LeftRight):

	textSize = len(textToAdd)
	print ("Text size: %s",(textSize))
        my_font = pygame.font.Font(None, 20)
        my_rect = pygame.Rect((x, y-textSize*1.05, 150, 100))
 	rendered_text = render_textrect(textToAdd, my_font, my_rect, white, black, 0)

 	if rendered_text:
		screen.blit(rendered_text, my_rect.topleft)
        if(LeftRight):
                screen.blit(leftTalk,(x,y))
                pygame.display.flip()

        else:
                screen.blit(rightTalk,(x,y))
                pygame.display.flip()

	pygame.display.update()

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
sqlConnectToDatabase()



while not done:
    checkKeyboard()
    time.sleep(2)
    getLastEntry()


    #if(newText):
#	getLastEntry()
#	applyTextBox(text[0],400,400,True)
#	text = []
#	time.sleep(2)
#	getLastEntry()
 #       applyTextBox(text[0],200,200,False)
#	text = []
 #       time.sleep(2)
#	newText = False
