"""
Sources des donnees
SAE Outils Decisionnels
"""

import streamlit as st

st.set_page_config(page_title="Sources", layout="wide")

st.title("Sources des donnees")
st.markdown("---")

col1, col2 = st.columns(2)

with col1:
    with st.expander("INSEE + DARES", expanded=True):
        st.markdown("""
        **Fichiers CSV locaux** (dossier `data/`) :

        - `liste_communes_20k_2023_v2.csv` — Population 2023, INSEE Recensement
          [insee.fr/statistiques/8680726](https://www.insee.fr/fr/statistiques/8680726?sommaire=8681011)

        - `alternance_communes_20k_2023.csv` — Apprentissages / Alternance, DARES
          [poem.travail-emploi.gouv.fr](https://poem.travail-emploi.gouv.fr/open-data/alternance-1#new_cap_second_stk)

        - `communes_20k_salaires_final.csv` — Salaires nets mensuels moyens 2023, INSEE Base Tous salaries
          [insee.fr/statistiques/2021266](https://www.insee.fr/fr/statistiques/2021266)
          - Couverture : **454 communes**
          - Champs : `Salaire_2023` (net mensuel moyen EQTP, euros), `Salaire_evol` (evolution 2023 vs 2022)

        - `url_cities_final.csv` — Thumbnails Wikipedia (API MediaWiki pre-cached)

        Licence : **Licence Ouverte**
        """)

    with st.expander("Open-Meteo API", expanded=True):
        st.markdown("""
        **open-meteo.com** — Donnees meteorologiques et qualite de l'air

        - Previsions 7 jours : temperatures, precipitations, code temps (WMO)
        - **Ensoleillement annuel** : Archive API (ERA5 reanalysis), moyenne 2020-2024
          - Fichier : `ensoleillement.csv`
          - Couverture : **410 communes**
          - Unite : heures de soleil par an → affiche en **% de l'annee** (heures / 8760h)
          - Note : valeurs ERA5 plus elevees que les observations au sol
            (Campbell-Stokes) ; l'ordre relatif entre villes est fiable
        - **Qualite de l'air** : Air Quality API (Copernicus CAMS), moyenne 2023-2024
          - Fichier : `aqi.csv`
          - Couverture : **422 communes**
          - Indice : **European AQI** (0-20 Bon / 20-40 Moyen / 40-60 Mediocre / 60-80 Mauvais / >80 Tres mauvais)
          - Note : l'archive Air Quality debute en juillet 2022, la moyenne couvre 2 ans complets (2023-2024)

        Aucune cle API requise &mdash; Gratuit

        Licence : **CC BY 4.0** (Archive API) / **CC0** (Forecast API)
        """)

    with st.expander("data.gouv.fr", expanded=True):
        st.markdown("""
        **data.gouv.fr** — Plateforme open data francaise

        - `communes_20k_avec_chomage_final.csv` — Taux de chomage departemental 2024
          [insee.fr/statistiques/2045861](https://www.insee.fr/fr/statistiques/2045861)
          - Couverture : **483 communes**
          - Champs : `dep_tx_chomage_24` (taux de chomage departemental, %)
          - Note : le taux est departemental (pas communal), attribue a chaque commune selon son departement

        - `communes_20k_avec_score_securite_2025_final.csv` — Score de securite 2025
          - Couverture : **483 communes**
          - Champs : `score_securite_25` (score 0-100)

        - `communes_20k_avec_lieux_culturel_2025_final.csv` — Lieux culturels 2025
          - Couverture : **483 communes**
          - Champs : `nb_lieux_culturels`, `nb_lieux_culturel_par_1000_habitants`

        - `restaurants_bars_filtre_communes.csv` — Restaurants et bars 2025
          - Couverture : **455 communes** (28 sans donnees)
          - Champs : `restaurants`, `bars`, `restaurants_pour_1000`, `bars_pour_1000`

        - `communes_20k_avec_secteurs_activites_2025_final.csv` — Secteurs d'activites 2025
          - Couverture : **483 communes**
          - 17 secteurs d'activite (emplois par secteur)
          - Affichage : camembert top 4 + Autres

        Licence : **Licence Ouverte 2.0**
        """)

with col2:
    with st.expander("Carte des loyers 2025 (ANIL / data.gouv.fr)", expanded=True):
        st.markdown("""
        **Carte des loyers 2025** — Indicateurs de loyers d'annonce par commune

        Source : ANIL (Agence nationale pour l'information sur le logement) / data.gouv.fr

        Fichier : `pred-app12-mef-dhup.csv` (appartements T1-T2, 37 m²)

        Couverture : **455 communes** de notre liste ont des donnees de loyer disponibles

        Champs utilisés : `loypredm2` (loyer prédit €/m², charges comprises)

        [data.gouv.fr/datasets/carte-des-loyers-2025](https://www.data.gouv.fr/datasets/carte-des-loyers-indicateurs-de-loyers-dannonce-par-commune-en-2025)

        **Note methodologique** :
        - Le fichier officiel fournit un loyer moyen par commune (€/m²)
        - `loyer_studio_centre` et `loyer_studio_peri` sont estimés à partir
          de la moyenne communale avec un coefficient centre/périphérie
        - `loyer_coloc` est estimé à ~55 % du loyer centre
          (données de colocation non disponibles dans la source officielle)
        - Paris, Lyon et Marseille : moyenne pondérée des arrondissements

        Licence : **Licence Ouverte 2.0**
        """)

    with st.expander("Methodologie des scores KPI", expanded=True):
        st.markdown("""  
        **Score global par ville** — moyenne equiponderee des indicateurs suivants :

        Chaque indicateur est normalise en score 0-100 (min-max sur les 483 communes).
        Les indicateurs "inverse" (valeur basse = meilleur score) : loyer, AQI, chomage.

        - **% Etudiants** : proportion d'etudiants dans la population (Ministere de l'Enseignement Superieur)
        - **Salaire** : net mensuel moyen EQTP 2023 (INSEE Base Tous salaries)
        - **Loyer** *(inverse)* : loyer moyen €/m² (Carte des loyers 2025)
        - **Ensoleillement** : % de l'annee (Open-Meteo ERA5)
        - **Qualite de l'air** *(inverse)* : indice AQI europeen (Open-Meteo Air Quality / Copernicus CAMS)
        - **Chomage** *(inverse)* : taux departemental 2024 (INSEE / data.gouv.fr)
        - **Securite** : score 0-100, 2025 (data.gouv.fr)

        Score global = moyenne des scores disponibles pour chaque ville.
        """)

st.markdown("---")
st.caption("Toutes les donnees sont issues de sources officielles ou open data. "
           "Loyer : 455 communes (Carte des loyers 2025). "
           "Salaire : 454 communes (INSEE Base Tous salaries 2023). "
           "Ensoleillement : 410 communes (Open-Meteo ERA5). "
           "Qualite de l'air : 422 communes (Open-Meteo Air Quality). "
           "Chomage : 483 communes (INSEE 2024). "
           "Securite : 483 communes (data.gouv.fr 2025). "
           "Lieux culturels : 483 communes (data.gouv.fr 2025). "
           "Restaurants & bars : 455 communes (data.gouv.fr 2025). "
           "Secteurs d'activite : 483 communes (data.gouv.fr 2025). "
           "Scores KPI : normalisation min-max, 7 indicateurs, equipondere.")
