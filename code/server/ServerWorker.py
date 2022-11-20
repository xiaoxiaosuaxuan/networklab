from random import randint
import sys, traceback, threading, socket

from VideoStream import VideoStream
from RtpPacket import RtpPacket

class ServerWorker:
	SETUP = 'SETUP'
	PLAY = 'PLAY'
	PAUSE = 'PAUSE'
	TEARDOWN = 'TEARDOWN'
	DESCRIBE = 'DESCRIBE'
	
	INIT = 0
	READY = 1
	PLAYING = 2
	state = INIT

	OK_200 = 0
	FILE_NOT_FOUND_404 = 1
	CON_ERR_500 = 2
	
	clientInfo = {}
	
	def __init__(self, clientInfo):
		self.clientInfo = clientInfo
		self.rtpPort = 9999
		
	def run(self):
		threading.Thread(target=self.recvRtspRequest).start()
	
	def recvRtspRequest(self):
		"""Receive RTSP request from the client."""
		connSocket = self.clientInfo['rtspSocket'][0]
		while True:            
			data = connSocket.recv(256)
			if data:
				print("Data received:\n" + data.decode("utf-8"))
				self.processRtspRequest(data.decode("utf-8"))
	
	def processRtspRequest(self, data):
		"""Process RTSP request sent from the client."""
		# Get the request type
		request = data.split('\n')
		line1 = request[0].split(' ')
		requestType = line1[0]
		self.requestType = requestType
		
		# Get the media file name
		filename = line1[1]
		
		# Get the RTSP sequence number 
		seq = request[1].split(' ')
		
		# Process SETUP request
		if requestType == self.SETUP:
			if self.state == self.INIT:
				# Update state
				print("processing SETUP\n")
				
				try:
					self.clientInfo['videoStream'] = VideoStream(filename)
					self.state = self.READY
				except IOError:
					self.replyRtsp(self.FILE_NOT_FOUND_404, seq[1])
				
				# Generate a randomized RTSP session ID
				self.clientInfo['session'] = randint(100000, 999999)
				
				# Send RTSP reply
				self.replyRtsp(self.OK_200, seq[1])
				
				# Get the RTP/UDP port from the last line
				self.clientInfo['rtpPort'] = request[2].split(' ')[3]
		
		# Process PLAY request 		
		elif requestType == self.PLAY:
			if self.state == self.READY:
				print("processing PLAY\n")
				self.state = self.PLAYING
				# scale:
				scale = request[3].split(' ')[1]
				scale = eval(scale)
				# start:
				start = request[4].split(' ')[1][4:-1]
				start = eval(start)
				self.clientInfo['start'] = start 
				self.clientInfo['scale'] = scale
				self.clientInfo['videoStream'].setScale(scale)
				self.clientInfo['videoStream'].setStart(start)
				# Create a new socket for RTP/UDP
				self.clientInfo["rtpSocket"] = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				self.clientInfo["rtpSocket"].bind(('', self.rtpPort))
				
				self.replyRtsp(self.OK_200, seq[1])
				
				# Create a new thread and start sending RTP packets
				self.clientInfo['event'] = threading.Event()
				self.clientInfo['worker']= threading.Thread(target=self.sendRtp) 
				self.clientInfo['worker'].start()
		
		# Process PAUSE request
		elif requestType == self.PAUSE:
			if self.state == self.PLAYING:
				print("processing PAUSE\n")
				self.state = self.READY
				
				self.clientInfo['event'].set()
			
				self.replyRtsp(self.OK_200, seq[1])
		
		# Process TEARDOWN request
		elif requestType == self.TEARDOWN:
			print("processing TEARDOWN\n")

			self.clientInfo['event'].set()
			
			self.replyRtsp(self.OK_200, seq[1])
			
			# Close the RTP socket
			self.clientInfo['rtpSocket'].close()
		
		elif requestType == self.DESCRIBE:
			print("processing DESCRIBE\n")
			self.replyRtsp(self.OK_200, seq[1])
			
	def sendRtp(self):
		"""Send RTP packets over UDP."""
		#cnt = 0   ####################################################################
		while True:
			self.clientInfo['event'].wait(0.05) 
			
			# Stop sending if request is PAUSE or TEARDOWN
			if self.clientInfo['event'].isSet(): 
				break 
				
			data = self.clientInfo['videoStream'].nextFrame()
			if data: 
				frameNumber = self.clientInfo['videoStream'].frameNbr()
				try:
					address = self.clientInfo['rtspSocket'][1][0]
					port = int(self.clientInfo['rtpPort'])
##############################
					#cnt += 1
					#packet = self.makeRtp(data, frameNumber)
					#load = open(str(cnt), "wb")
					#load.write(packet)
					#load.close()
##############################
					self.clientInfo['rtpSocket'].sendto(self.makeRtp(data, frameNumber),(address,port))
				except Exception as e:
					print("Connection Error")
					print(e)
					print('-'*60)
					traceback.print_exc(file=sys.stdout)
					print('-'*60)
	def makeRtp(self, payload, frameNbr):
		"""RTP-packetize the video data."""
		version = 2
		padding = 0
		extension = 0
		cc = 0
		marker = 0
		pt = 26 # MJPEG type
		seqnum = frameNbr
		ssrc = 0 
		
		rtpPacket = RtpPacket()
		rtpPacket.encode(version, padding, extension, cc, seqnum, marker, pt, ssrc, payload)
        

		return rtpPacket.getPacket()
		
	def replyRtsp(self, code, seq):
		"""Send RTSP reply to the client."""
		if code == self.OK_200:
			#print("200 OK")
			reply = 'RTSP/1.0 200 OK\nCSeq: ' + seq
			if self.requestType != self.DESCRIBE:
				reply = 'RTSP/1.0 200 OK\nCSeq: ' + seq + '\nSession: ' + str(self.clientInfo['session']) 
			if self.requestType == self.SETUP:
				reply = reply + '\nRange: npt=0.0-' + str(self.clientInfo['videoStream'].length)
			elif self.requestType == self.DESCRIBE:
				reply = (reply +"\n\n" 
				+"v=0\n" +"o=xxsVideoServer 0 0 IP4 127.0.0.1\n" + "s=xxsPLAY\n" +"t=0 0\n" +
				"m=video " + str(self.rtpPort) +" RTP/AVP 26\n"+
				"a=rtpmap:26 MJPEG/90000 20 1333\n")
			connSocket = self.clientInfo['rtspSocket'][0]
			connSocket.send(reply.encode())
		
		# Error messages
		elif code == self.FILE_NOT_FOUND_404:
			print("404 NOT FOUND")
		elif code == self.CON_ERR_500:
			print("500 CONNECTION ERROR")

	
