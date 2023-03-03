from fltk import *
import shapefile
import math
import choixinformation
import os

try:
  from shapely.geometry import Point, Polygon
except ImportError:
  print ("Installation du module: shapely")
  print("Si vous rencontrz une erreur veuillez relancer le programme\n")
  os.system('pip install shapely')
  from shapely.geometry import Point, Polygon
    # installe le module si il ne l'est pas déjà

# Initialisation des données
edge_x = 30
edge_y = 30
cree_fenetre(1000 + edge_x*2, 800 + edge_y*2)

num = [95,78,93,77,92,75,94,91] # numero du departement à afficher
data_csv = ['dans-le-val-doise.csv','dans-les-yvelines.csv','en-seine-saint-denis.csv',
            'en-seine-et-marne.csv','dans-les-hauts-de-seine.csv',None,
            'dans-le-val-de-marne.csv','en-essonne.csv']

noms_dep = ["Val-d'Oise", "Yvelines", "Seine-Saint-Denis", 
            "Seine-et-Marne", "Hauts-de-Seine", "Paris",
            "Val-de-Marne", "Essone"]

for i in range(len(data_csv)):
    if data_csv[i] != None: data_csv[i] = 'cartes/carte-des-licencies-sportifs-' + data_csv[i]

multi_x = 450
multi_y = 700
bbox=[]
ext_pts = []
lst_points = []

data_show = False
draw = False
is_menu = True

sf = shapefile.Reader("departements-20180101-shp/departements-20180101")
r = sf.records()


def menu():
    """
    Premiere fenetre de menu affichant les departement d'ile de france
    """
    # Création de l'Ile-de-France
    correct = 0.2 # premet de centrer le polygone 
    for m in range (len(num)):
        all_pts = []

        for i in range (len(r)):
            if r[i][0] == str(num[m]):
                region = sf.shape(i)

        bbox.append(region.bbox)
        points = region.points

        for i in range(len(bbox[0])): # réglage des coord des extrémités pour la fenêtre dans ext_pts
            if i%2 == 0: ext_pts.append(multi_x*bbox[m][i] + edge_x) # largeur
            else: ext_pts.append(multi_y*bbox[m][i] + edge_y) # hauteur


        largeur = ext_pts[2] - ext_pts[0] + edge_x*2
        hauteur = ext_pts[3] - ext_pts[1] + edge_y*2

        for i in reversed(range(len(points))): # réglage des coord des points pour la fenêtre dans all_pts
            all_pts.append((multi_x*(points[i][0]-bbox[0][0]+correct)+edge_x,
            hauteur-multi_y*(points[i][1]-bbox[0][1])-edge_y)) # largeur, hauteur

        lst_points.append(all_pts)
        polygone(lst_points[m], couleur='black', epaisseur=1)
    return bbox, multi_x, multi_y, hauteur, largeur


def retour_menu(edge_x, edge_y):
    """
    On revient à l'affichage de l'Ile-de-France
    apres avoir fait clic droit sur la souris
    """
    cree_fenetre(1000 + edge_x*2, 800 + edge_y*2)
    for m in range (len(num)):
        polygone(lst_points[m], couleur='black', epaisseur=1)


def affichepolygone(num, csv, dep, edge_x, egde_y, federation, information):

    # Création du département
    for i in range (len(r)):
        if r[i][0]==str(num):
            region = sf.shape(i)

    bbox = region.bbox
    points = region.points

    ext_pts = []
    all_pts = []
    multi_x = 550
    multi_y = 800
    multi = multi_y/multi_x

    for i in range(len(bbox)): # réglage des coord des extrémités pour la fenêtre dans ext_pts
        if i%2 == 0: ext_pts.append(multi_x*bbox[i] + edge_x) # largeur
        else: ext_pts.append(multi_y*bbox[i] + edge_y) # hauteur


    largeur = ext_pts[2] - ext_pts[0] + edge_x
    hauteur = ext_pts[3] - ext_pts[1] + edge_y

    while largeur < 400 or hauteur < 300:
        multi_x *= multi
        multi_y *= multi
        ext_pts = []
        for i in range(len(bbox)): # réglage des coord des extrémités pour la fenêtre dans ext_pts
            if i%2 == 0:
                ext_pts.append(multi_x*bbox[i] + edge_x) # largeur
            else:
                ext_pts.append(multi_y*bbox[i] + edge_y) # hauteur
        largeur = ext_pts[2] - ext_pts[0] + edge_x*2
        hauteur = ext_pts[3] - ext_pts[1] + edge_y*2

    largeur = ext_pts[2] - ext_pts[0] + edge_x*2
    hauteur = ext_pts[3] - ext_pts[1] + edge_y*2

    for i in reversed(range(len(points))): # réglage des coord des points pour la fenêtre dans all_pts
        all_pts.append((multi_x*(points[i][0]-bbox[0])+edge_x,
        hauteur-multi_y*(points[i][1]-bbox[1])-edge_y)) # largeur, hauteur


    # Affichage du département
    cree_fenetre(largeur, hauteur)
    polygone(all_pts, couleur='black', epaisseur=1)
    texte(5,5,dep+' ('+str(num)+')',taille=10)

    if num == 75:
        texte(largeur/2, hauteur/2-10, "Les données pour Paris", ancrage="center", taille=16)
        texte(largeur/2, hauteur/2+10, "ne sont pas disponibles.", ancrage="center", taille=16)
        return False


    # Dessin des cercles par rapport aux données
    data = []
    communes = [[],[],[],[],[]]
    with open(csv,'r') as csv_file: #carte-des-licencies-sportifs

        lines = csv_file.readlines()
        for i in range(1, len(lines)-1): # coordonnées des villes

            if federation in lines[i]:
                row = lines[i].split(';')
                data.append((row[3], row[5]))
                communes[0].append(row[2]) # nom de la commune
                communes[2].append(row[information]) # infos de la commune

        for i in range(len(data)): # dessin des cercles
            coord_x = float(data[i][0].split(',')[1])
            coord_y = float(data[i][0].split(',')[0])

            if data[i][1] != '': nb_lic = int(data[i][1])
            else: nb_lic = 0
            '''
            On veut que l'aire soit proportionelle au nombre de licenciés.
            Alors on calcule le rayon en fonction de l'aire.
            pi*r*r = aire
            r*r = aire/pi
            r = sqrt(aire/pi)
            '''
            rayon = math.sqrt(nb_lic/math.pi) # on multiplie par 2 car trop petit sinon

            cercle(multi_x*(coord_x-bbox[0])+edge_x, hauteur-multi_y*(coord_y-bbox[1])-edge_y,
                rayon, couleur='black', remplissage='blue')
            #print(multi_x*(coord_x-bbox[0]), multi_y-multi_y*(coord_y-bbox[1]))
            communes[1].append((multi_x*(coord_x-bbox[0])+edge_x,
                hauteur-multi_y*(coord_y-bbox[1])-edge_y)) # coordonnées sur la fenetre de chaque cercle
            communes[3].append(rayon) # rayon du cercle de chaque ville
            communes[4].append(largeur)
    csv_file.close

    return communes


