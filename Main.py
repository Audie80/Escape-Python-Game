"""
Jeu de labyrinthe
Auteur: Aude Velly Menut
Date: 26 mars 2021
Jeu de labyrinthe généré par turtle à partir d'un fichier texte représentant une matrice de pièces.
"""

from CONFIGS import *
import turtle
from copy import deepcopy

global glob_matrice, glob_pas, glob_position


def lire_matrice(fichier):
    """
    Lecture des données provenant d'un fichier de plan du chateau
    :param fichier: texte comprenant des représentations des pièces du château
    :return: matrice, ou liste de listes représentant les lignes et les colonnes du plan
    """
    plan_chateau_lignes = open(fichier, "r").readlines()
    matrice_chateau = deepcopy(plan_chateau_lignes)
    for i in range(len(plan_chateau_lignes)):
        matrice_chateau[i] = [int(j) for j in plan_chateau_lignes[i].split()]
    return matrice_chateau


glob_matrice = lire_matrice("plan_chateau.txt")  # La matrice est utilisée en variable globale


def afficher_plan(matrice):
    """
    Dessine avec Turtle le quadrillage du plan du château
    dans les couleurs correspondantes à ce que dit la matrice.
    :param matrice: liste de listes de lignes et de colonnes
    """
    turtle.title("Quête dans le château au sommet du Python des Neiges")
    turtle.tracer(10, 100)
    turtle.up()
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            tracer_case(coordonnees((i, j), calculer_pas(matrice), matrice), COULEURS[matrice[i][j]], calculer_pas(matrice))
    turtle.hideturtle()


def calculer_pas(matrice):
    """
    calcule la dimension à donner aux cases pour que le plan tienne dans la zone de la fenêtre turtle définie
    :param matrice: liste de listes de lignes et de colonnes
    :return: dimension maximale d'une case carrée
    """
    hauteur = ZONE_PLAN_MAXI[1] - ZONE_PLAN_MINI[1]
    largeur = ZONE_PLAN_MAXI[0] - ZONE_PLAN_MINI[0]
    nb_lignes = len(matrice)
    nb_colonnes = len(matrice[0])
    hauteur_ligne = hauteur / nb_lignes
    largeur_colonne = largeur / nb_colonnes
    return int(min(hauteur_ligne, largeur_colonne))


glob_pas = calculer_pas(glob_matrice)  # Le pas est utilisé en variable globale


def tracer_case(case, couleur, pas):
    """
    trace un carré d’une certaine couleur et taille à un certain endroit
    :param case: couple de coordonnées en indice dans la matrice contenant le plan
    :param couleur: chiffre de la matrice
    :param pas: taille d'un côté
    """
    turtle.goto(case)
    turtle.down()
    turtle.color(couleur)
    turtle.begin_fill()
    tracer_carre(pas)
    turtle.end_fill()
    turtle.up()


def tracer_carre(dimension):
    """
    trace un carré turtle à partir de son coin inférieur gauche
    :param dimension: côté du carré
    """
    for i in range(4):
        turtle.forward(dimension)
        turtle.left(90)


def coordonnees(case, pas, matrice):
    """
    calcule les coordonnées en pixels turtle du coin inférieur gauche d’une case définie par ses coordonnées
    :param case: tuple(x, y) représentant le numéro de ligne x et le numéro de colonne y d'une case
    :param pas: dimension d'une case
    :param matrice: matrice représentant le château
    :return: tuple(a, b) de coordonnées turtle
    """
    nb_lignes = len(matrice) - 1
    abscisse = ZONE_PLAN_MINI[0] + case[1] * pas
    ordonnee = ZONE_PLAN_MINI[0] + (nb_lignes - case[0]) * pas
    tuple_coordonnees = (abscisse, ordonnee)
    return tuple_coordonnees


afficher_plan(glob_matrice)  # Génère l'affichage du plan


def position_joueur(case, couleur):
    """
    Fonction qui dessine la position du joueur
    :param case: tuple(x, y) représentant le numéro de ligne x et le numéro de colonne y d'une case
    :param couleur: couleur désirée pour le point du joueur
    """
    turtle.goto(coordonnees(case, glob_pas, glob_matrice)[0] + glob_pas / 2, coordonnees(case, glob_pas, glob_matrice)[1] + glob_pas / 2)
    turtle.dot(glob_pas / 2, couleur)


