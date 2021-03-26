from CONFIGS import *
import turtle
from copy import deepcopy


def lire_matrice(fichier):
    """
    Lecture des données provenant d'un fichier de plan du chateau
    :param fichier texte comprenant des représentations des pièces du château
    :return: matrice, ou liste de listes représentant les lignes et les colonnes du plan
    """
    plan_chateau_lignes = open(fichier, "r").readlines()
    matrice_chateau = deepcopy(plan_chateau_lignes)
    for i in range(len(plan_chateau_lignes)):
        matrice_chateau[i] = [int(j) for j in plan_chateau_lignes[i].split()]
    return matrice_chateau


def calculer_pas(matrice):
    """
    calcule la dimension à donner aux cases pour que le plan tienne dans la zone de la fenêtre turtle que définie
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


def coordonnees(case, pas, matrice):
    """
    calcule les coordonnées en pixels turtle du coin inférieur gauche d’une case définie par ses coordonnées
    :param case: tuple(x, y) représentant le numéro de ligne x et le numéro de colonne y d'une case
    :param pas: dimension d'une case
    :return: tuple(a, b) de coordonnées turtle
    """
    nb_lignes = len(matrice) - 1
    abcisse = ZONE_PLAN_MINI[0] + case[1] * pas
    ordonnee = ZONE_PLAN_MINI[0] + (nb_lignes - case[0]) * pas
    coordonnees = (abcisse, ordonnee)
    return coordonnees


def tracer_carre(dimension):
    """
    trace un carré turtle à partir de son coin inférieur gauche
    :param dimension: côté du carré
    """
    for i in range(4):
        turtle.forward(dimension)
        turtle.left(90)


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


def afficher_plan(matrice):
    """
    Dessine avec Turtle le quadrillage du plan du château dans les couleurs correspondantes à ce que dit la matrice.
    :param matrice: liste de listes de lignes et de colonnes
    """
    turtle.tracer(10, 100)
    turtle.up()
    for i in range(len(matrice)):
        for j in range(len(matrice[i])):
            tracer_case(coordonnees((i, j), calculer_pas(matrice), matrice), COULEURS[matrice[i][j]], calculer_pas(matrice))
    turtle.hideturtle()
    turtle.done()


afficher_plan(lire_matrice("plan_chateau.txt"))
