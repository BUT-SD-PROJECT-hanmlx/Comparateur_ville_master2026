"""
Comparateur de Villes Françaises
================================
Application Streamlit pour comparer deux villes françaises
sur différents aspects : coût de la vie, logement, emploi, climat, etc.

Auteurs : [À compléter avec les noms des étudiants]
Cours : SAE Outils Décisionnels
"""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import requests
import time
from datetime import datetime, timedelta
import json

# ============================================================================
# CONFIGURATION DE LA PAGE
# ============================================================================

st.set_page_config(
    page_title="Comparateur de Villes Françaises",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Style CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 600;
        text-align: center;
        color: #2c3e50;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }
    .sub-header {
        font-size: 1rem;
        text-align: center;
        color: #7f8c8d;
        margin-bottom: 2rem;
        font-weight: normal;
    }
    .city-card {
        background-color: #faf8f5;
        padding: 1.5rem;
        border-radius: 4px;
        border: 1px solid #e0dcd5;
        color: #2c3e50;
        text-align: center;
    }
    .metric-card {
        background-color: #faf8f5;
        padding: 1rem;
        border-radius: 4px;
        border-left: 3px solid #8b7355;
    }
    .winner {
        background-color: #f0f4f0;
        color: #3d5a3d;
        padding: 0.5rem;
        border-radius: 4px;
        font-weight: 500;
    }
    .loser {
        background-color: #faf5f5;
        color: #6b4c4c;
        padding: 0.5rem;
        border-radius: 4px;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 2px solid #e0dcd5;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        font-weight: 500;
        color: #666;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #2c3e50;
    }
    .stButton > button {
        border-radius: 4px;
    }
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem;
    }
    div[data-testid="stMetricLabel"] {
        font-size: 0.85rem;
        color: #7f8c8d;
    }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DONNÉES DES VILLES FRANÇAISES (> 20 000 HABITANTS)
# ============================================================================

@st.cache_data
def load_villes_data():
    """Charge les données des villes françaises"""
    # Liste des villes françaises de plus de 20 000 habitants
    # Source: INSEE 2023
    villes = [
        {"ville": "Paris", "departement": "75", "population": 2161000, "superficie_km2": 105.4, "densite": 20505, "latitude": 48.8566, "longitude": 2.3522, "region": "Île-de-France"},
        {"ville": "Marseille", "departement": "13", "population": 870731, "superficie_km2": 240.6, "densite": 3619, "latitude": 43.2965, "longitude": 5.3698, "region": "Provence-Alpes-Côte d'Azur"},
        {"ville": "Lyon", "departement": "69", "population": 522969, "superficie_km2": 47.95, "densite": 10907, "latitude": 45.7640, "longitude": 4.8357, "region": "Auvergne-Rhône-Alpes"},
        {"ville": "Toulouse", "departement": "31", "population": 479553, "superficie_km2": 118.3, "densite": 4054, "latitude": 43.6047, "longitude": 1.4442, "region": "Occitanie"},
        {"ville": "Nice", "departement": "06", "population": 342669, "superficie_km2": 71.9, "densite": 4766, "latitude": 43.7102, "longitude": 7.2620, "region": "Provence-Alpes-Côte d'Azur"},
        {"ville": "Nantes", "departement": "44", "population": 318808, "superficie_km2": 65.2, "densite": 4890, "latitude": 47.2184, "longitude": -1.5536, "region": "Pays de la Loire"},
        {"ville": "Montpellier", "departement": "34", "population": 299096, "superficie_km2": 56.9, "densite": 5257, "latitude": 43.6119, "longitude": 3.8772, "region": "Occitanie"},
        {"ville": "Strasbourg", "departement": "67", "population": 291313, "superficie_km2": 78.3, "densite": 3720, "latitude": 48.5734, "longitude": 7.7521, "region": "Grand Est"},
        {"ville": "Bordeaux", "departement": "33", "population": 260958, "superficie_km2": 49.4, "densite": 5283, "latitude": 44.8378, "longitude": -0.5792, "region": "Nouvelle-Aquitaine"},
        {"ville": "Lille", "departement": "59", "population": 236710, "superficie_km2": 34.8, "densite": 6802, "latitude": 50.6292, "longitude": 3.0573, "region": "Hauts-de-France"},
        {"ville": "Rennes", "departement": "35", "population": 222485, "superficie_km2": 50.4, "densite": 4414, "latitude": 48.1173, "longitude": -1.6778, "region": "Bretagne"},
        {"ville": "Reims", "departement": "51", "population": 180752, "superficie_km2": 47.0, "densite": 3846, "latitude": 49.2583, "longitude": 4.0317, "region": "Grand Est"},
        {"ville": "Le Havre", "departement": "76", "population": 168290, "superficie_km2": 47.0, "densite": 3581, "latitude": 49.4944, "longitude": 0.1079, "region": "Normandie"},
        {"ville": "Saint-Étienne", "departement": "42", "population": 172565, "superficie_km2": 79.9, "densite": 2159, "latitude": 45.4397, "longitude": 4.3872, "region": "Auvergne-Rhône-Alpes"},
        {"ville": "Toulon", "departement": "83", "population": 176476, "superficie_km2": 42.8, "densite": 4123, "latitude": 43.1242, "longitude": 5.9280, "region": "Provence-Alpes-Côte d'Azur"},
        {"ville": "Grenoble", "departement": "38", "population": 158198, "superficie_km2": 18.1, "densite": 8740, "latitude": 45.1885, "longitude": 5.7245, "region": "Auvergne-Rhône-Alpes"},
        {"ville": "Dijon", "departement": "21", "population": 156920, "superficie_km2": 40.4, "densite": 3884, "latitude": 47.3220, "longitude": 5.0415, "region": "Bourgogne-Franche-Comté"},
        {"ville": "Angers", "departement": "49", "population": 156126, "superficie_km2": 42.0, "densite": 3717, "latitude": 47.4784, "longitude": -0.5632, "region": "Pays de la Loire"},
        {"ville": "Nîmes", "departement": "30", "population": 148104, "superficie_km2": 161.9, "densite": 915, "latitude": 43.8388, "longitude": 4.3602, "region": "Occitanie"},
        {"ville": "Clermont-Ferrand", "departement": "63", "population": 145683, "superficie_km2": 42.7, "densite": 3412, "latitude": 45.7772, "longitude": 3.0826, "region": "Auvergne-Rhône-Alpes"},
        {"ville": "Le Mans", "departement": "72", "population": 143252, "superficie_km2": 52.8, "densite": 2713, "latitude": 47.9960, "longitude": 0.1964, "region": "Pays de la Loire"},
        {"ville": "Aix-en-Provence", "departement": "13", "population": 142668, "superficie_km2": 186.2, "densite": 766, "latitude": 43.5299, "longitude": 5.4474, "region": "Provence-Alpes-Côte d'Azur"},
        {"ville": "Brest", "departement": "29", "population": 139619, "superficie_km2": 49.5, "densite": 2821, "latitude": 48.3904, "longitude": -4.4861, "region": "Bretagne"},
        {"ville": "Tours", "departement": "37", "population": 136463, "superficie_km2": 34.7, "densite": 3933, "latitude": 47.3941, "longitude": 0.6848, "region": "Centre-Val de Loire"},
        {"ville": "Amiens", "departement": "80", "population": 133891, "superficie_km2": 49.5, "densite": 2705, "latitude": 49.8942, "longitude": 2.2958, "region": "Hauts-de-France"},
        {"ville": "Limoges", "departement": "87", "population": 130588, "superficie_km2": 77.5, "densite": 1685, "latitude": 45.8517, "longitude": 1.2576, "region": "Nouvelle-Aquitaine"},
        {"ville": "Perpignan", "departement": "66", "population": 120158, "superficie_km2": 68.1, "densite": 1764, "latitude": 42.6887, "longitude": 2.8944, "region": "Occitanie"},
        {"ville": "Metz", "departement": "57", "population": 118489, "superficie_km2": 41.7, "densite": 2841, "latitude": 49.1194, "longitude": 6.1764, "region": "Grand Est"},
        {"ville": "Besançon", "departement": "25", "population": 115590, "superficie_km2": 65.0, "densite": 1778, "latitude": 47.2378, "longitude": 6.0241, "region": "Bourgogne-Franche-Comté"},
        {"ville": "Orléans", "departement": "45", "population": 116269, "superficie_km2": 27.5, "densite": 4228, "latitude": 47.9029, "longitude": 1.9093, "region": "Centre-Val de Loire"},
        {"ville": "Rouen", "departement": "76", "population": 112321, "superficie_km2": 21.4, "densite": 5249, "latitude": 49.4432, "longitude": 1.0993, "region": "Normandie"},
        {"ville": "Mulhouse", "departement": "68", "population": 108038, "superficie_km2": 22.2, "densite": 4867, "latitude": 47.7508, "longitude": 7.3359, "region": "Grand Est"},
        {"ville": "Caen", "departement": "14", "population": 105512, "superficie_km2": 25.7, "densite": 4106, "latitude": 49.1829, "longitude": -0.3707, "region": "Normandie"},
        {"ville": "Nancy", "departement": "54", "population": 103886, "superficie_km2": 15.0, "densite": 6926, "latitude": 48.6921, "longitude": 6.1844, "region": "Grand Est"},
        {"ville": "Avignon", "departement": "84", "population": 90637, "superficie_km2": 64.8, "densite": 1399, "latitude": 43.9493, "longitude": 4.8055, "region": "Provence-Alpes-Côte d'Azur"},
        {"ville": "Cannes", "departement": "06", "population": 73872, "superficie_km2": 19.6, "densite": 3770, "latitude": 43.5528, "longitude": 7.0174, "region": "Provence-Alpes-Côte d'Azur"},
        {"ville": "Antibes", "departement": "06", "population": 73702, "superficie_km2": 26.4, "densite": 2792, "latitude": 43.5804, "longitude": 7.1252, "region": "Provence-Alpes-Côte d'Azur"},
        {"ville": "Saint-Denis", "departement": "93", "population": 111607, "superficie_km2": 12.4, "densite": 9001, "latitude": 48.9356, "longitude": 2.3580, "region": "Île-de-France"},
        {"ville": "Vitry-sur-Seine", "departement": "94", "population": 95259, "superficie_km2": 11.7, "densite": 8142, "latitude": 48.7876, "longitude": 2.3919, "region": "Île-de-France"},
        {"ville": "Argenteuil", "departement": "95", "population": 106783, "superficie_km2": 16.2, "densite": 6592, "latitude": 48.9500, "longitude": 2.2484, "region": "Île-de-France"},
        {"ville": "Montreuil", "departement": "93", "population": 108402, "superficie_km2": 8.9, "densite": 12180, "latitude": 48.8615, "longitude": 2.4360, "region": "Île-de-France"},
        {"ville": "Roubaix", "departement": "59", "population": 98104, "superficie_km2": 13.2, "densite": 7435, "latitude": 50.6878, "longitude": 3.1809, "region": "Hauts-de-France"},
        {"ville": "Tourcoing", "departement": "59", "population": 97857, "superficie_km2": 15.2, "densite": 6438, "latitude": 50.7238, "longitude": 3.1606, "region": "Hauts-de-France"},
        {"ville": "Nanterre", "departement": "92", "population": 95027, "superficie_km2": 12.2, "densite": 7789, "latitude": 48.8924, "longitude": 2.2071, "region": "Île-de-France"},
        {"ville": "Créteil", "departement": "94", "population": 90728, "superficie_km2": 11.4, "densite": 7960, "latitude": 48.7771, "longitude": 2.4653, "region": "Île-de-France"},
        {"ville": "Versailles", "departement": "78", "population": 85205, "superficie_km2": 26.2, "densite": 3252, "latitude": 48.8014, "longitude": 2.1307, "region": "Île-de-France"},
        {"ville": "Pau", "departement": "64", "population": 77073, "superficie_km2": 31.5, "densite": 2447, "latitude": 43.2951, "longitude": -0.3708, "region": "Nouvelle-Aquitaine"},
        {"ville": "La Rochelle", "departement": "17", "population": 77541, "superficie_km2": 28.5, "densite": 2721, "latitude": 46.1601, "longitude": -1.1511, "region": "Nouvelle-Aquitaine"},
        {"ville": "Bayonne", "departement": "64", "population": 51794, "superficie_km2": 21.7, "densite": 2387, "latitude": 43.4929, "longitude": -1.4748, "region": "Nouvelle-Aquitaine"},
        {"ville": "Béziers", "departement": "34", "population": 78479, "superficie_km2": 95.4, "densite": 823, "latitude": 43.3448, "longitude": 3.2182, "region": "Occitanie"},
        {"ville": "Calais", "departement": "62", "population": 72701, "superficie_km2": 33.5, "densite": 2170, "latitude": 50.9513, "longitude": 1.8587, "region": "Hauts-de-France"},
        {"ville": "Cholet", "departement": "49", "population": 53573, "superficie_km2": 87.2, "densite": 615, "latitude": 47.0711, "longitude": -0.8791, "region": "Pays de la Loire"},
        {"ville": "Cergy", "departement": "95", "population": 65873, "superficie_km2": 11.7, "densite": 5632, "latitude": 49.0365, "longitude": 2.0600, "region": "Île-de-France"},
        {"ville": "Saint-Nazaire", "departement": "44", "population": 71608, "superficie_km2": 66.9, "densite": 1070, "latitude": 47.2828, "longitude": -2.2126, "region": "Pays de la Loire"},
        {"ville": "Vénissieux", "departement": "69", "population": 64719, "superficie_km2": 15.3, "densite": 4231, "latitude": 45.7021, "longitude": 4.8732, "region": "Auvergne-Rhône-Alpes"},
        {"ville": "Champigny-sur-Marne", "departement": "94", "population": 77057, "superficie_km2": 11.3, "densite": 6819, "latitude": 48.8171, "longitude": 2.5094, "region": "Île-de-France"},
    ]

    df = pd.DataFrame(villes)
    return df

