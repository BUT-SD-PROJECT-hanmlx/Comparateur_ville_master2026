"""
Comparateur de Villes Françaises
=================================
Auteurs : Matteo Cai, William Lefebre, Terryl Hassen
Cours : SAE Outils Decisionnels
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import requests
import urllib.parse
from pathlib import Path

st.set_page_config(
    page_title="Comparateur de Villes Françaises",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Logo in sidebar
st.sidebar.image(
    str(Path(__file__).parent / "src" / "UniversiteParis_IUTParis-RdS.png"),
    width=220
)

# ============================================================================
# CSS
# ============================================================================
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.1/css/all.min.css" crossorigin="anonymous" referrerpolicy="no-referrer" />
<style>
    /* ---- Page background ---- */
    .stApp { background: #f5f4f0; }

    /* ---- City card ---- */
    .city-card {
        border-radius: 16px;
        overflow: hidden;
        background: #ffffff;
        box-shadow: 0 4px 20px rgba(0,0,0,0.10);
        margin: 0 4px;
        position: relative;
    }
    .city-card-img {
        width: 100%;
        height: 160px;
        overflow: hidden;
        display: block;
    }
    .city-card-img img {
        width: 100%;
        height: 160px;
        object-fit: cover;
        display: block;
    }
    .city-card-overlay {
        position: absolute;
        bottom: 0; left: 0; right: 0;
        background: linear-gradient(transparent, rgba(0,0,0,0.75));
        padding: 24px 16px 12px 16px;
    }
    .city-card-name {
        font-size: 1.5rem;
        font-weight: 700;
        color: #ffffff;
        margin: 0;
        text-shadow: 0 2px 6px rgba(0,0,0,0.4);
    }
    .city-card-region {
        font-size: 0.75rem;
        color: rgba(255,255,255,0.75);
        margin: 2px 0 0 0;
    }
    /* Selector bar inside card */
    .card-selector-wrap {
        padding: 10px 12px 6px 12px;
        background: #fff;
    }

    /* ---- Indicator cards ---- */
    .ind-card {
        background: #ffffff;
        border-radius: 12px;
        padding: 16px 18px 12px 18px;
        border: 1px solid #e8e4de;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        position: relative;
        overflow: hidden;
    }
    .ind-card::after {
        content: '';
        position: absolute;
        top: 0; left: 0;
        width: 4px; height: 100%;
        background: #5d7a8c;
        border-radius: 4px 0 0 4px;
    }
    .ind-card.v2::after { background: #a67c5b; }
    .ind-icon {
        display: block;
        margin-bottom: 2px;
        font-size: 1.2rem;
        color: #5d7a8c;
    }
    .ind-card.v2 .ind-icon { color: #a67c5b; }
    .ind-label {
        font-size: 0.82rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.7px;
        color: #5d7a8c;
        margin-bottom: 6px;
    }
    .ind-value {
        font-size: 1.55rem;
        font-weight: 700;
        color: #2c3e50;
        line-height: 1;
        margin-bottom: 4px;
    }
    .ind-sub {
        font-size: 0.72rem;
        color: #666;
    }

    /* ---- KPI block (grouped per city) ---- */
    .kpi-block {
        background: #ffffff;
        border-radius: 14px;
        border: 1px solid #e8e4de;
        box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        padding: 18px 20px 10px;
        margin-bottom: 8px;
    }
    .kpi-block-title {
        font-size: 0.72rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 1px;
        margin-bottom: 14px;
        border-bottom: 1px solid #f0ece6;
        padding-bottom: 8px;
    }
    .kpi-row {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #f5f2ee;
    }
    .kpi-row:last-child { border-bottom: none; }
    .kpi-icon {
        width: 32px;
        height: 32px;
        border-radius: 8px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        font-size: 0.85rem;
    }
    .kpi-body { flex: 1; min-width: 0; }
    .kpi-label {
        font-size: 0.65rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        color: #5d7a8c;
        margin-bottom: 1px;
    }
    .kpi-value {
        font-size: 1.25rem;
        font-weight: 700;
        color: #2c3e50;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 0.68rem;
        color: #666;
        margin-top: 1px;
    }

    /* ---- Table text ---- */
    .stTable td, .stTable th { color: #333; font-size: 0.85rem; }

    /* ---- Tab content text ---- */
    .stTabs [data-baseweb="tab-panel"] { color: #2c3e50; }
    .stTabs [data-baseweb="tab-panel"] p { color: #2c3e50; }
    .stTabs [data-baseweb="tab-panel"] h4 { color: #2c3e50; }
    .stTabs [data-baseweb="tab-panel"] h5 { color: #2c3e50; }

    /* ---- Section label ---- */
    .sec-label {
        font-size: 0.68rem;
        text-transform: uppercase;
        letter-spacing: 1.2px;
        color: #bbb;
        font-weight: 600;
        margin: 18px 0 6px 0;
        text-align: center;
    }

    /* ---- Tab styling ---- */
    .stTabs [data-baseweb="tab-list"] {
        gap: 0;
        border-bottom: 2px solid #e0dbd3;
    }
    .stTabs [data-baseweb="tab"] {
        font-size: 0.88rem;
        font-weight: 500;
        padding: 6px 20px;
        color: #2c3e50 !important;
    }
    .stTabs [data-baseweb="tab"]:hover {
        color: #5d7a8c !important;
    }
    .stTabs [data-baseweb="tab"][aria-selected="true"] {
        color: #2c3e50 !important;
        border-bottom: 3px solid #5d7a8c;
    }

    /* ---- Footer ---- */
    .footer { text-align: center; color: #bbb; font-size: 0.75rem; margin-top: 24px; }

    /* hide default elements */
    #MainMenu, footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# ============================================================================
# DONNEES
# ============================================================================

DATA_DIR = Path(__file__).parent / "data"

def _parse_population(raw):
    """Parse INSEE population string (may have spaces as thousand sep)."""
    if raw is None:
        return 0
    return int(str(raw).replace(" ", "").replace("\xa0", ""))

@st.cache_data
def load_villes_data():
    """Charge les donnees INSEE depuis liste_communes_20k_2023_v2.csv."""
    path = DATA_DIR / "liste_communes_20k_2023_v2.csv"
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    # Clean column names
    df.columns = [c.strip() for c in df.columns]
    # Rename for easier access
    df = df.rename(columns={
        "Nom de la commune": "ville",
        "Population municipale": "population",
        "Code postal": "code_postal",
        "Nom du département": "departement",
        "Nom de la région": "region",
    })
    df["population"] = df["population"].apply(_parse_population)
    # Drop dupes keeping first (some cities may appear twice)
    df = df.drop_duplicates(subset="ville", keep="first")
    return df.reset_index(drop=True)

@st.cache_data
def load_etudiants_data():
    """Charge les donnees etudiants depuis communes_20k_2023_nb_etudiants_24.csv.
    
    Retourne un dict {nom_ville: {nb_etudiants, pct_etudiants, population}}
    avec pct_etudiants en pourcentage entier (ex: 19 pour 19%).
    
    Source : Ministere de l'Enseignement Superieur (communes_20k_2023_nb_etudiants_24.csv)
    """
    etudiants_path = DATA_DIR / "communes_20k_2023_nb_etudiants_24.csv"
    if not etudiants_path.exists():
        return {}
    
    df = pd.read_csv(etudiants_path, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    
    result = {}
    for _, row in df.iterrows():
        ville = str(row.get("Nom de la commune", "")).strip()
        if not ville:
            continue
        nb = row.get("nb_etudiants_total")
        taux = row.get("taux_etudiants")
        pop = row.get("Population municipale")
        if pd.notna(nb) and pd.notna(taux):
            # taux_etudiants est en decimal (ex: 0.07 = 7%), convertir en %
            pct = round(float(taux) * 100)
            result[ville] = {
                "nb_etudiants": int(float(nb)),
                "pct_etudiants": pct,
            }
            # Ajouter population si dispo pour calcul alternatif
            if pd.notna(pop):
                result[ville]["population_csv"] = int(float(pop))
    
    return result

@st.cache_data
def load_wiki_images():
    """Charge les URLs Wikipedia depuis url_cities_final.csv."""
    path = DATA_DIR / "url_cities_final.csv"
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    # Strip parenthetical suffix for matching (e.g. "Saint-Denis (Seine-Saint-Denis)")
    df["ville_match"] = df["city"].str.replace(r"\s*\([^)]*\)\s*$", "", regex=True).str.strip()
    return dict(zip(df["ville_match"], df["image_url"]))

@st.cache_data
def load_loyers_data():
    """Charge les donnees de loyer depuis la Carte des loyers 2025 (ANIL / data.gouv.fr).
    
    Retourne un dict {nom_ville: {loypredm2, loyer_studio_centre, loyer_studio_peri, loyer_coloc}}
    pour toutes les villes du CSV INSEE qui ont une correspondance.
    
    Source : pred-app12-mef-dhup.csv (appartements T1-T2, 37 m2, charges comprises)
    """
    import csv as _csv
    
    loyers_path = DATA_DIR / "loyers_t1t2_2025.csv"
    if not loyers_path.exists():
        return {}
    
    df_loyers = pd.read_csv(loyers_path, sep=";", encoding="utf-8-sig")
    # Convert comma-decimal to float
    df_loyers["loypredm2_num"] = df_loyers["loypredm2"].str.replace(",", ".").astype(float)
    if df_loyers["nbobs_com"].dtype == object:
        df_loyers["nbobs_num"] = df_loyers["nbobs_com"].str.replace(",", ".").astype(float)
    else:
        df_loyers["nbobs_num"] = df_loyers["nbobs_com"].astype(float)
    
    # Build lookup by INSEE code
    loyers_by_insee = {}
    for _, row in df_loyers.iterrows():
        insee = str(row["INSEE_C"]).strip()
        loyers_by_insee[insee] = row["loypredm2_num"]
    
    # Handle Paris/Lyon/Marseille: weighted average of arrondissements
    arrondissement_cities = {
        "Paris": "751",
        "Lyon": "693",
        "Marseille": "132",
    }
    for city_name, insee_prefix in arrondissement_cities.items():
        arr_rows = df_loyers[df_loyers["INSEE_C"].astype(str).str.startswith(insee_prefix)]
        if len(arr_rows) > 0:
            weighted_avg = (arr_rows["loypredm2_num"] * arr_rows["nbobs_num"]).sum() / arr_rows["nbobs_num"].sum()
            loyers_by_insee[city_name] = weighted_avg  # special key for name lookup
    
    # Load villes CSV to build mapping
    villes_df = load_villes_data()
    # We need the original CSV for INSEE codes
    raw_villes = pd.read_csv(DATA_DIR / "liste_communes_20k_2023_v2.csv", sep=";", encoding="utf-8-sig")
    raw_villes.columns = [c.strip() for c in raw_villes.columns]
    dept_col = [c for c in raw_villes.columns if "departement" in c.lower() or "département" in c.lower()][0]
    raw_villes["insee_full"] = raw_villes[dept_col].astype(str).str.zfill(2) + raw_villes["Code commune"].astype(str).str.zfill(3)
    raw_villes["ville"] = raw_villes["Nom de la commune"].str.strip()
    
    result = {}
    for _, vr in raw_villes.iterrows():
        ville = vr["ville"]
        code = str(vr["insee_full"]).strip()
        
        # Check arrondissement cities first
        if ville in arrondissement_cities and ville in loyers_by_insee:
            loy_m2 = loyers_by_insee[ville]
        elif code in loyers_by_insee:
            loy_m2 = loyers_by_insee[code]
        else:
            continue
        
        # Estimate studio prices from €/m² (T1-T2, 37m²)
        # centre = loypredm2 * 37 * 1.0 (base)
        # peri = loypredm2 * 37 * 0.72
        # coloc = loypredm2 * 37 * 0.55
        studio_centre = round(loy_m2 * 37)
        studio_peri = round(loy_m2 * 37 * 0.72)
        coloc = round(loy_m2 * 37 * 0.55)
        
        result[ville] = {
            "loypredm2": round(loy_m2, 2),
            "loyer_studio_centre": studio_centre,
            "loyer_studio_peri": studio_peri,
            "loyer_coloc": coloc,
        }
    
    return result

@st.cache_data
def load_salaires_data():
    """Charge les donnees de salaire depuis INSEE (Base Tous salaries 2023).

    Retourne un dict {nom_ville: {salaire_2023, salaire_evol}}
    avec salaire_2023 en euros (net mensuel moyen EQTP) et salaire_evol en decimal.

    Source : INSEE, Salaires dans le secteur prive (2023 vs 2022).
    """
    path = DATA_DIR / "communes_20k_salaires_final.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    df["ville"] = df["Nom de la commune"].str.strip()
    # Parse Salaire_2023: spaces as thousand sep (e.g. "2 609")
    df["salaire_2023"] = pd.to_numeric(
        df["Salaire_2023"].astype(str).str.replace(" ", "").str.replace("\xa0", ""),
        errors="coerce"
    )
    # Parse Salaire_evol: comma as decimal sep (e.g. "0,039")
    df["salaire_evol"] = pd.to_numeric(
        df["Salaire_evol"].astype(str).str.replace(",", "."),
        errors="coerce"
    )
    result = {}
    for _, row in df.iterrows():
        ville = row["ville"]
        sal = row.get("salaire_2023")
        evol = row.get("salaire_evol")
        if pd.notna(sal):
            result[ville] = {
                "salaire_2023": int(sal),
                "salaire_evol": round(float(evol), 4) if pd.notna(evol) else None,
            }
    return result

@st.cache_data
def load_ensoleillement_data():
    """Charge les donnees d'ensoleillement depuis Open-Meteo Historical API.
    
    Retourne un dict {nom_ville: heures_par_an} pour toutes les villes
    disponibles dans data/ensoleillement.csv.
    
    Source : Open-Meteo Archive API (ERA5 reanalysis), moyenne 2020-2024.
    Note : les valeurs sont plus elevees que les observations au sol
    (Campbell-Stokes), car le modele ERA5 tend a sous-estimer la couverture
    nuageuse. L'ordre relatif entre villes est fiable.
    """
    path = DATA_DIR / "ensoleillement.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, encoding="utf-8-sig")
    result = {}
    for _, row in df.iterrows():
        ville = str(row["ville"]).strip()
        h = row.get("ensoleillement_h")
        if pd.notna(h):
            result[ville] = int(h)
    return result

@st.cache_data
def load_aqi_data():
    """Charge les donnees qualite de l'air depuis Open-Meteo Air Quality API.

    Retourne un dict {nom_ville: aqi_moyen} (indice AQI europeen moyen 2023-2024).
    Echelle EU : 0-20 Bon / 20-40 Moyen / 40-60 Mediocre / 60-80 Mauvais / >80 Tres mauvais.

    Source : Open-Meteo Air Quality API (Copernicus CAMS), moyenne 2023-2024.
    """
    path = DATA_DIR / "aqi.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, encoding="utf-8-sig")
    result = {}
    for _, row in df.iterrows():
        ville = str(row["ville"]).strip()
        a = row.get("aqi_moyen")
        if pd.notna(a):
            result[ville] = round(float(a), 1)
    return result

@st.cache_data
def load_chomage_data():
    """Charge les donnees de taux de chomage depuis communes_20k_avec_chomage_final.csv.

    Retourne un dict {nom_ville: tx_chomage} en pourcentage (ex: 8.5 pour 8,5%).

    Source : INSEE / data.gouv.fr, taux de chomage departemental 2024.
    """
    path = DATA_DIR / "communes_20k_avec_chomage_final.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    result = {}
    for _, row in df.iterrows():
        ville = str(row.get("Nom de la commune", "")).strip()
        if not ville:
            continue
        tx = row.get("dep_tx_chomage_24")
        if pd.notna(tx):
            result[ville] = float(str(tx).replace(",", "."))
    return result

@st.cache_data
def load_age_moyen_data():
    """Charge les donnees d'age moyen depuis communes_20k_avec_age_moyen_2025_final.csv.

    Retourne un dict {nom_ville: age_moyen} en annees (ex: 40.5).

    Source : INSEE / data.gouv.fr, age moyen 2025.
    """
    path = DATA_DIR / "communes_20k_avec_age_moyen_2025_final.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    result = {}
    for _, row in df.iterrows():
        ville = str(row.get("Nom de la commune", "")).strip()
        if not ville:
            continue
        age = row.get("age moyen")
        if pd.notna(age):
            result[ville] = round(float(str(age).replace(",", ".")), 1)
    return result

@st.cache_data
def load_culture_data():
    """Charge les donnees culturelles depuis communes_20k_avec_lieux_culturel_2025_final.csv.

    Retourne un dict {nom_ville: {nb_lieux, nb_types, densite}} avec:
    - nb_lieux: nombre total de lieux culturels
    - nb_types: nombre de types differents
    - densite: nb lieux par 1000 habitants

    Source : data.gouv.fr, lieux culturels 2025.
    """
    path = DATA_DIR / "communes_20k_avec_lieux_culturel_2025_final.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, sep=";", encoding="latin-1")
    df.columns = [c.strip() for c in df.columns]
    result = {}
    for _, row in df.iterrows():
        ville = str(row.get("Nom de la commune", "")).strip()
        if not ville:
            continue
        nb = row.get("nb_lieux_culturels")
        types = row.get("nb_types_differents")
        dens = row.get("nb_lieux_culturel_par_1000_habitants")
        if pd.notna(nb):
            result[ville] = {
                "nb_lieux": int(float(nb)),
                "nb_types": int(float(types)) if pd.notna(types) else None,
                "densite": round(float(str(dens).replace(",", ".")), 2) if pd.notna(dens) else None,
            }
    return result

@st.cache_data
def load_restaurants_data():
    """Charge les donnees restaurants/bars depuis restaurants_bars_filtre_communes.csv.

    Retourne un dict {nom_ville: {nb_restaurants, nb_bars, rest_par_1000, bars_par_1000}} avec:
    - nb_restaurants: nombre total de restaurants
    - nb_bars: nombre total de bars
    - rest_par_1000: restaurants pour 1000 habitants
    - bars_par_1000: bars pour 1000 habitants

    Source : data.gouv.fr, restaurants et bars 2025.
    """
    path = DATA_DIR / "restaurants_bars_filtre_communes.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    result = {}
    for _, row in df.iterrows():
        ville = str(row.get("Nom de la commune", "")).strip()
        if not ville:
            continue
        rest = row.get("restaurants")
        bars = row.get("bars")
        r1000 = row.get("restaurants_pour_1000")
        b1000 = row.get("bars_pour_1000")
        if pd.notna(rest):
            result[ville] = {
                "nb_restaurants": int(float(rest)),
                "nb_bars": int(float(bars)) if pd.notna(bars) else None,
                "rest_par_1000": round(float(r1000), 2) if pd.notna(r1000) else None,
                "bars_par_1000": round(float(b1000), 2) if pd.notna(b1000) else None,
            }
    return result

@st.cache_data
def load_alternance_data():
    """Charge les donnees d'alternance depuis communes_20k_2023_nb_alternance_26.csv.

    Retourne un dict {nom_ville: {nb_alternance, nb_etudiants, alternance_par_10etudiants}} avec:
    - Dep_nbAlternance_2026-Janv: nombre de contrats d'alternance en 2026
    - Dep_nb_etudiants_total: nombre d'etudiants en 2026
    - Dep_alternance_par_10etudiants_2026: nombre de contrats d'alternance en 2026 pour 10 d'etudiants

    Source : poem.travail-emploi.gouv.fr.
    """
    path = DATA_DIR / "communes_20k_2023_nb_alternance_26.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    result = {}
    for _, row in df.iterrows():
        ville = str(row.get("Nom de la commune", "")).strip()
        if not ville:
            continue
        alternance = row.get("Dep_nbAlternance_2026-Janv")
        etudiants = row.get("Dep_nb_etudiants_total")
        alternancep10 = row.get("Dep_alternance_par_10etudiants_2026")
        if pd.notna(alternance):
            result[ville] = {
                "nb_alternance": int(float(str(alternance).replace(",", "."))),
                "nb_etudiants": int(float(str(etudiants).replace(",", "."))) if pd.notna(etudiants) else None,
                "alternance_par_10etudiants": round(float(str(alternancep10).replace(",", ".")), 2) if pd.notna(alternancep10) else None,
            }
    return result

@st.cache_data
def load_secteurs_data():
    """Charge les donnees de Secteurs d'activités depuis communes_20k_avec_secteurs_activites_2025_final.csv.

    Retourne un dict {nom_ville: {secteur: nb_emplois}} avec le nombre d'entreprises par secteur.

    Source : INSEE / data.gouv.fr, Secteurs d'activités 2025.
    """
    path = DATA_DIR / "communes_20k_avec_secteurs_activites_2025_final.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    # Colonnes secteurs = toutes sauf Nom de la commune et code commune
    secteur_cols = [c for c in df.columns if c not in ("Nom de la commune", "code commune")]
    result = {}
    for _, row in df.iterrows():
        ville = str(row.get("Nom de la commune", "")).strip()
        if not ville:
            continue
        secteurs = {}
        has_data = False
        for col in secteur_cols:
            val = row.get(col)
            if pd.notna(val):
                n = int(float(str(val).replace(" ", "")))
                if n > 0:
                    secteurs[col] = n
                    has_data = True
        if has_data:
            result[ville] = secteurs
    return result

@st.cache_data
def load_securite_data():
    """Charge les donnees de score securite depuis communes_20k_avec_score_securite_2025_final.csv.

    Retourne un dict {nom_ville: score_securite} (entier, echelle 0-100).

    Source : data.gouv.fr, score de securite 2025.
    """
    path = DATA_DIR / "communes_20k_avec_score_securite_2025_final.csv"
    if not path.exists():
        return {}
    df = pd.read_csv(path, sep=";", encoding="utf-8-sig")
    df.columns = [c.strip() for c in df.columns]
    result = {}
    for _, row in df.iterrows():
        ville = str(row.get("Nom de la commune", "")).strip()
        if not ville:
            continue
        sc = row.get("score_securite_25")
        if pd.notna(sc):
            result[ville] = int(float(sc))
    return result

def aqi_label(aqi):
    """Retourne un label qualitatif pour l'indice AQI europeen."""
    if aqi is None:
        return ""
    if aqi <= 20:
        return "Bon"
    elif aqi <= 40:
        return "Moyen"
    elif aqi <= 60:
        return "Mediocre"
    elif aqi <= 80:
        return "Mauvais"
    elif aqi <= 100:
        return "Tres mauvais"
    else:
        return "Ext. mauvais"

