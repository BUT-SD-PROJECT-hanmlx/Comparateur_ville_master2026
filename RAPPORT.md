# Rapport - SAE Outils Decisionnels
## Comparateur de Villes Francaises

**Auteurs :** [Noms des etudiants du groupe - Maximum 3 etudiants]

**Date :** [Date de rendu]

---

## 1. PRESENTATION DE L'INTERFACE

### 1.1 Description generale

L'application **Comparateur de Villes Francaises** est une interface web permettant de comparer deux villes francaises sur differents criteres :

- Donnees generales (population, superficie, densite)
- Emploi (taux de chomage, nombre d'emplois, secteurs)
- Logement (loyers, part de proprietaires, type d'habitat)
- Climat (temperature, ensolleillement, precipitations)
- Meteo forecast (previsions 7 jours en temps reel)

### 1.2 Adresse web de l'interface

**Application deployee sur :** https://[votre-compte].streamlit.app/

*(Remplacer par l'URL reelle apres deploiement)*

### 1.3 Fonctionnalites principales

| Fonctionnalite | Description |
|-----------------|-------------|
| Selection de villes | Choix parmi 55 villes francaises de plus de 20 000 habitants |
| Comparaison automatique | Affichage side-by-side des indicateurs |
| Graphiques interactifs | Visualisations Plotly pour chaque categorie |
| Export CSV | Telechargement des donnees comparees |
| Meteo temps reel | Previsions 7 jours via API Open-Meteo |
| Responsive design | Interface adaptee mobile et desktop |

---

## 2. SOURCES DE DONNEES

### 2.1 Donnees demographiques et geographiques

**Source : INSEE (Institut National de la Statistique et des Etudes Economiques)**

| Aspect | Detail |
|--------|--------|
| URL | https://www.insee.fr |
| Indicateurs | Population, superficie, densite, region, departement |
| Annee | 2023 |
| Methode d'acces | Telechargement direct depuis le site INSEE |

**Processus de recuperation :**
1. Se rendre sur https://www.insee.fr/fr/statistiques
2. Rechercher "Populations legales des communes"
3. Telecharger le fichier CSV
4. Filtrer les communes de plus de 20 000 habitants
5. Ajouter les coordonnees GPS (latitude, longitude)

### 2.2 Donnees emploi

**Source : INSEE / Pole Emploi**

| Aspect | Detail |
|--------|--------|
| URL | https://www.pole-emploi.org / https://www.insee.fr |
| Indicateurs | Taux de chomage, nombre d'emplois, secteur principal |
| Annee | 2023 |
| Methode d'acces | Open Data |

**Processus de recuperation :**
1. Acceder a data.gouv.fr
2. Rechercher "taux de chomage par commune"
3. Telecharger les donnees
4. Joindre avec la liste des villes

### 2.3 Donnees logement

**Source : Observatoires Locaux des Loyers / INSEE**

| Aspect | Detail |
|--------|--------|
| URL | https://www.data.gouv.fr / https://www.anil.org |
| Indicateurs | Loyer moyen, part de proprietaires, type de logement |
| Annee | 2023 |
| Methode d'acces | Open Data |

**Processus de recuperation :**
1. Se rendre sur https://www.anil.org
2. Consulter les observatoires locaux des loyers
3. Telecharger les statistiques par zone urbaine

### 2.4 Donnees climatiques

**Source : Meteo-France / Open-Meteo API**

| Aspect | Detail |
|--------|--------|
| URL | https://open-meteo.com |
| API | https://api.open-meteo.com/v1/forecast |
| Indicateurs | Temperature, precipitation, ensolleillement |
| Methode d'acces | API gratuite (sans cle API) |

**Processus de recuperation :**
```python
# Exemple d'appel API
url = "https://api.open-meteo.com/v1/forecast"
params = {
    "latitude": 48.8566,
    "longitude": 2.3522,
    "daily": "temperature_2m_max,temperature_2m_min",
    "timezone": "Europe/Paris"
}
```

### 2.5 Donnees meteo forecast

**Source : Open-Meteo API (temps reel)**

| Aspect | Detail |
|--------|--------|
| URL | https://open-meteo.com |
| Indicateurs | Previsions 7 jours, temps actuel |
| Limite | 10 000 requetes/jour |
| Mise a jour | Toutes les heures |

---

## 3. MODE D'EMPLOI

### 3.1 Installation en local

**Prerequis :**
- Python 3.9 ou superieur
- pip (gestionnaire de paquets)

**Etapes :**

```bash
# 1. Cloner ou telecharger le projet
cd villes_francaises

# 2. Creer un environnement virtuel (recommande)
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # Linux/Mac

# 3. Installer les dependances
pip install -r requirements.txt

# 4. Lancer l'application
streamlit run app.py
```

### 3.2 Utilisation de l'interface

1. **Selection des villes** : Dans la barre laterale, choisissez deux villes a comparer
2. **Navigation** : Les donnes s'affichent dans les onglets
3. **Graphiques** : Passez la souris sur les graphiques pour plus de details
4. **Export** : Cliquez sur le bouton de telechargement pour obtenir un fichier CSV

### 3.3 Deploiement sur Streamlit Cloud

1. Creer un compte sur https://streamlit.io
2. Connecter votre repository GitHub
3. Cliquer sur "Deploy New App"
4. Selectionner le fichier `app.py`
5. L'application sera accessible via une URL publique

---

## 4. ARCHITECTURE TECHNIQUE

### 4.1 Stack technique

| Composant | Technologie |
|-----------|-------------|
| Framework web | Streamlit 1.28+ |
| Langage | Python 3.9+ |
| Visualisation | Plotly |
| Donnees | Pandas, NumPy |
| API HTTP | Requests |
| Deploiement | Streamlit Cloud (gratuit) |

### 4.2 Structure du projet

```
villes_francaises/
├── app.py                    # Application principale
├── requirements.txt          # Dependances Python
├── README.md                 # Documentation
├── MODE_D_EMPLOI.md          # Guide utilisateur
├── RAPPORT.md                # Ce rapport
└── scripts/
    └── import_donnees.py     # Script d'import des donnees
```

### 4.3 Dependances

```
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
plotly>=5.18.0
requests>=2.31.0
```

---

## 5. LIMITES ET AMELIORATIONS

### 5.1 Limites actuelles

- Donnees emploi et logement sont des estimations
- Meteo temps reel depend de la connexion internet
- Limite de 55 villes (plus de 20 000 habitants)

### 5.2 Ameliorations possibles

- Integration de plus de villes
- Donnees en temps reel plus frequentes
- Ajout de categories (culture, sports, education)
- Comparaison multi-villes (3+)
- Application mobile

---

## 6. CONCLUSION

Cette application permet de comparer facilement deux villes francaises sur les criteres essentiels : population, emploi, logement et climat. Elle utilise des sources de donnees ouvertes (INSEE, Open-Meteo) et peut etre deployee gratuitement sur Streamlit Cloud.

---

**Document genere pour SAE Outils Decisionnels**