# ============================================================================
# DONNÉES EMPLOI
# ============================================================================

@st.cache_data
def load_emploi_data():
    """Charge les données d'emploi des villes"""
    emploi = {
        "Paris": {"taux_chomage": 7.1, "nb_emplois": 1850000, "secteur_principal": "Services", "part_secteur_services": 85},
        "Marseille": {"taux_chomage": 11.2, "nb_emplois": 280000, "secteur_principal": "Services", "part_secteur_services": 78},
        "Lyon": {"taux_chomage": 7.8, "nb_emplois": 420000, "secteur_principal": "Services", "part_secteur_services": 82},
        "Toulouse": {"taux_chomage": 8.5, "nb_emplois": 380000, "secteur_principal": "Industrie/Tech", "part_secteur_services": 75},
        "Nice": {"taux_chomage": 9.8, "nb_emplois": 145000, "secteur_principal": "Tourisme", "part_secteur_services": 88},
        "Nantes": {"taux_chomage": 7.2, "nb_emplois": 185000, "secteur_principal": "Services", "part_secteur_services": 80},
        "Montpellier": {"taux_chomage": 10.1, "nb_emplois": 150000, "secteur_principal": "Services/Tech", "part_secteur_services": 82},
        "Strasbourg": {"taux_chomage": 8.2, "nb_emplois": 160000, "secteur_principal": "Services/Admin", "part_secteur_services": 79},
        "Bordeaux": {"taux_chomage": 7.9, "nb_emplois": 175000, "secteur_principal": "Services/Tourisme", "part_secteur_services": 81},
        "Lille": {"taux_chomage": 11.5, "nb_emplois": 190000, "secteur_principal": "Commerce", "part_secteur_services": 76},
        "Rennes": {"taux_chomage": 6.8, "nb_emplois": 145000, "secteur_principal": "Tech/Services", "part_secteur_services": 84},
        "Reims": {"taux_chomage": 9.5, "nb_emplois": 85000, "secteur_principal": "Industrie", "part_secteur_services": 68},
        "Le Havre": {"taux_chomage": 10.8, "nb_emplois": 80000, "secteur_principal": "Industrie/Port", "part_secteur_services": 65},
        "Saint-Étienne": {"taux_chomage": 9.2, "nb_emplois": 95000, "secteur_principal": "Industrie", "part_secteur_services": 70},
        "Toulon": {"taux_chomage": 10.5, "nb_emplois": 72000, "secteur_principal": "Tourisme/Militaire", "part_secteur_services": 75},
        "Grenoble": {"taux_chomage": 7.5, "nb_emplois": 115000, "secteur_principal": "Tech/Recherche", "part_secteur_services": 83},
        "Dijon": {"taux_chomage": 7.8, "nb_emplois": 78000, "secteur_principal": "Services", "part_secteur_services": 79},
        "Angers": {"taux_chomage": 8.1, "nb_emplois": 82000, "secteur_principal": "Services", "part_secteur_services": 77},
        "Nîmes": {"taux_chomage": 12.5, "nb_emplois": 68000, "secteur_principal": "Tourisme/Services", "part_secteur_services": 72},
        "Clermont-Ferrand": {"taux_chomage": 7.2, "nb_emplois": 75000, "secteur_principal": "Industrie/Recherche", "part_secteur_services": 71},
        "Le Mans": {"taux_chomage": 9.5, "nb_emplois": 68000, "secteur_principal": "Industrie", "part_secteur_services": 68},
        "Aix-en-Provence": {"taux_chomage": 8.2, "nb_emplois": 72000, "secteur_principal": "Services/Tech", "part_secteur_services": 85},
        "Brest": {"taux_chomage": 9.8, "nb_emplois": 72000, "secteur_principal": "Militaire/Recherche", "part_secteur_services": 73},
        "Tours": {"taux_chomage": 8.5, "nb_emplois": 85000, "secteur_principal": "Services", "part_secteur_services": 79},
        "Amiens": {"taux_chomage": 12.8, "nb_emplois": 72000, "secteur_principal": "Services/Commerce", "part_secteur_services": 74},
        "Limoges": {"taux_chomage": 8.9, "nb_emplois": 65000, "secteur_principal": "Industrie/Artisanat", "part_secteur_services": 66},
        "Perpignan": {"taux_chomage": 14.2, "nb_emplois": 55000, "secteur_principal": "Tourisme/Commerce", "part_secteur_services": 70},
        "Metz": {"taux_chomage": 8.5, "nb_emplois": 72000, "secteur_principal": "Services/Admin", "part_secteur_services": 78},
        "Besançon": {"taux_chomage": 7.8, "nb_emplois": 62000, "secteur_principal": "Horlogerie/Services", "part_secteur_services": 74},
        "Orléans": {"taux_chomage": 8.9, "nb_emplois": 72000, "secteur_principal": "Services/Commerce", "part_secteur_services": 80},
        "Rouen": {"taux_chomage": 9.2, "nb_emplois": 78000, "secteur_principal": "Services/Industrie", "part_secteur_services": 76},
        "Mulhouse": {"taux_chomage": 11.8, "nb_emplois": 58000, "secteur_principal": "Industrie", "part_secteur_services": 67},
        "Caen": {"taux_chomage": 8.5, "nb_emplois": 62000, "secteur_principal": "Services/Santé", "part_secteur_services": 78},
        "Nancy": {"taux_chomage": 8.2, "nb_emplois": 68000, "secteur_principal": "Services/Santé", "part_secteur_services": 81},
        "Avignon": {"taux_chomage": 11.5, "nb_emplois": 48000, "secteur_principal": "Tourisme/Tertiaire", "part_secteur_services": 82},
        "Cannes": {"taux_chomage": 9.2, "nb_emplois": 42000, "secteur_principal": "Tourisme/Culture", "part_secteur_services": 90},
        "Antibes": {"taux_chomage": 8.8, "nb_emplois": 38000, "secteur_principal": "Tourisme/Tech", "part_secteur_services": 88},
        "Saint-Denis": {"taux_chomage": 15.2, "nb_emplois": 65000, "secteur_principal": "Services/Commerce", "part_secteur_services": 85},
        "Vitry-sur-Seine": {"taux_chomage": 12.5, "nb_emplois": 32000, "secteur_principal": "Industrie/Services", "part_secteur_services": 78},
        "Argenteuil": {"taux_chomage": 13.8, "nb_emplois": 35000, "secteur_principal": "Commerce/Services", "part_secteur_services": 82},
        "Montreuil": {"taux_chomage": 12.2, "nb_emplois": 38000, "secteur_principal": "Services/Culture", "part_secteur_services": 86},
        "Roubaix": {"taux_chomage": 18.5, "nb_emplois": 38000, "secteur_principal": "Commerce/Textile", "part_secteur_services": 75},
        "Tourcoing": {"taux_chomage": 16.8, "nb_emplois": 35000, "secteur_principal": "Commerce/Textile", "part_secteur_services": 74},
        "Nanterre": {"taux_chomage": 11.5, "nb_emplois": 58000, "secteur_principal": "Services/Admin", "part_secteur_services": 88},
        "Créteil": {"taux_chomage": 12.8, "nb_emplois": 42000, "secteur_principal": "Santé/Services", "part_secteur_services": 84},
        "Versailles": {"taux_chomage": 7.5, "nb_emplois": 55000, "secteur_principal": "Admin/Services", "part_secteur_services": 88},
        "Pau": {"taux_chomage": 8.5, "nb_emplois": 45000, "secteur_principal": "Énergie/Services", "part_secteur_services": 76},
        "La Rochelle": {"taux_chomage": 8.2, "nb_emplois": 48000, "secteur_principal": "Tourisme/Services", "part_secteur_services": 82},
        "Bayonne": {"taux_chomage": 8.8, "nb_emplois": 35000, "secteur_principal": "Tourisme/Services", "part_secteur_services": 84},
        "Béziers": {"taux_chomage": 14.5, "nb_emplois": 38000, "secteur_principal": "Agriculture/Tourisme", "part_secteur_services": 68},
        "Calais": {"taux_chomage": 14.8, "nb_emplois": 35000, "secteur_principal": "Commerce/Transport", "part_secteur_services": 70},
        "Cholet": {"taux_chomage": 6.2, "nb_emplois": 32000, "secteur_principal": "Industrie/Commerce", "part_secteur_services": 65},
        "Cergy": {"taux_chomage": 10.5, "nb_emplois": 28000, "secteur_principal": "Services/Commerce", "part_secteur_services": 83},
        "Saint-Nazaire": {"taux_chomage": 10.2, "nb_emplois": 38000, "secteur_principal": "Industrie/Naval", "part_secteur_services": 62},
        "Vénissieux": {"taux_chomage": 14.5, "nb_emplois": 25000, "secteur_principal": "Industrie/Services", "part_secteur_services": 72},
        "Champigny-sur-Marne": {"taux_chomage": 13.2, "nb_emplois": 28000, "secteur_principal": "Commerce/Services", "part_secteur_services": 80},
    }

    df_list = []
    for ville, data in emploi.items():
        df_list.append({"ville": ville, **data})
    return pd.DataFrame(df_list)