# Raccourcis pour les noms de Secteurs d'activités (trop longs pour le camembert)
_SECTEUR_SHORT = {
    "Agriculture, sylviculture et pêche": "Agriculture",
    "Fabrication de denrées alimentaires, de boissons et de produits à base de tabac": "Agroalimentaire",
    "Cokéfaction et raffinage": "Raffinage",
    "Fabrication d'équipements électriques, électroniques, informatiques\xa0: fabrication de machines": "Équip. électr./info.",
    "Fabrication de matériels de transport": "Matériels transport",
    "Fabrication d'autres produits industriels": "Autres prod. indust.",
    "Industries extractives, énergie, eau, gestion des déchets et dépollution": "Énergie/Déchets",
    "Construction": "Construction",
    "Commerce : réparation d'automobiles et de motocycles": "Commerce",
    "Transports et entreposage": "Transports",
    "Hébergement et restauration": "Hébergement/Restauration",
    "Information et communication": "Info./Communication",
    "Activités financières et d'assurance": "Finance/Assurance",
    "Activités immobilières": "Immobilier",
    "Activités spécialisées, scientifiques et techniques et activités de services administratifs et de soutien": "Services techn./admin.",
    "Administration publique, enseignement, santé humaine et action sociale": "Admin./Enseig./Santé",
    "Autres activités de services": "Services divers",
}

