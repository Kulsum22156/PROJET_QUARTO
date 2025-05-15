

#-----CONFIGURATION-----

import socket
import json
import time
import random

host = "192.168.129.205" #adresse IP du serveur 
port = 3000 #port du serveur
inscription= {
  "request": "subscribe",
  "port": 7777,
  "name": "PLATO_12",
  "matricules": ["22156"]
} #messag d'inscription qu'on va envoier pour s'inscrire

#-----INSCRIPTION-----

s=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((host, port)) #en faisant connect on se remet en mode client où on dmd de se connecter
s.sendall((json.dumps(inscription)+ "\n").encode()) #envoie le message d'inscription
message =s.recv(1024).decode() #décode le message json reçu
print("Serveur: ", message) #affiche le message reçu
s.close() #ferme le socket

s2=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s2.bind(("0.0.0.0",7777)) #notre port où on va recevoir les demandes 
s2.listen(1)

time.sleep(1)



#-----LES FONCTIONS-----

# Crée une fonction qui genère un ensemble de toutes les pièces du jeu :
def pieces_quarto():

    liste_pieces = [] #création d'une liste vide dans laquelle on va venir ajouter toutes les pièces du jeu
    for taille in ["B","S"]:
        for couleur in ["D","L"]:
            for concavite in ["E","F"]:
                for forme in ["C","P"]:
                    liste_pieces.append(taille+couleur+ concavite +forme)

    return set(liste_pieces)


# Crée une fonction qui crée une liste des pieces deja utilisée ; parcours board pour les pièces à ajouter et ajoute la pièce à jouer (pièce donnée par l'adversaire) :
def pieces_utilisees():

    pieces_prises = [] #création d'une liste vide dans laquelle on va venir ajouter toutes les pièces déjà joué, et donc qu'on ne pourra pas jouer

    #1. parcourir board et ajouter les pièces qui n'y sont pas déjà
    for piece in state["board"]:
        if piece is not None: #vérifie si la case contient une pièce
            if piece not in pieces_prises : #vérifie si la case n'est pas déjà dans la liste des pièces prises, si non on ajoute dans la liste
                 pieces_prises.append(piece)

    #2. ajouter la pièce que l'adversaire m'a donné
    if state['piece'] is not None: #vérifie si on a bien une pièce à jouer 
        if state["piece"] not in pieces_prises: #vérifie si la pièce ne se situe pas déjà dans la liste, si non l'ajoute dans cette liste
            pieces_prises.append(state["piece"])

    return set(pieces_prises) #fais un set() pour être sûr qu'il n'y a pas de doublons



# Crée une fonction qui donne une pièce à l'adversaire qui n'est pas dans pieces_utilisees() pour éviter le badmove
def piece_adversaire():

    piece_possible = [] #création d'une liste vide dans laquelle on va venir ajouter les pièces qu'on peut donner à l'adversaire
    for i in pieces_quarto(): #pour l'ensemble des pièces du jeu, si ces pièce ne se situent pas dans pieces_utilisees(), et donc qu'elles peuvent être jouées, on les ajoute à notre liste piece_possible
        if i not in pieces_utilisees():
            piece_possible.append(i)
          
    pieces_safe=[] #crée une liste ou on va venir ajouter les pièces qui ne vont pas permettre à l'adversaire de gagner
    plateau=state["board"]
    for piece in piece_possible: 
        risque=False #configure risque comme si y a pas de risque au début
        for i in range(4): #4 car 4 caractères possible pour la pièce
            meme_caract=0
            for position in plateau:
                if position is not None and position[i]==piece[i]: #si la case n'est pas vide et si le caractère est le même pour les deux pièces
                    meme_caract+=1 #ajoute un point car même caractère
            if meme_caract >=3: #si on a 3 ou plus de caractèristiques similaire, on a un risque sur cette pièce de laisser l'adversaire gagner ; cette pièce ne sera pas donnée
                risque=True
        if not risque:
            pieces_safe.append(piece) #si y a aucun risque, on ajoute la pièce dans notre liste; elle pourra être donnée à l'adversaire
    if pieces_safe:
        return random.choice(pieces_safe) #si on a des pièces safe dans la liste, alors donne une pièce de cette liste
    else:
        return random.choice(piece_possible) #si on n'a pas de pièce dans le liste, alors donne une pièce au hasard parmis les pièces possibles
        


# Crée un fonction qui regarde les cases vides et qui me donne la position ou le numero de la case vide
def cases_vides():

    vide=[] #création d'une liste vide dans laquelle on va venir ajouter les cases vides
    for i, case in enumerate(state["board"]): #parcours board
        if case is None: #si la case est vide, l'ajoute à la liste
            vide.append(i)
    return vide


# Crée une fonction qui sélectionne aléatoirement une case 
def case_joue():
    if len(cases_vides()) > 0: #si y a au moins une case vide, alors choisis aléatoirement
        case_choisie=random.choice(cases_vides())
        return case_choisie
    else:
        pass


