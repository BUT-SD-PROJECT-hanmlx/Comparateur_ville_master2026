# MODE D'EMPLOI - Comparateur de Villes Françaises

## 1. PRÉSENTATION

Cette application permet de comparer deux villes françaises (de plus de 20 000 habitants) sur différents critères :
- Données générales (population, superficie, densité)
- Emploi (taux de chômage, nombre d'emplois)
- Logement (loyers, type d'habitat)
- Climat (températures, précipitations)
- Météo forecast (7 prochains jours)

## 2. COMMENT LANCER L'APPLICATION

### Option A : En local (recommandé pour le développement)

1. **Prérequis** :
   - Python 3.9 ou supérieur installé
   - pip (gestionnaire de paquets Python)

2. **Étapes d'installation** :

   ```bash
   # Ouvrir un terminal

   # Cloner ou télécharger le projet
   cd villes_francaises

   # Créer un environnement virtuel (recommandé)
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   # source venv/bin/activate  # Linux/Mac

   # Installer les dépendances
   pip install -r requirements.txt
   ```

3. **Lancer l'application** :

   ```bash
   streamlit run app.py
   ```

4. **Accéder à l'application** :
   - Un navigateur s'ouvrira automatiquement
   - Ou accédez manuellement à : http://localhost:8501

### Option B : Version en ligne (si déployée)

1. Accédez à l'URL fournie (ex: https://votre-app.streamlit.app)
2. L'application est prête à l'emploi

## 3. COMMENT UTILISER L'INTERFACE

### Étape 1 : Sélectionner les villes
- Dans la barre latérale gauche, vous verrez deux menus déroulants
- Choisissez la **Première Ville** et la **Deuxième Ville**
- Seules les villes françaises de plus de 20 000 habitants sont proposées

### Étape 2 : Consulter les comparaisons
- L'application affiche automatiquement les comparaisons dans plusieurs onglets :
  - **Vue d'ensemble** : Résumé des indicateurs clés
  - **Données générales** : Population, superficie, densité
  - **Emploi** : Taux de chômage, nombre d'emplois, secteurs
  - **Logement** : Type de logement, loyers, propriétaires
  - **Climat** : Températures annuelles, précipitations
  - **Météo** : Prévisions des 7 prochains jours

### Étape 3 : Interpréter les résultats
- **Vert** : Indique que la ville est plus favorable (ex: loyer plus bas, taux de chômage plus faible)
- **Rouge** : Indique que la ville est moins favorable
- Les graphiques permettent de visualiser facilement les différences

## 4. SOURCES DE DONNÉES

### Données générales et démographiques
- **Source** : INSEE (Institut National de la Statistique)
- **URL** : https://www.insee.fr
- **Indicateurs** : Population, superficie, densité

### Données emploi
- **Source** : INSEE / Pôle Emploi
- **URL** : https://www.pole-emploi.org
- **Indicateurs** : Taux de chômage, nombre d'emplois

### Données logement
- **Source** : INSEE / Open Data
- **URL** : https://data.gouv.fr
- **Indicateurs** : Loyers, type d'habitat, propriétaires

### Données climatiques
- **Source** : Open-Meteo API (gratuit)
- **URL** : https://open-meteo.com
- **Indicateurs** : Températures, précipitations

### Données météo forecast
- **Source** : Open-Meteo API
- **URL** : https://open-meteo.com
- **Indicateurs** : Prévisions 7 jours

## 5. FONCTIONNALITÉS AVANCÉES

### Mode sombre
- L'application détecte automatiquement le thème de votre système
- Basculer manuellement via le menu ⋮ (trois points) en haut à droite

### Téléchargement des données
- Chaque onglet propose un bouton de téléchargement CSV
- Permet d'exporter les données comparatives

### Rafraîchissement des données météo
- Les données météo sont mises à jour à chaque chargement de page
- Cliquez sur le bouton "Actualiser" pour une mise à jour immédiate

## 6. RÉSOLUTION DES PROBLÈMES

### L'application ne démarre pas
- Vérifiez que Python est installé : `python --version`
- Vérifiez que Streamlit est installé : `pip show streamlit`
- Réinstallez les dépendances : `pip install -r requirements.txt`

### Erreur de connexion aux données météo
- Vérifiez votre connexion internet
- Les données peuvent être temporairement indisponibles

### Une ville n'apparaît pas dans la liste
- Seules les villes de plus de 20 000 habitants sont incluses
- La ville peut avoir été ajoutée récemment

## 7. INFORMATIONS TECHNIQUES

### Technologies utilisées
- **Framework** : Streamlit (Python)
- **Visualisation** : Plotly, Altair
- **Données** : Pandas, NumPy
- **API Météo** : Open-Meteo (gratuit, sans clé API)

### Configuration matérielle requise
- Minimum : 4 Go RAM, CPU dual-core
- Recommandé : 8 Go RAM, CPU quad-core

## 8. CONTACT ET SUPPORT

Pour toute question concernant l'application, contactez l'équipe de développement.