def build_pie_data(secteurs_dict, top_n=4):
    """Construit les donnees pour un camembert: top N secteurs + Autres secteurs.
    "Autres activites de services" est toujours fusionne dans "Autres secteurs".
    Retourne (labels, values) ou (None, None) si pas de donnees.
    """
    if not secteurs_dict:
        return None, None
    # Toujours fusionner "Autres activites de services" dans les restes
    AUTRES_KEY = "Autres activités de services"
    sorted_items = sorted(secteurs_dict.items(), key=lambda x: x[1], reverse=True)
    labels = []
    values = []
    autres = 0
    for i, (name, val) in enumerate(sorted_items):
        if name == AUTRES_KEY:
            autres += val
            continue
        short = _SECTEUR_SHORT.get(name, name[:20])
        if len(labels) < top_n:
            labels.append(short)
            values.append(val)
        else:
            autres += val
    if autres > 0:
        labels.append("Autres secteurs")
        values.append(autres)
    return labels, values

@st.cache_data(ttl=86400)
def get_climat_annuel(lat, lon):
    """Recupere les moyennes mensuelles (temperature, precipitation) via Open-Meteo Historical API.
    Utilise ERA5 reanalysis sur les 5 dernieres annees (daily), puis agregation par mois.
    Retourne dict {mois: {tmax, tmin, precip}} ou None.
    """
    try:
        url = (f"https://archive-api.open-meteo.com/v1/archive"
               f"?latitude={lat}&longitude={lon}"
               f"&start_date=2020-01-01&end_date=2024-12-31"
               f"&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
               f"&timezone=Europe/Paris")
        r = requests.get(url, timeout=30)
        if r.status_code != 200:
            return None
        data = r.json()
        daily = data.get("daily", {})
        time_arr = daily.get("time", [])
        tmax_arr = daily.get("temperature_2m_max", [])
        tmin_arr = daily.get("temperature_2m_min", [])
        precip_arr = daily.get("precipitation_sum", [])
        if not time_arr:
            return None
        # Grouper par mois (1-12) sur les 5 ans
        mois_data = {m: {"tmax": [], "tmin": [], "precip": []} for m in range(1, 13)}
        for i, t in enumerate(time_arr):
            m = int(t.split("-")[1])
            if i < len(tmax_arr) and tmax_arr[i] is not None:
                mois_data[m]["tmax"].append(tmax_arr[i])
            if i < len(tmin_arr) and tmin_arr[i] is not None:
                mois_data[m]["tmin"].append(tmin_arr[i])
            if i < len(precip_arr) and precip_arr[i] is not None:
                mois_data[m]["precip"].append(precip_arr[i])
        # Moyennes (temperature) et totaux (precipitations)
        result = {}
        noms_mois = ["Jan", "Fev", "Mar", "Avr", "Mai", "Jun",
                     "Jul", "Aou", "Sep", "Oct", "Nov", "Dec"]
        for m in range(1, 13):
            d = mois_data[m]
            result[m] = {
                "nom": noms_mois[m - 1],
                "tmax": round(sum(d["tmax"]) / len(d["tmax"]), 1) if d["tmax"] else None,
                "tmin": round(sum(d["tmin"]) / len(d["tmin"]), 1) if d["tmin"] else None,
                "precip": round(sum(d["precip"]) / 5, 1) if d["precip"] else None,
            }
        return result
    except Exception:
        pass
    return None

@st.cache_data(ttl=3600)
def get_previsions_7_jours(lat, lon):
    try:
        url = (f"https://api.open-meteo.com/v1/forecast"
               f"?latitude={lat}&longitude={lon}"
               f"&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_sum"
               f"&timezone=Europe/Paris&forecast_days=7")
        r = requests.get(url, timeout=10)
        if r.status_code == 200:
            return r.json()
    except Exception:
        pass
    return None

@st.cache_data(ttl=86400)
def get_wikipedia_image(city_name):
    """Fetch city photo from url_cities_final.csv (pre-cached Wikipedia images)."""
    wiki_images = load_wiki_images()
    # Try exact match first
    url = wiki_images.get(city_name)
    if url:
        return url
    # Try without parenthetical suffix (e.g. "Saint-Denis (Seine-Saint-Denis)" -> "Saint-Denis")
    url = wiki_images.get(city_name.strip())
    return url

def code_meteo(code):
    codes = {
        0: "Ciel dégagé",
        1: "Majoritairement dégagé",
        2: "Partiellement nuageux",
        3: "Très nuageux",
        45: "Brouillard",
        48: "Brouillard givrant",
        51: "Bruine légère",
        53: "Bruine modérée",
        55: "Bruine dense",
        61: "Pluie légère",
        63: "Pluie modérée",
        65: "Pluie forte",
        71: "Neige légère",
        73: "Neige modérée",
        75: "Neige forte",
        80: "Averses légères",
        81: "Averses modérées",
        82: "Averses violentes",
        95: "Orage",
        96: "Orage avec grêle",
        99: "Orage violent"
    }
    return codes.get(code, f"Code {code}")

# ============================================================================
# HTML HELPERS
# ============================================================================