# Partie principale
bbox, multi_x, multi_y, hauteur, largeur = menu()
information = 0

while True:
    ev = donne_ev()
    tev = type_ev(ev)
    x = abscisse_souris()
    y = ordonnee_souris()

    # Affichage des infos des villes
    if not is_menu:
        display = False

        if communes:
            for i in range(len(communes[0])):

                x_commune = communes[1][i][0] # x du centrez du cercle de la commune
                y_commune = communes[1][i][1] # y du centre du cercle de la commune
                distance = math.sqrt((x - x_commune)**2 + (y - y_commune)**2) # distance entre la souris et le centre du cecle
                rayon = communes[3][i]

                if distance > 5 and distance > rayon and not display:
                    efface("info")

                elif distance <= 5 or distance <= rayon:
                    # Réglage d'un bug d'affichage lors du choix de la dernière option
                    if information == 21:
                        ancragebis = 11
                    else:
                        ancragebis = 20

                    nom = str(communes[0][i])+': '+str(communes[2][i]) # chaine de caratères avec le nom de la commune et le nombre d'habitant
                    long, haut = taille_texte(nom, taille='10')

                    display = True
                    efface("info")

                    if x + long//2 >= communes[4][0] - 5: # Si le texte depasse du cote droit de la fentre
                        x = communes[4][0] - long//2 - 5
                    elif x - long//2 <= 5: # Si le texte depasse du cote gauche de la fentre
                        x = long//2 + 5

                    cercle(x_commune, y_commune, rayon, remplissage="red", tag="info")
                    rectangle(x-1 -long//2, y-ancragebis -haut//2, x+1 +long//2, y-ancragebis +haut//2,couleur="black",remplissage='white',tag="info")
                    texte(x, y-ancragebis, nom, couleur="black", taille = 10, ancrage='center', tag="info")

        if tev == "ClicDroit":
            is_menu=True
            ferme_fenetre()
            retour_menu(edge_x, edge_y)


    # Choix du département et des infos
    point_to_check = (x,y) # an x,y tuple

    if is_menu == True:
        for i in range(len(lst_points)):

            poly = Polygon(lst_points[i]) # get a boundary polygon

            if Point(point_to_check).within(poly): # make a point and see if it's in the polygon
                name = num[i] # get the second field of the corresponding record
                efface('p'+ str(i))
                polygone(lst_points[i], couleur='black',remplissage="blue", epaisseur=1,tag='p'+ str(i) )

                if tev == "ClicGauche":
                    is_menu=False

                    if data_csv[i] is not None :
                        efface_tout()
                        federation=choixinformation.page_recherche(data_csv[i])
                        efface_tout()
                        information=choixinformation.infoclique(data_csv[i])
                    else:
                        efface_tout()
                        federation=None
                        information=None
                    efface_tout()
                    ferme_fenetre()
                    communes = affichepolygone(num[i],data_csv[i],noms_dep[i],edge_x,edge_y,federation,information)
                    data_show = True
            else :
                efface('p'+ str(i))

    # on met à jour pour détecter les nouveaux événements
    mise_a_jour()
    if tev == 'Quitte':
        break
# Le dernier événement était 'Quitte', on ferme la fenêtre
ferme_fenetre()