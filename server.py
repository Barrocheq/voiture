import socket, sys, time, os
from struct import pack, unpack, calcsize

HOST = '192.168.1.107'
PORT = 2340
mySocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
try:
   mySocket.bind((HOST, PORT))
except socket.error:
   print "La liaison du socket a l adresse choisie a echoue."
   sys.exit()


import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)
GPIO.cleanup()

Moteur_1_avant = 37
Moteur_1_arriere = 33 # Droite
Moteur_2_avant = 35
Moteur_2_arriere = 31 # Gauche


GPIO.setup(Moteur_1_avant, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Moteur_1_arriere, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Moteur_2_avant, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(Moteur_2_arriere, GPIO.OUT, initial=GPIO.LOW)


# Extrait le code du type de message ainsi que les donnees du paquet
def process_packet(packet):
    return unpack("!I{}s".format(len(packet)-calcsize("!I")), packet)

def avant() :
    print ("marche avant")
    GPIO.output(Moteur_1_avant, GPIO.HIGH)

def arriere() :
    print ("marche arriere")
    GPIO.output(Moteur_2_avant, GPIO.HIGH)

def droite() :
    print ("droite")
    GPIO.output(Moteur_1_arriere, GPIO.HIGH)

def gauche() :
    print ("gauche")
    GPIO.output(Moteur_2_arriere, GPIO.HIGH)

def avantEND() :
    print ("marche avant end")
    GPIO.output(Moteur_1_avant, GPIO.LOW)

def arriereEND() :
    print ("marche arriere end")
    GPIO.output(Moteur_2_avant, GPIO.LOW)


def droiteEND() :
    print ("droite end")
    GPIO.output(Moteur_1_arriere, GPIO.LOW)

def gaucheEND() :
    print ("gauche end")
    GPIO.output(Moteur_2_arriere, GPIO.LOW)

def stop() :
    GPIO.output(Moteur_1_avant, GPIO.LOW)
    GPIO.output(Moteur_1_arriere, GPIO.LOW)
    GPIO.output(Moteur_2_avant, GPIO.LOW)
    GPIO.output(Moteur_2_arriere, GPIO.LOW)

def malus():
    stop()
    time.sleep(1)

   
while 1:
   response = 1
   while response != 0:
       response = os.system("ping -c 1 192.168.1.1")
       time.sleep(1)
   print "Serveur pret, en attente de requetes ..."
   mySocket.listen(5)
   connexion, adresse = mySocket.accept()
   print "Client connecte, adresse IP %s, port %s" % (adresse[0], adresse[1])
   connexion.send("Vous etes connecte au serveur Envoyez vos messages.")
   msgClient = connexion.recv(2048)
   while 1:
       print msgClient
       if msgClient == "UP":
           avant()
       elif msgClient == "DOWN":
           arriere()
       elif msgClient == "LEFT":
           gauche()
       elif msgClient == "RIGHT":
           droite()
       elif msgClient == "UPEND":
           avantEND()
       elif msgClient == "DOWNEND":
           arriereEND()
       elif msgClient == "LEFTEND":
           gaucheEND()
       elif msgClient == "RIGHTEND":
           droiteEND()
       elif msgClient.upper() == "FIN" or msgClient =="":
           stop()
       else:
	   code, message = process_packet(msgClient)
	   if code == 4:
	       print "malus recu"
	       malus()
       msgClient = connexion.recv(1024)

   connexion.send("Au revoir !")
   print "Connexion interrompue."
   connexion.close()

   ch = raw_input("<R>ecommencer <T>erminer ? ")
   if ch.upper() =='T':
       break





