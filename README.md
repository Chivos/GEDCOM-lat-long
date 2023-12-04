# GEDCOM-lat-long
Ajouter latitude et longitude aux fichiers GEDCOM, à partir du code INSEE de la ville

Objectif : 
- lire le code INSEE pour chaque lieu du fichier GEDCOM
- récuper les coordonnées LAT / LONG à partir des données issues de https://www.data.gouv.fr/fr/datasets/communes-de-france-base-des-codes-postaux/ (et modifié pour supprimer les données non nécessaires, les doublons, et ajouter les codes INSEE pour les villes à arrondissements)
- les insérer dans le fichier GED avec les bonnes balises

L'exécution prend  plusieurs minutes, en fonction de la taille du fichier GED en entrée.

Le dossier tools contient le fichier FR.txt avant réduction aux villes et villages, mais avec suppression des caractères non ASCII, ainsi que le script qui a permis de faire le filtre.
