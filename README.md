# GEDCOM-lat-long
Ajouter latitude et longitude aux fichiers GEDCOM, à partir du code INSEE de la ville

Objectif : 
- lire le code INSEE pour chaque lieu du fichier GEDCOM
- récuper les coordonnées LAT / LONG à partir du fichier FR.txt issu de http://download.geonames.org/export/dump/ (et modifié pour supprimer les caractères non ASCII afin d'éviter des problèmes de lecture et réduit aux seules villes et vilages)
- les insérer dans le fichier GED avec les bonnes balises

L'exécution prend  plusieurs minutes, en fonction de la taille du fichier GED en entrée.
