class VideoStream:
	def __init__(self, filename):  #预处理视频文件
		self.filename = filename
		try:
			self.file = open(filename, 'rb')
		except:
			raise IOError
		self.frameNum = 0
		self.frameSeq = 0
		###
		self.frameRate = 20            #帧率
		frameSizeList = list()
		while True:   #记录每一帧的大小
			frameSize = self.file.read(5)
			if not frameSize:
				break
			frameSize = int(frameSize)
			frameSizeList.append(frameSize)
			self.file.seek(frameSize, 1)
		self.file.seek(0,0)   #还原文件指针
		self.length = len(frameSizeList) / 20        #时长
		self.framePosList = list()
		self.framePosList.append(0)
		for i in range(1,len(frameSizeList)):
			self.framePosList.append(self.framePosList[i-1] + 5 + frameSizeList[i-1]) 
	
	def setScale(self, scale):        #设置帧的读取位置与速率
		self.scale = scale
		self.keepFrame = False
		self.LastFrame = ''
	
	def setStart(self, start):
		self.start = start
		startFrame = int(self.start * 20)
		self.frameSeq = startFrame
		try:
			self.file.seek(self.framePosList[startFrame], 0)
		except Exception as e:
			print(e)
		
	def nextFrame(self):                 #帧的读取
		"""Get next frame."""
		if self.scale == 2:
			data = self.readOneFrame()
			data = self.readOneFrame()
			self.frameSeq += 2
		elif self.scale == 0.5:
			if self.keepFrame:
				data = self.LastFrame
				self.keepFrame = False
			else:
				data = self.readOneFrame()
				self.LastFrame = data
				self.keepFrame = True
				self.frameSeq += 1
		elif self.scale == 1:
			data = self.readOneFrame()
			self.frameSeq += 1
		self.frameNum += 1
		return data

	def readOneFrame(self):
		data = self.file.read(5)
		if data:
			framelength = int(data)
			data = self.file.read(framelength)
		return data
		
	def frameNbr(self):
		"""Get frame number."""
		return self.frameNum
	
	