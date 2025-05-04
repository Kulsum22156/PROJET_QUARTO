# PROJET_QUARTO

projet réalisé par 22156

bibliothèques utilisées : random, json, socket, time

Ce ReadMe a pour but de montrer la stratégie de jeu de mon IA pour le jeu QUARTO.

Voici qlq points auxquels j'ai pensé pour mener à bien la partie:
1. s'inscrire ( oke )
2. répondre au "play" en :
    2.1 analysant le json envoyé, notamment la clé "state_of_the_game" 
Cette analyse permettra de voir le plateau, les cases disponible ou non, la pièce à jouer pour éviter les badmoves et jouer
    2.2 envoyé sous forme d'un json son move, càd la case ou l'on veut mettre la pièce sélectionner par l'adversaire, ainsi que notre pièce  pour l'adversaire

pour ce faire, je vais créer des fonctions pour la lecture du json envoyé, la création d'une liste de toutes les pieces, la création des cases(dmd au prof), une gestion de badmoves (cases prises, pieces deja joué), ect.

ce fichier sera bien sur mis a jour dans les jours a venir pour avoir un resultats final a la fin du codage.