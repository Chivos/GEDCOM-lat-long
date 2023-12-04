import os #pour lecture du dossier courant
import re #pour regex


##Adresse des fichiers cherchés dans dossier courant du script

adresse_coord = os.path.dirname(os.path.realpath(__file__)) + "\\FR - Copie.txt"
adresse_coord_mod = os.path.dirname(os.path.realpath(__file__)) + "\\FR-copie-mod.txt"


##Ouverture des fichiers et création d'une copie
file_coord = open(adresse_coord, 'r')
file_coord_mod = open(adresse_coord_mod, 'w')

coord_file_list = file_coord.readlines() #Fichier des coordonnées d'entrée sous forme de liste
file_coord_mod_list = [] #Liste du FR modifié


###################################################################################################
###################  BOUCLE PRINCIPALE  ###################
###################################################################################################

for line_number, line in enumerate(coord_file_list):

    lieu_administratif = re.search(r"PPL", line)

    
    if lieu_administratif: #Si un code PPLA ou PPLA2 ou... est trouvé sur la ligne
        
        ligne_ajoute = coord_file_list[line_number]
        ligne_ajoute = re.sub(r"^\d*", "",ligne_ajoute)
        ligne_ajoute = re.sub(r"^\W*", "",ligne_ajoute)
        ligne_ajoute = re.sub(r"Europe.*", "" ,ligne_ajoute)
        #pattern = r"[^.]\d{5}(.*)"
        #ligne_ajoute = re.sub(pattern, r"\1" ,ligne_ajoute) #après code INSEE
        file_coord_mod_list.append(ligne_ajoute) #copie de la ligne en cours


##Ecriture fichier GED modifié, complété avec les coordonnées lat/long
for ligne_ecriture in file_coord_mod_list:
    file_coord_mod.write(ligne_ecriture)