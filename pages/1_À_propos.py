"""
À propos - Présentation du projet
SAE Outils Décisionnels
"""

import streamlit as st

st.set_page_config(page_title="À propos", page_icon="")

st.title("À propos du projet")

st.markdown("""
## Comparateur de Villes Françaises

Cette application a été développée dans le cadre de la **SAE Outils Décisionnels** 
pour permettre la comparaison objective de villes françaises sur plusieurs critères 
essentiels.
""")

st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Objectif")
    st.markdown("""
    Fournir une **vision complète** et **objective** des villes françaises pour 
    faciliter la prise de décision, que ce soit pour :
    
    - Choisir une ville de résidence
    - Évaluer une opportunité professionnelle
    - Planifier un projet immobilier
    - **Sélectionner une ville pour ses études supérieures**
    """)

with col2:
    st.markdown("### Critères de comparaison")
    st.markdown("""
    L'application compare les villes sur **6 dimensions** :
    
    1. **Démographie** - Population, superficie, densité
    2. **Emploi** - Taux de chômage, secteurs économiques
    3. **Logement** - Loyers, taux de propriétaires
    4. **Climat** - Températures, précipitations, ensoleillement
    5. **Météo** - Prévisions à 7 jours (temps réel)
    """)

st.markdown("---")

st.markdown("### Pour la sélection universitaire")

st.info("L'application peut vous aider à choisir votre ville d'études !")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### Critères académiques à considérer")
    st.markdown("""
    - **Taille de la ville** : Grandes métropoles vs villes moyennes
    - **Présence d'universités** : Rennes, Lyon, Paris, Toulouse...
    - **Coût de la vie** : Loyers, transports, alimentation
    - **Marché du travail local** : Opportunités de stage/emploi
    """)

with col2:
    st.markdown("#### Comment utiliser l'application")
    st.markdown("""
    1. Comparez les villes où vous envisagez d'étudier
    2. Analysez le **coût du logement** (crucial pour étudiant)
    3. Vérifiez le **taux de chômage** local (perspectives d'emploi)
    4. Consultez le **climat** (qualité de vie au quotidien)
    5. Regardez la **météo forecast** pour préparer vos valises !
    """)

st.markdown("---")

st.markdown("### Données disponibles")

st.markdown("""
L'application couvre **55 villes françaises** de plus de 20 000 habitants, 
avec des données provenant de sources officielles :
""")

st.markdown("""
| Source | Données | Mise à jour |
|--------|---------|-------------|
| INSEE | Population, superficie, densité | Annuelle |
| Open-Meteo | Météo temps réel et prévisions | Quotidienne |
| Données publiques | Emploi, logement, climat | Variable |
""")

st.markdown("---")

st.markdown("### Limites et Remarques importantes")

st.warning("""
**Points à considérer :**

- Les données sont des **moyennes** et peuvent varier selon les quartiers
- Les loyers indiqués sont des **estimations moyennes** (réel peut varier)
- Le taux de chômage est une **moyenne régionale** (donnée communale parfois indisponible)
- La météo forecast est fiable à **7 jours** mais moins précise au-delà
- Certaines données peuventdater de **2022-2023** selon la source

Pour une décision importante (logement, estudios), vérifiez toujours 
les informations auprès de sources locales officielles.
""")

st.markdown("---")

st.markdown("*Projet académique - SAE Outils Décisionnels*", unsafe_allow_html=True)
