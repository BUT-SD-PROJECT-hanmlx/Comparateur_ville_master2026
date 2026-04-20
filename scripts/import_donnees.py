"""
Script d'import et de gestion des donnees
==========================================
Script pour importer et mettre a jour les donnees des villes francaises.

Auteurs : [A completer avec les noms des etudiants]
Cours : SAE Outils Decisionnels
"""

import pandas as pd
import requests
import json
from datetime import datetime
import os

# ============================================================================
# CONFIGURATION
# ============================================================================

DATA_DIR = "data"
VILLES_FILE = os.path.join(DATA_DIR, "villes_data.csv")

# ============================================================================
# SOURCES DE DONNEES
# ============================================================================

"""
Sources utilisees :

1. INSEE (Institut National de la Statistique et des Etudes Economiques)
   - URL : https://www.insee.fr
   - Donnees : Population, superficie, densite
   - Acces : Open Data (telechargement direct)

2. Open-Meteo API
   - URL : https://open-meteo.com
   - Donnees : Meteo actuelle, previsions
   - Acces : Gratuit, sans cle API
   - Limite : 10 000 requetes/jour

3. Donnees Emploi (Pole Emploi / INSEE)
   - URL : https://www.pole-emploi.org / https://www.insee.fr
   - Donnees : Taux de chomage, secteurs d'activite
   - Acces : Open Data

4. Observatoires Locaux des Loyers
   - URL : https://www.data.gouv.fr
   - Donnees : Loyers, type de logement
   - Acces : Open Data
"""

# ============================================================================
# FONCTIONS D'IMPORT
# ============================================================================

def importer_donnees_insee():
    """
    Importe les donnees demographiques depuis l'INSEE.

    Procesus :
    1. Se rendre sur https://www.insee.fr/fr/statistiques
    2. Telecharger le fichier des communes francaises
    3. Filtrer les communes de plus de 20 000 habitants
    4. Exporter en CSV
    """
    print("=" * 60)
    print("IMPORT DONNEES INSEE")
    print("=" * 60)

    urls = {
        "population": "https://www.insee.fr/fr/statistiques/2012713",
        "superficie": "https://www.insee.fr/fr/statistiques/2028028",
        "communes": "https://www.data.gouv.fr/fr/datasets/r/70cef04f-f2d1-42a3-8307-2d875c2f69d8"
    }

    print("\nInstructions pour recuperer les donnees :")
    print("-" * 40)
    print("1. Allez sur https://www.insee.fr/fr/statistiques")
    print("2. Recherchez 'populations legales des communes'")
    print("3. Telechargez le fichier CSV")
    print("4. Placez le fichier dans le dossier 'data'")
    print("-" * 40)

    return None


def importer_donnees_meteo_api(lat, lon):
    """
    Importe les donnees meteo via l'API Open-Meteo.
    """
    url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum&timezone=Europe/Paris&forecast_days=7"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"+ Donnees meteo recuperees pour ({lat}, {lon})")
            return data
        else:
            print(f"- Erreur API: {response.status_code}")
            return None
    except Exception as e:
        print(f"- Erreur: {e}")
        return None


def mise_a_jour_meteo_toutes_villes():
    """
    Met a jour les donnees meteo pour toutes les villes.
    """
    print("\n" + "=" * 60)
    print("MISE A JOUR METEO")
    print("=" * 60)

    if os.path.exists(VILLES_FILE):
        df = pd.read_csv(VILLES_FILE)
    else:
        print("- Fichier villes non trouve.")
        return

    donnees_meteo = []
    for _, ville in df.iterrows():
        data = importer_donnees_meteo_api(ville['latitude'], ville['longitude'])
        if data:
            meteo = {
                'ville': ville['ville'],
                'date_maj': datetime.now().strftime('%Y-%m-%d %H:%M'),
                'temperature_actuelle': data.get('current', {}).get('temperature_2m', 'N/A'),
            }
            donnees_meteo.append(meteo)

    df_meteo = pd.DataFrame(donnees_meteo)
    meteo_file = os.path.join(DATA_DIR, "meteo_actuelle.csv")
    df_meteo.to_csv(meteo_file, index=False, encoding='utf-8')
    print(f"+ Fichier {meteo_file} cree")

    return df_meteo


# ============================================================================
# EXECUTION PRINCIPALE
# ============================================================================

if __name__ == "__main__":
    print("\n" + "=" * 60)
    print("SCRIPT D'IMPORT DES DONNEES")
    print("=" * 60)
    print(f"Date : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    importer_donnees_insee()
    print("\n" + "=" * 60)
    print("TERMINÉ")
    print("=" * 60)
