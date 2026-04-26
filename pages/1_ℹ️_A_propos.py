"""
A propos
SAE Outils Décisionnels
"""

import streamlit as st
from pathlib import Path


st.set_page_config(
    page_title="Comparateur de Villes Françaises",
    page_icon="ℹ️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Logo in sidebar
st.sidebar.image(
    str(Path(__file__).parent.parent / "src" / "UniversiteParis_IUTParis-RdS.png"),
    width=220
)

st.set_page_config(page_title="A propos", layout="wide")

st.title("A propos")

st.markdown("---")

st.markdown("""
### Comparateur de Villes Francaises

Ce projet a ete réalisé dans le cadre de la **SAE Outils Décisionnels** du BUT SD (Sciences des Données), parcours Visualisation et Conception d'Outils Décisionnels, à l'IUT de Paris - Universite Paris Cité.

**Objectif** : fournir aux étudiants un outil de comparaison entre villes francaises afin de les aider à choisir leur future ville d'études. Au moment de sélectionner un etablissement pour la suite de leur cursus, les étudiants sont souvent confrontés à une question essentielle : au-dela du programme, **quelle ville correspond le mieux à mes attentes et à mon mode de vie ?**

L'application permet de comparer deux villes sur plusieurs dimensions :

- **Population & Etudiants** : taille de la ville, part étudiante, age moyen
- **Revenus & Emploi** : salaire moyen, taux de chomage, secteurs d'activités
- **Cadre de vie** : ensoleillement, qualité de l'air
- **Logement** : loyer moyen
- **Securité** : score de securité
- **Culture & Loisirs** : lieux culturels, restaurants, bars
- **Météo** : previsions à 7 jours

Chaque indicateur est issu de sources officielles (INSEE, data.gouv.fr, Open-Meteo) et est présenté de manière synthétique. 

Un **score de sécurité** (combinaison pondérée des actes recensés : violences 40 %, vols violents 30 %, cambriolages 20 %, stupéfiants 10 %) permet une comparaison indicative du niveau de sécurité entre communes. <br>
Un **score global** (normalisation min-max, 7 indicateurs equiponderes) permet une lecture rapide des points forts et faibles de chaque ville.
""", unsafe_allow_html=True)


st.markdown("---")

st.markdown("""
**Cours** : SAE Outils Décisionnels - BUT SD, IUT de Paris - Université Paris Cité

**Auteurs** : Matteo CAI, William LEFEBVRE, Terryl HASSEN  
""")

st.markdown("---")

st.markdown("**Contact :** ")

st.markdown("""
<div style="display: flex; gap: 40px;">

<div>
<b>Matteo CAI</b><br>
<a href="https://www.linkedin.com/in/matteo-cai-696b062b5/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/24/174/174857.png"/> LinkedIn
</a><br>
<a href="https://github.com/hanmlx" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/24/25/25231.png"/> GitHub
</a>
</div>

<div>
<b>William LEFEBVRE</b><br>
<a href="https://www.linkedin.com/in/william-lefebvre-a924a1187/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/24/174/174857.png"/> LinkedIn
</a><br>
<a href="https://github.com/Lalmytox" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/24/25/25231.png"/> GitHub
</a>
</div>

<div>
<b>Terryl HASSEN</b><br>
<a href="https://www.linkedin.com/in/terryl-hassen-394a3620b/" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/24/174/174857.png"/> LinkedIn
</a><br>
<a href="https://github.com/Tnxhsn" target="_blank">
<img src="https://cdn-icons-png.flaticon.com/24/25/25231.png"/> GitHub
</a>
</div>

</div>
""", unsafe_allow_html=True)

