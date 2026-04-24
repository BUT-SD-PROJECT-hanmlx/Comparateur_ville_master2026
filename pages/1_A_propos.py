"""
A propos
SAE Outils Décisionnels
"""

import streamlit as st
from pathlib import Path

st.set_page_config(page_title="A propos", layout="wide")

st.title("A propos")

st.markdown("---")

st.markdown("""
### Comparateur de Villes Francaises

Ce projet a ete réalisé dans le cadre de la **SAE Outils Décisionnels** du BUT SD (Sciences des Données), parcours Data Science, a l'IUT de Paris - Universite Paris Cité.

**Objectif** : fournir aux etudiants un outil de comparaison entre villes francaises afin de les aider à choisir leur future ville d'études. Au moment de sélectionner un etablissement pour la suite de leur cursus, les etudiants sont souvent confrontés à une question essentielle : au-dela du programme, **quelle ville correspond le mieux à mes attentes et à mon mode de vie ?**

L'application permet de comparer deux villes sur plusieurs dimensions :

- **Population & Etudiants** : taille de la ville, part etudiante, age moyen
- **Revenus & Emploi** : salaire moyen, taux de chomage, secteurs d'activités
- **Cadre de vie** : ensoleillement, qualité de l'air
- **Logement** : loyer moyen
- **Securité** : score de securité
- **Culture & Loisirs** : lieux culturels, restaurants, bars
- **Météo** : previsions a 7 jours

Chaque indicateur est issu de sources officielles (INSEE, data.gouv.fr, Open-Meteo) et présente de maniere synthétique. Un **score global** (normalisation min-max, 7 indicateurs equiponderes) permet une lecture rapide des points forts et faibles de chaque ville.
""")

st.markdown("---")

st.markdown("""
**Auteurs** : Matteo Cai, William Lefebre, Terryl Hassen

**Cours** : SAE Outils Décisionnels - BUT SD, IUT de Paris - Universite Paris Cité
""")

# Logo: decommenter si le fichier est disponible dans pages/src/
# st.image(
#     str(Path(__file__).parent / "src" / "UniversiteParis_IUTParis-RdS.png"),
#     width=220
# )
