
import socket, threading, sys, traceback, os, time
from PyQt5.QtWidgets import QMessageBox, QSlider
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from RtpPacket import RtpPacket
CACHE_FILE_NAME = "cache-"
CACHE_FILE_EXT = ".jpg"

from myWindow import myWindow #自定义的窗口


class Client:
	INIT = 0
	READY = 1
	PLAYING = 2
	state = INIT
	
	SETUP = 0
	PLAY = 1
	PAUSE = 2
	TEARDOWN = 3
	DESCRIBE = 4
	
	# Initiation..
	def __init__(self, serveraddr, serverport, rtpport, filename):
		self.window = myWindow()
		self.initWindow()
		self.serverAddr = serveraddr
		self.serverPort = int(serverport)
		self.rtpPort = int(rtpport)
		self.fileName = filename
		self.rtspSeq = 0
		self.sessionId = 0
		self.requestSent = -1
		self.teardownAcked = 0
		self.connectToServer()
		self.frameNbr = 0
		self.scale = 1
		self.time = 0
		#self.lock = threading.Lock()    ###锁
		self.sendRtspRequest(self.DESCRIBE)
		#self.lock.acquire()              ###锁
		time.sleep(0.1)
		self.setupMovie() ############  1.2
		self.window.window.show()
	
	def closeEvent(self, event):            #重写窗口的关闭事件
		self.pauseMovie()
		askIfClose = QMessageBox.question(self.window.window, "标题", "确认关闭吗？", QMessageBox.Yes | QMessageBox.No)
		if (askIfClose == QMessageBox.Yes):
			self.exitClient()
			event.accept()	
		else:
			self.playMovie()
			event.ignore()
		
	def initWindow(self):                                        
		self.window.window.closeEvent = self.closeEvent
		self.window.PPbutton.clicked.connect(self.PlayPause)
		self.window.BackButton.clicked.connect(self.backMovie)
		self.window.ForwardButton.clicked.connect(self.forwardMovie)
		self.window.scaleBox.currentIndexChanged.connect(self.changeScale)
		self.window.timeSlider.setMinimum(0)
		self.window.timeSlider.setMaximum(100)
		self.window.timeSlider.mousePressEvent = self.sliderMousePress
    

	def sliderMousePress(self, event):                    #重写滑块的鼠标点击函数，使之可以跟随鼠标移动，并且改变时间
		if event.button() == Qt.LeftButton:
			event.accept()
			x = event.pos().x()
			slider = self.window.timeSlider
			value = (slider.maximum() - slider.minimum()) * x / slider.width() + slider.minimum()
			print(x, slider.width(), value)
			slider.setValue(value)
			self.changeTime(value * self.length / slider.maximum())
		
    
	

##################################		 这部分用来控制播放时间的重定位，以及播放速度的调整
	def forwardMovie(self):               #快进按钮
		self.pauseMovie()
		start = min(self.length, self.time+2)
		self.playEvent.wait(0.02)
		self.time = round(start,3)
		self.playMovie()

	def backMovie(self):                #快退按钮
		self.pauseMovie()
		start = max(0, self.time - 2)
		self.playEvent.wait(0.02)
		self.time = round(start,3)
		self.playMovie()
	
	def changeTime(self, newtime):      #通用的改变时间
		if self.state == self.READY:
			self.time = newtime
		elif self.state == self.PLAYING:
			self.pauseMovie()
			self.playEvent.wait(0.02)
			self.time = newtime
			self.playMovie()
	
	def changeScale(self, i):
		if self.state == self.PLAYING:
			if i == 0:
				self.pauseMovie()
				self.playEvent.wait(0.02)
				self.scale = 1
				self.playMovie()
			elif i == 1:
				self.pauseMovie()
				self.playEvent.wait(0.02)
				self.scale = 0.5
				self.playMovie()
			elif i == 2:
				self.pauseMovie()
				self.playEvent.wait(0.02)
				self.scale = 2
				self.playMovie()
		elif self.state == self.PAUSE:
			tmplist = [1,0.5,2]
			self.scale = tmplist[i]
