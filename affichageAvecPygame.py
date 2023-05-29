#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      Ocean6
#
# Created:     11/05/2023
# Copyright:   (c) Ocean6 2023
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# importation des modules innés
import pygame
import time
import copy
import os

# importation du moteur du jeu de la vie que nous avons créé
# utilisation d'un alias pour simplifier le code
import projetJeuDeLaVie as jdlv

import canon_planeur as cp


def countdown(num_of_secs):
    while num_of_secs:
        m, s = num_of_secs//60, num_of_secs%60
        min_sec_format = '{:02d}:{:02d}'.format(m, s)


def compte_nb_cellules(world):
    """Retourne le nombre de cellules total dans la grille

    Parameters:
        world (list): matrice du jeu de la vie

    Returns:
        int: nombre de cellules dans la grille
    """
    compteur = 0
    for ligne in world:
        for case in ligne:
            if case:
                compteur += 1
    return compteur


def dessiner_grille(nb_colonnes, marge):
    """Affiche le cadrillage du jeu sur l'écran

    Parameters:
        nb_colonnes (int): le nombre de colonnes de la matrice
        marge (int): le nombre de pixel depuis le haut de la fenêtre où commencera le dessin

    Returns:
        None: None

    """
    # utilisation de variables globales car elles contiennent des données uniques "invariables"
    global screen
    global intervalle
    global depart_gauche

    # trouve la taille maximal du cadrillage qui rentre dans la fenêtre
    intervalle_hauteur = (screen.get_height()-marge) // nb_colonnes
    intervalle_largeur = (screen.get_width()-marge) // nb_colonnes
    intervalle = intervalle_hauteur if intervalle_hauteur < intervalle_largeur else intervalle_largeur
    # définie la coordonnée horizontale du bord gauche du cadrillage
    depart_gauche = screen.get_width()/2 - intervalle*nb_colonnes/2

    for ligne in range(nb_colonnes):
        # dessine une ligne verticale et horizontale par colonne de la matrice
        draw_line((intervalle*ligne + depart_gauche, marge/2), (intervalle*ligne + depart_gauche, nb_colonnes*intervalle + (marge/2)))
        draw_line((depart_gauche, intervalle*ligne + (marge/2)), (intervalle*nb_colonnes + depart_gauche, ligne*intervalle + (marge/2)))
    # dessine les dernières lignes verticale et horizontale du cadrillage
    draw_line((intervalle*(ligne+1) + depart_gauche, marge/2), (intervalle*(ligne+1) + depart_gauche, nb_colonnes*intervalle + (marge/2)))
    draw_line((depart_gauche, intervalle*(ligne+1) + (marge/2)), (intervalle*nb_colonnes + depart_gauche, (ligne+1)*intervalle + (marge/2)))


def draw_line(pos1, pos2):
    """Dessine une ligne sur l'écran

    Parameters:
        pos1 (tuple): couple des coordonnées de départ de la ligne
        pos2 (tuple): couple des coordonnnées de fin de la ligne

    Returns:
        None: None

    """
    # utilisation d'une variable globale pour conserver un seul écran actif
    global screen
    pygame.draw.line(screen, 'black', pos1, pos2)


def dessiner_cellules(world, marge):
    """Dessine une ligne sur l'écran

    Parameters:
        pos1 (tuple): couple des coordonnées de départ de la ligne
        pos2 (tuple): couple des coordonnnées de fin de la ligne

    Returns:
        None: None

    """
    global intervalle
    global screen
    global depart_gauche

    # parcours toutes les cellules de la matrice
    for i in range(len(world)):
        for j in range(len(world[0])):
            if world[i][j]:
                # si la case contient une cellule vivante, la dessiner en noir
                couleur = "black"
            else:
                # sinon la dessiner en blanc
                couleur = "white"
            pygame.draw.rect(screen, couleur, ((j*intervalle)+depart_gauche+1, (i*intervalle)+marge/2+1, intervalle-1, intervalle-1))


