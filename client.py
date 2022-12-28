# COMUNICATION IMPORTS ______________________________________________________________________________________________
import socket
from paho.mqtt import client as mqtt_client
import xmlrpc.client
from xmlrpc.server import SimpleXMLRPCServer as SimpleServer

# TUPLESPACE IMPORTS ________________________________________________________________________________________________
import linsimpy

# GEOLOCALIZATION IMPORTS ___________________________________________________________________________________________
import geocoder
from geopy import distance as geo

# UTENSILS IMPORTS __________________________________________________________________________________________________
from PySide6.QtCore import Qt
from time import sleep
from threading import Thread
from random import randint as rand

# CLIENT CALSS ______________________________________________________________________________________________________
class Client():
    def __init__(self, user):
# CLIENT ATRIBUTES __________________________________________________________________________________________________

        self.user = user # provém acesso à janela da aplicação

        self.broker = 'broker.hivemq.com'
        
        self.ip = socket.gethostbyname(socket.gethostname())
        self.port = rand(1234, 65000)
        self.addr = (self.ip, self.port)
        self.fullAddr = str('http://' + str(self.ip) + ':' + str(self.port) + '/') # endereço de acesso xml rpc

        self.flag = True # flag para quebra de o loop ao desconectar
        self.username = user.username
        self.nickname = user.nickname
        self.password = 'public'
        self.id = user.username + ' - ' + user.nickname

        self.coordinates = None # coordendas geograficas

        self.contacts = linsimpy.TupleSpace() # espaço de tuplas
        
        self.client = None # client MOM
        self.server = SimpleServer(self.addr) # server xml para acesso remoto

        self.loop = 0 # contador que possibilita o recebimento de mensagens da fila

    def onRange(self, lat, lng): 
        # calcula a distancia do user em relação as coordenadas informadas
        target = (lat, lng)
        if geo.distance(self.coordinates, target).km > self.user.communicationMeter.value():
            return False
        else:
            return True

    def searchContact(self, username, nickname): 
        # busca um contato no espaço de tuplas com base no nome e apelido
        for contact in self.contacts.items:
            if contact[1] == username and contact[2] == nickname:
                return contact
        
        return False

    def removeContact(self, username, nickname, status): 
        # remove um contato do espaço de tuplas e da lista de contatos da janela
        if status == 'off':
            status = 'on'
        elif status == 'on':
            status = 'off'

        contact = self.searchContact(username, nickname)
        if contact:
            self.contacts.in_(contact)
            items = self.user.contactsList.findItems(username + ' - ' + nickname + ' - ' + status, Qt.MatchExactly)
            mock = self.user.contactsList.takeItem(self.user.contactsList.row(items[0]))
            del mock
    
    def addContact(self, username, nickname, addr, status, newLat, newLng): 
        # adiciona(ou modifica) um contato no espaco de tuplas
        contact = self.searchContact(username, nickname)
        if contact: 
            # caso o contato já exista no espaço de tuplas, modifica o contato de acordo com os novos parametros
            messages = contact[4]
            self.removeContact(username, nickname, status)
            newContact = self.addContact(username, nickname, addr, status, newLat, newLng)
            for message in messages:
                newContact[4].append(message)
        else: 
            # caso contrário, adiciona o novo contato ao espaço de tuplas e à tela do user, também se adiciona á lista do contato, remotamente
            proxy = False
            if status != 'off':
                proxy = xmlrpc.client.ServerProxy(addr)
                mock = proxy.addMe(self.username, self.nickname, self.fullAddr, 'on', newLat, newLng)
            messages = []
            newUser = (proxy, username, nickname, status, messages, newLat, newLng)
            self.contacts.out(newUser)
            self.user.contactsList.addItem(username + ' - ' + nickname + ' - ' + status)
            return newUser
            
    def addMe(self, username, nickname, addr, status, newLat, newLng): 
        # metodo para que possibilita outros users se adicionarem ao espaço de tuplas deste user
        proxy = xmlrpc.client.ServerProxy(addr)
        messages = []
        newUser = (proxy, username, nickname, status, messages, newLat, newLng)
        self.contacts.out(newUser)
        self.user.contactsList.addItem(username + ' - ' + nickname + ' - ' + status)
        return True
    

    def on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    def on_disconnect(self, client, userdata, rc):
        if rc == 0:
            print('Connection terminated!')

    def on_subscribe(self, client, userdata, mid, granted_qos):
        print('Subscribed to:', str(mid), str(granted_qos))


    def on_message(self, client, userdata, message): 
        # função executada ao receber uma mensagem do broker
        match message.topic:
            case 'newUserOnline':
                # se um um novo usuario está online adiciona esse usuario ao espaco de tuplas
                message = message.payload.decode('utf-8')
                newUsername, newNickname, newIp, newPort, newLat, newLng = message.split(':')
                newAddr = str('http://' + str(newIp) + ':' + str(newPort) + '/')
                if newUsername != self.username and newNickname != self.nickname:
                    self.addContact(newUsername, newNickname, newAddr, 'on', newLat, newLng)


            case 'newUserOffline':
                # se um um novo usuario está offline altera o status de online para offline
                message = message.payload.decode('utf-8')
                newUsername, newNickname, newIp, newPort, newLat, newLng = message.split(':')
                newAddr = str('http://' + str(newIp) + ':' + str(newPort) + '/')
                if newUsername != self.username and newNickname != self.nickname:
                    self.addContact(newUsername, newNickname, newAddr, 'off', newLat, newLng)

            case self.id:
                # caso receba uma mensagem da fila de mensagens executa o metodo de recebimento de mensagens
                message = message.payload.decode('utf-8')
                username, nickname, message, addr, lat, lng = message.split(' - ')
                thread = Thread(target=self.receiveMessage, args=(message, username, nickname, addr, lat, lng))
                thread.start()

    
    def receiveMessage(self, message, username, nickname, addr, lat, lng):
        # função de recebimento de mensagens, de forma sincrona via rpc, ou internamente para a exibiçao de mensagens assicronas
        contact = self.searchContact(username, nickname)
        if contact:
            contact[4].append(message)
            if self.user.currentChat:
                # caso o remetente esteja online:
                if self.user.currentChat == username + ' - ' + nickname + ' - ' + 'off':
                    self.user.currentChat = username + ' - ' + nickname + ' - ' + 'on'

                if self.user.currentChat == username + ' - ' + nickname + ' - ' + 'on':
                    self.user.messageList.addItem(message)
        else:
            # caso o remetente esteja aparentemente offline, espera por 3 segundos para garantir 
            if self.loop != 3:
                self.loop = self.loop + 1
                sleep(1)
                self.receiveMessage(message, username, nickname, addr, lat, lng)
            else:
                # após os 3 segundos, adiciona o contato offline ao espaço de tuplas, e as mensagens da fila, ao chat
                self.loop = 0
                newUser = self.addContact(username, nickname, addr, 'off', lat, lng)
                newUser[4].append(message)
        return True


    def sendMsgOn(self, message, contact):
        # envia mensagem sincrona
        mock = contact[0].receiveMessage(message, self.username, self.nickname, self.fullAddr, self.coordinates[0], self.coordinates[1])

    def sendMsgOff(self, message, contact):
        # envia mensagem assincrona
        topic = contact[1] + ' - ' + contact[2]
        print('publishing the message [', message, '] to the topic [', topic,']')
        message = self.id + ' - ' + message + ' - ' + self.fullAddr + ' - ' + str(self.coordinates[0]) + ' - ' + str(self.coordinates[1])
        self.client.publish(topic, message, 1)

    def sendMessage(self, message, contact):
        # decide se a mensagem será enviada de forma sincrona ou assincrona
        username, nickname, status = contact.split(' - ')
        contact = self.searchContact(username, nickname)

        contact[4].append(message)
        message = '[' + self.nickname + ']:' + message

        if status == 'on' and self.onRange(contact[5], contact[6]):
            self.sendMsgOn(message, contact)
        else:
            self.sendMsgOff(message, contact)
        

    def startServer(self):
        # inicia o server rpc
        self.server.serve_forever()


    def start(self):
        self.flag = True
        self.server.register_function(self.addMe, 'addMe')
        self.server.register_function(self.receiveMessage, 'receiveMessage')

        thread = Thread(target=self.startServer)
        thread.start()

        geoinfo = geocoder.ipinfo('me')
        self.coordinates = (geoinfo.latlng[0],geoinfo.latlng[1])

        
        if not self.client:
            self.client = mqtt_client.Client(self.id, clean_session= False)

            self.client.on_connect = self.on_connect
            self.client.on_disconnect = self.on_disconnect
            self.client.on_subscribe = self.on_subscribe
            self.client.on_message = self.on_message

            self.client.connect(self.broker)

            sleep(0.5)
            self.client.loop_start()

            sleep(0.3)
            self.client.subscribe('newUserOnline',1)
            sleep(0.3)
            self.client.subscribe('newUserOffline',1)
            sleep(0.3)
            self.client.subscribe(self.id,1)
        else:
            self.client.connect(self.broker)

            sleep(0.5)
            self.client.loop_start()


        sleep(0.3)
        self.client.publish('newUserOnline', self.username + ':' + self.nickname + ':' + self.ip + ':' + str(self.port) + ':' + str(self.coordinates[0]) + ':' + str(self.coordinates[1]))
        sleep(0.3)


        while True:
            if self.flag == False:
                break

        self.client.disconnect()
        self.client.loop_stop()


    def stopserver(self):
        # desliga o server rpc
        self.server.shutdown()
        
    def stop(self):
        #, avisa aos outros users a mudança de status para offline, para o loop de conexão, desliga o server rpc
        thread = Thread(target=self.stopserver)
        thread.start()

        self.client.publish('newUserOffline', self.username + ':' + self.nickname + ':' + self.ip + ':' + str(self.port) + ':' + str(self.coordinates[0]) + ':' + str(self.coordinates[1]))
        sleep(0.3)

        self.flag = False

        self.contacts = None
        newContactsList = linsimpy.TupleSpace()
        self.contacts = newContactsList

        self.coordinates = None