###################3
	def setupMovie(self):
		"""Setup button handler."""
		if self.state == self.INIT:
			self.sendRtspRequest(self.SETUP)
	
	def exitClient(self):
		"""Teardown button handler."""
		self.sendRtspRequest(self.TEARDOWN)	

		os.remove(CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT) # Delete the cache image from video
		##########################3
		#self.rtspSocket.close()
		self.rtpSocket.close()
		########################
		
	def PlayPause(self):
		if self.state == self.PLAYING:
			self.window.PPbutton.setText("PLAY")
			self.pauseMovie()
		elif self.state == self.READY:
			self.window.PPbutton.setText("PAUSE")
			self.playMovie()
	
	
	def pauseMovie(self):
		'''Pause button handler'''
		if self.state == self.PLAYING:
			self.sendRtspRequest(self.PAUSE)
	
	'''def playMovie(self):
		"""Play button handler."""
		if self.state == self.READY:
			# Create a new thread to listen for RTP packets
			threading.Thread(target=self.listenRtp).start()
			self.playEvent = threading.Event()
			self.playEvent.clear()
			self.sendRtspRequest(self.PLAY)'''
	
    
    # scale为倍速，start为视频起始播放时间
	def playMovie(self):   
		if self.state == self.READY:
			threading.Thread(target=self.listenRtp).start()
			self.playEvent = threading.Event()
			self.playEvent.clear()
			self.sendRtspRequest(self.PLAY, start=round(self.time,3), scale=self.scale)


	def listenRtp(self):
		"""Listen for RTP packets."""
		cnt = 0
		while True:
			try:
				data = self.rtpSocket.recv(20480)
				if data:
					self.time += 0.05 * self.scale
					self.window.timeLabel.setText(str(int(self.time)) +"s/" + str(int(self.length)) +"s") #设置时间
					self.window.timeSlider.setValue(self.time * self.window.timeSlider.maximum() / self.length)  #滑块移动
					rtpPacket = RtpPacket()
					rtpPacket.decode(data)
##############################
					#cnt += 1
					#img = open(str(cnt)+".jpg", "wb")
					#img.write(rtpPacket.getPayload())
					#img.close()
					#cnt += 1
					#load = open(str(cnt) , "wb")
					#load.write(data)
					#load.close()
