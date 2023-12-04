from time import time
debut = time()
import os #pour lecture du dossier courant
import re #pour regex

def recherche_coord(coord_file_list, INSEE):
    lat_long = False

    pattern_ville = r'^' + re.escape(INSEE)
    
    for line_number_coord, line_coord in enumerate(coord_file_list):
        if re.search(pattern_ville, line_coord):
            break

    ville = coord_file_list[line_number_coord]
    pattern_lat_long = r'(-?\d{1,3}\.\d+)' #signe - optionnel, valeur de 1 à 3 chiffres, un point, et un ou plusieurs chiffres
    lat_long = re.findall(pattern_lat_long, ville) #renvoi une liste avec lat puis long
    return(lat_long)

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

nb_insertion = 0 #Variable pour compter le nombre d'insertion de coordonnées et corriger la dérive entre le fichier GED d'entrée et sa copie

###################################################################################################
###################  BOUCLE PRINCIPALE  ###################
###################################################################################################

for line_number_GED, line_GED in enumerate(GED_file_list):
    GED_mod_file_list.append(line_GED) #copie de la ligne GED en cours

    #INSEE = re.search(r"\D+(\d{5})\D+", line_GED) #en série - caractères non digits, 1 ou plus ; 5 digits ; caractères non digits, 1 ou plus
    #INSEE = re.search(r"[ ,](\d{5})[ ,]", line_GED) #en série - espace ou virgule ; 5 digits ; espace ou virgule
    INSEE = re.search(r"\bPLAC\b.*(\d{5})", line_GED) #en série text avec PLAC, des caractères et 5 digits

    if INSEE: #Si un code INSEE est trouvé sur la ligne
        INSEE = INSEE.group(1)
        #print("Code INSEE lu", INSEE)
        #print("Ligne associée", line_number_GED+1)
        
        lat_long = recherche_coord(coord_file_list, INSEE)
        
        GED_mod_file_list.insert(line_number_GED+1 + nb_insertion*3, "3 MAP\n")
        GED_mod_file_list.insert(line_number_GED+2 + nb_insertion*3, "4 LATI N" + lat_long[0] + "\n")
        GED_mod_file_list.insert(line_number_GED+3 + nb_insertion*3, "4 LONG E" + lat_long[1] + "\n")

        nb_insertion += 1


##Ecriture fichier GED modifié, complété avec les coordonnées lat/long
for ligne_ecriture in GED_mod_file_list:
    file_GED_mod.write(ligne_ecriture)


print("Nombre de coordonnées ajoutées : ", nb_insertion)
print("Durée : ", time()-debut)