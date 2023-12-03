import os #pour lecture du dossier courant
import re #pour regex


adresse_GED = os.path.dirname(os.path.realpath(__file__)) + "\\base.ged"
adresse_coord = os.path.dirname(os.path.realpath(__file__)) + "\\FR.txt"
adresse_GED_mod = os.path.dirname(os.path.realpath(__file__)) + "\\base_mod.ged"

file_GED = open(adresse_GED, 'r')
file_coord = open(adresse_coord, 'r')
file_GED_mod = open(adresse_GED_mod, 'w')

lines_GED = file_GED.readlines() #Fichier GED d'entrée sous forme de liste
lines_coord = file_coord.readlines() #Fichier des coordonnées d'entrée sous forme de liste

for line_number_GED, line in enumerate(lines_GED):
    INSEE = re.search(r"\D+(\d{5})\D+", line) #en série - caractères non digits, 1 ou plus ; 5 digits ; caractères non digits, 1 ou plus
    if INSEE:
        INSEE = INSEE.group(1)
        print("Code INSEE lu", INSEE)
        print("Ligne associée", line_number_GED)
        break
        
line_coord_number = None
pattern_ville = r'\bPPLA.?\b.*\b' + re.escape(INSEE) + r'\b' #ligne qui contient PPLA / PPLA2 / ... (lieu habité de division administrative, pour ne pas s'accrocher aux hameaux, quartiers...) + le code INSEE

for index, line_coord in enumerate(lines_coord, start=0):
    if re.search(pattern_ville, line_coord):
        line_number = index
        print("ligne trouvé FR.txt", line_number)
        break


ville = lines_coord[line_number]
pattern_lat_long = r'(-?\d{1,3}\.\d+)' #signe - optionnel, valeur de 1 à 3 chiffres, un point, et un ou plusieurs chiffres
lat_long = re.findall(pattern_lat_long, ville) #renvoi un liste avec lat puis long
print(lat_long)

print("line_number", line_number)

lines_GED.insert(line_number_GED+1, "3 MAP\n")
lines_GED.insert(line_number_GED+2, "4 LATI N" + lat_long[0] + "\n")
lines_GED.insert(line_number_GED+3, "4 LONG E" + lat_long[1] + "\n")

for ligne_ecriture in lines_GED:
    file_GED_mod.write(ligne_ecriture)