###############################					
					currFrameNbr = rtpPacket.seqNum()
					print("Current Seq Num: " + str(currFrameNbr))
										
					if currFrameNbr > self.frameNbr: # Discard the late packet
						self.frameNbr = currFrameNbr
						self.updateMovie(self.writeFrame(rtpPacket.getPayload()))
			except:
				# Stop listening upon requesting PAUSE or TEARDOWN
				if self.playEvent.isSet():
					break
				
				# Upon receiving ACK for TEARDOWN request,
				# close the RTP socket
				if self.teardownAcked == 1:
					self.rtpSocket.shutdown(socket.SHUT_RDWR)
					self.rtpSocket.close()
					break
					
	def writeFrame(self, data):
		"""Write the received frame to a temp image file. Return the image file."""
		cachename = CACHE_FILE_NAME + str(self.sessionId) + CACHE_FILE_EXT
		file = open(cachename, "wb")
		file.write(data)
		file.close()
		
		return cachename
	
	def updateMovie(self, imageFile):
		"""Update the image file as video frame in the GUI."""
		self.window.update(imageFile)
		
	def connectToServer(self):
		"""Connect to the Server. Start a new RTSP/TCP session."""
		self.rtspSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		try:
			self.rtspSocket.connect((self.serverAddr, self.serverPort))
		except:
			QMessageBox.warning(self, "Connection Error!", 'Connection to \'%s\' failed.' %self.serverAddr)
	
	def sendRtspRequest(self, requestCode, start=0.0, scale=1):
		"""Send RTSP request to the server."""	
		#-------------
		# TO COMPLETE
		#-------------
		
		# Setup request
		if requestCode == self.SETUP and self.state == self.INIT:
			
			# Update RTSP sequence number.
			# ...
			self.rtspSeq += 1
			
			# Write the RTSP request to be sent.
			# request = ...
			request = ("SETUP " + self.fileName + " RTSP/1.0" + "\n" 
			+ "CSeq: " + str(self.rtspSeq) + "\n" 
			+ "Transport: RTP/UDP; client_port= " + str(self.rtpPort) + "\n\n")
			
			# Keep track of the sent request.
			# self.requestSent = ...
			self.requestSent = self.SETUP
		
		# Play request
		elif requestCode == self.PLAY and self.state == self.READY:
			# Update RTSP sequence number.
			# ...
			self.rtspSeq += 1
			# Write the RTSP request to be sent.
			# request = ...
			request = ("PLAY " + self.fileName + " RTSP/1.0" + "\n" 
			+"CSeq: " + str(self.rtspSeq) + "\n" 
			+ "Session: " + str(self.sessionId) + "\n" 
			+ "Scale: " + str(scale) + "\n" 
			+ "Range: npt=" + str(start)+"-"+ "\n\n")
			# Keep track of the sent request.
			# self.requestSent = ...
			self.requestSent = self.PLAY
		
		# Pause request
		elif requestCode == self.PAUSE and self.state == self.PLAYING:
			# Update RTSP sequence number.
			# ...
			self.rtspSeq += 1
			
			# Write the RTSP request to be sent.
			# request = ...
			request = ("PAUSE " + self.fileName + " RTSP/1.0" + "\n" 
			+ "CSeq: " + str(self.rtspSeq) + "\n" 
			+ "Session: " + str(self.sessionId) + "\n\n")
			
			# Keep track of the sent request.
			# self.requestSent = ...
			self.requestSent = self.PAUSE
			
		# Teardown request
		elif requestCode == self.TEARDOWN and not self.state == self.INIT:
			# Update RTSP sequence number.
			# ...
			self.rtspSeq += 1
			
			# Write the RTSP request to be sent.
			# request = ...
			request = ("TEARDOWN " + self.fileName + " RTSP/1.0" + "\n"
			+ "CSeq: " + str(self.rtspSeq) 
			+ "\n"+ "Session: " + str(self.sessionId) + "\n\n")
			# Keep track of the sent request.
			# self.requestSent = ...
			self.requestSent = self.TEARDOWN
		elif requestCode == self.DESCRIBE and self.state == self.INIT:
			threading.Thread(target=self.recvRtspReply).start()
			self.rtspSeq += 1
			request = ("DESCRIBE " + self.fileName + " RTSP/1.0\n"
			+ "CSeq: " + str(self.rtspSeq) + "\n"
			"Session: sdp\n\n" )
			self.requestSent = self.DESCRIBE
		else:
			return
		
		# Send the RTSP request using rtspSocket.
		# ...
		self.rtspSocket.send(request.encode())
		
		print('\nData sent:\n' + request)
	
	def recvRtspReply(self):
		"""Receive RTSP reply from the server."""
		#if self.requestSent == self.DESCRIBE:
		#	self.lock.acquire()
		while True:
			reply = self.rtspSocket.recv(1024)
			
			if reply: 
				self.parseRtspReply(reply.decode("utf-8"))
				print("Receive:\n" + reply.decode("utf-8"))
			
			# Close the RTSP socket upon requesting Teardown
			if self.requestSent == self.TEARDOWN:
				self.rtspSocket.shutdown(socket.SHUT_RDWR)
				self.rtspSocket.close()
				break
	
	def parseRtspReply(self, data):
		"""Parse the RTSP reply from the server."""
		lines = data.split('\n')
		seqNum = int(lines[1].split(' ')[1])
		
		# Process only if the server reply's sequence number is the same as the request's
		if seqNum == self.rtspSeq:
			if self.requestSent != self.DESCRIBE:
				session = int(lines[2].split(' ')[1])
			# New RTSP session ID
				if self.sessionId == 0:
					self.sessionId = session
			else:
				session = 0
			# Process only if the session ID is the same
			if self.sessionId == session:
				if int(lines[0].split(' ')[1]) == 200: 
					if self.requestSent == self.SETUP:
						#-------------
						# TO COMPLETE
						#-------------
						# Update RTSP  state.
						# self.state = ...
						self.state = self.READY
						length = lines[3].split(' ')[1][8:]
						self.length = eval(length)
						self.window.timeLabel.setText("0s/" + str(int(self.length)) +"s")   #初始化播放时间
 						# Open RTP port.
						self.openRtpPort() 
					elif self.requestSent == self.PLAY:
						# self.state = ...
						self.state = self.PLAYING
					elif self.requestSent == self.PAUSE:
						# self.state = ...
						self.state = self.READY
						
						# The play thread exits. A new thread is created on resume.
						self.playEvent.set()
					elif self.requestSent == self.TEARDOWN:
						# self.state = ...
						
						# Flag the teardownAcked to close the socket.
						self.teardownAcked = 1 
					elif self.requestSent == self.DESCRIBE:                          #describe
						#self.lock.release()
						sdpInfo = self.parseSdp(lines[2:])
	
	def parseSdp(self, lines):
		self.window.infoBox.setFont(QFont('Consolas',20))
		'''text = "SDP:\n"
		for line in lines:
			text += line + '\n'
		self.window.infoBox.setText(text)'''
		self.window.infoBox.append("SDP:\n")
		for line in lines:
			self.window.infoBox.append(line)



	def openRtpPort(self):
		"""Open RTP socket binded to a specified port."""
		#-------------
		# TO COMPLETE
		#-------------
		# Create a new datagram socket to receive RTP packets from the server
		# self.rtpSocket = ...
		self.rtpSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		# Set the timeout value of the socket to 0.5sec
		# ...
		self.rtpSocket.settimeout(0.5)
		try:
			# Bind the socket to the address using the RTP port given by the client user
			# ...
			self.rtpSocket.bind(("", self.rtpPort))
		except Exception as e:
			tkMessageBox.showwarning('Unable to Bind', 'Unable to bind PORT=' ,self.rtpPort)
			print(e)
	