glob_position = (0, 1)  # Initialise la position du joueur sur la porte d'entrée
position_joueur(glob_position, "red")  # Dessine le joueur


def attendre_fin():
    """
    Fonction qui ferme la fenêtre turtle à la fin du jeu
    """
    turtle.bye()


def deplacer(matrice, position, mouvement):
    """
    Fonction principale de gestion des déplacements.
    Lorsque le personnage tentera un déplacement vers une case de mur ou vers l’extérieur du plan,
    rien ne se produira.
    Lorsqu’il tentera un déplacement vers une case vide,
    il avancera d’une case (en pratique, il s’agira de retracer la case de départ pour effacer le personnage,
    et de replacer ce dernier sur la case de destination).
    :param matrice: matrice représentant le château
    :param position: un couple définissant la position où se trouve le personnage
    :param mouvement: un couple définissant le mouvement demandé par le joueur
    """
    global glob_position
    position_demandee = (position[0] + mouvement[0], position[1] + mouvement[1])
    # Si le mouvement sort du labyrinthe ou mène vers un mur, la fonction ne fait rien
    if position_demandee[0] == -1 or matrice[position_demandee[0]][position_demandee[1]] == 1:
        return
    else:
        # Efface l'ancien turtle_dot
        position_joueur(position, COULEURS[matrice[position[0]][position[1]]])
        # Réaffecte la nouvelle position à la variable globale
        glob_position = position_demandee
        # Dessine le nouveau turtle_dot
        position_joueur(position_demandee, "red")
        # Si c'est la sortie, c'est gagné ! (le joueur ne peut plus se déplacer et la fenêtre se ferme)
        if matrice[position_demandee[0]][position_demandee[1]] == 2:
            turtle.onkeypress(None, "Left")
            turtle.onkeypress(None, "Right")
            turtle.onkeypress(None, "Up")
            turtle.onkeypress(None, "Down")
            print("Bravo !")
            turtle.ontimer(attendre_fin, 2000)


def deplacer_gauche():
    """
    Ajoute un événement sur la touche de clavier associée
    """
    turtle.onkeypress(None, "Left")   # Désactive la touche Left
    deplacer(glob_matrice, glob_position, (0, -1))
    turtle.onkeypress(deplacer_gauche, "Left")   # Réassocie la touche Left à la fonction deplacer_gauche


def deplacer_droite():
    """
    Ajoute un événement sur la touche de clavier associée
    """
    turtle.onkeypress(None, "Right")   # Désactive la touche Right
    deplacer(glob_matrice, glob_position, (0, 1))
    turtle.onkeypress(deplacer_droite, "Right")   # Réassocie la touche Right à la fonction deplacer_droite


def deplacer_haut():
    """
    Ajoute un événement sur la touche de clavier associée
    """
    turtle.onkeypress(None, "Up")   # Désactive la touche Up
    deplacer(glob_matrice, glob_position, (-1, 0))
    turtle.onkeypress(deplacer_haut, "Up")   # Réassocie la touche Up à la fonction deplacer_haut


def deplacer_bas():
    """
    Ajoute un événement sur la touche de clavier associée
    """
    turtle.onkeypress(None, "Down")   # Désactive la touche Down
    deplacer(glob_matrice, glob_position, (1, 0))
    turtle.onkeypress(deplacer_bas, "Down")   # Réassocie la touche Down à la fonction deplacer_bas


turtle.listen()  # Déclenche l’écoute du clavier
turtle.onkeypress(deplacer_gauche, "Left")  # Associe à la touche Left une fonction appelée deplacer_gauche
turtle.onkeypress(deplacer_droite, "Right")  # Associe à la touche Left une fonction appelée deplacer_droite
turtle.onkeypress(deplacer_haut, "Up")  # Associe à la touche Left une fonction appelée deplacer_haut
turtle.onkeypress(deplacer_bas, "Down")  # Associe à la touche Left une fonction appelée deplacer_bas
turtle.mainloop()  # Place le programme en position d’attente d’une action du joueur
