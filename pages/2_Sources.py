"""
Sources des données
SAE Outils Décisionnels
"""

import streamlit as st

st.set_page_config(page_title="Sources", page_icon="")

st.title("Sources des données")

st.markdown("""
Toutes les données utilisées dans cette application proviennent de 
**sources officielles et ouvertes** (Open Data). L'objectif est de garantir 
la fiabilité et la transparence des informations présentées.
""")

st.markdown("---")

# INSEE
with st.expander("INSEE - Institut national de la statistique", expanded=True):
    st.markdown("""
    **Site web :** [insee.fr](https://www.insee.fr)
    
    **Données utilisées :**
    - Population légale des communes
    - Superficie (en km²)
    - Densité de population (habitants/km²)
    - Code région et département
    
    **Format :** CSV téléchargé depuis le site officiel
    
    **Fréquence de mise à jour :** Annuelle (populations légales)
    
    **URL directe :**
    [Populations légales des communes](https://www.insee.fr/fr/statistiques/1893198)
    """)

# Open-Meteo
with st.expander("Open-Meteo API - Données météorologiques", expanded=True):
    st.markdown("""
    **Site web :** [open-meteo.com](https://open-meteo.com)
    
    **API :** [api.open-meteo.com](https://api.open-meteo.com/v1/forecast)
    
    **Données utilisées :**
    - Températures minimales et maximales
    - Précipitations
    - Ensoleillement
    - Vent
    - Code météo WMO (description du temps)
    
    **Format :** JSON via API REST
    
    **Avantages :**
    - Entièrement gratuit
    - Aucune clé API requise
    - 10 000 requêtes/jour
    - Données en temps réel
    
    **Exemple de requête :**
    ```
    https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true
    ```
    """)

# data.gouv.fr
with st.expander("data.gouv.fr - Plateforme open data française", expanded=True):
    st.markdown("""
    **Site web :** [data.gouv.fr](https://www.data.gouv.fr)
    
    **Données utilisées :**
    - Taux de chômage par zone d'emploi
    - Nombre d'emplois
    - Secteurs économiques majoritaires
    - Part de propriétaires/locataires
    
    **Format :** CSV / Excel téléchargeables
    
    **Note :** Les données communales de chômage ne sont pas toujours disponibles. 
    Nous utilisons les données par **zone d'emploi** comme approximation.
    """)

# ANIL/CLL
with st.expander("ANIL - Observatoire des loyers", expanded=True):
    st.markdown("""
    **Site web :** [anil.org](https://www.anil.org)
    
    **Données utilisées :**
    - Loyer moyen €/m² par commune
    - Part de propriétaires
    - Part de locataires
    - Type de logement dominant
    
    **Format :** Données agrégées par l'Observatoire des Loyers de l'Agglomération Parisienne (OLAP)
    
    **Note :** Ces données concernent principalement l'Ile-de-France et les grandes métropoles.
    """)

st.markdown("---")

st.markdown("### Qualité des données")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("#### Fiabilité")
    st.markdown("""
    - Sources officielles uniquement
    - Données vérifiées et validées
    - Mise à jour régulière
    """)

with col2:
    st.markdown("#### Limitations")
    st.markdown("""
    - Moyennes générales (pas de granularité par quartier)
    - Délais de mise à jour variables
    - Données parfois manquantes pour petites communes
    """)

with col3:
    st.markdown("#### Recommandations")
    st.markdown("""
    - Croiser plusieurs sources
    - Vérifier sur sites officiels avant décisions importantes
    - Considérer le contexte local
    """)

st.markdown("---")

st.markdown("### Méthodologie")

st.markdown("""
**Collecte des données :**

1. **Données statiques** (population, superficie) : Import depuis CSV INSEE
2. **Données dynamiques** (météo) : Requêtes API en temps réel
3. **Données semi-dynamiques** (emploi, logement) : Import périodique depuis sources officielles

**Calculs dérivés :**

- Densité = Population / Superficie
- Différences en pourcentage pour comparaisons
- Normalisation des échelles pour graphiques
""")

st.markdown("---")

st.markdown("### Licences")

st.success("""
**Toutes les données sont utilisées dans le respect des licences open data :**

- **INSEE :** Licence Ouverte (utilisation libre, même commerciale)
- **Open-Meteo :** Creative Commons Zero (CC0) - Domaine public
- **data.gouv.fr :** Licence Ouverte 2.0

L'application elle-même est un projet académique, libre de consultation et de modification.
""")

st.markdown("---")

st.markdown("*Projet académique - SAE Outils Décisionnels*", unsafe_allow_html=True)
