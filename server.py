#!/usr/bin/python
import subprocess
from BaseHTTPServer import BaseHTTPRequestHandler,HTTPServer

PORT_NUMBER = 1337

#This class will handles any incoming request from
#the browser 
class myHandler(BaseHTTPRequestHandler):
	
	#Handler for the GET requests
	def do_GET(self):
		self.send_response(200)
		self.send_header('Content-type','text/html')
		self.end_headers()
		
		parsed_path = urlparse.urlparse(self.path)
		b64_img = parsed_path.path

		fh = open("tmp_img.jpg", "wb")
		fh.write(b64_img.decode('base64'))
		fh.close()

		p = subprocess.Popen("colorify.sh", stdout=subprocess.PIPE, shell=True)
		(output, err) = p.communicate()

		colors = output.split()
		colors.pop(0)

		self.wfile.write(colors)
		return

try:
	#Create a web server and define the handler to manage the
	#incoming request
	server = HTTPServer(('', PORT_NUMBER), myHandler)
	print 'Started httpserver on port ' , PORT_NUMBER
	
	#Wait forever for incoming htto requests
	server.serve_forever()

except KeyboardInterrupt:
	print '^C received, shutting down the web server'
	server.socket.close()