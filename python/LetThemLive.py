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

#open text file, and write message to log
def sendToText(text):
    text_file = open("lazar.log", "a")
    text_file.write(str(text))

sendToText("Started" + '\n')

sendToText("Init pygame" + '\n')
pygame.init()

sendToText("Connect to sql" + '\n')

def sqlConnectToDatabase():
	mySQLconnection = mysql.connector.connect(user='lazare', password='cxfuKhZ9uhw9',
                                host='178.62.187.251',
                                database='lazare',
	)
def sqlDissConnectFromDatabase():
	if(mySQLconnection .is_connected()):
		mySQLconnection.close()
		print("MySQL connection is closed")
	mySQLconnection.close()

#except mysql.connector.Error as err:
#  if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
#    print("Something is wrong with your user name or password")
#  elif err.errno == errorcode.ER_BAD_DB_ERROR:
#    print("Database does not exist")
#  else:
#    print(err)
#else:
#  mySQLconnection.close()

text = []
Character_ID = []
def updateEntry(ID):
        mySQLconnection = mysql.connector.connect(user='lazare', password='cxfuKhZ9uhw9',
                                host='178.62.187.251',
                                database='lazare',
        )
        cursor = mySQLconnection .cursor()
        sql_update_Query = "UPDATE lazare_database set DONE=0 where ID=%s" % (ID)
        cursor.execute (sql_update_Query)
	mySQLconnection.commit()
        print (sql_update_Query)
        cursor.close()
        if(mySQLconnection .is_connected()):
                mySQLconnection.close()
                print("MySQL connection is closed")
        mySQLconnection.close()

def getLastEntry():
	mySQLconnection = mysql.connector.connect(user='lazare', password='cxfuKhZ9uhw9',
                                host='178.62.187.251',
                                database='lazare',
        )
	sql_select_Query = "select * from lazare_database where DONE = TRUE"
	cursor = mySQLconnection .cursor()
	cursor.execute(sql_select_Query)
	row = cursor.fetchone()
	print("Total number of rows in lazare_database is - ", cursor.rowcount)
	print ("Printing each row's column values i.e.  developer record")
  	print("ID = ", row[0])
	currentID = row[0]
	print(currentID)
    	print("TIME = ", row[1])
    	print("PIC_ID = ", row[2])
    	print("ENTRY_ID = ", row[3])
    	print("CHAR_ID = ", row[4])
   	print("TEXT = ", row[5])
    	text.append(row[5])
    	Character_ID.append(row[4])
    	print("ENABLE = ", row[6])
	print("DONE = ", row[7])
	updateEntry(currentID)

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
def applyTextBox(textToAdd,x,y,LeftRight):

        my_font = pygame.font.Font(None, 20)
        #my_string = "Hi there! I'm a nice bit of wordwrapped text. Won't you be my friend? Honestly, wordwrapping is easy, with David's fancy new render_textrect () fu$
        #my_rect = pygame.Rect((x, y, 300, 300))
        #rendered_text = render_textrect(my_string, my_font, my_rect, white, black, 0)

        #my_font = pygame.font.Font(None, 20)

	#if(LeftRight):

        my_rect = pygame.Rect((x, y-100, 150, 100))

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
    #sendToText("In loop" + '\n')
    checkKeyboard()
    if(newText):
        #my_font = pygame.font.Font(None, 22)
        #my_string = "Hi there! I'm a nice bit of wordwrapped text. Won't you be my friend? Honestly, wordwrapping is easy, with David's fancy new render_textrect () function.\nThis is a new line.\n\nThis is another one.\n\n\nAnother line, you lucky dog."
        #my_rect = pygame.Rect((40, 40, 300, 300))
    	#rendered_text = render_textrect(my_string, my_font, my_rect, white, black, 0)

    	#if rendered_text:
       # 	screen.blit(rendered_text, my_rect.topleft)

    	#pygame.display.update()

	#time.sleep(2)
	getLastEntry()
	applyTextBox(text[0],400,400,True)
	text = []
	time.sleep(2)
	getLastEntry()
        applyTextBox(text[0],200,200,False)
	text = []
        time.sleep(2)
        #time.sleep(2)

    	#applyText("Character:" + str(Character_ID[0]) + "Text:" + text[0],100,100,True)
#    	sendToText("Charaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaacter:" + str(Character_ID[0]) + "Text:" + text[0])
	#applyText("Character:" + str(Character_ID[1]) + "Text:" + text[1],300,300,False)
#	sendToText("Character:" + str(Character_ID[1]) + "Text:" + text[1])
	newText = False
	#message_display("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
