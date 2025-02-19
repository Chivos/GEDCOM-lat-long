from time import time
import os
import re # pour regex

debut = time()

def load_coord_dict(coord_file_path):
    coord_dict = {}
    pattern_ville = re.compile(r'^(\d\w\d{3})') #Numéro INSEE : 1 chiffre, chiffre ou lettre (pour corse) puis 3 chiffres
    pattern_lat_long = re.compile(r'(-?\d{1,3}\.\d+)') #signe - optionnel, valeur de 1 à 3 chiffres, un point, et un ou plusieurs chiffres #regex pour rechercher coordonées géographiques
    with open(coord_file_path, 'r') as f:
        for line in f:
            match_ville = pattern_ville.match(line)
            if match_ville:
                INSEE = match_ville.group(1)
                lat_long = pattern_lat_long.findall(line) #renvoi une liste avec lat puis long
                if len(lat_long) == 2:
                    coord_dict[INSEE] = lat_long
    return coord_dict


# File paths
adresse_GED = os.path.join(os.path.dirname(os.path.realpath(__file__)), "base.ged")
adresse_coord = os.path.join(os.path.dirname(os.path.realpath(__file__)), "FR.txt")
adresse_GED_mod = os.path.join(os.path.dirname(os.path.realpath(__file__)), "base_mod.ged")

# Load coordinates into a dictionary
coord_dict = load_coord_dict(adresse_coord)

# Ouverture des fichiers
file_GED = open(adresse_GED, 'r')
file_coord = open(adresse_coord, 'r')
file_GED_mod = open(adresse_GED_mod, 'w')


pattern_insee = re.compile(r"\bPLAC\b.*(\d\w\d{3})") #en série text avec PLAC, des caractères et 1 digit, 1 lettre ou chiffre puis 3 digits, pour Corse

GED_mod_file_list = [] #Liste du GED complété
nb_insertion = 0 #Variable pour compter le nombre d'insertion de coordonnées et corriger la dérive entre le fichier GED d'entrée et sa copie
unfound_INSEE = set() #Liste des codes INSEE non trouvés dans la base de données des coordonnées géographiques

for line in file_GED:
    line_mod = re.sub(r"\[.*] - ", '', line) #Suppression du lieu dit au format Geneanet "[Lieu-dit] - "
    GED_mod_file_list.append(line_mod) #copie de la ligne en cours dans le futur GED

    match_insee = pattern_insee.search(line_mod)
    if match_insee: #Si un code INSEE est trouvé sur la ligne
        INSEE = match_insee.group(1)
        lat_long = coord_dict.get(INSEE)
        if lat_long:
            GED_mod_file_list.append("3 MAP\n")
            GED_mod_file_list.append(f"4 LATI N{lat_long[0]}\n")
            GED_mod_file_list.append(f"4 LONG E{lat_long[1]}\n")
            nb_insertion += 1
        else:
            unfound_INSEE.add(INSEE)

print("-------------------------------------")
print("Non trouvé pour les code INSEE suivants:")
for item in unfound_INSEE:
    print(item)

##Ecriture fichier GED modifié, complété avec les coordonnées lat/long
file_GED_mod.writelines(GED_mod_file_list)
print("-------------------------------------")
print("Nombre de coordonnées ajoutées :", nb_insertion)

fin = time()
print("Durée :", round(fin - debut, 1), "secondes")
print("Vitesse :", round(nb_insertion / (fin - debut), 1), "ajouts par seconde")
print("-------------------------------------")