from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QMessageBox
from PyQt5.QtGui import QPixmap
import Ui_playerWindow
import time



'''class myWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_playerWindow.Ui_playerWindow()
        self.ui.setupUi(self)
        self.ui.video.setScaledContents(True)
    
    def update(img):
        pix = QPixmap(img)
        self.ui.video.setPixmap(pix)'''

class myWindow(Ui_playerWindow.Ui_playerWindow):
    def __init__(self):
        self.window = QMainWindow()
        self.setupUi(self.window)
        self.video.setScaledContents(True)

    def update(self,img):
        pix = QPixmap(img)
        self.video.setPixmap(pix)
    
    
'''class myRealWindow(QMainWindow):
    def closeEvent(self, event):
        askIfClose = QMessageBox.question(self, "标题", "确认关闭吗？", QMessageBox.Yes | QMessageBox.No)
        if (askIfClose == QMessageBox.Yes):
            event.accept()
        else:
            event.ignore()'''






'''app = QApplication([])
window = myWindow()
window.show()
pix = QPixmap()
pix.load("img1.jpg")
window.ui.video.setPixmap(pix)
time.sleep(3)
pix.load("img2.png")
window.ui.video.setPixmap(pix)
app.exec_()'''
'''def a():
    print("aaaa")

app = QApplication([])
w = myWindow()
w.window.show()
w.update("img1.jpg")
app.exec_()'''