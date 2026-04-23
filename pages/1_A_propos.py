"""
A propos
SAE Outils Decisionnels
"""

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="A propos", layout="wide")

st.title("A propos")

st.markdown("---")

st.markdown("""
### Comparateur de Villes Francaises

Ce projet a ete realise dans le cadre de la **SAE Outils Decisionnels** du BUT SD (Sciences des Donnees), parcours Data Science, a l'IUT de Paris - Universite Paris Cite.

**Objectif** : fournir aux etudiants un outil de comparaison entre villes francaises afin de les aider a choisir leur future ville d'etudes. Au moment de selectionner un etablissement pour la suite de leur cursus, les etudiants sont souvent confrontes a une question essentielle : au-dela du programme, **quelle ville correspond le mieux a mes attentes et a mon mode de vie ?**

L'application permet de comparer deux villes sur plusieurs dimensions :

- **Population & Etudiants** : taille de la ville, part etudiante, age moyen
- **Revenus & Emploi** : salaire moyen, taux de chomage, secteurs d'activite
- **Cadre de vie** : ensoleillement, qualite de l'air
- **Logement** : loyer moyen
- **Securite** : score de securite
- **Culture & Loisirs** : lieux culturels, restaurants, bars
- **Meteo** : previsions a 7 jours

Chaque indicateur est issu de sources officielles (INSEE, data.gouv.fr, Open-Meteo) et presente de maniere synthetique. Un **score global** (normalisation min-max, 7 indicateurs equiponderes) permet une lecture rapide des points forts et faibles de chaque ville.
""")

st.markdown("---")

st.markdown("""
**Auteurs** : Matteo Cai, William Lefebre, Terryl Hassen

**Cours** : SAE Outils Decisionnels - BUT SD, IUT de Paris - Universite Paris Cite
""")

# Logo: decommenter si le fichier est disponible dans pages/src/
# st.image(
#     str(Path(__file__).parent / "src" / "UniversiteParis_IUTParis-RdS.png"),
#     width=220
# )
