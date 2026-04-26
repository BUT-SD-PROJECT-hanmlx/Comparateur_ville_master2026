"""
Comparateur de Villes Françaises
=================================
Auteurs : Matteo Cai, William Lefebre, Terryl Hassen
Cours : SAE Outils Decisionnels
"""

import streamlit as st
from pathlib import Path

st.set_page_config(
    page_title="Comparateur de Villes Françaises",
    page_icon="🏙️",
    layout="centered"
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
    .stApp { background: #f5f4f0; }
    .center-content {
        display: flex;
        flex-direction: column;
        align-items: center;
        text-align: center;
        padding: 60px 0;
    }
    .cover-banner {
        width: 100%;
        max-width: 640px;
        min-height: 160px;
        border-radius: 24px;
        background: linear-gradient(135deg, #5d7a8c 0%, #8aa7b3 100%);
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        padding: 28px 24px;
        margin-bottom: 30px;
        box-shadow: 0 18px 40px rgba(30, 50, 70, 0.12);
    }
    .banner-text {
        font-size: 1.4rem;
        font-weight: 700;
        line-height: 1.2;
        letter-spacing: 0.02em;
    }
    .title {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        margin-bottom: 20px;
    }
    .description {
        font-size: 1.1rem;
        color: #666;
        margin-bottom: 30px;
        max-width: 600px;
    }
    .stButton {
        width: 100%;
        display: flex;
        justify-content: center;
    }
    .stButton button {
        background: #5d7a8c;
        color: white;
        border: none;
        padding: 12px 24px;
        border-radius: 8px;
        font-size: 1.1rem;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.3s;
        margin: 0;
    }
    .stButton button:hover {
        background: #4a6470;
    }
    /* hide default elements */
    #MainMenu, footer { visibility: hidden; }
    .stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)

# -----------------------------
# CONTENU CENTRÉ
# -----------------------------
st.markdown('<div class="center-content">', unsafe_allow_html=True)

# Bannière de couverture
st.markdown('<div class="cover-banner"><div class="banner-text">Quelle ville choisir pour mon master ?</div></div>', unsafe_allow_html=True)

# Titre
st.markdown('<div class="title">Comparateur de ville française</div>', unsafe_allow_html=True)

# Texte descriptif
st.markdown("""
<div class="description">

Cet outil t'aide à choisir la meilleure ville pour ton master en comparant les villes, les perspectives de carrière, le coût de la vie ainsi que la qualité de la vie.
</div>
""", unsafe_allow_html=True)

# Bouton centré
if st.button("Accéder au comparateur"):
    st.switch_page("pages/0_⚖️_Comparateur_villes.py")

st.markdown('</div>', unsafe_allow_html=True)