def ind_card(label, value, sub, icon="", variant=""):
    icon_html = f'<span class="ind-icon">{icon}</span>' if icon else ""
    return f"""
    <div class="ind-card {'v2' if variant=='v2' else ''}">
        <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:10px;">
            <div>
                {icon_html}
                <div class="ind-label">{label}</div>
                <div class="ind-sub">{sub}</div>
            </div>
            <div class="ind-value" style="font-size:2.5rem;line-height:1;text-align:right;">{value}</div>
        </div>
    </div>
    """

def fmt_num(n):
    """Format number with K/M suffix."""
    if n is None:
        return "N/A"
    if n >= 1_000_000:
        return f"{n/1_000_000:.1f}M".rstrip('0').rstrip('.')
    if n >= 1_000:
        return f"{n/1_000:.0f}K"
    return str(n)

def ind_card_combo(icon1, label1, value1, sub1, icon2, label2, value2, sub2, variant=""):
    return f"""
    <div class="ind-card {'v2' if variant=='v2' else ''}">
        <div style="display:flex;gap:12px;">
            <div style="flex:1;">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;">
                    <div>
                        <span class="ind-icon">{icon1}</span>
                        <div class="ind-label">{label1}</div>
                        <div class="ind-sub">{sub1}</div>
                    </div>
                    <div class="ind-value" style="font-size:2.2rem;line-height:1;text-align:right;">{value1}</div>
                </div>
            </div>
            <div style="width:1px;background:#e8e4de;margin:4px 0;"></div>
            <div style="flex:1;">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:8px;">
                    <div>
                        <span class="ind-icon">{icon2}</span>
                        <div class="ind-label">{label2}</div>
                        <div class="ind-sub">{sub2}</div>
                    </div>
                    <div class="ind-value" style="font-size:2.2rem;line-height:1;text-align:right;">{value2}</div>
                </div>
            </div>
        </div>
    </div>
    """

def ind_card_combo3(icon1, label1, value1, sub1, icon2, label2, value2, sub2, icon3, label3, value3, sub3, variant=""):
    return f"""
    <div class="ind-card {'v2' if variant=='v2' else ''}">
        <div style="display:flex;gap:10px;">
            <div style="flex:1;">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:6px;">
                    <div>
                        <span class="ind-icon">{icon1}</span>
                        <div class="ind-label">{label1}</div>
                        <div class="ind-sub">{sub1}</div>
                    </div>
                    <div class="ind-value" style="font-size:1.8rem;line-height:1;text-align:right;">{value1}</div>
                </div>
            </div>
            <div style="width:1px;background:#e8e4de;margin:4px 0;"></div>
            <div style="flex:1;">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:6px;">
                    <div>
                        <span class="ind-icon">{icon2}</span>
                        <div class="ind-label">{label2}</div>
                        <div class="ind-sub">{sub2}</div>
                    </div>
                    <div class="ind-value" style="font-size:1.8rem;line-height:1;text-align:right;">{value2}</div>
                </div>
            </div>
            <div style="width:1px;background:#e8e4de;margin:4px 0;"></div>
            <div style="flex:1;">
                <div style="display:flex;align-items:flex-start;justify-content:space-between;gap:6px;">
                    <div>
                        <span class="ind-icon">{icon3}</span>
                        <div class="ind-label">{label3}</div>
                        <div class="ind-sub">{sub3}</div>
                    </div>
                    <div class="ind-value" style="font-size:1.8rem;line-height:1;text-align:right;">{value3}</div>
                </div>
            </div>
        </div>
    </div>
    """

# ============================================================================
# COORDONNEES (complement CSV - non disponibles dans les fichiers INSEE)
# ============================================================================

COORD_CITIES = {
    "Paris": (48.8566, 2.3522),
    "Marseille": (43.2965, 5.3698),
    "Lyon": (45.7640, 4.8357),
    "Toulouse": (43.6047, 1.4442),
    "Nice": (43.7102, 7.2620),
    "Nantes": (47.2184, -1.5536),
    "Montpellier": (43.6119, 3.8772),
    "Strasbourg": (48.5734, 7.7521),
    "Bordeaux": (44.8378, -0.5792),
    "Lille": (50.6292, 3.0573),
    "Rennes": (48.1173, -1.6778),
    "Reims": (49.2583, 4.0317),
    "Grenoble": (45.1885, 5.7245),
    "Saint-Étienne": (45.4397, 4.3872),
    "Dijon": (47.3220, 5.0415),
    "Angers": (47.4784, -0.5632),
    "Nîmes": (43.8388, 4.3602),
    "Clermont-Ferrand": (45.7772, 3.0826),
    "Aix-en-Provence": (43.5299, 5.4474),
    "Brest": (48.3904, -4.4861),
    "Tours": (47.3941, 0.6848),
    "Limoges": (45.8517, 1.2576),
    "Metz": (49.1194, 6.1764),
    "Orléans": (47.9029, 1.9093),
    "Rouen": (49.4432, 1.0993),
    "Caen": (49.1829, -0.3707),
    "Nancy": (48.6921, 6.1844),
    "La Rochelle": (46.1601, -1.1511),
    "Versailles": (48.8014, 2.1307),
    "Le Havre": (50.6278, 0.1779),
    "Saint-Denis": (48.9352, 2.3580),
    "Villeurbanne": (45.7714, 4.8853),
    "Annecy": (45.8992, 6.1294),
    "Le Mans": (47.9960, 0.1963),
    "Amiens": (49.8942, 2.2957),
    "Mulhouse": (47.7508, 7.3359),
    "Perpignan": (42.6888, 2.8947),
    "Besançon": (47.2378, 6.0240),
    "Oran": (35.6969, -0.6331),
}

# ============================================================================
# MAIN
# ============================================================================

