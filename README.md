# Comparateur de Villes Francaises

Application web interactive permettant de comparer deux villes francaises sur plusieurs dimensions : population, revenus, logement, qualite de vie, meteo et scores globalises. Concue pour aider les etudiants a choisir leur ville d'etudes pour un master.

**Auteurs** : Matteo Cai, William Lefebvre, Terryl Hassen  
**Cours** : SAE Outils Decisionnels — IUT de Paris, BUT Sciences des Donnees

---

## Acces en ligne

L'application est deployee sur Streamlit Cloud et accessible publiquement :

> **https://comparateurvillemaster2026.streamlit.app/**

Aucune installation n'est necessaire pour consulter l'application en ligne.

---

## Fonctionnalites

| Onglet | Contenu |
|---|---|
| **Vision globale** | Population, % etudiants, age moyen, salaire, chomage, alternance, secteurs d'activite, loyer |
| **Qualite de vie** | Ensoleillement, qualite de l'air, securite, lieux culturels, restaurants et bars |
| **Scores** | Classement normalise (0-100) sur 7 indicateurs avec radar chart |
| **Meteo** | Climat annuel (moyennes mensuelles 2020-2024) + previsions 7 jours |

Chaque ville affiche une photo issue de Wikipedia et des indicateurs sous forme de cartes.

---

## Structure du projet

```
villes_francaises/
├── Accueil.py                              # Page d'accueil
├── pages/
│   ├── 0_Comparateur_villes.py              # Application principale
│   ├── 1_A_propos.py                        # Presentation du projet
│   └── 2_Sources.py                         # Sources des donnees
├── data/
│   ├── communes_20k_2023_v2.csv             # Liste des 483 communes > 20k hab.
│   ├── communes_20k_2023_nb_etudiants_24.csv
│   ├── communes_20k_2023_nb_alternance_26.csv
│   ├── communes_20k_avec_age_moyen_2025_final.csv
│   ├── communes_20k_salaires_final.csv
│   ├── communes_20k_avec_chomage_final.csv
│   ├── communes_20k_avec_secteurs_activites_2025_final.csv
│   ├── communes_20k_avec_score_securite_2025_final.csv
│   ├── communes_20k_avec_lieux_culturel_2025_final.csv
│   ├── communes_20k_avec_bar_restaurants_final.csv
│   ├── restaurants_bars_filtre_communes.csv
│   ├── loyers_t1t2_2025.csv                 # Carte des loyers (ANIL)
│   ├── ensoleillement.csv                   # Open-Meteo ERA5
│   ├── aqi.csv                              # Qualite de l'air (WAQI)
│   └── url_cities_final.csv                 # Photos Wikipedia
├── src/
│   └── UniversiteParis_IUTParis-RdS.png     # Logo IUT
├── scripts/
│   └── import_donnees.py
├── requirements.txt
├── README.md
├── DEPLOY.md
├── MODE_D_EMPLOI.md
└── RAPPORT.md
```

---

## Installation locale

### Prerequis

- Python 3.11 ou superieur
- pip

### Etapes

```bash
# 1. Cloner le depot
git clone https://github.com/BUT-SD-PROJECT-hanmlx/Comparateur_ville_master2026.git
cd Comparateur_ville_master2026/villes_francaises

# 2. Creer un environnement virtuel (recommande)
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# 3. Installer les dependances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run Accueil.py
```

L'application s'ouvre automatiquement dans le navigateur a l'adresse `http://localhost:8501`.

---

## Deploiement sur Streamlit Cloud

L'application est deja deployee. Pour redeployer ou deployer une autre instance :

1. **Creer un compte** sur [streamlit.io](https://streamlit.io)
2. **Pousser le projet** sur un depot GitHub public
3. Depuis le dashboard Streamlit Cloud, cliquer sur **New App**
4. Selectionner le depot et specifier `Accueil.py` comme fichier principal
5. Cliquer sur **Deploy**

> **Note** : le fichier `requirements.txt` a la racine du dossier `villes_francaises/` doit etre present pour que Streamlit Cloud installe les dependances automatiquement.

---

## Sources des donnees

| Donnees | Source |
|---|---|
| Communes et population | INSEE, Recensement 2021 |
| Etudiants | INSEE, Recensement 2024 |
| Alternance | Data.gouv.fr, 2026 |
| Salaires | INSEE, Base Tous salaries 2023 |
| Chomage | INSEE, Taux departementaux 2024 |
| Secteurs d'activite | INSEE / Data.gouv.fr, 2025 |
| Loyers | ANIL, Carte des loyers 2025 |
| Ensoleillement | Open-Meteo Archive API (ERA5, 2020-2024) |
| Qualite de l'air | World Air Quality Index (WAQI) |
| Securite | Score compile 2025 |
| Lieux culturels | INSEE / Data.gouv.fr, 2025 |
| Restaurants et bars | INSEE / Data.gouv.fr |
| Photos de villes | Wikipedia API (FR) |
| Meteo | Open-Meteo Forecast API |

---

## Licence

Projet academique realise dans le cadre du BUT Sciences des Donnees, IUT de Paris — Universite Paris Cite. Usage pedagogique uniquement.
