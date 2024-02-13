# GEDCOM-lat-long
Ajouter latitude et longitude aux fichiers GEDCOM, à partir du code INSEE de la ville

### Objectif : 
- lire le code INSEE pour chaque lieu du fichier GEDCOM
- récuper les coordonnées LAT / LONG à partir des données issues de https://www.data.gouv.fr/fr/datasets/communes-de-france-base-des-codes-postaux/ (et modifié pour supprimer les données non nécessaires, les doublons, et ajouter les codes INSEE pour les villes à arrondissements)
- les insérer dans le fichier GED avec les bonnes balises

En complément :
- supprimer les lieux dits saisis au format Généanet
- ajouter dans le header du GEDCOM la description du format de saisie des lieux

L'exécution prend quelques dizaines de secondes, en fonction de la taille du fichier GED en entrée.


### Utilisation
- téélcharger le fichier de scipt python gedcom_mod.py et le fichier source des coordonnées FR.txt
- déposer le même dossier le fichier .ged à compléter, par défaut nommé base.ged, sinon adapter le script
- exécuter le script avec la commande ```python gedcom_mod.py```

## English
This script aims to add latitude and longitude to a GEDCOM file for French cities when the INSEE code is used to specify the event location. (The INSEE code is a unique identifier for each French city.)
