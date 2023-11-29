import os #pour lecture du dossier courant
import re
import chardet

adresse_GED = os.path.dirname(os.path.realpath(__file__)) + "\\base.ged"
adresse_coord = os.path.dirname(os.path.realpath(__file__)) + "\\FR.txt"

file_GED = open(adresse_GED, 'r')
file_coord = open(adresse_coord, 'r')

lines_GED = file_GED.readlines()

for line_number, line in enumerate(lines_GED):
    INSEE = re.search(r"\D+(\d{5})\D+", line) #en série - caractères non digits, 1 ou plus ; 5 digits ; caractères non digits, 1 ou plus
    if INSEE:
        INSEE = INSEE.group(1)
        print("Code INSEE lu", INSEE)
        print("Ligne associée", line_number)
        break
        

lines_coord = file_coord.readlines()

line_coord_number = None
pattern = r'\D(' + re.escape(INSEE) + r')\D'

for index, line_coord in enumerate(lines_coord, start=1):
    if re.search(pattern, line_coord):
    #if re.search(r"\D(30189)\D", line_coord): #en serie - espace ou tabulation ; 5 digits ; espace ou tabulation
        line_number = index
        print("ligne trouvé FR.txt", line_number)
        break



#if re.search(r"[  ]+(\d{5})[  ]+", line_coord): #en serie - espace ou tabulation ; 5 digits ; espace ou tabulation