# ============================================================================
# DONNÉES LOGEMENT
# ============================================================================

@st.cache_data
def load_logement_data():
    """Charge les données de logement des villes"""
    logement = {
        "Paris": {"loyer_m2": 25.5, "part_proprietaires": 33, "part_locataires": 67, "type_principal": "Appartement", "ratio_appart_maison": 85},
        "Marseille": {"loyer_m2": 14.2, "part_proprietaires": 42, "part_locataires": 58, "type_principal": "Appartement", "ratio_appart_maison": 72},
        "Lyon": {"loyer_m2": 17.8, "part_proprietaires": 38, "part_locataires": 62, "type_principal": "Appartement", "ratio_appart_maison": 78},
        "Toulouse": {"loyer_m2": 15.5, "part_proprietaires": 40, "part_locataires": 60, "type_principal": "Appartement", "ratio_appart_maison": 70},
        "Nice": {"loyer_m2": 16.2, "part_proprietaires": 45, "part_locataires": 55, "type_principal": "Appartement", "ratio_appart_maison": 75},
        "Nantes": {"loyer_m2": 14.5, "part_proprietaires": 44, "part_locataires": 56, "type_principal": "Appartement", "ratio_appart_maison": 65},
        "Montpellier": {"loyer_m2": 14.8, "part_proprietaires": 38, "part_locataires": 62, "type_principal": "Appartement", "ratio_appart_maison": 68},
        "Strasbourg": {"loyer_m2": 14.2, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 70},
        "Bordeaux": {"loyer_m2": 16.8, "part_proprietaires": 42, "part_locataires": 58, "type_principal": "Appartement", "ratio_appart_maison": 68},
        "Lille": {"loyer_m2": 14.5, "part_proprietaires": 32, "part_locataires": 68, "type_principal": "Appartement", "ratio_appart_maison": 75},
        "Rennes": {"loyer_m2": 14.2, "part_proprietaires": 40, "part_locataires": 60, "type_principal": "Appartement", "ratio_appart_maison": 62},
        "Reims": {"loyer_m2": 12.5, "part_proprietaires": 38, "part_locataires": 62, "type_principal": "Appartement", "ratio_appart_maison": 65},
        "Le Havre": {"loyer_m2": 11.8, "part_proprietaires": 48, "part_locataires": 52, "type_principal": "Appartement", "ratio_appart_maison": 68},
        "Saint-Étienne": {"loyer_m2": 10.2, "part_proprietaires": 42, "part_locataires": 58, "type_principal": "Appartement", "ratio_appart_maison": 65},
        "Toulon": {"loyer_m2": 14.5, "part_proprietaires": 50, "part_locataires": 50, "type_principal": "Appartement", "ratio_appart_maison": 62},
        "Grenoble": {"loyer_m2": 15.2, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 75},
        "Dijon": {"loyer_m2": 12.8, "part_proprietaires": 40, "part_locataires": 60, "type_principal": "Appartement", "ratio_appart_maison": 68},
        "Angers": {"loyer_m2": 12.2, "part_proprietaires": 42, "part_locataires": 58, "type_principal": "Appartement", "ratio_appart_maison": 60},
        "Nîmes": {"loyer_m2": 11.5, "part_proprietaires": 45, "part_locataires": 55, "type_principal": "Appartement", "ratio_appart_maison": 58},
        "Clermont-Ferrand": {"loyer_m2": 11.8, "part_proprietaires": 38, "part_locataires": 62, "type_principal": "Appartement", "ratio_appart_maison": 65},
        "Le Mans": {"loyer_m2": 10.8, "part_proprietaires": 48, "part_locataires": 52, "type_principal": "Maison/Apppartement", "ratio_appart_maison": 50},
        "Aix-en-Provence": {"loyer_m2": 17.2, "part_proprietaires": 48, "part_locataires": 52, "type_principal": "Appartement", "ratio_appart_maison": 65},
        "Brest": {"loyer_m2": 11.2, "part_proprietaires": 45, "part_locataires": 55, "type_principal": "Maison/Apppartement", "ratio_appart_maison": 55},
        "Tours": {"loyer_m2": 12.5, "part_proprietaires": 40, "part_locataires": 60, "type_principal": "Appartement", "ratio_appart_maison": 62},
        "Amiens": {"loyer_m2": 11.2, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 60},
        "Limoges": {"loyer_m2": 9.8, "part_proprietaires": 52, "part_locataires": 48, "type_principal": "Maison/Apppartement", "ratio_appart_maison": 48},
        "Perpignan": {"loyer_m2": 10.5, "part_proprietaires": 52, "part_locataires": 48, "type_principal": "Appartement", "ratio_appart_maison": 55},
        "Metz": {"loyer_m2": 12.2, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 68},
        "Besançon": {"loyer_m2": 11.8, "part_proprietaires": 40, "part_locataires": 60, "type_principal": "Appartement", "ratio_appart_maison": 62},
        "Orléans": {"loyer_m2": 12.5, "part_proprietaires": 38, "part_locataires": 62, "type_principal": "Appartement", "ratio_appart_maison": 60},
        "Rouen": {"loyer_m2": 13.2, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 68},
        "Mulhouse": {"loyer_m2": 10.8, "part_proprietaires": 32, "part_locataires": 68, "type_principal": "Appartement", "ratio_appart_maison": 70},
        "Caen": {"loyer_m2": 12.2, "part_proprietaires": 38, "part_locataires": 62, "type_principal": "Appartement", "ratio_appart_maison": 60},
        "Nancy": {"loyer_m2": 12.5, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 68},
        "Avignon": {"loyer_m2": 12.8, "part_proprietaires": 48, "part_locataires": 52, "type_principal": "Appartement", "ratio_appart_maison": 60},
        "Cannes": {"loyer_m2": 20.5, "part_proprietaires": 55, "part_locataires": 45, "type_principal": "Appartement", "ratio_appart_maison": 80},
        "Antibes": {"loyer_m2": 19.2, "part_proprietaires": 52, "part_locataires": 48, "type_principal": "Appartement", "ratio_appart_maison": 75},
        "Saint-Denis": {"loyer_m2": 18.5, "part_proprietaires": 28, "part_locataires": 72, "type_principal": "Appartement", "ratio_appart_maison": 88},
        "Vitry-sur-Seine": {"loyer_m2": 17.2, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 72},
        "Argenteuil": {"loyer_m2": 17.8, "part_proprietaires": 38, "part_locataires": 62, "type_principal": "Appartement", "ratio_appart_maison": 68},
        "Montreuil": {"loyer_m2": 19.5, "part_proprietaires": 32, "part_locataires": 68, "type_principal": "Appartement", "ratio_appart_maison": 78},
        "Roubaix": {"loyer_m2": 11.5, "part_proprietaires": 32, "part_locataires": 68, "type_principal": "Appartement", "ratio_appart_maison": 75},
        "Tourcoing": {"loyer_m2": 11.8, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 72},
        "Nanterre": {"loyer_m2": 18.2, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 78},
        "Créteil": {"loyer_m2": 16.5, "part_proprietaires": 38, "part_locataires": 62, "type_principal": "Appartement", "ratio_appart_maison": 72},
        "Versailles": {"loyer_m2": 22.5, "part_proprietaires": 45, "part_locataires": 55, "type_principal": "Appartement/Maison", "ratio_appart_maison": 55},
        "Pau": {"loyer_m2": 11.2, "part_proprietaires": 52, "part_locataires": 48, "type_principal": "Appartement/Maison", "ratio_appart_maison": 50},
        "La Rochelle": {"loyer_m2": 13.8, "part_proprietaires": 48, "part_locataires": 52, "type_principal": "Appartement", "ratio_appart_maison": 58},
        "Bayonne": {"loyer_m2": 13.5, "part_proprietaires": 50, "part_locataires": 50, "type_principal": "Appartement", "ratio_appart_maison": 55},
        "Béziers": {"loyer_m2": 9.8, "part_proprietaires": 55, "part_locataires": 45, "type_principal": "Maison/Apppartement", "ratio_appart_maison": 45},
        "Calais": {"loyer_m2": 10.2, "part_proprietaires": 45, "part_locataires": 55, "type_principal": "Appartement", "ratio_appart_maison": 55},
        "Cholet": {"loyer_m2": 9.8, "part_proprietaires": 58, "part_locataires": 42, "type_principal": "Maison", "ratio_appart_maison": 40},
        "Cergy": {"loyer_m2": 16.2, "part_proprietaires": 38, "part_locataires": 62, "type_principal": "Appartement", "ratio_appart_maison": 65},
        "Saint-Nazaire": {"loyer_m2": 10.5, "part_proprietaires": 52, "part_locataires": 48, "type_principal": "Maison/Apppartement", "ratio_appart_maison": 45},
        "Vénissieux": {"loyer_m2": 14.2, "part_proprietaires": 35, "part_locataires": 65, "type_principal": "Appartement", "ratio_appart_maison": 78},
        "Champigny-sur-Marne": {"loyer_m2": 17.5, "part_proprietaires": 42, "part_locataires": 58, "type_principal": "Appartement", "ratio_appart_maison": 60},
    }

    df_list = []
    for ville, data in logement.items():
        df_list.append({"ville": ville, **data})
    return pd.DataFrame(df_list)

