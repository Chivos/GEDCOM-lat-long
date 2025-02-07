from time import time
debut = time()
import os #pour lecture du dossier courant
import re #pour regex

def recherche_coord(coord_file_list, INSEE):
    lat_long = False

    pattern_ville = r'^' + re.escape(INSEE) #regex pour recherche code INSEE
    pattern_lat_long = r'(-?\d{1,3}\.\d+)' #signe - optionnel, valeur de 1 à 3 chiffres, un point, et un ou plusieurs chiffres #regex pour rechercher coordonées géographiques
    
    for line_number_coord, line_coord in enumerate(coord_file_list):
        if re.search(pattern_ville, line_coord):
            ville = coord_file_list[line_number_coord]
            lat_long = re.findall(pattern_lat_long, ville) #renvoi une liste avec lat puis long
            break


    return(lat_long, line_coord)

###################################################################################################
###################  FIN FONCTIONS, DEBUT SCRIPT  ###################
###################################################################################################

##Adresse des fichiers cherchés dans dossier courant du script
adresse_GED = os.path.dirname(os.path.realpath(__file__)) + "\\base.ged"
adresse_coord = os.path.dirname(os.path.realpath(__file__)) + "\\FR.txt"
adresse_GED_mod = os.path.dirname(os.path.realpath(__file__)) + "\\base_mod.ged"

##Ouverture des fichiers et création d'une copie du GED  
file_GED = open(adresse_GED, 'r')
file_coord = open(adresse_coord, 'r')
file_GED_mod = open(adresse_GED_mod, 'w')

GED_file_list = file_GED.readlines() #Fichier GED d'entrée sous forme de liste
coord_file_list = file_coord.readlines() #Fichier des coordonnées d'entrée sous forme de liste
GED_mod_file_list = [] #Liste du GED complété

unfound_INSEE = [] #Liste des codes INSEE non trouvés dans la base de données des coordonnées géographiques

nb_insertion = 0 #Variable pour compter le nombre d'insertion de coordonnées et corriger la dérive entre le fichier GED d'entrée et sa copie

GED_file_list[1:1] = ['1 PLAC\n', '2 FORM city, area code, county, state, country\n'] #Ajout dans l'en-tête de la description du format des lieux

###################################################################################################
###################  BOUCLE PRINCIPALE  ###################
###################################################################################################

for line_number_GED, line_GED in enumerate(GED_file_list):
    line_GED = re.sub(r"\[.*] - " , '', line_GED) #Suppression du lieu dit au format Geneanet "[Lieu-dit] - "
    GED_mod_file_list.append(line_GED) #copie de la ligne GED en cours

    #INSEE = re.search(r"\bPLAC\b.*(\d{5})", line_GED) #en série text avec PLAC, des caractères et 5 digits
    INSEE = re.search(r"\bPLAC\b.*(\d\w\d{3})", line_GED) #en série text avec PLAC, des caractères et 1 digit, 1 lettre ou chiffre puis 3 digits, pour Corse

    if INSEE: #Si un code INSEE est trouvé sur la ligne
        INSEE = INSEE.group(1)
        
        lat_long, line_coord = recherche_coord(coord_file_list, INSEE) #réception des coordonnées et de la ligne complète du fichier source
        
        if lat_long != False:
            ## optimisation vitesse
            #coord_file_list.insert(0, line_coord) #insertion de la ligne complète en tête du fichier source pour optimisation temps
                #semble le plus rapide mais augmente la taille de la liste des coordonnées
                #devrait être moins efficace sur très grand GEDCOM
            index = coord_file_list.index(line_coord) #recherche index de l'élément de la liste des coordonnées
            if index > 100: #ne pas reconstruire la liste systématiquement si coordonnées bien placées
                coord_file_list = [line_coord] + coord_file_list[:index] + coord_file_list[index+1:] #le déplace en premier et reconstruit la liste par slices
            
            GED_mod_file_list.insert(line_number_GED+1 + nb_insertion*3, "3 MAP\n")
            GED_mod_file_list.insert(line_number_GED+2 + nb_insertion*3, "4 LATI N" + lat_long[0] + "\n")
            GED_mod_file_list.insert(line_number_GED+3 + nb_insertion*3, "4 LONG E" + lat_long[1] + "\n")

            nb_insertion += 1
        
        else:
            if INSEE not in unfound_INSEE:
                print("Non trouvé pour le code INSEE :", INSEE)
                unfound_INSEE.append(INSEE)


##Ecriture fichier GED modifié, complété avec les coordonnées lat/long
for ligne_ecriture in GED_mod_file_list:
    file_GED_mod.write(ligne_ecriture)

fin = time()
print("Nombre de coordonnées ajoutées :", nb_insertion)
print("Durée :", round(fin-debut, 1), "secondes")
print("Vitesse :", round(nb_insertion/(fin-debut),1), "ajouts par seconde")