def main():
    villes_df = load_villes_data()
    liste_villes = sorted(villes_df['ville'].tolist())

    # ========================================================================
    # TITLE
    # ========================================================================
    st.markdown(
        '<div style="text-align:center;margin:0 0 20px 0;">'
        '<i class="fas fa-map-marked-alt" style="font-size:2.8rem;color:#5d7a8c;display:block;margin-bottom:10px;"></i>'
        '<p style="font-size:1.75rem;font-weight:700;color:#2c3e50;margin:0;letter-spacing:0.3px;">'
        'Quelle ville choisir pour mon master ?'
        '</p>'
        '</div>',
        unsafe_allow_html=True
    )

    # ========================================================================
    # TOP SECTION: City photo cards with selectors
    # ========================================================================
    col_c1, col_c2 = st.columns(2)

    for idx, (col, init_city) in enumerate([(col_c1, "Paris"), (col_c2, "Lyon")]):
        variant = "v2" if idx == 1 else ""

        with col:
            # Selector inside card
            st.markdown('<div class="city-card">', unsafe_allow_html=True)
            st.markdown('<div class="card-selector-wrap">', unsafe_allow_html=True)
            sel = st.selectbox(
                "Ville", liste_villes,
                index=liste_villes.index(init_city) if init_city in liste_villes else 0,
                label_visibility="collapsed", key=f"city_sel_{idx}"
            )
            st.markdown('</div>', unsafe_allow_html=True)

            city_img = get_wikipedia_image(sel)
            if city_img:
                st.markdown(f'<div class="city-card-img"><img src="{city_img}" alt="{sel}"/></div>', unsafe_allow_html=True)
            else:
                # Fallback gradient
                st.markdown(
                    f'<div style="height:160px;background:linear-gradient(135deg,{"#34495e" if idx==0 else "#5d4e37"},{"#5d7a8c" if idx==0 else "#a67c5b"});display:flex;align-items:center;justify-content:center;">'
                    f'<span style="color:white;font-size:3rem;font-weight:700;opacity:0.25;">{sel[0]}</span>'
                    f'</div>',
                    unsafe_allow_html=True
                )

            row = villes_df[villes_df['ville'] == sel].iloc[0]
            st.markdown(
                f'<div class="city-card-overlay">'
                f'<p class="city-card-name">{sel}</p>'
                f'<p class="city-card-region">{row["region"]}</p>'
                f'</div>',
                unsafe_allow_html=True
            )
            st.markdown('</div>', unsafe_allow_html=True)

    # Get selected city from session state (default fallback)
    # We use the key names from above
    sel1 = st.session_state.get("city_sel_0", "Paris")
    sel2 = st.session_state.get("city_sel_1", "Lyon")

    v1_row = villes_df[villes_df['ville'] == sel1].iloc[0]
    v2_row = villes_df[villes_df['ville'] == sel2].iloc[0]
    # Coordonnees depuis le dict local (non presentes dans le CSV INSEE)
    lat1, lon1 = COORD_CITIES.get(sel1, (0, 0))
    lat2, lon2 = COORD_CITIES.get(sel2, (0, 0))
    # Construire les dicts de donnees a partir des sources CSV/API
    d1, d2 = {}, {}
    # Etudiants data
    etudiants = load_etudiants_data()
    e1 = etudiants.get(sel1)
    e2 = etudiants.get(sel2)
    if e1:
        d1["nb_etudiants"] = e1["nb_etudiants"]
        d1["pct_etudiants"] = e1["pct_etudiants"]
    if e2:
        d2["nb_etudiants"] = e2["nb_etudiants"]
        d2["pct_etudiants"] = e2["pct_etudiants"]
    # Loyer data from Carte des loyers 2025
    loyers = load_loyers_data()
    l1 = loyers.get(sel1)
    l2 = loyers.get(sel2)
    if l1:
        d1["loyer_studio_centre"] = l1["loyer_studio_centre"]
        d1["loyer_studio_peri"] = l1["loyer_studio_peri"]
        d1["loyer_coloc"] = l1["loyer_coloc"]
    if l2:
        d2["loyer_studio_centre"] = l2["loyer_studio_centre"]
        d2["loyer_studio_peri"] = l2["loyer_studio_peri"]
        d2["loyer_coloc"] = l2["loyer_coloc"]
    # Alternance data
    alternance_data = load_alternance_data()
    alt1 = alternance_data.get(sel1)
    alt2 = alternance_data.get(sel2)
    if alt1:
        d1["offres_stage_alternance"] = alt1["nb_alternance"]
        d1["alternance_par_10etudiants"] = alt1["alternance_par_10etudiants"]  
    if alt2:
        d2["offres_stage_alternance"] = alt2["nb_alternance"]
        d2["alternance_par_10etudiants"] = alt2["alternance_par_10etudiants"]
    # Salaires data from INSEE (Base Tous salaries 2023)
    salaires = load_salaires_data()
    s1 = salaires.get(sel1)
    s2 = salaires.get(sel2)
    if s1:
        d1["salaire_2023"] = s1["salaire_2023"]
        d1["salaire_evol"] = s1["salaire_evol"]
    if s2:
        d2["salaire_2023"] = s2["salaire_2023"]
        d2["salaire_evol"] = s2["salaire_evol"]
    # Ensoleillement data from Open-Meteo (all cities)
    ensoleillement = load_ensoleillement_data()
    ens1 = ensoleillement.get(sel1)
    ens2 = ensoleillement.get(sel2)
    if ens1:
        d1["ensoleillement_pct"] = round(ens1 / 8760 * 100, 1)
    if ens2:
        d2["ensoleillement_pct"] = round(ens2 / 8760 * 100, 1)
    # Qualite de l'air (AQI europeen) from Open-Meteo Air Quality API
    aqi_data = load_aqi_data()
    aqi1 = aqi_data.get(sel1)
    aqi2 = aqi_data.get(sel2)
    if aqi1 is not None:
        d1["aqi_moyen"] = aqi1
    if aqi2 is not None:
        d2["aqi_moyen"] = aqi2
    # Taux de chomage departemental 2024
    chomage = load_chomage_data()
    ch1 = chomage.get(sel1)
    ch2 = chomage.get(sel2)
    if ch1 is not None:
        d1["taux_chomage"] = ch1
    if ch2 is not None:
        d2["taux_chomage"] = ch2
    # Score securite 2025
    securite = load_securite_data()
    sec1 = securite.get(sel1)
    sec2 = securite.get(sel2)
    if sec1 is not None:
        d1["score_securite"] = sec1
    if sec2 is not None:
        d2["score_securite"] = sec2
    # Age moyen 2025
    age_moyen = load_age_moyen_data()
    age1 = age_moyen.get(sel1)
    age2 = age_moyen.get(sel2)
    if age1 is not None:
        d1["age_moyen"] = age1
    if age2 is not None:
        d2["age_moyen"] = age2
    # Lieux culturels 2025
    culture = load_culture_data()
    cul1 = culture.get(sel1)
    cul2 = culture.get(sel2)
    if cul1:
        d1["nb_lieux_culturels"] = cul1["nb_lieux"]
        d1["densite_culturelle"] = cul1["densite"]
    if cul2:
        d2["nb_lieux_culturels"] = cul2["nb_lieux"]
        d2["densite_culturelle"] = cul2["densite"]
    # Restaurants & Bars
    restos = load_restaurants_data()
    r1 = restos.get(sel1)
    r2 = restos.get(sel2)
    if r1:
        d1["nb_restaurants"] = r1["nb_restaurants"]
        d1["nb_bars"] = r1["nb_bars"]
        d1["rest_par_1000"] = r1["rest_par_1000"]
        d1["bars_par_1000"] = r1["bars_par_1000"]
    if r2:
        d2["nb_restaurants"] = r2["nb_restaurants"]
        d2["nb_bars"] = r2["nb_bars"]
        d2["rest_par_1000"] = r2["rest_par_1000"]
        d2["bars_par_1000"] = r2["bars_par_1000"]
    # Secteurs d'activités
    secteurs = load_secteurs_data()
    if secteurs.get(sel1):
        d1["secteurs"] = secteurs[sel1]
    if secteurs.get(sel2):
        d2["secteurs"] = secteurs[sel2]

    # ========================================================================
    # TABS
    # ========================================================================
    st.markdown("")
    tabs = st.tabs(["Vision globale", "Qualité de vie", "Météo", "Scores"])

    # ========================================================================
    # TAB 1: VISION GLOBALE
    # ========================================================================
    with tabs[0]:
        # ======================================================================
        # SECTION 1: Population & Etudiants
        # ======================================================================
        st.markdown('<p class="sec-label">Population &amp; Etudiants</p>', unsafe_allow_html=True)
        r1c1, r1c2 = st.columns(2)
        pct1 = f"{d1['pct_etudiants']}%" if d1 and "pct_etudiants" in d1 else "N/A"
        pct2 = f"{d2['pct_etudiants']}%" if d2 and "pct_etudiants" in d2 else "N/A"
        with r1c1:
            st.markdown(ind_card_combo(
                '<i class="fas fa-users"></i>', f"Population — {sel1}",
                fmt_num(v1_row['population']), f"{v1_row['region']}",
                '<i class="fas fa-graduation-cap"></i>', f"% Etudiants — {sel1}",
                pct1, f"{fmt_num(d1['nb_etudiants'])} etudiants" if d1 and "nb_etudiants" in d1 else "N/A",
                variant=""
            ), unsafe_allow_html=True)
        with r1c2:
            st.markdown(ind_card_combo(
                '<i class="fas fa-users"></i>', f"Population — {sel2}",
                fmt_num(v2_row['population']), f"{v2_row['region']}",
                '<i class="fas fa-graduation-cap"></i>', f"% Etudiants — {sel2}",
                pct2, f"{fmt_num(d2['nb_etudiants'])} etudiants" if d2 and "nb_etudiants" in d2 else "N/A",
                variant="v2"
            ), unsafe_allow_html=True)
        # Row 2: Age moyen
        age1_val = d1.get("age_moyen")
        age2_val = d2.get("age_moyen")
        age1_str = f"{age1_val} ans" if age1_val is not None else "N/A"
        age1_sub = "Age moyen 2025" if age1_val is not None else "Source a venir"
        age2_str = f"{age2_val} ans" if age2_val is not None else "N/A"
        age2_sub = "Age moyen 2025" if age2_val is not None else "Source a venir"
        r1c3, r1c4 = st.columns(2)
        with r1c3:
            st.markdown(ind_card(
                f"Age moyen — {sel1}",
                age1_str, age1_sub,
                icon='<i class="fas fa-cake-candles"></i>',
                variant=""
            ), unsafe_allow_html=True)
        with r1c4:
            st.markdown(ind_card(
                f"Age moyen — {sel2}",
                age2_str, age2_sub,
                icon='<i class="fas fa-cake-candles"></i>',
                variant="v2"
            ), unsafe_allow_html=True)

        # ======================================================================
        # SECTION 2: Revenus & Emploi
        # ======================================================================
        st.markdown('<p class="sec-label">Revenus &amp; Emploi</p>', unsafe_allow_html=True)
        sal1_val = d1.get("salaire_2023")
        sal2_val = d2.get("salaire_2023")
        sal1_str = f"{sal1_val} €" if sal1_val else "N/A"
        sal2_str = f"{sal2_val} €" if sal2_val else "N/A"
        sal1_evol = d1.get("salaire_evol")
        sal2_evol = d2.get("salaire_evol")
        # Alternance
        alt1_val = d1.get("alternance_par_10etudiants")
        alt2_val = d2.get("alternance_par_10etudiants")
        alt1_str = f"{alt1_val}" if alt1_val is not None else "N/A"
        alt2_str = f"{alt2_val}" if alt2_val is not None else "N/A"
        alt1_sub = "Alternance pour 10 etudiants" if alt1_val is not None else "Source a venir"
        alt2_sub = "Alternance pour 10 etudiants" if alt2_val is not None else "Source a venir"
        # Chomage
        ch1_val = d1.get("taux_chomage")
        ch2_val = d2.get("taux_chomage")
        ch1_str = f"{ch1_val}%" if ch1_val is not None else "N/A"
        ch1_sub = "Taux départemental 2024" if ch1_val is not None else "Source a venir"
        ch2_str = f"{ch2_val}%" if ch2_val is not None else "N/A"
        ch2_sub = "Taux départemental 2024" if ch2_val is not None else "Source a venir"
        # Row 1: Salaire + Chomage (combo)
        # Row 1: Salaire + Evolution salaire (combo)
        evol1_str = f"{sal1_evol*100:+.1f}%" if sal1_evol is not None else "N/A"
        evol2_str = f"{sal2_evol*100:+.1f}%" if sal2_evol is not None else "N/A"
        evol1_sub = "2023 vs 2022" if sal1_evol is not None else "Source a venir"
        evol2_sub = "2023 vs 2022" if sal2_evol is not None else "Source a venir"
        r2c3, r2c4 = st.columns(2)
        r2c1, r2c2 = st.columns(2)
        with r2c1:
            st.markdown(ind_card_combo(
                '<i class="fas fa-euro-sign"></i>', f"Salaire 2023 — {sel1}",
                sal1_str, "Net mensuel moyen EQTP",
                '<i class="fas fa-chart-line"></i>', f"Evolution salaire",
                evol1_str, evol1_sub,
                variant=""
            ), unsafe_allow_html=True)
        with r2c2:
            st.markdown(ind_card_combo(
                '<i class="fas fa-euro-sign"></i>', f"Salaire 2023 — {sel2}",
                sal2_str, "Net mensuel moyen EQTP",
                '<i class="fas fa-chart-line"></i>', f"Evolution salaire",
                evol2_str, evol2_sub,
                variant="v2"
            ), unsafe_allow_html=True)
        # Row 2: Alternance + Chomage (combo)
        r2c3, r2c4 = st.columns(2)
        with r2c3:
            st.markdown(ind_card_combo(
                '<i class="fas fa-chart-line"></i>', f"Taux de chomage — {sel1}",
                ch1_str, ch1_sub,
                '<i class="fas fa-handshake"></i>', f"Alternance — {sel1}",
                alt1_str, alt1_sub,
                variant=""
            ), unsafe_allow_html=True)
        with r2c4:
            # st.markdown(ind_card(
            #     f"Evolution salaire — {sel2}",
            #     evol2_str, evol2_sub,
            #     icon='<i class="fas fa-arrow-trend-up"></i>',
            #     variant="v2"
            # ), unsafe_allow_html=True)
            st.markdown(ind_card_combo(
                '<i class="fas fa-euro-sign"></i>', f"Taux de chomage — {sel2}",
                ch2_str, ch2_sub,
                '<i class="fas fa-handshake"></i>', f"Alternance — {sel2}",
                alt2_str, alt2_sub,
                variant=""
            ), unsafe_allow_html=True)

        # Row 3: Secteurs d'activités (camembert top 4 + Autres)
        sec1_data = d1.get("secteurs")
        sec2_data = d2.get("secteurs")
        if sec1_data or sec2_data:
            r3c1, r3c2 = st.columns(2)
            with r3c1:
                labels1, values1 = build_pie_data(sec1_data)
                if labels1:
                    fig1 = go.Figure(data=[go.Pie(
                        labels=labels1, values=values1,
                        hole=0.4,
                        marker=dict(colors=['#5d7a8c','#7d9aac','#9dbacc','#bddaec','#d5d5d5']),
                        textinfo='label+percent',
                        textposition='outside',
                        textfont=dict(size=10, color='#2c3e50'),
                        hovertemplate='<b>%{label}</b><br>%{value:,} entreprises<br>%{percent}<extra></extra>',
                        pull=[0.03]*len(labels1),
                    )])
                    fig1.update_layout(
                        title=dict(text=f"Secteurs d'activite — {sel1}", font=dict(size=13, color='#2c3e50')),
                        height=260, margin=dict(t=40, b=10, l=10, r=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                    )
                    st.plotly_chart(fig1, use_container_width=True)
            with r3c2:
                labels2, values2 = build_pie_data(sec2_data)
                if labels2:
                    fig2 = go.Figure(data=[go.Pie(
                        labels=labels2, values=values2,
                        hole=0.4,
                        marker=dict(colors=['#a67c5b','#bf9a78','#d4b895','#e9d6b2','#d5d5d5']),
                        textinfo='label+percent',
                        textposition='outside',
                        textfont=dict(size=10, color='#2c3e50'),
                        hovertemplate='<b>%{label}</b><br>%{value:,} entreprises<br>%{percent}<extra></extra>',
                        pull=[0.03]*len(labels2),
                    )])
                    fig2.update_layout(
                        title=dict(text=f"Secteurs d'activite — {sel2}", font=dict(size=13, color='#2c3e50')),
                        height=260, margin=dict(t=40, b=10, l=10, r=10),
                        paper_bgcolor='rgba(0,0,0,0)',
                        showlegend=False,
                    )
                    st.plotly_chart(fig2, use_container_width=True)


        # ======================================================================
        # SECTION 3: Logement
        # ======================================================================
        st.markdown('<p class="sec-label">Logement</p>', unsafe_allow_html=True)
        r4c1, r4c2 = st.columns(2)
        # Loyer: from Carte des loyers CSV (via d1/d2)
        def get_loyer_info(d):
            """Get loyer display info from data dict."""
            if d and "loyer_studio_centre" in d:
                lo = (d['loyer_studio_centre'] + d['loyer_studio_peri']) / 2
                return (
                    f"{fmt_num(int(lo))} €/mois",
                    f"Centre {fmt_num(d['loyer_studio_centre'])}€ / Péri {fmt_num(d['loyer_studio_peri'])}€"
                )
            return "N/A", ""
        lo1_str, lo1_sub = get_loyer_info(d1)
        lo2_str, lo2_sub = get_loyer_info(d2)
        with r4c1:
            st.markdown(ind_card(
                f"Loyer moyen — {sel1}",
                lo1_str, lo1_sub,
                icon='<i class="fas fa-home"></i>',
                variant=""
            ), unsafe_allow_html=True)
        with r4c2:
            st.markdown(ind_card(
                f"Loyer moyen — {sel2}",
                lo2_str, lo2_sub,
                icon='<i class="fas fa-home"></i>',
                variant="v2"
            ), unsafe_allow_html=True)


    # ========================================================================
    # TAB 2: QUALITE DE VIE
    # ========================================================================
    with tabs[1]:
        # Section: Ensoleillement & Qualite de l'air
        st.markdown('<p class="sec-label">Ensoleillement &amp; Qualite de l\'air</p>', unsafe_allow_html=True)
        qv1c1, qv1c2 = st.columns(2)
        if ens1:
            sol1_pct = round(ens1 / 8760 * 100, 1)
            sol1 = f"{sol1_pct}%"
            sol1_sub = f"{ens1}h/an (moy. 2020-2024)"
        else:
            sol1 = "N/A"
            sol1_sub = ""
        if ens2:
            sol2_pct = round(ens2 / 8760 * 100, 1)
            sol2 = f"{sol2_pct}%"
            sol2_sub = f"{ens2}h/an (moy. 2020-2024)"
        else:
            sol2 = "N/A"
            sol2_sub = ""
        aqi1_val = d1.get("aqi_moyen")
        aqi2_val = d2.get("aqi_moyen")
        aqi1_str = str(aqi1_val) if aqi1_val is not None else "N/A"
        aqi1_sub = aqi_label(aqi1_val) + " (moy. 2023-2024)" if aqi1_val is not None else "Source a venir"
        aqi2_str = str(aqi2_val) if aqi2_val is not None else "N/A"
        aqi2_sub = aqi_label(aqi2_val) + " (moy. 2023-2024)" if aqi2_val is not None else "Source a venir"
        with qv1c1:
            st.markdown(ind_card_combo(
                '<i class="fas fa-sun"></i>', f"Ensoleillement — {sel1}",
                sol1, sol1_sub,
                '<i class="fas fa-wind"></i>', f"Qualite air — {sel1}",
                aqi1_str, aqi1_sub,
                variant=""
            ), unsafe_allow_html=True)
        with qv1c2:
            st.markdown(ind_card_combo(
                '<i class="fas fa-sun"></i>', f"Ensoleillement — {sel2}",
                sol2, sol2_sub,
                '<i class="fas fa-wind"></i>', f"Qualite air — {sel2}",
                aqi2_str, aqi2_sub,
                variant="v2"
            ), unsafe_allow_html=True)


        # Section: Lieux culturels
        st.markdown('<p class="sec-label">Lieux culturels</p>', unsafe_allow_html=True)
        # Row 1: Nombre de lieux
        nb1_str = str(d1.get("nb_lieux_culturels", "N/A")) if d1.get("nb_lieux_culturels") is not None else "N/A"
        nb2_str = str(d2.get("nb_lieux_culturels", "N/A")) if d2.get("nb_lieux_culturels") is not None else "N/A"
        cc1, cc2 = st.columns(2)
        with cc1:
            st.markdown(ind_card(
                f"Nb lieux — {sel1}",
                nb1_str, "Lieux culturels recensés",
                icon='<i class="fas fa-landmark"></i>',
                variant=""
            ), unsafe_allow_html=True)
        with cc2:
            st.markdown(ind_card(
                f"Nb lieux — {sel2}",
                nb2_str, "Lieux culturels recensés",
                icon='<i class="fas fa-landmark"></i>',
                variant="v2"
            ), unsafe_allow_html=True)
        # Row 2: Densite culturelle (lieux/1000 hab)
        den1 = d1.get("densite_culturelle")
        den2 = d2.get("densite_culturelle")
        den1_str = f"{den1}" if den1 is not None else "N/A"
        den1_sub = "Lieux / 1 000 hab." if den1 is not None else "Source a venir"
        den2_str = f"{den2}" if den2 is not None else "N/A"
        den2_sub = "Lieux / 1 000 hab." if den2 is not None else "Source a venir"
        cc3, cc4 = st.columns(2)
        with cc3:
            st.markdown(ind_card(
                f"Densite culturelle — {sel1}",
                den1_str, den1_sub,
                icon='<i class="fas fa-chart-bar"></i>',
                variant=""
            ), unsafe_allow_html=True)
        with cc4:
            st.markdown(ind_card(
                f"Densite culturelle — {sel2}",
                den2_str, den2_sub,
                icon='<i class="fas fa-chart-bar"></i>',
                variant="v2"
            ), unsafe_allow_html=True)

        # Section: Restaurants & Bars
        st.markdown('<p class="sec-label">Restaurants &amp; Bars</p>', unsafe_allow_html=True)
        # Row 1: Restaurants + Bars (combo)
        rest1 = d1.get("nb_restaurants")
        rest2 = d2.get("nb_restaurants")
        bars1 = d1.get("nb_bars")
        bars2 = d2.get("nb_bars")
        rest1_str = str(rest1) if rest1 is not None else "N/A"
        rest2_str = str(rest2) if rest2 is not None else "N/A"
        bars1_str = str(bars1) if bars1 is not None else "N/A"
        bars2_str = str(bars2) if bars2 is not None else "N/A"
        rc1, rc2 = st.columns(2)
        with rc1:
            st.markdown(ind_card_combo(
                '<i class="fas fa-utensils"></i>', f"Restaurants — {sel1}",
                rest1_str, "Etablissements recensés",
                '<i class="fas fa-wine-glass"></i>', f"Bars — {sel1}",
                bars1_str, "Etablissements recensés",
                variant=""
            ), unsafe_allow_html=True)
        with rc2:
            st.markdown(ind_card_combo(
                '<i class="fas fa-utensils"></i>', f"Restaurants — {sel2}",
                rest2_str, "Etablissements recensés",
                '<i class="fas fa-wine-glass"></i>', f"Bars — {sel2}",
                bars2_str, "Etablissements recensés",
                variant="v2"
            ), unsafe_allow_html=True)
        # Row 2: Densite restaurants & bars (/1000 hab)
        dr1 = d1.get("rest_par_1000")
        dr2 = d2.get("rest_par_1000")
        db1 = d1.get("bars_par_1000")
        db2 = d2.get("bars_par_1000")
        dr1_str = f"{dr1}" if dr1 is not None else "N/A"
        dr2_str = f"{dr2}" if dr2 is not None else "N/A"
        db1_str = f"{db1}" if db1 is not None else "N/A"
        db2_str = f"{db2}" if db2 is not None else "N/A"
        dr1_sub = "Rest. / 1 000 hab." if dr1 is not None else "Source a venir"
        dr2_sub = "Rest. / 1 000 hab." if dr2 is not None else "Source a venir"
        db1_sub = "Bars / 1 000 hab." if db1 is not None else "Source a venir"
        db2_sub = "Bars / 1 000 hab." if db2 is not None else "Source a venir"
        rc3, rc4 = st.columns(2)
        with rc3:
            st.markdown(ind_card_combo(
                '<i class="fas fa-utensils"></i>', f"Densite rest. — {sel1}",
                dr1_str, dr1_sub,
                '<i class="fas fa-wine-glass"></i>', f"Densite bars — {sel1}",
                db1_str, db1_sub,
                variant=""
            ), unsafe_allow_html=True)
        with rc4:
            st.markdown(ind_card_combo(
                '<i class="fas fa-utensils"></i>', f"Densite rest. — {sel2}",
                dr2_str, dr2_sub,
                '<i class="fas fa-wine-glass"></i>', f"Densite bars — {sel2}",
                db2_str, db2_sub,
                variant="v2"
            ), unsafe_allow_html=True)

        # Section: Securite
        st.markdown('<p class="sec-label">Securite</p>', unsafe_allow_html=True)
        qv2c1, qv2c2 = st.columns(2)
        sec1_val = d1.get("score_securite")
        sec2_val = d2.get("score_securite")
        sec1_str = f"{sec1_val}/100" if sec1_val is not None else "N/A"
        sec1_sub = "Score 2025" if sec1_val is not None else "Source a venir"
        sec2_str = f"{sec2_val}/100" if sec2_val is not None else "N/A"
        sec2_sub = "Score 2025" if sec2_val is not None else "Source a venir"
        with qv2c1:
            st.markdown(ind_card(
                f"Securite — {sel1}",
                sec1_str, sec1_sub,
                icon='<i class="fas fa-shield-halved"></i>',
                variant=""
            ), unsafe_allow_html=True)
        with qv2c2:
            st.markdown(ind_card(
                f"Securite — {sel2}",
                sec2_str, sec2_sub,
                icon='<i class="fas fa-shield-halved"></i>',
                variant="v2"
            ), unsafe_allow_html=True)

    
    # ========================================================================
    # TAB 3: METEO
    # ========================================================================

    with tabs[2]:
        # ------------------------------------------------------------------
        # Climat a l'annee (moyennes mensuelles sur 5 ans)
        # ------------------------------------------------------------------
        st.markdown('<p class="sec-label">Climat a l\'annee</p>', unsafe_allow_html=True)
        climat1 = get_climat_annuel(lat1, lon1)
        climat2 = get_climat_annuel(lat2, lon2)

        if climat1 or climat2:
            noms_mois = ["Janvier", "Fevrier", "Mars", "Avril", "Mai", "Juin",
                         "Juillet", "Aout", "Septembre", "Octobre", "Novembre", "Decembre"]
            # Filtre mois
            mois_selected = st.selectbox("Mois", options=list(range(1, 13)),
                                         format_func=lambda m: noms_mois[m - 1], index=0)

            # Cards : T max / T moy / T min
            cc1, cc2 = st.columns(2)
            if climat1:
                d1m = climat1[mois_selected]
                tmax1 = d1m["tmax"]
                tmin1 = d1m["tmin"]
                tmoy1 = round((tmax1 + tmin1) / 2, 1) if tmax1 is not None and tmin1 is not None else None
                precip1 = d1m["precip"]
                with cc1:
                    st.markdown(ind_card_combo(
                        '<i class="fas fa-temperature-high"></i>', f"T max — {sel1}",
                        f"{tmax1}C" if tmax1 is not None else "N/A", f"Moy. {noms_mois[mois_selected-1]} 2020-2024",
                        '<i class="fas fa-temperature-low"></i>', f"T min — {sel1}",
                        f"{tmin1}C" if tmin1 is not None else "N/A", f"Moy. {noms_mois[mois_selected-1]} 2020-2024",
                        variant=""
                    ), unsafe_allow_html=True)
                    st.markdown(ind_card(
                        f"Temperature moy. — {sel1}",
                        f"{tmoy1}C" if tmoy1 is not None else "N/A",
                        f"Moy. {noms_mois[mois_selected-1]} 2020-2024",
                        icon='<i class="fas fa-thermometer-half"></i>',
                        variant=""
                    ), unsafe_allow_html=True)
                    st.markdown(ind_card(
                        f"Pluviometrie — {sel1}",
                        f"{precip1} mm" if precip1 is not None else "N/A",
                        f"Moy. {noms_mois[mois_selected-1]} 2020-2024",
                        icon='<i class="fas fa-cloud-rain"></i>',
                        variant=""
                    ), unsafe_allow_html=True)
            if climat2:
                d2m = climat2[mois_selected]
                tmax2 = d2m["tmax"]
                tmin2 = d2m["tmin"]
                tmoy2 = round((tmax2 + tmin2) / 2, 1) if tmax2 is not None and tmin2 is not None else None
                precip2 = d2m["precip"]
                with cc2:
                    st.markdown(ind_card_combo(
                        '<i class="fas fa-temperature-high"></i>', f"T max — {sel2}",
                        f"{tmax2}C" if tmax2 is not None else "N/A", f"Moy. {noms_mois[mois_selected-1]} 2020-2024",
                        '<i class="fas fa-temperature-low"></i>', f"T min — {sel2}",
                        f"{tmin2}C" if tmin2 is not None else "N/A", f"Moy. {noms_mois[mois_selected-1]} 2020-2024",
                        variant="v2"
                    ), unsafe_allow_html=True)
                    st.markdown(ind_card(
                        f"Temperature moy. — {sel2}",
                        f"{tmoy2}C" if tmoy2 is not None else "N/A",
                        f"Moy. {noms_mois[mois_selected-1]} 2020-2024",
                        icon='<i class="fas fa-thermometer-half"></i>',
                        variant="v2"
                    ), unsafe_allow_html=True)
                    st.markdown(ind_card(
                        f"Pluviometrie — {sel2}",
                        f"{precip2} mm" if precip2 is not None else "N/A",
                        f"Moy. {noms_mois[mois_selected-1]} 2020-2024",
                        icon='<i class="fas fa-cloud-rain"></i>',
                        variant="v2"
                    ), unsafe_allow_html=True)
            st.caption("Source climat : Open-Meteo Archive API (ERA5, moy. 2020-2024)")
        else:
            st.info("Climat annuel non disponible.")

        st.markdown("---")

        # ------------------------------------------------------------------
        # Previsions 7 jours
        # ------------------------------------------------------------------
        st.markdown('<p class="sec-label">Previsions 7 jours</p>', unsafe_allow_html=True)
        meteo1 = get_previsions_7_jours(lat1, lon1)
        meteo2 = get_previsions_7_jours(lat2, lon2)

        if meteo1 or meteo2:
            labels = (pd.to_datetime(meteo1['daily']['time']).strftime('%d/%m')
                      if meteo1 else pd.to_datetime(meteo2['daily']['time']).strftime('%d/%m'))

            fig_t = go.Figure()
            if meteo1:
                fig_t.add_trace(go.Scatter(
                    x=list(labels) + list(labels)[::-1],
                    y=list(meteo1['daily']['temperature_2m_max']) + list(meteo1['daily']['temperature_2m_min'])[::-1],
                    fill='toself', fillcolor='rgba(93,122,140,0.15)',
                    line=dict(width=0), name=f"{sel1} amplitude",
                    showlegend=False, hoverinfo='skip'
                ))
                fig_t.add_trace(go.Scatter(
                    x=labels, y=meteo1['daily']['temperature_2m_max'],
                    line=dict(color='#5d7a8c', width=2.5), mode='lines+markers',
                    marker=dict(size=7), name=f"{sel1} T max", showlegend=True
                ))
                fig_t.add_trace(go.Scatter(
                    x=labels, y=meteo1['daily']['temperature_2m_min'],
                    line=dict(color='#5d7a8c', width=1.5, dash='dot'), mode='lines+markers',
                    marker=dict(size=5), name=f"{sel1} T min", showlegend=True
                ))
            if meteo2:
                fig_t.add_trace(go.Scatter(
                    x=list(labels) + list(labels)[::-1],
                    y=list(meteo2['daily']['temperature_2m_max']) + list(meteo2['daily']['temperature_2m_min'])[::-1],
                    fill='toself', fillcolor='rgba(166,124,91,0.15)',
                    line=dict(width=0), name=f"{sel2} amplitude",
                    showlegend=False, hoverinfo='skip'
                ))
                fig_t.add_trace(go.Scatter(
                    x=labels, y=meteo2['daily']['temperature_2m_max'],
                    line=dict(color='#a67c5b', width=2.5), mode='lines+markers',
                    marker=dict(size=7), name=f"{sel2} T max", showlegend=True
                ))
                fig_t.add_trace(go.Scatter(
                    x=labels, y=meteo2['daily']['temperature_2m_min'],
                    line=dict(color='#a67c5b', width=1.5, dash='dot'), mode='lines+markers',
                    marker=dict(size=5), name=f"{sel2} T min", showlegend=True
                ))
            fig_t.update_layout(
                height=280, margin=dict(t=10, b=10), font_size=10,
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',
                font_color='#2c3e50',
                yaxis=dict(title="Temperature (C)", title_font_color='#2c3e50', tickcolor='#2c3e50', gridcolor='#e0dbd3'),
                xaxis=dict(tickangle=0, tickcolor='#2c3e50'),
                legend=dict(orientation='h', y=-0.2, x=0.5, xanchor='center', font=dict(size=9, color='#2c3e50')),
            )
            st.plotly_chart(fig_t, use_container_width=True)

            # Detail tables
            col_t1, col_t2 = st.columns(2)
            if meteo1:
                df_m1 = pd.DataFrame({
                    'Date': labels,
                    'Temps': [code_meteo(c) for c in meteo1['daily']['weather_code']],
                    'T min': [f"{v:.0f}C" for v in meteo1['daily']['temperature_2m_min']],
                    'T max': [f"{v:.0f}C" for v in meteo1['daily']['temperature_2m_max']],
                })
                with col_t1:
                    st.markdown(f"**{sel1}**")
                    st.table(df_m1.set_index("Date"))
            if meteo2:
                df_m2 = pd.DataFrame({
                    'Date': labels,
                    'Temps': [code_meteo(c) for c in meteo2['daily']['weather_code']],
                    'T min': [f"{v:.0f}C" for v in meteo2['daily']['temperature_2m_min']],
                    'T max': [f"{v:.0f}C" for v in meteo2['daily']['temperature_2m_max']],
                })
                with col_t2:
                    st.markdown(f"**{sel2}**")
                    st.table(df_m2.set_index("Date"))
            st.caption("Source meteo : Open-Meteo API")
        else:
            st.info("Meteo non disponible. Verifiez votre connexion.")

    st.markdown('<p class="footer">Comparateur de Villes Francaises | SAE Outils Decisionnels | Matteo Cai, William Lefebre, Terryl Hassen</p>', unsafe_allow_html=True)


    # ========================================================================
    # TAB 4: SCORES
    # ========================================================================
    with tabs[3]:
        # Calcul des scores KPI pour les deux villes selectionnees
        # Donnees necessaires : charger toutes les villes pour normalisation min-max
        all_etudiants = load_etudiants_data()
        all_salaires = load_salaires_data()
        all_loyers = load_loyers_data()
        all_ens = load_ensoleillement_data()
        all_aqi = load_aqi_data()
        all_chomage = load_chomage_data()
        all_securite = load_securite_data()

        # Collecter les valeurs pour chaque indicateur (toutes villes)
        def _vals(source_dict, key=None):
            """Extraire les valeurs numeriques d'un dict de donnees."""
            vals = []
            for v in source_dict.values():
                if key:
                    x = v.get(key) if isinstance(v, dict) else None
                else:
                    x = v
                if x is not None:
                    vals.append(x)
            return vals

        pct_vals = _vals(all_etudiants, "pct_etudiants")
        sal_vals = _vals(all_salaires, "salaire_2023")
        loy_vals = [v["loypredm2"] for v in all_loyers.values() if v.get("loypredm2")]
        ens_vals = list(all_ens.values())
        aqi_vals = list(all_aqi.values())
        chom_vals = list(all_chomage.values())
        sec_vals = list(all_securite.values())

        def _norm(val, vmin, vmax, inverse=False):
            """Normalisation min-max vers [0, 100]. Si inverse, les basses valeurs = meilleur score."""
            if vmax == vmin or val is None or vmin is None:
                return None
            n = (val - vmin) / (vmax - vmin) * 100
            return 100 - n if inverse else n

        def _score_ville(sel):
            """Calculer le score KPI d'une ville."""
            d = d1 if sel == sel1 else d2
            scores = {}
            # % Etudiants (plus haut = mieux)
            v = d.get("pct_etudiants")
            if v is not None and pct_vals:
                scores["% Etudiants"] = _norm(v, min(pct_vals), max(pct_vals))
            # Salaire (plus haut = mieux)
            v = d.get("salaire_2023")
            if v is not None and sal_vals:
                scores["Salaire"] = _norm(v, min(sal_vals), max(sal_vals))
            # Loyer (plus bas = mieux → inverse)
            loy = all_loyers.get(sel)
            if loy and loy.get("loypredm2") and loy_vals:
                scores["Loyer"] = _norm(loy["loypredm2"], min(loy_vals), max(loy_vals), inverse=True)
            # Ensoleillement (plus haut = mieux)
            v = all_ens.get(sel)
            if v is not None and ens_vals:
                scores["Ensoleillement"] = _norm(v, min(ens_vals), max(ens_vals))
            # AQI (plus bas = mieux → inverse)
            v = d.get("aqi_moyen")
            if v is not None and aqi_vals:
                scores["Qualite air"] = _norm(v, min(aqi_vals), max(aqi_vals), inverse=True)
            # Chomage (plus bas = mieux → inverse)
            v = d.get("taux_chomage")
            if v is not None and chom_vals:
                scores["Chomage"] = _norm(v, min(chom_vals), max(chom_vals), inverse=True)
            # Securite (plus haut = mieux)
            v = d.get("score_securite")
            if v is not None and sec_vals:
                scores["Securite"] = _norm(v, min(sec_vals), max(sec_vals))
            return scores

        sc1 = _score_ville(sel1)
        sc2 = _score_ville(sel2)

        # Score global (moyenne des scores disponibles)
        avg1 = sum(sc1.values()) / len(sc1) if sc1 else None
        avg2 = sum(sc2.values()) / len(sc2) if sc2 else None

        # Radar chart (7 axes)
        # Utiliser l'ordre fixe des indicateurs pour que le radar soit coherent
        indic_order = ["% Etudiants", "Salaire", "Loyer", "Ensoleillement", "Qualite air", "Chomage", "Securite"]
        r_labels = [i for i in indic_order if i in sc1 or i in sc2]
        r_vals1 = [sc1.get(k, 0) or 0 for k in r_labels]
        r_vals2 = [sc2.get(k, 0) or 0 for k in r_labels]

        fig_radar = go.Figure()
        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals1 + [r_vals1[0]] if r_vals1 else [],
            theta=r_labels + [r_labels[0]] if r_labels else [],
            fill='toself',
            fillcolor='rgba(93,122,140,0.18)',
            line=dict(color='#5d7a8c', width=2.5),
            name=f"{sel1} ({avg1:.0f})" if avg1 is not None else sel1,
        ))
        fig_radar.add_trace(go.Scatterpolar(
            r=r_vals2 + [r_vals2[0]] if r_vals2 else [],
            theta=r_labels + [r_labels[0]] if r_labels else [],
            fill='toself',
            fillcolor='rgba(166,124,91,0.18)',
            line=dict(color='#a67c5b', width=2.5),
            name=f"{sel2} ({avg2:.0f})" if avg2 is not None else sel2,
        ))
        fig_radar.update_layout(
            polar=dict(
                radialaxis=dict(
                    visible=True, range=[0, 100],
                    tickfont=dict(size=9, color='#999'),
                    gridcolor='#e0dbd3',
                    linecolor='#e0dbd3',
                ),
                angularaxis=dict(
                    tickfont=dict(size=11, color='#2c3e50'),
                    gridcolor='#e0dbd3',
                    linecolor='#e0dbd3',
                ),
                bgcolor='rgba(0,0,0,0)',
            ),
            showlegend=True,
            legend=dict(
                orientation='h', y=-0.15, x=0.5, xanchor='center',
                font=dict(size=12, color='#2c3e50'),
            ),
            height=420,
            margin=dict(t=30, b=30, l=30, r=30),
            paper_bgcolor='rgba(0,0,0,0)',
            font_color='#2c3e50',
        )
        st.plotly_chart(fig_radar, use_container_width=True)

        # Score global sous le radar
        if avg1 is not None or avg2 is not None:
            col_avg1, col_avg2 = st.columns(2)
            with col_avg1:
                if avg1 is not None:
                    st.markdown(
                        f'<div style="text-align:center;">'
                        f'<span style="font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;color:#5d7a8c;font-weight:600;">Score global — {sel1}</span><br>'
                        f'<span style="font-size:2.4rem;font-weight:800;color:#5d7a8c;">{avg1:.0f}</span>'
                        f'<span style="font-size:0.9rem;color:#999;"> / 100</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )
            with col_avg2:
                if avg2 is not None:
                    st.markdown(
                        f'<div style="text-align:center;">'
                        f'<span style="font-size:0.75rem;text-transform:uppercase;letter-spacing:1px;color:#a67c5b;font-weight:600;">Score global — {sel2}</span><br>'
                        f'<span style="font-size:2.4rem;font-weight:800;color:#a67c5b;">{avg2:.0f}</span>'
                        f'<span style="font-size:0.9rem;color:#999;"> / 100</span>'
                        f'</div>',
                        unsafe_allow_html=True
                    )

        st.caption("Methode : normalisation min-max (0-100) sur les 483 communes. "
                   "Loyer, AQI et chomage sont inverses (valeur basse = meilleur score). "
                   "Score global = moyenne equiponderee des indicateurs disponibles.")


if __name__ == "__main__":
    main()