# ============================================================================
# DONNÉES CLIMATIQUES
# ============================================================================

@st.cache_data
def load_climat_data():
    """Charge les données climatiques annuelles"""
    climat = {
        "Paris": {
            "temp_min_jan": 2.1, "temp_max_jan": 7.2, "temp_min_juil": 14.3, "temp_max_juil": 25.2,
            "ensoleillement_annuel": 1660, "precipitations_annuelles": 640, "nb_jours_pluie": 112,
            "climat": "Océanique dégradé"
        },
        "Marseille": {
            "temp_min_jan": 3.1, "temp_max_jan": 11.3, "temp_min_juil": 18.5, "temp_max_juil": 29.8,
            "ensoleillement_annuel": 2750, "precipitations_annuelles": 540, "nb_jours_pluie": 68,
            "climat": "Méditerranéen"
        },
        "Lyon": {
            "temp_min_jan": 0.3, "temp_max_jan": 6.5, "temp_min_juil": 16.2, "temp_max_juil": 27.8,
            "ensoleillement_annuel": 2010, "precipitations_annuelles": 830, "nb_jours_pluie": 105,
            "climat": "Semi-continental"
        },
        "Toulouse": {
            "temp_min_jan": 2.1, "temp_max_jan": 9.8, "temp_min_juil": 17.2, "temp_max_juil": 29.2,
            "ensoleillement_annuel": 2100, "precipitations_annuelles": 660, "nb_jours_pluie": 92,
            "climat": "Océanique altéré"
        },
        "Nice": {
            "temp_min_jan": 5.2, "temp_max_jan": 13.2, "temp_min_juil": 19.8, "temp_max_juil": 28.5,
            "ensoleillement_annuel": 2690, "precipitations_annuelles": 730, "nb_jours_pluie": 62,
            "climat": "Méditerranéen"
        },
        "Nantes": {
            "temp_min_jan": 3.2, "temp_max_jan": 9.2, "temp_min_juil": 14.8, "temp_max_juil": 24.5,
            "ensoleillement_annuel": 1935, "precipitations_annuelles": 820, "nb_jours_pluie": 135,
            "climat": "Océanique"
        },
        "Montpellier": {
            "temp_min_jan": 3.2, "temp_max_jan": 11.8, "temp_min_juil": 18.2, "temp_max_juil": 30.1,
            "ensoleillement_annuel": 2680, "precipitations_annuelles": 580, "nb_jours_pluie": 72,
            "climat": "Méditerranéen"
        },
        "Strasbourg": {
            "temp_min_jan": -1.5, "temp_max_jan": 4.2, "temp_min_juil": 14.5, "temp_max_juil": 26.2,
            "ensoleillement_annuel": 1690, "precipitations_annuelles": 620, "nb_jours_pluie": 108,
            "climat": "Semi-continental"
        },
        "Bordeaux": {
            "temp_min_jan": 2.8, "temp_max_jan": 10.5, "temp_min_juil": 16.5, "temp_max_juil": 28.2,
            "ensoleillement_annuel": 2040, "precipitations_annuelles": 900, "nb_jours_pluie": 125,
            "climat": "Océanique altéré"
        },
        "Lille": {
            "temp_min_jan": 1.2, "temp_max_jan": 5.8, "temp_min_juil": 13.2, "temp_max_juil": 23.5,
            "ensoleillement_annuel": 1620, "precipitations_annuelles": 700, "nb_jours_pluie": 128,
            "climat": "Océanique dégradé"
        },
        "Rennes": {
            "temp_min_jan": 2.5, "temp_max_jan": 8.2, "temp_min_juil": 13.5, "temp_max_juil": 24.2,
            "ensoleillement_annuel": 1850, "precipitations_annuelles": 720, "nb_jours_pluie": 122,
            "climat": "Océanique"
        },
        "Reims": {
            "temp_min_jan": -0.2, "temp_max_jan": 5.8, "temp_min_juil": 13.8, "temp_max_juil": 25.8,
            "ensoleillement_annuel": 1700, "precipitations_annuelles": 580, "nb_jours_pluie": 105,
            "climat": "Semi-continental"
        },
        "Le Havre": {
            "temp_min_jan": 2.8, "temp_max_jan": 7.2, "temp_min_juil": 14.2, "temp_max_juil": 21.2,
            "ensoleillement_annuel": 1780, "precipitations_annuelles": 800, "nb_jours_pluie": 138,
            "climat": "Océanique"
        },
        "Saint-Étienne": {
            "temp_min_jan": -0.2, "temp_max_jan": 6.2, "temp_min_juil": 14.8, "temp_max_juil": 26.5,
            "ensoleillement_annuel": 1950, "precipitations_annuelles": 720, "nb_jours_pluie": 100,
            "climat": "Semi-continental"
        },
        "Toulon": {
            "temp_min_jan": 5.5, "temp_max_jan": 13.5, "temp_min_juil": 19.5, "temp_max_juil": 29.2,
            "ensoleillement_annuel": 2850, "precipitations_annuelles": 600, "nb_jours_pluie": 58,
            "climat": "Méditerranéen"
        },
        "Grenoble": {
            "temp_min_jan": -0.5, "temp_max_jan": 5.8, "temp_min_juil": 15.2, "temp_max_juil": 27.5,
            "ensoleillement_annuel": 2080, "precipitations_annuelles": 920, "nb_jours_pluie": 108,
            "climat": "Semi-continental"
        },
        "Dijon": {
            "temp_min_jan": -0.2, "temp_max_jan": 5.5, "temp_min_juil": 14.5, "temp_max_juil": 26.5,
            "ensoleillement_annuel": 1850, "precipitations_annuelles": 780, "nb_jours_pluie": 112,
            "climat": "Semi-continental"
        },
        "Angers": {
            "temp_min_jan": 2.5, "temp_max_jan": 8.5, "temp_min_juil": 14.2, "temp_max_juil": 25.5,
            "ensoleillement_annuel": 1900, "precipitations_annuelles": 680, "nb_jours_pluie": 118,
            "climat": "Océanique"
        },
        "Nîmes": {
            "temp_min_jan": 2.5, "temp_max_jan": 11.2, "temp_min_juil": 18.5, "temp_max_juil": 31.2,
            "ensoleillement_annuel": 2650, "precipitations_annuelles": 580, "nb_jours_pluie": 75,
            "climat": "Méditerranéen"
        },
        "Clermont-Ferrand": {
            "temp_min_jan": 0.2, "temp_max_jan": 6.8, "temp_min_juil": 15.2, "temp_max_juil": 27.2,
            "ensoleillement_annuel": 1980, "precipitations_annuelles": 780, "nb_jours_pluie": 105,
            "climat": "Semi-continental"
        },
        "Le Mans": {
            "temp_min_jan": 2.2, "temp_max_jan": 8.2, "temp_min_juil": 14.2, "temp_max_juil": 25.2,
            "ensoleillement_annuel": 1800, "precipitations_annuelles": 720, "nb_jours_pluie": 122,
            "climat": "Océanique dégradé"
        },
        "Aix-en-Provence": {
            "temp_min_jan": 2.8, "temp_max_jan": 11.5, "temp_min_juil": 17.8, "temp_max_juil": 30.2,
            "ensoleillement_annuel": 2800, "precipitations_annuelles": 520, "nb_jours_pluie": 65,
            "climat": "Méditerranéen"
        },
        "Brest": {
            "temp_min_jan": 4.2, "temp_max_jan": 9.2, "temp_min_juil": 13.5, "temp_max_juil": 20.5,
            "ensoleillement_annuel": 1680, "precipitations_annuelles": 1200, "nb_jours_pluie": 155,
            "climat": "Océanique"
        },
        "Tours": {
            "temp_min_jan": 2.2, "temp_max_jan": 8.2, "temp_min_juil": 14.5, "temp_max_juil": 25.8,
            "ensoleillement_annuel": 1850, "precipitations_annuelles": 680, "nb_jours_pluie": 115,
            "climat": "Océanique dégradé"
        },
        "Amiens": {
            "temp_min_jan": 1.2, "temp_max_jan": 6.2, "temp_min_juil": 13.5, "temp_max_juil": 24.2,
            "ensoleillement_annuel": 1680, "precipitations_annuelles": 650, "nb_jours_pluie": 118,
            "climat": "Océanique dégradé"
        },
        "Limoges": {
            "temp_min_jan": 1.2, "temp_max_jan": 7.2, "temp_min_juil": 14.2, "temp_max_juil": 25.5,
            "ensoleillement_annuel": 1880, "precipitations_annuelles": 1020, "nb_jours_pluie": 130,
            "climat": "Semi-continental"
        },
        "Perpignan": {
            "temp_min_jan": 4.5, "temp_max_jan": 13.2, "temp_min_juil": 19.2, "temp_max_juil": 29.8,
            "ensoleillement_annuel": 2480, "precipitations_annuelles": 580, "nb_jours_pluie": 72,
            "climat": "Méditerranéen"
        },
        "Metz": {
            "temp_min_jan": -0.8, "temp_max_jan": 4.5, "temp_min_juil": 14.5, "temp_max_juil": 25.8,
            "ensoleillement_annuel": 1650, "precipitations_annuelles": 700, "nb_jours_pluie": 115,
            "climat": "Semi-continental"
        },
        "Besançon": {
            "temp_min_jan": -0.2, "temp_max_jan": 5.2, "temp_min_juil": 14.8, "temp_max_juil": 26.2,
            "ensoleillement_annuel": 1780, "precipitations_annuelles": 1100, "nb_jours_pluie": 130,
            "climat": "Semi-continental"
        },
        "Orléans": {
            "temp_min_jan": 1.5, "temp_max_jan": 7.2, "temp_min_juil": 14.2, "temp_max_juil": 25.5,
            "ensoleillement_annuel": 1800, "precipitations_annuelles": 620, "nb_jours_pluie": 108,
            "climat": "Océanique dégradé"
        },
        "Rouen": {
            "temp_min_jan": 1.8, "temp_max_jan": 6.8, "temp_min_juil": 13.5, "temp_max_juil": 23.5,
            "ensoleillement_annuel": 1720, "precipitations_annuelles": 780, "nb_jours_pluie": 128,
            "climat": "Océanique dégradé"
        },
        "Mulhouse": {
            "temp_min_jan": -1.2, "temp_max_jan": 4.5, "temp_min_juil": 14.8, "temp_max_juil": 26.5,
            "ensoleillement_annuel": 1630, "precipitations_annuelles": 880, "nb_jours_pluie": 120,
            "climat": "Semi-continental"
        },
        "Caen": {
            "temp_min_jan": 2.5, "temp_max_jan": 7.5, "temp_min_juil": 13.8, "temp_max_juil": 22.5,
            "ensoleillement_annuel": 1750, "precipitations_annuelles": 750, "nb_jours_pluie": 125,
            "climat": "Océanique"
        },
        "Nancy": {
            "temp_min_jan": -0.8, "temp_max_jan": 4.5, "temp_min_juil": 14.8, "temp_max_juil": 25.5,
            "ensoleillement_annuel": 1680, "precipitations_annuelles": 780, "nb_jours_pluie": 118,
            "climat": "Semi-continental"
        },
        "Avignon": {
            "temp_min_jan": 2.8, "temp_max_jan": 11.5, "temp_min_juil": 18.2, "temp_max_juil": 31.5,
            "ensoleillement_annuel": 2800, "precipitations_annuelles": 660, "nb_jours_pluie": 68,
            "climat": "Méditerranéen"
        },
        "Cannes": {
            "temp_min_jan": 5.8, "temp_max_jan": 13.8, "temp_min_juil": 20.2, "temp_max_juil": 29.2,
            "ensoleillement_annuel": 2740, "precipitations_annuelles": 800, "nb_jours_pluie": 58,
            "climat": "Méditerranéen"
        },
        "Antibes": {
            "temp_min_jan": 5.5, "temp_max_jan": 13.5, "temp_min_juil": 19.8, "temp_max_juil": 28.8,
            "ensoleillement_annuel": 2760, "precipitations_annuelles": 750, "nb_jours_pluie": 60,
            "climat": "Méditerranéen"
        },
        "Saint-Denis": {
            "temp_min_jan": 2.5, "temp_max_jan": 7.2, "temp_min_juil": 14.5, "temp_max_juil": 25.2,
            "ensoleillement_annuel": 1650, "precipitations_annuelles": 640, "nb_jours_pluie": 112,
            "climat": "Océanique dégradé"
        },
        "Vitry-sur-Seine": {
            "temp_min_jan": 2.2, "temp_max_jan": 7.5, "temp_min_juil": 14.8, "temp_max_juil": 25.8,
            "ensoleillement_annuel": 1680, "precipitations_annuelles": 620, "nb_jours_pluie": 108,
            "climat": "Océanique dégradé"
        },
        "Argenteuil": {
            "temp_min_jan": 2.2, "temp_max_jan": 7.2, "temp_min_juil": 14.5, "temp_max_juil": 25.2,
            "ensoleillement_annuel": 1660, "precipitations_annuelles": 640, "nb_jours_pluie": 110,
            "climat": "Océanique dégradé"
        },
        "Montreuil": {
            "temp_min_jan": 2.5, "temp_max_jan": 7.5, "temp_min_juil": 14.8, "temp_max_juil": 25.5,
            "ensoleillement_annuel": 1680, "precipitations_annuelles": 620, "nb_jours_pluie": 108,
            "climat": "Océanique dégradé"
        },
        "Roubaix": {
            "temp_min_jan": 1.5, "temp_max_jan": 6.2, "temp_min_juil": 13.5, "temp_max_juil": 23.2,
            "ensoleillement_annuel": 1600, "precipitations_annuelles": 720, "nb_jours_pluie": 130,
            "climat": "Océanique dégradé"
        },
        "Tourcoing": {
            "temp_min_jan": 1.5, "temp_max_jan": 6.2, "temp_min_juil": 13.5, "temp_max_juil": 23.2,
            "ensoleillement_annuel": 1600, "precipitations_annuelles": 720, "nb_jours_pluie": 130,
            "climat": "Océanique dégradé"
        },
        "Nanterre": {
            "temp_min_jan": 2.2, "temp_max_jan": 7.2, "temp_min_juil": 14.5, "temp_max_juil": 25.2,
            "ensoleillement_annuel": 1660, "precipitations_annuelles": 640, "nb_jours_pluie": 110,
            "climat": "Océanique dégradé"
        },
        "Créteil": {
            "temp_min_jan": 2.5, "temp_max_jan": 7.5, "temp_min_juil": 14.8, "temp_max_juil": 25.5,
            "ensoleillement_annuel": 1680, "precipitations_annuelles": 620, "nb_jours_pluie": 108,
            "climat": "Océanique dégradé"
        },
        "Versailles": {
            "temp_min_jan": 1.8, "temp_max_jan": 6.8, "temp_min_juil": 14.2, "temp_max_juil": 24.8,
            "ensoleillement_annuel": 1650, "precipitations_annuelles": 650, "nb_jours_pluie": 112,
            "climat": "Océanique dégradé"
        },
        "Pau": {
            "temp_min_jan": 2.5, "temp_max_jan": 10.2, "temp_min_juil": 16.2, "temp_max_juil": 27.2,
            "ensoleillement_annuel": 1950, "precipitations_annuelles": 1080, "nb_jours_pluie": 118,
            "climat": "Océanique altéré"
        },
        "La Rochelle": {
            "temp_min_jan": 4.2, "temp_max_jan": 9.5, "temp_min_juil": 16.2, "temp_max_juil": 24.5,
            "ensoleillement_annuel": 2100, "precipitations_annuelles": 750, "nb_jours_pluie": 110,
            "climat": "Océanique"
        },
        "Bayonne": {
            "temp_min_jan": 4.8, "temp_max_jan": 11.2, "temp_min_juil": 17.2, "temp_max_juil": 25.5,
            "ensoleillement_annuel": 1880, "precipitations_annuelles": 1450, "nb_jours_pluie": 145,
            "climat": "Océanique"
        },
        "Béziers": {
            "temp_min_jan": 3.5, "temp_max_jan": 12.2, "temp_min_juil": 18.8, "temp_max_juil": 30.5,
            "ensoleillement_annuel": 2480, "precipitations_annuelles": 520, "nb_jours_pluie": 70,
            "climat": "Méditerranéen"
        },
        "Calais": {
            "temp_min_jan": 2.5, "temp_max_jan": 7.2, "temp_min_juil": 13.8, "temp_max_juil": 21.5,
            "ensoleillement_annuel": 1700, "precipitations_annuelles": 780, "nb_jours_pluie": 135,
            "climat": "Océanique"
        },
        "Cholet": {
            "temp_min_jan": 2.5, "temp_max_jan": 8.5, "temp_min_juil": 14.5, "temp_max_juil": 25.2,
            "ensoleillement_annuel": 1850, "precipitations_annuelles": 720, "nb_jours_pluie": 120,
            "climat": "Océanique dégradé"
        },
        "Cergy": {
            "temp_min_jan": 2.2, "temp_max_jan": 7.2, "temp_min_juil": 14.5, "temp_max_juil": 25.2,
            "ensoleillement_annuel": 1660, "precipitations_annuelles": 640, "nb_jours_pluie": 110,
            "climat": "Océanique dégradé"
        },
        "Saint-Nazaire": {
            "temp_min_jan": 3.8, "temp_max_jan": 9.2, "temp_min_juil": 15.2, "temp_max_juil": 23.5,
            "ensoleillement_annuel": 1920, "precipitations_annuelles": 800, "nb_jours_pluie": 130,
            "climat": "Océanique"
        },
        "Vénissieux": {
            "temp_min_jan": 0.5, "temp_max_jan": 6.5, "temp_min_juil": 16.2, "temp_max_juil": 27.8,
            "ensoleillement_annuel": 2000, "precipitations_annuelles": 820, "nb_jours_pluie": 102,
            "climat": "Semi-continental"
        },
        "Champigny-sur-Marne": {
            "temp_min_jan": 2.5, "temp_max_jan": 7.5, "temp_min_juil": 14.8, "temp_max_juil": 25.5,
            "ensoleillement_annuel": 1680, "precipitations_annuelles": 620, "nb_jours_pluie": 108,
            "climat": "Océanique dégradé"
        },
    }

    df_list = []
    for ville, data in climat.items():
        df_list.append({"ville": ville, **data})
    return pd.DataFrame(df_list)

