#1socket pour 'inscription et un pour envoie message
#separer inscription (client nous serveur le gestionnaire: gesti reond anotre dmd) et le jeu (client lui; il envoie des dmd a nous)
#inscrition (local host piur le moment, port du gestonnaire de partie)
# port inscrip = port d'ecoute 


# CONFIGURATION

import socket
import json
import time
import random

host = "192.168.129.205"
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

# Crée une fonction qui genère un ensemble de toutes les pièces du jeu
def pieces_quarto():

    liste_pieces = []
    for taille in ["B","S"]:
        for couleur in ["D","L"]:
            for concavite in ["E","F"]:
                for forme in ["C","P"]:
                    liste_pieces.append(taille+couleur+ concavite +forme)

    return set(liste_pieces)

# Crée une fonction qui crée une liste des pieces deja utilisée ; parcours board pour les pieces a ajt enplus et ajt la piece a jouer 
def pieces_utilisees():
    pieces_prises = []

    #1. parcourir board et ajt les pieces qui n'y sont pas deja
    for piece in state["board"]:
        if piece is not None:
            if piece not in pieces_prises :
                 pieces_prises.append(piece)

    #2. ajt la piece que l'adv m'a donné
    if state['piece'] is not None:
        if state["piece"] not in pieces_prises:
            pieces_prises.append(state["piece"])

    return set(pieces_prises)

# Crée une focntion qui joue donne une peice a l'adv qui n'est pas dans pieces_utilisees() pour eviter le badmove
def piece_adversaire():
    piece_possible = []
    for i in pieces_quarto():
        if i not in pieces_utilisees():
            piece_possible.append(i)
          
    return random.choice(piece_possible) #utilise random pour choisir une piece aléatoirement pour l'adversaire parmis les pieces possible


# Crée un fonction qui rgd les cases vides et qui me donne la position(dmd prof) ou le numero de la case vide
def cases_vides():
    vide=[]
    for i, case in enumerate(state["board"]):
        if case is None:
            vide.append(i)
    return vide
        

# Crée une fonction qui rgd les cases voisines pour jouer la meilleure piece et qui rgd l'ensbmle du plato pour jouer sa piece
def cases_voisines():
    pass

# Crée une fonction qui va créer le dictionnaire json du move
def move_joue():
    move = {"case": cases_vides() , "piece": piece_adversaire()}
    texto = ["move envoyé", "move genéré", "coup envoyé", "coup genéré", "à ton tour", "let's go ma star"]
    texto_ale = random.choice(texto)
    return {"response" : "move", "move":move, "message" : texto_ale}


while True:
    print("en attente")
    connexion, adresse = s2.accept()
    print("Connecté avec:", adresse)
    ping = connexion.recv(1024).decode()
    print(" message reçu:",ping) #j'ai mis ping car au moment du coadage de ce texte je travaillais sur l'inscription mais ping ici fait reference uniquement au a la dmd du server
    #ping_json=json.loads(ping)
    if len(ping)>0:
    #if ping_json.get("request")=="pong":
        try:
            message = json.loads(ping) #load la request du server
            if message.get("request")=="ping":
                reponse = {"response":"pong"}
                connexion.send((json.dumps(reponse)).encode())
                print("pong envoyé")

            elif message.get("request")=="play":
                state = message["state"]
                reponse=move_joue()
                connexion.send((json.dumps(reponse)).encode())
                print("coup joué: ", reponse)


        except:
            print("erreur json")



connexion.close()
s2.close() 











