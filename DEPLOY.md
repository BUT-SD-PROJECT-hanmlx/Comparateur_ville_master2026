# Deployment Script - Comparateur de Villes Francaises

## Instructions de Deploiement sur Streamlit Cloud

### Methode 1 : Via Streamlit Cloud (Recommandee)

1. **Creer un compte** sur https://streamlit.io
2. **Uploader le projet** sur GitHub
3. **Connecter GitHub** a Streamlit Cloud
4. **Deployer** :
   - Cliquer sur "New App"
   - Selectionner le repository
   - Specifier `app.py` comme fichier principal
   - Cliquer sur "Deploy"

### Methode 2 : Via ligne de commande

```bash
# Installer streamlit cloud
pip install streamlit

# Deployer (necessite un compte streamlit cloud)
streamlit deploy [github-url]
```

## URL de l'Application

A remplir apres deploiement :
```
https://[username]-[repo]-[hash].streamlit.app
```

## Structure des Fichiers Requis

```
villes_francaises/
├── app.py              # Application principale (OBLIGATOIRE)
├── requirements.txt    # Dependances (OBLIGATOIRE)
├── README.md           # Documentation
├── MODE_D_EMPLOI.md    # Guide utilisateur
├── RAPPORT.md          # Rapport du projet
└── scripts/
    └── import_donnees.py
```

## Verification du Deploiement

Apres le deploiement :
1. Verifier que l'URL est accessible
2. Tester la selection des villes
3. Verifier le chargement des graphiques
4. Tester le telechargement CSV