# ============================================================================
# FONCTIONS API MÉTÉO (Open-Meteo - gratuit, sans clé API)
# ============================================================================

@st.cache_data(ttl=3600)
def get_previsions_7_jours(lat, lon):
    """Récupère les prévisions à 7 jours via Open-Meteo API"""
    try:
        url = f"https://api.open-meteo.com/v1/forecast?latitude={lat}&longitude={lon}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum,precipitation_probability_max,wind_speed_10m_max&timezone=Europe/Paris&forecast_days=7"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        return None
    except Exception as e:
        st.error(f"Erreur lors de la récupération des prévisions: {e}")
        return None

def code_meteo_to_description(code):
    """Convertit le code météo WMO en description française"""
    codes = {
        0: "Ciel dégagé", 1: "Mainly clear", 2: "Partly cloudy", 3: "Overcast",
        45: "Brouillard", 48: "Brouillard givrant",
        51: "Bruine légère", 53: "Bruine modérée", 55: "Bruine dense",
        61: "Pluie légère", 63: "Pluie modérée", 65: "Pluie forte",
        71: "Neige légère", 73: "Neige modérée", 75: "Neige forte",
        80: "Averses légères", 81: "Averses modérées", 82: "Averses violentes",
        95: "Orage", 96: "Orage avec grêle", 99: "Orage violent"
    }
    return codes.get(code, f"Code {code}")