def next_generation(world, generation_affichee, former_generations, actual_gen, derniere_gen,v2,nb_cellules_init, precedente=False):
    """Retourne la prochaine génération demandée par l'utilisateur

    Parameters:
        world (list): matrice du jeu de la vie
        generation_affichee (int): numéro de la génération affichée actuellement sur l'écran
        former_generations (list): matrice contenant les dix dernières générations générées
        actual_gen (int): indice de la liste former_generations qui contient la matrice affichée actuellement à l'écran
        derniere_gen (int): indice de la liste former_generations qui contient la derniere génération générée
        precedente (bool): indique si l'utilisateur souhaite obtenir la précédente génération

    Returns:
        world (list): matrice du jeu de la vie
        generation_affichee (int): numéro de la génération affichée actuellement sur l'écran
        former_generations (list): matrice contenant les dix dernières générations générées
        actual_gen (int): indice de la liste former_generations qui contient la matrice affichée actuellement à l'écran
        derniere_gen (int): indice de la liste former_generations qui contient la derniere génération générée
    """
    font = pygame.font.SysFont(None, 30)
    if precedente is False:
        generation_affichee += 1

        if actual_gen == derniere_gen:
            # récupère la prochaine génération grâce au module jdlv
            world = jdlv.next_generation(world)

            # cas dans lequel la civilisation s'est stabilisé
            if world in former_generations:
                #instructions d'arrêt du programme
                # créé une nouvelle matrice et réinitialise toutes les variables
                world = jdlv.start(len(world))
                if v2 is False:
                    world = jdlv.init_world(world)
                    nb_cellules_init=compte_nb_cellules(world)
                else:
                    world=jdlv.new_world(len(world), len(world))
                former_generations = [[[False for i in range (len(world))] for j in range (len(world))] for i in range(10)]
                actual_gen = 0
                derniere_gen = 0
                # copie profonde de la génération actuelle vers la mémoire
                former_generations[actual_gen] = copy.deepcopy(world)
                generation_affichee = 1
            else:
                # incrémentation des variables d'indice
                actual_gen = 0 if actual_gen == 9 else actual_gen+1
                derniere_gen = 0 if derniere_gen == 9 else derniere_gen+1
                # copie profonde de la génération actuelle vers la mémoire
                former_generations[actual_gen] = copy.deepcopy(world)

        # cas où l'utilisateur serait revenu en arrière dans les générations
        else:
            actual_gen = 0 if actual_gen == 9 else actual_gen+1
            world = former_generations[actual_gen]

    elif precedente:
        # tous les cas sauf lorsque la limite de la mémoire est atteinte
        if actual_gen != derniere_gen+1 and derniere_gen != 9:
            # décrémentation des variables
            actual_gen = 9 if actual_gen==0 else actual_gen-1
            generation_affichee -= 1
            # actualisation de la génration actuelle
            world = former_generations[actual_gen]
        # lorsque la limite de la mémoire est atteinte, ne rien faire
    return world, generation_affichee, former_generations, actual_gen, derniere_gen

def setup():
    """Démarre pygame et créé l'écran

    Parameters:
        None: None

    Returns:
        None: None

    """
    global screen
    global clock
    pygame.init()
    # positionne la fenêtre en haut à gauche de l'écran
    os.environ['SDL_VIDEO_WINDOW_POS'] = "0,31"
    # créé une fenêtre de la taille de l'écran
    screen = pygame.display.set_mode((pygame.display.get_desktop_sizes()[0][0], pygame.display.get_desktop_sizes()[0][1]-79), pygame.RESIZABLE)
    pygame.display.set_caption("Programme du Jeu de la Vie")
    clock = pygame.time.Clock()


