# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\user\Desktop\计网大作业\version1.3_添加describe命令，信息显示\client\playerWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_playerWindow(object):
    def setupUi(self, playerWindow):
        playerWindow.setObjectName("playerWindow")
        playerWindow.resize(941, 751)
        playerWindow.setIconSize(QtCore.QSize(0, 0))
        self.centralwidget = QtWidgets.QWidget(playerWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.layoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget.setGeometry(QtCore.QRect(70, 60, 791, 521))
        self.layoutWidget.setObjectName("layoutWidget")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.video = QtWidgets.QLabel(self.layoutWidget)
        self.video.setText("")
        self.video.setObjectName("video")
        self.verticalLayout.addWidget(self.video)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.timeSlider = QtWidgets.QSlider(self.layoutWidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(1)
        sizePolicy.setHeightForWidth(self.timeSlider.sizePolicy().hasHeightForWidth())
        self.timeSlider.setSizePolicy(sizePolicy)
        self.timeSlider.setSingleStep(1)
        self.timeSlider.setPageStep(3)
        self.timeSlider.setOrientation(QtCore.Qt.Horizontal)
        self.timeSlider.setTickInterval(0)
        self.timeSlider.setObjectName("timeSlider")
        self.horizontalLayout.addWidget(self.timeSlider)
        self.timeLabel = QtWidgets.QLabel(self.layoutWidget)
        self.timeLabel.setText("")
        self.timeLabel.setObjectName("timeLabel")
        self.horizontalLayout.addWidget(self.timeLabel)
        self.horizontalLayout.setStretch(0, 7)
        self.horizontalLayout.setStretch(1, 1)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(0, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.infoBox = QtWidgets.QTextBrowser(self.layoutWidget)
        self.infoBox.setObjectName("infoBox")
        self.horizontalLayout_3.addWidget(self.infoBox)
        self.horizontalLayout_3.setStretch(0, 7)
        self.horizontalLayout_3.setStretch(1, 2)
        self.layoutWidget1 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget1.setGeometry(QtCore.QRect(110, 620, 451, 61))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.BackButton = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.BackButton.sizePolicy().hasHeightForWidth())
        self.BackButton.setSizePolicy(sizePolicy)
        self.BackButton.setObjectName("BackButton")
        self.horizontalLayout_4.addWidget(self.BackButton)
        self.PPbutton = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PPbutton.sizePolicy().hasHeightForWidth())
        self.PPbutton.setSizePolicy(sizePolicy)
        self.PPbutton.setMinimumSize(QtCore.QSize(0, 0))
        self.PPbutton.setObjectName("PPbutton")
        self.horizontalLayout_4.addWidget(self.PPbutton)
        self.ForwardButton = QtWidgets.QPushButton(self.layoutWidget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(2)
        sizePolicy.setHeightForWidth(self.ForwardButton.sizePolicy().hasHeightForWidth())
        self.ForwardButton.setSizePolicy(sizePolicy)
        self.ForwardButton.setObjectName("ForwardButton")
        self.horizontalLayout_4.addWidget(self.ForwardButton)
        self.layoutWidget2 = QtWidgets.QWidget(self.centralwidget)
        self.layoutWidget2.setGeometry(QtCore.QRect(650, 620, 191, 51))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.scaleLabel = QtWidgets.QLabel(self.layoutWidget2)
        self.scaleLabel.setObjectName("scaleLabel")
        self.horizontalLayout_2.addWidget(self.scaleLabel)
        self.scaleBox = QtWidgets.QComboBox(self.layoutWidget2)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.scaleBox.sizePolicy().hasHeightForWidth())
        self.scaleBox.setSizePolicy(sizePolicy)
        self.scaleBox.setObjectName("scaleBox")
        self.scaleBox.addItem("")
        self.scaleBox.addItem("")
        self.scaleBox.addItem("")
        self.horizontalLayout_2.addWidget(self.scaleBox)
        self.horizontalLayout_2.setStretch(1, 1)
        playerWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(playerWindow)
        self.statusbar.setObjectName("statusbar")
        playerWindow.setStatusBar(self.statusbar)

        self.retranslateUi(playerWindow)
        QtCore.QMetaObject.connectSlotsByName(playerWindow)

    def retranslateUi(self, playerWindow):
        _translate = QtCore.QCoreApplication.translate
        playerWindow.setWindowTitle(_translate("playerWindow", "videoPlayer"))
        self.BackButton.setText(_translate("playerWindow", "back"))
        self.PPbutton.setText(_translate("playerWindow", "play"))
        self.ForwardButton.setText(_translate("playerWindow", "forward"))
        self.scaleLabel.setText(_translate("playerWindow", "倍速设置"))
        self.scaleBox.setItemText(0, _translate("playerWindow", "1x"))
        self.scaleBox.setItemText(1, _translate("playerWindow", "0.5x"))
        self.scaleBox.setItemText(2, _translate("playerWindow", "2x"))
