import socket, sys, json
from pynput.keyboard import Key, Listener
from struct import pack, unpack, calcsize
from threading import Thread

# Message code pour le serveur
CONNECT_TO_CAR = 1
MOVE_CAR       = 2
GET_MALUS      = 3
SEND_MALUS     = 4

# Addresse IP des victimes
victimes = ['192.168.1.100','192.168.1.101','192.168.1.102','192.168.1.103','192.168.1.104','192.168.1.105','192.168.1.106','192.168.1.108']
nbr_malus = 1


# Cree un paquet avec le code du type de message
def create_packet(op_code, data):
    return pack("!I{}s".format(len(data)), op_code, data.encode())

# Extrait le code du type de message ainsi que les donnees du paquet
def process_packet(packet):
    return unpack("!I{}s".format(len(packet)-calcsize("!I")), packet)

# Connexion au serveur
HOST = '192.168.1.1'
PORT = 1337
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
    mySocket.connect((HOST, PORT))
    connect_packet = create_packet(CONNECT_TO_CAR, json.dumps({'ip': '192.168.1.107', 'port': 2340}))
    mySocket.send(connect_packet)
except socket.error:
    print "La connexion a echoue."
    sys.exit()
print "Connexion etablie avec le serveur."
#msgServeur = mySocket.recv(2048).decode()

def on_press(key):
    global nbr_malus
    if key == Key.up:
        mySocket.send(create_packet(MOVE_CAR, "UP"))
    if key == Key.down:
        mySocket.send(create_packet(MOVE_CAR, "DOWN"))
    if key == Key.left:
        mySocket.send(create_packet(MOVE_CAR, "LEFT"))
    if key == Key.right:
        mySocket.send(create_packet(MOVE_CAR, "RIGHT"))
    if key == Key.esc:
        mySocket.send(create_packet(MOVE_CAR, "FIN"))
    if key == Key.f1:
        if nbr_malus > 0:
            mySocket.send(create_packet(SEND_MALUS, victimes[0]))
            nbr_malus -= 1
    if key == Key.f2:
        if nbr_malus > 0:
            mySocket.send(create_packet(SEND_MALUS, victimes[1]))
    if key == Key.f3:
        if nbr_malus > 0:
            mySocket.send(create_packet(SEND_MALUS, victimes[2]))
            nbr_malus -= 1
    if key == Key.f4:
        if nbr_malus > 0:
            mySocket.send(create_packet(SEND_MALUS, victimes[3]))
            nbr_malus -= 1
    if key == Key.f5:
        if nbr_malus > 0:
            mySocket.send(create_packet(SEND_MALUS, victimes[4]))
            nbr_malus -= 1
    if key == Key.f6:
        if nbr_malus > 0:
            mySocket.send(create_packet(SEND_MALUS, victimes[5]))
            nbr_malus -= 1
    if key == Key.f7:
        if nbr_malus > 0:
            mySocket.send(create_packet(SEND_MALUS, victimes[6]))
            nbr_malus -= 1
    if key == Key.f8:
        if nbr_malus > 0:
            mySocket.send(create_packet(SEND_MALUS, victimes[7]))
            nbr_malus -= 1


def on_release(key):
    if key == Key.up:
        mySocket.send(create_packet(MOVE_CAR, "UPEND"))
    if key == Key.down:
        mySocket.send(create_packet(MOVE_CAR, "DOWNEND"))
    if key == Key.left:
        mySocket.send(create_packet(MOVE_CAR, "LEFTEND"))
    if key == Key.right:
        mySocket.send(create_packet(MOVE_CAR, "RIGHTEND"))
    if key == Key.esc:
        mySocket.send(create_packet(MOVE_CAR, "FIN"))
        mySocket.close()
        return false
    if key == Key.space:
        mySocket.send(create_packet(MOVE_CAR, "FIN"))

# Thread pour ecouter si on obtiens un BONUS
def waitMalus():
    while 1:
        global nbr_malus
        packet = mySocket.recv(2048)
        code, msg = process_packet(packet)
        if code == GET_MALUS:
            print("MALUS RECU", nbr_malus)
            nbr_malus += 1

thread = Thread(target = waitMalus)
thread.start()

# Collect events until released
with Listener(
        on_press=on_press,
        on_release=on_release) as listener:
    listener.join()
