#1socket pour 'inscription et un pour envoie message
#separer inscription (client nous serveur le gestionnaire: gesti reond anotre dmd) et le jeu (client lui; il envoie des dmd a nous)
#inscrition (local host piur le moment, port du gestonnaire de partie)
# port inscrip = port d'ecoute 


# CONFIGURATION

import socket
import json
import time

host = "172.17.10.133"
port = 3000
inscription= {
  "request": "subscribe",
  "port": 8888,
  "name": "PLATO",
  "matricules": ["22156"]
}

# INSCRIPTION

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port))
s.sendall((json.dumps(inscription)+ "\n").encode())
message =s.recv(1024).decode()
print("Serveur: ", message)
s.close()

# PING

s2=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#s2.connect(("192.168.129.205", 3000 )) #en faisant connecte on se remet en mode client ou on dmd de se connecter, or on veut recevoir qlqch, on veut etre le serveur mnt donc utilise;
s2.bind(("0.0.0.0",8888)) #notre port ou on va recevoir les dmd mais npt quel ip de client
s2.listen(1)

#message reçu

time.sleep(1)

# PONG ; doit repondre a tous les pings, donc fait une boucle, pas besoin de break car doit repondre a tout a tt instant
#dans cette boucle faut mettre la request pley aussi
#le server enverra soit une requete ping ou une requete play, mais pas en meme temps donc pndt que ca n'envoie pas de ping, ca enverra un play et faut un code pour les deux dans la boucle prcq ca envoie npt de quand

while True:
    print("en attente")
    connexion, adresse = s2.accept()
    print("Connecté avec:", adresse)

    ping = connexion.recv(1024).decode()
    print(" message reçu:",ping)
    #ping_json=json.loads(ping)
    if len(ping)>0:
    #if ping_json.get("request")=="pong":
        try:
            message = json.loads(ping)
            if message.get("request")=="ping":
                reponse = {"response":"pong"}
                connexion.send((json.dumps(reponse)).encode())
                print("pong envoyé")


        except:
            print("erreur json")



connexion.close()
s2.close() 











