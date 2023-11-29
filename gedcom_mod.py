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
pattern = r'\bPPLA.?\b.*\b' + re.escape(INSEE) + r'\b' #ligne qui contient PPLA / PPLA2 / ... (lieu habité de division administratif, pour ne pas s'accrocher aux hameaux, quartiers...) + le code INSEE
print(pattern)


for index, line_coord in enumerate(lines_coord, start=1):
    if re.search(pattern, line_coord):
        line_number = index
        print("ligne trouvé FR.txt", line_number)
        break


