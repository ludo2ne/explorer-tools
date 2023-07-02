import csv
import os
import re

def supprimer_symboles_csv(chemin_entree):
    """
    Supprime les symboles spécifiés dans un fichier CSV.

    Args:
        chemin_entree (str): Chemin vers le fichier CSV d'entrée.

    Raises:
        FileNotFoundError: Si le fichier d'entrée n'est pas trouvé.

    Returns:
        str: Chemin du fichier CSV de sortie créé.
    """

    # Liste des symboles à supprimer
    symboles = ['(', ')', '+', '&', '*']

    # Vérifier si le fichier d'entrée existe
    if not os.path.isfile(chemin_entree):
        raise FileNotFoundError("Le fichier d'entrée spécifié est introuvable.")

    # Créer le chemin de sortie avec le suffixe '_cleaned'
    chemin_sortie = os.path.splitext(chemin_entree)[0] + '_cleaned.csv'

    # Ouverture du fichier d'entrée en mode lecture et du fichier de sortie en mode écriture
    with open(chemin_entree, 'r') as file_in, open(chemin_sortie, 'w', newline='') as file_out:
        # Création des objets de lecture et d'écriture CSV
        reader = csv.reader(file_in, delimiter=';')
        writer = csv.writer(file_out, delimiter=';')

        for row in reader:
            # Suppression des symboles dans chaque élément de la ligne
            row_modifiee = [re.sub('[' + re.escape(''.join(symboles)) + ']', '', element) for element in row]

            # Écriture de la ligne modifiée dans le fichier de sortie
            writer.writerow(row_modifiee)

    print(f"Le fichier CSV a été traité et le résultat a été écrit dans {chemin_sortie}.")

    return chemin_sortie

supprimer_symboles_csv('/home/ludovic/Documents/03. Pro/50. Pret de corbeaux/october/a.csv')