# ============================================================================
# INTERFACE PRINCIPALE
# ============================================================================

def main():
    st.markdown('<h1 class="main-header">Comparateur de Villes Françaises</h1>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Comparez deux villes françaises sur le coût de la vie, l\'emploi, le logement et le climat</p>', unsafe_allow_html=True)

    villes_df = load_villes_data()
    emploi_df = load_emploi_data()
    logement_df = load_logement_data()
    climat_df = load_climat_data()

    st.sidebar.header("Sélection des villes")
    st.sidebar.markdown("---")

    liste_villes = sorted(villes_df['ville'].tolist())

    ville1 = st.sidebar.selectbox(
        "Première ville", liste_villes,
        index=liste_villes.index("Paris") if "Paris" in liste_villes else 0
    )
    ville2 = st.sidebar.selectbox(
        "Deuxième ville", liste_villes,
        index=liste_villes.index("Lyon") if "Lyon" in liste_villes else 1
    )

    st.sidebar.markdown("---")
    st.sidebar.info("**Sources :**\n- INSEE (population)\n- Open-Meteo (météo)\n- Données 2023")

    v1_data = villes_df[villes_df['ville'] == ville1].iloc[0]
    v2_data = villes_df[villes_df['ville'] == ville2].iloc[0]

    col1, col2 = st.columns(2)
    with col1:
        st.markdown(f"""
        <div class="city-card">
            <h2>{ville1}</h2>
            <p>{v1_data['region']}</p>
            <p style="font-size: 2rem; margin: 10px 0;">{v1_data['population']:,}</p>
            <p>habitants</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="city-card" style="background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);">
            <h2>{ville2}</h2>
            <p>{v2_data['region']}</p>
            <p style="font-size: 2rem; margin: 10px 0;">{v2_data['population']:,}</p>
            <p>habitants</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    tabs = st.tabs(["Vue d'ensemble", "Données générales", "Emploi", "Logement", "Climat", "Météo forecast"])

    # Données pour les villes
    v1_emploi = emploi_df[emploi_df['ville'] == ville1].iloc[0] if len(emploi_df[emploi_df['ville'] == ville1]) > 0 else None
    v2_emploi = emploi_df[emploi_df['ville'] == ville2].iloc[0] if len(emploi_df[emploi_df['ville'] == ville2]) > 0 else None
    v1_logement = logement_df[logement_df['ville'] == ville1].iloc[0] if len(logement_df[logement_df['ville'] == ville1]) > 0 else None
    v2_logement = logement_df[logement_df['ville'] == ville2].iloc[0] if len(logement_df[logement_df['ville'] == ville2]) > 0 else None
    v1_climat = climat_df[climat_df['ville'] == ville1].iloc[0] if len(climat_df[climat_df['ville'] == ville1]) > 0 else None
    v2_climat = climat_df[climat_df['ville'] == ville2].iloc[0] if len(climat_df[climat_df['ville'] == ville2]) > 0 else None

    # ONGLET 1: Vue d'ensemble
    with tabs[0]:
        st.subheader("Résumé comparatif")
        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Population", f"{v1_data['population']:,}")
        with col2:
            if v1_emploi is not None and v2_emploi is not None:
                chomage_diff = v1_emploi['taux_chomage'] - v2_emploi['taux_chomage']
                st.metric("Taux de chômage", f"{v1_emploi['taux_chomage']}%", delta=f"{chomage_diff:.1f}%")
        with col3:
            if v1_logement is not None and v2_logement is not None:
                st.metric("Loyer €/m²", f"{v1_logement['loyer_m2']}")
        with col4:
            st.metric("Densité", f"{v1_data['densite']:,}/km²")

    # ONGLET 2: Données générales
    with tabs[1]:
        st.subheader("Données générales")
        comparaison = pd.DataFrame({
            'Indicateur': ['Population', 'Superficie (km²)', 'Densité (hab/km²)', 'Région', 'Département'],
            ville1: [f"{v1_data['population']:,}", f"{v1_data['superficie_km2']:.1f}", f"{v1_data['densite']:,}", v1_data['region'], v1_data['departement']],
            ville2: [f"{v2_data['population']:,}", f"{v2_data['superficie_km2']:.1f}", f"{v2_data['densite']:,}", v2_data['region'], v2_data['departement']]
        })
        st.table(comparaison)

        col1, col2 = st.columns(2)
        with col1:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=[ville1, ville2], y=[v1_data['population'], v2_data['population']], marker_color=['#5d7a8c', '#a67c5b'], text=[f"{v1_data['population']:,}", f"{v2_data['population']:,}"], textposition='outside'))
            fig.update_layout(title="Population", showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)
        with col2:
            fig = go.Figure()
            fig.add_trace(go.Bar(x=[ville1, ville2], y=[v1_data['densite'], v2_data['densite']], marker_color=['#5d7a8c', '#a67c5b'], text=[f"{v1_data['densite']:,}", f"{v2_data['densite']:,}"], textposition='outside'))
            fig.update_layout(title="Densité (hab/km²)", showlegend=False, height=300)
            st.plotly_chart(fig, use_container_width=True)

        st.download_button("Télécharger les données", comparaison.to_csv(index=False), f"donnees_{ville1}_{ville2}.csv", "text/csv")

    # ONGLET 3: Emploi
    with tabs[2]:
        st.subheader("Données emploi")
        if v1_emploi is not None and v2_emploi is not None:
            comparaison_emploi = pd.DataFrame({
                'Indicateur': ['Taux de chômage (%)', "Nombre d'emplois", 'Secteur principal', 'Part services (%)'],
                ville1: [f"{v1_emploi['taux_chomage']}%", f"{v1_emploi['nb_emplois']:,}", v1_emploi['secteur_principal'], f"{v1_emploi['part_secteur_services']}%"],
                ville2: [f"{v2_emploi['taux_chomage']}%", f"{v2_emploi['nb_emplois']:,}", v2_emploi['secteur_principal'], f"{v2_emploi['part_secteur_services']}%"]
            })
            st.table(comparaison_emploi)
            winner = ville1 if v1_emploi['taux_chomage'] < v2_emploi['taux_chomage'] else ville2
            st.markdown(f"**{winner}** a le meilleur taux de chômage", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=[ville1, ville2], y=[v1_emploi['taux_chomage'], v2_emploi['taux_chomage']], marker_color=['#5d7a8c', '#a67c5b'], text=[f"{v1_emploi['taux_chomage']}%", f"{v2_emploi['taux_chomage']}%"], textposition='outside'))
                fig.update_layout(title="Taux de chômage (%)", showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=[ville1, ville2], y=[v1_emploi['nb_emplois'], v2_emploi['nb_emplois']], marker_color=['#5d7a8c', '#a67c5b'], text=[f"{v1_emploi['nb_emplois']:,}", f"{v2_emploi['nb_emplois']:,}"], textposition='outside'))
                fig.update_layout(title="Nombre d'emplois", showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)

            st.download_button("Télécharger", comparaison_emploi.to_csv(index=False), f"emploi_{ville1}_{ville2}.csv", "text/csv")

    # ONGLET 4: Logement
    with tabs[3]:
        st.subheader("Données logement")
        if v1_logement is not None and v2_logement is not None:
            comparaison_logement = pd.DataFrame({
                'Indicateur': ['Loyer moyen (€/m²)', 'Part propriétaires (%)', 'Part locataires (%)', 'Type principal'],
                ville1: [f"{v1_logement['loyer_m2']}€", f"{v1_logement['part_proprietaires']}%", f"{v1_logement['part_locataires']}%", v1_logement['type_principal']],
                ville2: [f"{v2_logement['loyer_m2']}€", f"{v2_logement['part_proprietaires']}%", f"{v2_logement['part_locataires']}%", v2_logement['type_principal']]
            })
            st.table(comparaison_logement)
            winner = ville1 if v1_logement['loyer_m2'] < v2_logement['loyer_m2'] else ville2
            st.markdown(f"**{winner}** a les loyers les plus bas", unsafe_allow_html=True)

            col1, col2 = st.columns(2)
            with col1:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=[ville1, ville2], y=[v1_logement['loyer_m2'], v2_logement['loyer_m2']], marker_color=['#5d7a8c', '#a67c5b'], text=[f"{v1_logement['loyer_m2']}€", f"{v2_logement['loyer_m2']}€"], textposition='outside'))
                fig.update_layout(title="Loyer moyen (€/m²)", showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)
            with col2:
                fig = go.Figure()
                fig.add_trace(go.Bar(x=[ville1, ville2], y=[v1_logement['part_proprietaires'], v2_logement['part_proprietaires']], marker_color=['#5d7a8c', '#a67c5b'], text=[f"{v1_logement['part_proprietaires']}%", f"{v2_logement['part_proprietaires']}%"], textposition='outside'))
                fig.update_layout(title="Part de propriétaires (%)", showlegend=False, height=300)
                st.plotly_chart(fig, use_container_width=True)

            st.download_button("Télécharger", comparaison_logement.to_csv(index=False), f"logement_{ville1}_{ville2}.csv", "text/csv")

    # ONGLET 5: Climat
    with tabs[4]:
        st.subheader("Données climatiques annuelles")
        if v1_climat is not None and v2_climat is not None:
            comparaison_climat = pd.DataFrame({
                'Indicateur': ['Type de climat', 'T° min jan (°C)', 'T° max jan (°C)', 'T° min juil (°C)', 'T° max juil (°C)', 'Ensoleillement (h/an)', 'Précipitations (mm/an)'],
                ville1: [v1_climat['climat'], f"{v1_climat['temp_min_jan']}°C", f"{v1_climat['temp_max_jan']}°C", f"{v1_climat['temp_min_juil']}°C", f"{v1_climat['temp_max_juil']}°C", f"{v1_climat['ensoleillement_annuel']}h", f"{v1_climat['precipitations_annuelles']}mm"],
                ville2: [v2_climat['climat'], f"{v2_climat['temp_min_jan']}°C", f"{v2_climat['temp_max_jan']}°C", f"{v2_climat['temp_min_juil']}°C", f"{v2_climat['temp_max_juil']}°C", f"{v2_climat['ensoleillement_annuel']}h", f"{v2_climat['precipitations_annuelles']}mm"]
            })
            st.table(comparaison_climat)

            fig = make_subplots(rows=1, cols=2, subplot_titles=['Ensoleillement (h/an)', 'Précipitations (mm/an)'])
            fig.add_trace(go.Bar(x=[ville1, ville2], y=[v1_climat['ensoleillement_annuel'], v2_climat['ensoleillement_annuel']], marker_color=['#5d7a8c', '#a67c5b']), row=1, col=1)
            fig.add_trace(go.Bar(x=[ville1, ville2], y=[v1_climat['precipitations_annuelles'], v2_climat['precipitations_annuelles']], marker_color=['#5d7a8c', '#a67c5b']), row=1, col=2)
            fig.update_layout(height=300, showlegend=False)
            st.plotly_chart(fig, use_container_width=True)

            st.download_button("Télécharger", comparaison_climat.to_csv(index=False), f"climat_{ville1}_{ville2}.csv", "text/csv")

    # ONGLET 6: Météo forecast
    with tabs[5]:
        st.subheader("Météo des 7 prochains jours (temps réel)")
        if st.button("Actualiser"):
            st.rerun()

        meteo1 = get_previsions_7_jours(v1_data['latitude'], v1_data['longitude'])
        meteo2 = get_previsions_7_jours(v2_data['latitude'], v2_data['longitude'])

        if meteo1 and meteo2:
            dates = meteo1['daily']['time']
            df_meteo1 = pd.DataFrame({
                'Date': pd.to_datetime(dates).strftime('%d/%m'),
                'Temps': [code_meteo_to_description(c) for c in meteo1['daily']['weather_code']],
                'T° min': meteo1['daily']['temperature_2m_min'],
                'T° max': meteo1['daily']['temperature_2m_max'],
                'Précip. (mm)': meteo1['daily']['precipitation_sum']
            })
            df_meteo2 = pd.DataFrame({
                'Date': pd.to_datetime(dates).strftime('%d/%m'),
                'Temps': [code_meteo_to_description(c) for c in meteo2['daily']['weather_code']],
                'T° min': meteo2['daily']['temperature_2m_min'],
                'T° max': meteo2['daily']['temperature_2m_max'],
                'Précip. (mm)': meteo2['daily']['precipitation_sum']
            })

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"#### {ville1}")
                st.table(df_meteo1)
            with col2:
                st.markdown(f"#### {ville2}")
                st.table(df_meteo2)

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=df_meteo1['Date'], y=df_meteo1['T° max'], name=f'{ville1} T° max', line=dict(color='#5d7a8c', width=2), mode='lines+markers'))
            fig.add_trace(go.Scatter(x=df_meteo1['Date'], y=df_meteo1['T° min'], name=f'{ville1} T° min', line=dict(color='#8fa4ad', width=2), mode='lines+markers'))
            fig.add_trace(go.Scatter(x=df_meteo2['Date'], y=df_meteo2['T° max'], name=f'{ville2} T° max', line=dict(color='#a67c5b', width=2, dash='dash'), mode='lines+markers'))
            fig.add_trace(go.Scatter(x=df_meteo2['Date'], y=df_meteo2['T° min'], name=f'{ville2} T° min', line=dict(color='#c9a87c', width=2, dash='dash'), mode='lines+markers'))
            fig.update_layout(xaxis_title="Date", yaxis_title="Température (°C)", height=400)
            st.plotly_chart(fig, use_container_width=True)
            st.caption("Données : Open-Meteo")

    st.markdown("---")
    st.markdown("**Comparateur de Villes Françaises** | SAE Outils Décisionnels")

if __name__ == "__main__":
    main()
