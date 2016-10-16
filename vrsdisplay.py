import os
import pygame
import time
import random
from threading import Thread
from datetime import datetime
import socket
import fcntl
import struct
import urllib2
import base64
import json
import sys

station="YourStationname" #In my case it is EDDT
url="http://example.com/AircraftList.json" #Enter your VRS-Url
login="on" #Change to "off" if your VRS is public.
username="username" #Only needed if Login=on
password="password" #Only needed if Login=on
querytime=5 #Server Querytime
 
class pyscope :
    screen = None;
    
    def __init__(self):
        "Ininitializes a new pygame screen using the framebuffer"
        # Based on "Python GUI in Linux frame buffer"
        # http://www.karoltomala.com/blog/?p=679
        disp_no = os.getenv("DISPLAY")
        if disp_no:
            print "I'm running under X display = {0}".format(disp_no)
        
        # Check which frame buffer drivers are available
        # Start with fbcon since directfb hangs with composite output
        drivers = ['fbcon', 'directfb', 'svgalib']
        found = False
        for driver in drivers:
            # Make sure that SDL_VIDEODRIVER is set
            if not os.getenv('SDL_VIDEODRIVER'):
                os.putenv('SDL_VIDEODRIVER', driver)
            try:
                pygame.display.init()
            except pygame.error:
                print 'Driver: {0} failed.'.format(driver)
                continue
            found = True
            break
    
        if not found:
            raise Exception('No suitable video driver found!')
        
        size = (pygame.display.Info().current_w, pygame.display.Info().current_h)
        print "Framebuffer size: %d x %d" % (size[0], size[1])
        self.screen = pygame.display.set_mode(size, pygame.FULLSCREEN)
        # Clear the screen to start
        self.screen.fill((0, 0, 0))        
        # Initialise font support
        pygame.font.init()
		
        # Render the screen
        pygame.display.update()
 
    def __del__(self):
        "Destructor to make sure pygame shuts down, etc."

scope = pyscope()
font = pygame.font.Font("digital.ttf", 26)

def readvrs():
	while True:
		if login == "on":
			request=urllib2.Request(url)
			base64string=base64.encodestring('%s:%s' % (username, password)).replace('\n', '')
			request.add_header("Authorization", "Basic %s" % base64string)
			response=urllib2.urlopen(request)
		else:
			request=urllib2.Request(url)
			response=urllib2.urlopen(request)
		flights=json.load(response)
		global flightscount
		flightscount=flights['totalAc']
		flieger=flights['acList']
		mil_list = list()
		mlat_list = list()
		heli_list = list()
		for each in flieger:
			try:
				mil_list.append(each['Mil'])
			except KeyError:
				continue

		for each in flieger:
			try:
				mlat_list.append(each['Mlat'])
			except KeyError:
				continue

		for each in flieger:
			try:
				heli_list.append(each['Species'])
			except KeyError:
				continue
		global milflights
		milflights=mil_list.count(True)
		global mlatflights
		mlatflights=mlat_list.count(True)
		global heliflights
		heliflights=heli_list.count(4)
		time.sleep(querytime)
t1 = Thread(target = readvrs)
t1.daemon = True

def printvrs():
	while True:
		if 'flightscount' in globals():
			pygame.mouse.set_visible(0)
			scope.screen.fill((0, 0, 0))
			scope.screen.blit(pygame.image.load('radar.png').convert(), (0, 0))
			scope.screen.blit(font.render('Station: %s' %station , True, (255, 255, 255)), (0, 0))
			scope.screen.blit(font.render('%s' %time.strftime("%d.%b.%y") , True, (255, 255, 255)), (0, 30))
			scope.screen.blit(font.render('%s' %datetime.now().strftime("%H:%M:%S.%f") , True, (255, 255, 255)), (0, 60))
			scope.screen.blit(font.render('Aircraft: %s' %flightscount , True, (151,255,255)), (0, 90))
			scope.screen.blit(font.render('Military: %s' %milflights , True, (255, 0, 0)), (0, 120))
			scope.screen.blit(font.render('Multilateration: %s' %mlatflights , True, (0,255,255)), (0, 150))
			scope.screen.blit(font.render('Helicopter: %s' %heliflights , True, (255,215,0)), (0, 180))
			scope.screen.blit(font.render('Querytime: %s' %querytime , True, (127, 255, 0)), (0, 210))
			scope.screen.blit(pygame.image.load('vrs2.png').convert(), (420, 50))
			pygame.display.update()
			time.sleep(0.1)
		else:
			scope.screen.fill((0, 0, 0))
			pygame.display.update()
			scope.screen.blit(font.render('No data. Please wait.', True, (255, 20, 147)), (200, 200))
			pygame.display.update()
			time.sleep(1)
			scope.screen.fill((0, 0, 0))
			pygame.display.update()
			scope.screen.blit(font.render('No data. Please wait..', True, (255, 20, 147)), (200, 200))
			pygame.display.update()
			time.sleep(1)
			scope.screen.fill((0, 0, 0))
			pygame.display.update()
			scope.screen.blit(font.render('No data. Please wait...', True, (255, 20, 147)), (200, 200))
			pygame.display.update()
			time.sleep(1)

t2 = Thread(target = printvrs)
t2.daemon = True

t1.start()
t2.start()

raw_input ("Hit enter to quit VRS-Display: ")
exit()
