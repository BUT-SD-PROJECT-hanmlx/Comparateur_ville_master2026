# Comparateur de Villes Françaises

Application Streamlit pour comparer deux villes françaises sur différents aspects :
coût de la vie, logement, emploi, climat, activités, etc.

## Structure du projet

```
villes_francaises/
├── app.py                    # Application principale Streamlit
├── requirements.txt          # Dépendances Python
├── data/
│   ├── villes_data.csv       # Données générales des villes
│   ├── logement_data.csv      # Données logement
│   ├── emploi_data.csv        # Données emploi
│   └── villes_20000_plus.csv  # Liste villes > 20000 hab.
├── scripts/
│   ├── import_donnees.py      # Script d'import des données
│   └── mise_a_jour.py         # Script de mise à jour
├── README.md                  # Ce fichier
└── MODE_D_EMPLOI.md          # Mode d'emploi
```

## Installation

```bash
# Cloner ou télécharger le projet
cd villes_francaises

# Installer les dépendances
pip install -r requirements.txt

# Lancer l'application
streamlit run app.py
```

## Déploiement sur Streamlit Cloud

1. Créer un compte sur [streamlit.io](https://streamlit.io)
2. Connecter votre repository GitHub
3. Déployer depuis le fichier `app.py`
4. L'application sera accessible via une URL publique

## Fonctionnalités

- Comparaison de 2 villes françaises (> 20 000 habitants)
- Données générales (population, superficie, densité)
- Données emploi (taux de chômage, secteurs)
- Données logement (loyers, propriétaires)
- Données climatiques (températures, précipitations)
- Météo des 7 prochains jours
- Visualisations comparatives
- Classements et scores

## Auteurs

Projet académique - SAE Outils Décisionnels
