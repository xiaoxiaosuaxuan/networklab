import sys
from PyQt5.QtWidgets import QApplication
from Client import Client
from qt_material import apply_stylesheet

if __name__ == "__main__":
	try:
		#serverAddr = sys.argv[1]
		#serverPort = sys.argv[2]
		#rtpPort = sys.argv[3]
		#fileName = sys.argv[4]	
		serverAddr = "127.0.0.1"
		serverPort = "5001"
		rtpPort = "5070"
		fileName = "movie.Mjpeg"
	except:
		print("[Usage: ClientLauncher.py Server_name Server_port RTP_port Video_file]\n")	
	app = QApplication([])
	apply_stylesheet(app, theme='dark_teal.xml')
	app.setStyle('Fusion')
	# Create a new client
	client = Client(serverAddr, serverPort, rtpPort, fileName)
	app.exec_()