# Crée une fonction qui regarde les cases voisines pour jouer la meilleure case, en parcourant tout le plateau/board
def cases_voisines():

    plateau=state["board"] 
    meilleure_piece=-1 #ici on initialise une variable à -1 pour que lorsqu'on trouve une pièce qui a plus de points en communs qu'elle, sa valeur se met à jour 
    meilleure_case=[]
    for position in cases_vides():
        #transfome numéro de la case en coordonnées
        ligne = position//4 #prend le numéro de la case (= position) et divise par 4 (car plateau quarto 4x4) pour obtenir la ligne 
        colonne =position%4 #prend le numéro de la case (= position) et fais le modulo de 4, le reste nous donne la colonne de la case
        voisine =[] 

        for dx in [-1,0,1]: #parcours les voisines sur la même ligne
            for dy in [-1,0,1]: #parcours les voisines sur la même colonne
                if dx !=0 or dy != 0: #exclu la case sur laquelle on est
                    x = ligne +dx #pour avancer sur la ligne
                    y = colonne +dy #pour avancer sur la colonne
                    if 0 <= x < 4 and 0 <= y < 4: #limite du plateau
                        case = x * 4 + y #passe de coordonnées à numéro de case
                        piece = plateau[case] #ajout de la valeur de la case dans une variable pour regarder sa valeur (un par un) et puis si elle n'est pas none, l'ajoute dans la liste voisines
                        if piece is not None:
                            voisine.append(piece)

            points_communs=0                
            if len(voisine) >= 2:#pour comparer faut min 2 pièces, logique, on va comparer un par un les caractéristiques du str qui défini les pièces
                for i in range(4): #car 4caractères pour une pièce
                    piece_caractere = voisine[0][i] #prend la 1ère pièce comme réference
                    meme_caractere=True 
                    for pos in voisine[1:]: #compare avec les autres voisines
                        if pos[i] != piece_caractere:
                            meme_caractere=False #si différente, alors devient False 
                        elif meme_caractere:#si meme caractère, ajoute un point en commun à points_communs
                            points_communs += 1 
                
           
            if points_communs > meilleure_piece: #si la pièce a plus de points en communs que la valeur de meilleur_piece, elle se met à jour;
                meilleure_piece = points_communs #mis à jour du nombre de points en communs
                meilleure_case = [position] #mis à jour de la meilleure case à jouer
                
            elif points_communs==meilleure_piece:
                meilleure_case.append(position)
    if meilleure_case:
        return random.choice(meilleure_case)
    else:
        return case_joue()
                    
    assert False, "on devrait pas arriver ici" #ne devrait jamais exécuter cette ligne


# Crée une fonction qui va créer le dictionnaire json du move
def move_joue():

    move = {"pos": cases_voisines(), "piece": piece_adversaire()} #dictionnaire de réponse du move reprenant la case jouée ainsi que la pièce à donne à l'adversaire
    texto = ["move envoyé", "coup genéré", "à ton tour princesse", "let's go ma star", "à ton tour bichette","miaou ᓚᘏᗢ","<33",":-P",">:(","(*^3^)r"]
    texto_ale = random.choice(texto) #génère aléatoirement un message parmis les messages de la liste texto
    return {"response" : "move", "move":move, "message" : texto_ale} #dictionnaire de réponse à play reprenant la réponse "move", le move joué et le message



#-----BOUCLE-----

#Cette boucle n'a pas de break, on l'éxécute sans cesse puisqu'on reçoit soit une requête ping auquel on répond pong, soit un play auquel on repond grâce à la fonction move_jou() juste au dessus
while True:
    print("\033[35mEn attente d'une requête\033[0m") #ajout de couleur pour les prints pour une meilleure lisibilité dans le terminal
    connexion, adresse = s2.accept()
    print("\033[35mConnecté avec: \033[0m", adresse)
    ping = connexion.recv(1024).decode()
    print("\033[35mMessage reçu: \033[0m",ping) #j'ai mis ping car au moment du coadage de ce texte je travaillais sur l'inscription mais ping ici fait reference uniquement au a la dmd du server
    #ping_json=json.loads(ping)
    if len(ping)>0:
    #if ping_json.get("request")=="pong":
        try:
            message = json.loads(ping) #load la request du server
            if message.get("request")=="ping":
                reponse = {"response":"pong"}
                connexion.send((json.dumps(reponse)).encode())
                print("\033[33mPong envoyé\033[0m")

            elif message.get("request")=="play":
                state = message["state"]
                reponse=move_joue()
                connexion.send((json.dumps(reponse)).encode())
                print("\033[33mCoup joué: \033[0m", reponse)


        except json.JSONDecodeError: #spécifie l'erreur qu'on ne veut pas et si en a une autre, va l'afficher "précisément" dans le terminal
            print("\033[31mErreur json\033[0m")



#-----FERMETURE-----
connexion.close()
s2.close() 