def run(nb_tick, marge, v2=False):
    """Affiche chaque génération du jeu de la vie

    Parameters:
        nb_tick (int): nombre de tick entre chaque image affichée
        marge (int): nombre de pixel de marge en haut de l'écran avant que la grille soit dessinée

    Returns:
        None: None

    """
    # cette fonction peut être considérée comme la fonction principale
    global screen
    global clock
    global depart_gauche
    global intervalle

    setup()
    # créé et initialise un nouvelle matrice
    world = jdlv.start()
    world = jdlv.init_world(world)
    nb_cellules_init=compte_nb_cellules(world)
    # nous commençons à la génration 1
    generation_affichee = 1
    # définit l'avancée des génrations sur pause
    play = False
    # initialise l'affichage du texte
    font = pygame.font.SysFont(None, 30)
    # cette liste est une mémoire qui contiendra les dix dernières générations
    # cela permet de savoir si la civilisation s'est stabilisée
    former_generations = [[[False for i in range (len(world))] for j in range (len(world))] for i in range(10)]
    actual_gen = 0
    derniere_gen = 0
    former_generations[actual_gen] = copy.deepcopy(world)
    # compteur qui permet d'afficher les générations à un rythme agréable
    compteur_frames = 0

    # créé les éléments visuels tels que les boutons etc...
    fond = pygame.image.load("background.jpg").convert()
    play_button = pygame.image.load("playButton.png").convert_alpha()
    pause_button = pygame.image.load("pauseButton.png").convert_alpha()
    next_button = pygame.image.load("nextButton.png").convert_alpha()
    prev_button = pygame.image.load("prevButton.png").convert_alpha()
    v2_button = pygame.image.load("button_v2.png").convert_alpha()
    cannon_button = pygame.image.load("canon_button.png").convert_alpha()
    rectangle_bouton_play = play_button.get_rect(topleft=(70, 50))
    rectangle_bouton_pause = pause_button.get_rect(topleft=(160, 50))
    rectangle_bouton_suivant = next_button.get_rect(topleft=(70, 500))
    rectangle_bouton_precedent = prev_button.get_rect(topleft=(160, 500))
    rectangle_button_v2= v2_button.get_rect(topleft=(70,150))
    canon_vie_button=cannon_button.get_rect(topleft=(160,150))
    gen_affichage=font.render(f"Génération actuelle : {str(generation_affichee)}",True,(0,0,0))


    main_while = True
    while main_while:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # permet de quitter la fenêtre si la croix est cliquée
                main_while = False

            if pygame.mouse.get_focused():
                # récupère les coordonnées de la souris
                x, y = pygame.mouse.get_pos()

                # détecte les clics sur les boutons / cellules
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if rectangle_bouton_play.collidepoint(x, y):
                        # si le bouton play est cliqué, l'avancée des générations démarre
                        play = True
                    if rectangle_bouton_pause.collidepoint(x, y):
                        # si le bouton pause est cliqué, l'avancée des générations s'arrête
                        play = False
                    if rectangle_bouton_suivant.collidepoint(x, y):
                        # déclenche la prochaine génération
                        world, generation_affichee, former_generations, actual_gen, derniere_gen = \
                        next_generation(world, generation_affichee, former_generations, actual_gen, derniere_gen,v2, nb_cellules_init)
                    if rectangle_bouton_precedent.collidepoint(x, y):
                        # déclenche la précédente génération
                        world, generation_affichee, former_generations, actual_gen, derniere_gen = \
                        next_generation(world, generation_affichee, former_generations, actual_gen, derniere_gen,v2,nb_cellules_init, precedente=True)
                    if canon_vie_button.collidepoint(x,y):
                        if len(world)>=36:
                            world=jdlv.new_world(len(world),len(world))
                            world=cp.canon_planeur(world)
                        pygame.display.update()
                    if play is False:
                        if rectangle_button_v2.collidepoint(x,y):
                            v2=not v2
                            generation_affichee=1
                            if v2:
                                #on recrée une matrice cette fois vide
                                world=jdlv.new_world(len(world), len(world))
                            else:
                                world=jdlv.start(len(world))
                                world=jdlv.init_world(world)
                                nb_cellules_init=compte_nb_cellules(world)
            if pygame.mouse.get_pressed()[0]:
                x,y=pygame.mouse.get_pos()
                if play is False:
                    # récupère les indices correspondants à la cellule cliquée
                    coord_x = int((x - depart_gauche) / intervalle)
                    coord_y = int((y - marge) / intervalle)
                    # gère les clics dans le cdrillage
                    if coord_x >= 0 and coord_y >= 0:
                        try:
                            world[coord_y][coord_x] = True
                        except IndexError:
                            None


        # rafraichit l'écran
        pygame.display.flip()

        #actualise le compteur de génération
        gen_affichage=font.render(f"Génération actuelle : {str(generation_affichee)}",True,(0,0,0))
        # place les éléments visuels sur l'écran
        screen.blit(fond, (0,0))
        screen.blit(play_button, (70, 50))
        screen.blit(pause_button, (160, 50))
        screen.blit(next_button, (70, 500))
        screen.blit(prev_button, (160, 500))
        screen.blit(gen_affichage, (915, 50))
        screen.blit(v2_button,(70,150))
        screen.blit(cannon_button, (160,150))

        dessiner_grille(len(world), marge*2)
        dessiner_cellules(world, marge*2)

        if play:
            # permet d'afficher au rythme de deux images par seconde
            if compteur_frames > nb_tick:
                # déclenche la prochaine génération
                world, generation_affichee, former_generations, actual_gen, derniere_gen = \
                next_generation(world, generation_affichee, former_generations, actual_gen, derniere_gen,v2, nb_cellules_init)
                compteur_frames = 0

        compteur_frames +=1
        clock.tick(120)

    pygame.quit()

marge = 20
nb_frame_sec = 10
nb_ticks_entre_chaque_image = 120/nb_frame_sec
run(nb_ticks_entre_chaque_image, marge)