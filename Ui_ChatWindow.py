# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'chatWindow.ui'
##
## Created by: Qt User Interface Compiler version 6.3.1
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QLineEdit, QListWidget,
    QListWidgetItem, QMainWindow, QPushButton, QSizePolicy,
    QSpinBox, QWidget)

class Ui_ChatWindow(object):
    def setupUi(self, ChatWindow):
        if not ChatWindow.objectName():
            ChatWindow.setObjectName(u"ChatWindow")
        ChatWindow.resize(481, 551)
        self.centralwidget = QWidget(ChatWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.messageList = QListWidget(self.centralwidget)
        self.messageList.setObjectName(u"messageList")
        self.messageList.setGeometry(QRect(10, 10, 291, 501))
        self.contactsList = QListWidget(self.centralwidget)
        self.contactsList.setObjectName(u"contactsList")
        self.contactsList.setGeometry(QRect(310, 120, 161, 341))
        self.messageEdit = QLineEdit(self.centralwidget)
        self.messageEdit.setObjectName(u"messageEdit")
        self.messageEdit.setGeometry(QRect(10, 520, 461, 21))
        self.communicationMeter = QSpinBox(self.centralwidget)
        self.communicationMeter.setObjectName(u"communicationMeter")
        self.communicationMeter.setGeometry(QRect(310, 490, 161, 21))
        self.communicationMeter.setMinimum(5)
        self.communicationMeter.setMaximum(999999)
        self.contactsLabel = QLabel(self.centralwidget)
        self.contactsLabel.setObjectName(u"contactsLabel")
        self.contactsLabel.setGeometry(QRect(310, 100, 49, 16))
        self.communicationLabel = QLabel(self.centralwidget)
        self.communicationLabel.setObjectName(u"communicationLabel")
        self.communicationLabel.setGeometry(QRect(310, 470, 121, 16))
        self.loginButton = QPushButton(self.centralwidget)
        self.loginButton.setObjectName(u"loginButton")
        self.loginButton.setGeometry(QRect(310, 70, 161, 24))
        self.nicknameEdit = QLineEdit(self.centralwidget)
        self.nicknameEdit.setObjectName(u"nicknameEdit")
        self.nicknameEdit.setGeometry(QRect(310, 40, 161, 21))
        self.nameEdit = QLineEdit(self.centralwidget)
        self.nameEdit.setObjectName(u"nameEdit")
        self.nameEdit.setGeometry(QRect(310, 10, 161, 21))
        ChatWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(ChatWindow)

        QMetaObject.connectSlotsByName(ChatWindow)
    # setupUi

    def retranslateUi(self, ChatWindow):
        ChatWindow.setWindowTitle(QCoreApplication.translate("ChatWindow", u"MainWindow", None))
        self.messageEdit.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"Digite aqui uma nova mensagem", None))
        self.communicationMeter.setSuffix(QCoreApplication.translate("ChatWindow", u"km", None))
        self.contactsLabel.setText(QCoreApplication.translate("ChatWindow", u"Contatos", None))
        self.communicationLabel.setText(QCoreApplication.translate("ChatWindow", u"Raio de comunica\u00e7\u00e3o", None))
        self.loginButton.setText(QCoreApplication.translate("ChatWindow", u"Conectar", None))
        self.nicknameEdit.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"Digite seu apelido", None))
        self.nameEdit.setPlaceholderText(QCoreApplication.translate("ChatWindow", u"Digite seu nome", None))
    # retranslateUi

