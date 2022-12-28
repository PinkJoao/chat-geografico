# PYSIDE6 IMPORTS ___________________________________________________________________________________________________
import sys
from PySide6.QtWidgets import QApplication, QMainWindow
from PySide6.QtCore import Qt
from Ui_ChatWindow import Ui_ChatWindow

# APP IMPORTS _______________________________________________________________________________________________________
from threading import Thread
from client import Client

# GLOBALS ___________________________________________________________________________________________________________
APP = ''
ISCONECTED = False


# APP CLASS _________________________________________________________________________________________________________
class ChatWindow(QMainWindow,Ui_ChatWindow):
    def __init__(self):
        super(ChatWindow, self).__init__()
        self.setupUi(self)

# APP ATRIBUTES _____________________________________________________________________________________________________
        self.client = None
        self.username = ''
        self.nickname = ''
        self.currentChat = None

# APP ROUTINE _______________________________________________________________________________________________________
        self.messageEdit.setReadOnly(True)

# APP EVENTS ________________________________________________________________________________________________________
        self.messageEdit.returnPressed.connect(lambda: self.sendMessageTo(self.messageEdit.text(), self.contactsList.currentItem()))

        self.contactsList.itemPressed.connect(lambda: self.changeChat(self.contactsList.currentItem().text()))

        self.loginButton.clicked.connect(lambda: self.login(self.nameEdit.text(), self.nicknameEdit.text()))

        self.nameEdit.textEdited.connect(lambda: self.loginButton.setText('Conectar'))
        self.nicknameEdit.textEdited.connect(lambda: self.loginButton.setText('Conectar'))

# CLOSE APP EVENT ___________________________________________________________________________________________________
    def closeEvent(self, event):
        can_exit = True

        if self.client:
            self.client.stop()

        if can_exit:
            event.accept()
        else:
            event.ignore()



# APP FUNCTIONS _____________________________________________________________________________________________________
    def sendMessageTo(self, message, contact):
        self.messageEdit.clear()
        if contact or self.currentChat:
            if contact:
                contact = contact.text()
                 
            elif self.currentChat:
                items = self.contactsList.findItems(self.currentChat, Qt.MatchExactly)
                if len(items) == 0:
                    username, nickname, status = self.currentChat.split(' - ')
                    self.currentChat = username + ' - ' + nickname + ' - off'
                
                contact = self.currentChat

            print('sending the message [', message, '] to [', contact, ']')
            self.messageList.addItem(message)
            self.client.sendMessage(message, contact)


    def changeChat(self, contact):
        self.messageEdit.setReadOnly(False)
        self.currentChat = contact
        username, nickname, status = contact.split(' - ')
        self.messageList.clear()
        contact = self.client.searchContact(username, nickname)
        self.messageList.addItems(contact[4])

    def login(self, username, nickname):
        if username and nickname and self.loginButton.text() == 'Conectar':
            self.username = username
            self.nickname = nickname

            self.nameEdit.setReadOnly(True)
            self.nicknameEdit.setReadOnly(True)
            self.loginButton.setText('Desconectar')

            self.client = Client(self)
            
            thread = Thread(target=self.startClient)
            thread.start()

        elif self.loginButton.text() == 'Desconectar':
            self.nameEdit.setReadOnly(False)
            self.nicknameEdit.setReadOnly(False)
            self.loginButton.setText('Reconectar')

            self.logoff()

        elif self.loginButton.text() == 'Reconectar':
            self.nameEdit.setReadOnly(True)
            self.nicknameEdit.setReadOnly(True)
            self.loginButton.setText('Desconectar')

            thread = Thread(target=self.startClient)
            thread.start()
        
    def startClient(self):
        self.client.start()

    def logoff(self):
        self.client.stop()
        self.contactsList.clear()
        self.messageList.clear()
        self.currentChat = None


# SETUP FUNCTIONS ___________________________________________________________________________________________________
def startWindow():
    global APP
    if __name__ == '__main__':
        app = QApplication(sys.argv)
        APP = ChatWindow()
        APP.show()
        sys.exit(app.exec())

startWindow()

