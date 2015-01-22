#!/usr/bin/python
import pygame.camera
import pygame.image
import socket
import cgi
import time
from RoombaSCI import RoombaAPI

from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer
from os import curdir, sep

PORT_NUMBER = 8080

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		if self.path=="/":
			self.path="/roomba.html"

		try:
			#Check the file extension required and
			#set the right mime type

			sendReply = False
			if self.path.endswith(".html"):
				mimetype='text/html'
				sendReply = True
			if self.path.endswith(".jpg"):
				mimetype='image/jpg'
				sendReply = True
			if self.path.endswith(".gif"):
				mimetype='image/gif'
				sendReply = True
			if self.path.endswith(".js"):
				mimetype='application/javascript'
				sendReply = True
			if self.path.endswith(".css"):
				mimetype='text/css'
				sendReply = True
			if self.path.endswith(".bmp"):
				print 'Take a picture'
				img = cam.get_image()
				pygame.image.save(img, "photo.bmp")
				mimetype='image/bmp'
				sendReply = True

			if sendReply == True:
				#Open the static file requested and send it
				f = open(curdir + sep + self.path) 
				self.send_response(200)
				self.send_header('Content-type',mimetype)
				self.end_headers()
				self.wfile.write(f.read())
				f.close()
			return
		

		except IOError:
			self.send_error(404,'File Not Found: %s' % self.path)
#Handler for the POST requests
	def do_POST(self):
		if self.path=="/send":
			form = cgi.FieldStorage(
				fp=self.rfile, 
				headers=self.headers,
				environ={'REQUEST_METHOD':'POST',
		                 'CONTENT_TYPE':self.headers['Content-Type'],
			})

			print "Your command is: %s" % form["command"].value
			f = open(curdir + sep + "roomba.html") 
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write(f.read())
			f.close()			
#			self.send_response(200)
#			self.end_headers()
			self.wfile.write("Command: %s !" % form["command"].value)
			return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(("gmail.com",80))
	print(s.getsockname()[0])
	s.close()
	pygame.camera.init()
	cam = pygame.camera.Camera(pygame.camera.list_cameras()[0])
	cam.start()

	print "starting serial to roomba..."
    	x = RoombaAPI("/dev/ttyUSB0",57600)
        x.connect()
        x.start()
        x.control()
        x.clean()
        time.sleep(5)
        x.control()
        x.spin_left()
        time.sleep(5)

	print "starting the web server"
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()
	pygame.camera.quit()
	
