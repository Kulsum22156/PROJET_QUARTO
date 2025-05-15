
# PROJET_QUARTO

Projet réalisé par: UMME Kulsum 22156

Ce projet a pour but de créer une IA avec un serveur TCP et codé en python capable de jouer au jeu QUARTO. Ce ReadMe sert à montrer la stratégie de jeu de l'IA ainsi que les bibliothèques utilisées. Nous allons aborder l'inscription, la réponse aux requêtes (notamment grâce à des fonctions) ainsi que les éventuelles améliorations à apporter à cette IA.

***

## Bibliothèques utilisées :

1. socket : utilisé pour la communication entre serveur et client
2. json : utilisé pour la transmission et lecture de message entre client et serveur
3. random : utilisé dans des fonctions pour envoyer des pièces ou sélectionner des cases au hasard
4. time : utilisé pour faire une pause d'une seconde

***

## Inscription :

On crée un socket client pour se connecter au serveur, auquel on envoie un message d'inscription contenant nos informations telles que notre nom et matricule. Une fois l'inscription faite, on ferme ce socket pour en ouvrir un autre pour pouvoir recevoir des requêtes "ping" ou "play" (se met en mode écoute).

## Stratégie de jeu :

L'IA utilise une stratégie simple : elle évite les BadMoves et analyse le plateau à chaque tour pour trouver des points communs entre des pièces pour jouer la meilleure case. 
Elle propose ensuite une pièce à son adversaire en analysant de nouveau l'état du plateau et choisissant une pièce qui l'empêcherait de gagner la manche.
Voyons de plus près comment elle fonctionne :

### Fonctions utilisées :

NB: voir code pour plus de détails sur comment les fonctions sont crées

La stratégie est répartie en 7 fonctions :

1. pieces_quarto() : cette fonction génère les différentes pièces du jeu (16 au total).

2. pieces_utilisees() : crée une liste de toutes les pièces déjà utilisées ( c'est-à-dire déjà sur le plateau) en incluant le pièce que l'adversaire a donné à jouer.

3. piece_adversaire() : cette fonction permet de choisir une pièce pour l'adversaire en tenant compte de l'état du plateau ainsi que des pièces déjà joué (évite un BadMove). En analysant les caractèristiques des pièces de la liste des pièces jouable avec les pièces qui se trouvent sur le plateau, elle ne propose que des pièces avec le moins de chance de gagner, qui ont le moins de caractèristiques communes avec celles du plateau. La sélection de la pièce est faite en utilisant random. 

4. cases_vides() : crée une liste des positions (0 à 15) des cases libres, des cases où on peut placer une pièce.

5. case_joue() : choisit une case vide au hasard, grâce à random.

6. cases_voisines() : cette fonction analyse les cases voisines pour chercher le meilleur endroit où placer la pièce à jouer. Elle analyse les pièces voisines de là où on se trouve et regarde si les caractéristiques des pièces match avec la pièce à jouer. A la fin, elle choisit la case, une des case (choisit par random) dont les voisines regroupent le plus de caractéristiques communes avec la pièce à jouer. 

7. move_joue() : cette fonction construit le dictionnaire de réponse à la requête "play". Elle génère la réponse "move", le move joué, c'est-à-dire la case où on positionne la pièce et la pièce qu'on donne à l'adversaire, ainsi qu'un message sélectionné aléatoirement (grâce à random de nouveau).


### Boucle principale :

Cette boucle tourne en permanence pour répondre aux requêtes du serveur à n'importe quel moment.
Pour se faire, on décode le message, la requête reçu (de la part du serveur) :
- si nous envoie un "ping", on répond par un "pong",
- si nous envoie un "play", répond par move_joue()
Ces réponses sont reçu et envoyé sous forme de JSON.
Des print colorés ont été ajouté pour rendre le terminal plus agréable et lisible.

***
## Améliorations :

Il y a pas mal de points sur lesquels bosser pour élever le niveau de l'IA. Parmi elles, on cite :
1. Création une fonction victoire() qui servirait à détecter si une ligne, colonne ou diagonale est gagnante, c'est-à-dire qu'il ne manque plus que une pièce pour remporter la manche,
2. Généré des messages en tenant compte de ce qui se passe lors de la partie,
3. Utiliser une heuristique plutôt pour regarder les points en communs entre les pièces (dans la fonctions cases_voisines()).