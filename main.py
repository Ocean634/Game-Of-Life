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
import sys
import time
import copy

# importation du moteur du jeu de la vie que nous avons créé
# utilisation d'un alias pour simplifier le code
import projetJeuDeLaVie as jdlv

# importation de la bibliothèque de situations initales
import modelsLibrary as models

mainClock = pygame.time.Clock()

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    """permet de redimmensionner un texte de sorte à ce qu'il ne dépasse pas de la fenêtre pygame

    Parameters:
        surface (pygame.surface.Surface) : écran
        text (str) : message à redimensionner
        pos (tuple) : position de départ du texte en haut à gauche
        font (pygame.font.Font) : police du texte

    Returns:
        None: None

    """
    words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
    space = font.size(' ')[0]  # The width of a space.
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = font.render(word, 0, color)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]  # Reset the x.
                y += word_height  # Start on new row.
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]  # Reset the x.
        y += word_height  # Start on new row.


def welcome():
    """permet d'afficher une page d'acceuil avec uune descriptioon du jeu de la vie et un bouton pour accéder à la simulation

    Parameters:
        None:None

    Returns:
        None: None

    """
    font = pygame.font.SysFont(None, 60)
    font1 = pygame.font.SysFont(None, 30)
    running = True
    fond = pygame.image.load("background.jpg").convert()
    play_button=pygame.image.load("pygame_run.png").convert_alpha()
    welcome_title=font.render("Le Jeu de la vie", True, (0,0,0))
    play_game_txt=font1.render("Voir la simulation :",True,(0,0,0))
    welcome_txt_p1="Bienvenue dans la fascinante simulation du Jeu de la Vie ! Dans cet univers virtuel, vous avez le pouvoir de créer et de contrôler la vie elle-même. Vous êtes sur le point d'embarquer dans un voyage captivant où vous serez témoin de l'évolution, de la complexité et de la beauté de la vie, tout en explorant les principes fondamentaux qui la gouvernent."
    welcome_txt_p2="Dans cette simulation, vous vous trouverez face à une grille constituée de cellules. Chaque cellule peut être dans l'un des deux états possibles : vivante ou morte. En interagissant avec ces cellules, vous découvrirez comment elles évoluent au fil du temps en fonction de règles simples mais fascinantes."
    welcome_txt_p3="Votre rôle en tant qu'observateur et joueur est crucial. Vous pouvez créer de nouvelles cellules, les faire interagir et les voir se multiplier, se déplacer et même s'éteindre. La façon dont vous manipulez ces cellules et les règles que vous établissez auront un impact direct sur l'évolution de cet écosystème numérique."
    welcome_txt_p4= "Mais ne vous méprenez pas, cette simulation est plus qu'un simple jeu. Elle porte en elle des principes complexes de dynamique, d'émergence et de systèmes complexes. Vous pourrez observer l'apparition de schémas étonnants, de structures stables et même de formes de vie émergentes à partir de règles de base."
    welcome_txt_p5="Préparez-vous à être émerveillé par la puissance de cette simulation et à vous émerger dans un monde où la vie prend vie grâce à votre imagination et à vos décisions. Prêt à plonger dans l'univers du Jeu de la Vie ? Alors, préparez-vous à explorer, à expérimenter et à apprendre en jouant avec les fondements mêmes de la vie !"
    play_button_vie=play_button.get_rect(topleft=(260,35))
    screen.blit(fond, (0,0))
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if pygame.mouse.get_pressed()[0]:
                x,y=pygame.mouse.get_pos()
                if play_button_vie.collidepoint(x,y):
                    run(120/nb_frame_sec, marge, world)
        screen.blit(welcome_title, (450,20))
        screen.blit(play_game_txt, (70,50))
        screen.blit(play_button, (260,35))
        blit_text(screen, welcome_txt_p1, (70,100), font1)
        blit_text(screen, welcome_txt_p2, (70,200), font1)
        blit_text(screen, welcome_txt_p3, (70,300), font1)
        blit_text(screen, welcome_txt_p4, (70,400), font1)
        blit_text(screen, welcome_txt_p5, (70,500), font1)

        pygame.display.update()
        mainClock.tick(60)


