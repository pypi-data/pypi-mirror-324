import os
import pandas as pd
from datetime import datetime
import MetManagement as MetManagement

#get_aait_store_remote_version

# Fonction pour récupérer les informations des fichiers dans un dossier donné
def get_file_info(directory):
    """
    Récupère les informations des fichiers dans un dossier donné.

    :param directory: Chemin du dossier à analyser.
    :return: Un dictionnaire contenant les noms des fichiers comme clés et leurs tailles et dates de modification comme valeurs.
    """
    file_info = {}
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_stats = os.stat(file_path)
            file_info[file] = {
                'size': MetManagement.get_size(file_path),
                'modified': datetime.fromtimestamp(file_stats.st_mtime).isoformat()
            }
    return file_info

# Fonction pour comparer deux dossiers
def compare_directories(local_dir, shared_dir):
    """
    Compare deux dossiers et identifie les différences entre les fichiers.

    :param local_dir: Chemin du dossier local.
    :param shared_dir: Chemin du dossier partagé.
    :return: Une liste de dictionnaires contenant les informations sur les fichiers comparés, avec les colonnes pour les tailles, les dates et le statut.
    """
    # Récupérer les informations des fichiers pour les deux dossiers
    local_files = get_file_info(local_dir)
    shared_files = get_file_info(shared_dir)

    data = []

    # Comparer les fichiers présents dans les deux dossiers
    for file, local_info in local_files.items():
        if file in shared_files:
            shared_info = shared_files[file]
            size_diff = local_info['size'] != shared_info['size']
            date_diff = local_info['modified'] != shared_info['modified']

            # Déterminer le statut du fichier
            status = "OK" if not size_diff and not date_diff else "N-OK"

            # Ajouter les informations au résultat
            data.append({
                'File': file,
                'Status': status,
                'Local Size (bytes)': local_info['size'],
                'Shared Size (bytes)': shared_info['size'],
                'Local Modified Date': local_info['modified'],
                'Shared Modified Date': shared_info['modified']
            })
        else:
            # Cas où le fichier est absent dans le dossier partagé
            data.append({
                'File': file,
                'Status': "N-OK",
                'Local Size (bytes)': local_info['size'],
                'Shared Size (bytes)': "Absent",
                'Local Modified Date': local_info['modified'],
                'Shared Modified Date': "Absent"
            })

    # Vérifier les fichiers manquants localement
    for file in shared_files.keys():
        if file not in local_files:
            shared_info = shared_files[file]
            data.append({
                'File': file,
                'Status': "N-OK",
                'Local Size (bytes)': "Absent",
                'Shared Size (bytes)': shared_info['size'],
                'Local Modified Date': "Absent",
                'Shared Modified Date': shared_info['modified']
            })

    return data

# Exemple d'utilisation :
local_dir = r"C:\\Users\\Admin\\Desktop\\test"
shared_dir = r"E:\\01-Hotline\\test"
result = compare_directories(local_dir, shared_dir)

# Créer un DataFrame pour organiser les résultats
print("Création d'un DataFrame pour les résultats de la comparaison...")
df = pd.DataFrame(result)

# Exporter les résultats vers un fichier Excel
output_file = "comparison_result.xlsx"
print(f"Exportation des résultats dans le fichier Excel : {output_file}...")
df.to_excel(output_file, index=False)

# Afficher les résultats dans le terminal
print("Résultats de la comparaison :")
print(df)

print("ress path", MetManagement.get_aait_store_remote_ressources_path())

print(f"Les résultats de la comparaison ont été enregistrés dans {output_file}.")
