# Créé par Ocean6, le 20/04/2023 en Python 3.11

# importation des modules innés
import copy
import random
import sys
import time


def new_world(nb_lignes, nb_colonnes):
    """Retourne une matrice de taille donnée

    Parameters:
        nb_lignes (int): le nombre de lignes que la matrice contiendra
        nb_colonnes (int): le nombre de colonnes que la matrice contiendra

    Returns:
        list: matrice générée

    """
    # création de la matrice par compréhention
    world = [[False for i in range (nb_colonnes)] for j in range (nb_lignes)]
    return world


def init_world(world):
    """Retourne une matrice remplie aléatoirement

    Parameters:
        world (list): la matrice à remplir

    Returns:
        list: matrice remplie

   """
    for i in range(len(world)):
        world[i][len(world)//2] = True
        # for j in range(len(world[0])):
            # world[i][j]=bool(random.randint(0,1))
    return world


def afficher_world(world):
    """Affiche dans la console les donées brutes de la matrice

    Parameters:
        world (list): la matrice à afficher

    Returns:
        None: None

    """
    for ligne in world:
        for case in ligne:
            print(case, end=" ")
        print("")
    return None


def compte_voisins(world, x, y):
    """Retourne le nombre de cellules vivantes autour d'une cellule choisie

    Parameters:
        world (list): la matrice contenant les cellules
        x (int): coordonée x de la cellule choisie
        y (int): coordonée y de la cellule choisie

    Returns:
        int: nombre de voisins trouvés autour de la cellule choisie

   """
    nb_voisins = 0
    for i in range (y-1, y+2):
        # évite d'obtenir l'indice -1 qui signifierait "la derniere ligne"
        if i < 0:
            continue

        for j in range (x-1, x+2):
            # évite d'obtenir l'indice -1 qui signifierait "la derniere colonne"
            if j < 0:
                continue
            # évite de compter la cellule choisie comme voisine d'elle même
            if j == x and i == y:
                    continue
            try:
                if world[j][i] == True:
                    nb_voisins += 1
            # évite de faire planter le programme lorsque la cellule choisie est
            # au bord du tableau, dans ce cas les cellules hors champ sont
            # considérées comme mortes
            except IndexError:
                continue
    return nb_voisins


def next_generation (world):
    """Retourne la génération suivante selon le jeu de la vie de John Conway

    https://en.wikipedia.org/wiki/Conway%27s_Game_of_Life

    Parameters:
        world (list): la matrice contenant les cellules

    Returns:
        list: matrice contenant les cellules de la génération suivante

   """
   # permet de réaliser une véritable copie complète de la matrice afin de ne
   # pas écraser la matrice de la génération précédente
    next_world = copy.deepcopy(world)

    for i in range (len(world)):
        for j in range (len(world[0])):
            nb_voisins = compte_voisins(world, i, j)
            # application des trois règles du jeu de la vie
            if nb_voisins <= 1:
                next_world[i][j] = False
            if nb_voisins >= 4:
                next_world[i][j] = False
            if nb_voisins == 3:
                next_world[i][j] = True
    return next_world


def bel_affichage (world):
    """Affiche dans la console les donées de la matrice avec une mise en forme

    Parameters:
        world (list): la matrice à afficher

    Returns:
        None: None

   """
    print("|" + "-"*(len(world[0])*4-1) + "|")
    for i in range (len(world)*2):
        if i%2 == 1:
            ligne = "-"*(len(world[0]*4)-1)
        else:
            ligne = ""
            for j in range (len(world[0])):
                if world[i//2][j] == True:
                    chaine = "| * " if j != 0 else " * "
                else:
                    chaine = "|   " if j != 0 else "   "
                ligne += chaine
        print("|" + ligne + "|")
    return None


def start(largeur=None):
    """Permet d'initialiser une matrice du jeu de la vie

    Parameters:
        largeur (int): la largeur de la matrice à créer

    Returns:
        list: matrice créée

   """
    if largeur == None:
        largeur = try_input("Saisissez la largeur de la grille:")

        # gestion des entrées de l'utilisateur
        while True:
            if largeur == "":
                largeur = try_input("La valeur que vous venez d'entrer est vide, veuillez saisir\nun nombre entier positif compris entre 1 et 100 : ")
                continue
            try:
                largeur = int(largeur)
            except ValueError:
                largeur = try_input("La valeur que vous venez d'entrer (\"" + largeur + "\")\nn'est pas un nombre. Veuillez rééssayer : ")
                continue
            if largeur <= 0:
                largeur = try_input("Le nombre que vous avez entré n'est pas strictement positif,\nveuillez entrer un nombre entre 1 et 100 : ")
                continue
            #if largeur > 100:
            #    largeur = try_input("Le nombre que vous avez entré est trop grand pour que l'affichage puisse se faire correctement.\nVeuillez entrer un nombre entre 1 et 100 :")
            #    continue
            break

    world = new_world(largeur, largeur)
    return world


def try_input(message):
    """Permet à l'utilisateur d'entrer une valeur au clavier proprement

    Parameters:
        message (str): message qui va être afficher dans la boite de dialogue

    Returns:
        str: valeur entrée par l'utilisateur

   """
    try:
        inputTest = input(message)
    # permet d'éviter de faire planter le programme si la boite de dialogue est fermée
    except KeyboardInterrupt:
        print("Programme arrêté après la fermeture d'une boîte de saisie.")
        sys.exit()
    return inputTest


def main():
    world = start()
    bel_affichage(world)
    nb_generation = try_input("Saisissez le nombre de génération que vous souhaitez générer :")

    # gestion des entrées de l'utilisateur
    while True:
            if nb_generation == "":
                largeur = try_input("La valeur que vous venez d'entrer est vide, veuillez saisir\nun nombre entier positif supérieur à 1 : ")
                continue
            try:
                nb_generation = int(nb_generation)
            except ValueError:
                nb_generation = try_input("La valeur que vous venez d'entrer (\"" + nb_generation + "\")\nn'est pas un nombre. Veuillez rééssayer : ")
                continue
            if nb_generation <= 0:
                nb_generation = try_input("Le nombre que vous avez entré n'est pas strictement positif,\nveuillez entrer un nombre supérieur à 1 : ")
                continue
            break

    for i in range(nb_generation):
        world = next_generation(world)
        print("")
        bel_affichage(world)
        time.sleep(0.5)
#main()