def options():
    """permet d'afficher une page de menu et les fonctionnalités

    Parameters:
        None:None

    Returns:
        None: None

    """
    global world
    font = pygame.font.SysFont(None, 60)
    font1 = pygame.font.SysFont(None, 30)
    running = True
    fond = pygame.image.load("background.jpg").convert()
    cannon_button = pygame.image.load("canon_button.png").convert_alpha()
    moulin_button = pygame.image.load("moulin_img.png").convert_alpha()
    retour_button = pygame.image.load("retour_img.png").convert_alpha()
    canon_vie_button=cannon_button.get_rect(topleft=(70,350))
    moulin_vie_button=moulin_button.get_rect(topleft=(70,250))
    retour_vie_button=retour_button.get_rect(topleft=(70,60))
    menu_title=font.render("Fonctionalités",True,(0,0,0))
    canon_txt=font1.render("crée une figure qui lance des planeurs, cependant elle nécessite une grille avec une largeur supérieur 39",True,(0,0,0))
    moulin_txt=font1.render("crée une figure clignotante plutôt curieuse, cependant elle nécessite une grille avec une largeur supérieur 9",True,(0,0,0))
    screen.blit(fond, (0,0))
    while running:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if pygame.mouse.get_pressed()[0]:
                # récupère les coordonnées de la souris
                x, y = pygame.mouse.get_pos()
                if retour_vie_button.collidepoint(x,y):
                    running=False
                if canon_vie_button.collidepoint(x,y):
                    if len(world)>=36:
                        world=jdlv.new_world(len(world),len(world))
                        world=models.canon_planeur(world)
                        run(120/nb_frame_sec, marge, world)
                if moulin_vie_button.collidepoint(x,y):
                    if len(world)>=9:
                        world=jdlv.new_world(len(world),len(world))
                        world=models.moulin_figure(world)
                        run(120/nb_frame_sec, marge, world)
        x,y=pygame.mouse.get_pos()
        if moulin_vie_button.collidepoint(x,y):
            screen.blit(moulin_txt, (130,265))
        else:
            screen.blit(fond, (0,0))
        x,y=pygame.mouse.get_pos()
        if canon_vie_button.collidepoint(x,y):
            screen.blit(canon_txt, (130,365))
        else:
            screen.blit(fond, (0,0))

        screen.blit(cannon_button, (70,350))
        screen.blit(moulin_button, (70,250))
        screen.blit(menu_title, (450,60))
        screen.blit(retour_button, (70,60))
        pygame.display.update()
        mainClock.tick(60)
    pygame.quit()



"""def compte_nb_cellules(world):

    compteur=0
    for ligne in world:
        for case in ligne:
            if case:
                compteur+=1
    return compteur"""

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


def next_generation(world, generation_affichee, former_generations, actual_gen, derniere_gen,v2, precedente=False):
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
    # créé une fenêtre de 1200 pixels de large et 600 pixels de haut
    screen = pygame.display.set_mode((1200, 600), pygame.RESIZABLE)
    pygame.display.set_caption("Programme du Jeu de la Vie")
    clock = pygame.time.Clock()


def run(nb_tick, marge, world, v2=False):
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

    # créé et initialise un nouvelle matrice
    """world = jdlv.start()
    world = jdlv.init_world(world)
    setup()"""
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
    menu_button = pygame.image.load("dropdown_menu.png").convert_alpha()
    v2_button = pygame.image.load("button_v2.png").convert_alpha()
    rectangle_bouton_play = play_button.get_rect(topleft=(70, 50))
    rectangle_bouton_pause = pause_button.get_rect(topleft=(160, 50))
    rectangle_bouton_suivant = next_button.get_rect(topleft=(70, 500))
    rectangle_bouton_precedent = prev_button.get_rect(topleft=(160, 500))
    rectangle_button_v2= v2_button.get_rect(topleft=(900,20))
    menu_vie_button=menu_button.get_rect(topleft=(1135,20))
    gen_affichage=font.render(f"Génération actuelle : {str(generation_affichee)}",True,(0,0,0))


    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # permet de quitter la fenêtre si la croix est cliquée
                running = False

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
                        next_generation(world, generation_affichee, former_generations, actual_gen, derniere_gen,v2)
                    if rectangle_bouton_precedent.collidepoint(x, y):
                        # déclenche la précédente génération
                        world, generation_affichee, former_generations, actual_gen, derniere_gen = \
                        next_generation(world, generation_affichee, former_generations, actual_gen, derniere_gen,v2, precedente=True)
                    if menu_vie_button.collidepoint(x,y):
                        options()
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
        screen.blit(gen_affichage, (915, 550))
        screen.blit(menu_button, (1135, 20))
        screen.blit(v2_button,(900,20))

        dessiner_grille(len(world), marge*2)
        dessiner_cellules(world, marge*2)

        if play:
            # permet d'afficher au rythme de deux images par seconde
            if compteur_frames > nb_tick:
                # déclenche la prochaine génération
                world, generation_affichee, former_generations, actual_gen, derniere_gen = \
                next_generation(world, generation_affichee, former_generations, actual_gen, derniere_gen,v2)
                compteur_frames = 0

        compteur_frames +=1
        clock.tick(120)

    pygame.quit()

world = jdlv.start()
world = jdlv.init_world(world)
setup()
marge = 20
nb_frame_sec = 120
welcome()
