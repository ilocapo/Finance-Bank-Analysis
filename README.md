# 📊 Analyse Financière des Banques Françaises

Dashboard interactif professionnel d'analyse comparative des principales banques françaises (BNP Paribas, Société Générale, Crédit Agricole).

## 🎯 Présentation

Analyse financière approfondie des trois principales banques françaises sur la période 2021-2024. Ce projet évalue la rentabilité, la solidité financière et les tendances stratégiques à travers 8 indicateurs clés et des visualisations interactives.

## ✨ Fonctionnalités

### 📈 Analyses Financières Complètes
- **Ratios de Rentabilité** : ROE, ROA, Marge bénéficiaire
- **Structure Financière** : Ratio de levier, Equity ratio
- **Dynamique de Croissance** : Revenus, Bénéfices nets, Actifs
- **Analyse de Volatilité** : Écart-types, Coefficient de variation
- **Score Global** : Évaluation comparative multi-critères

### 🎨 Dashboard Web Multi-Pages
- **Synthèse** : Vue d'ensemble avec KPIs et graphiques d'évolution
- **Comparaison** : Tableaux, graphiques radar, analyse risque-rendement
- **Analyses Détaillées** : Profils par banque avec forces/faiblesses/recommandations
- **Méthodologie** : Formules et seuils d'interprétation

### 📊 Visualisations Interactives
- Graphiques Plotly interactifs
- Box plots de distribution
- Graphiques radar multi-dimensionnels
- Matrices de corrélation

## 📂 Structure du Projet

```
finance-banks-analysis/
├── data/                              # Données financières
├── notebooks/                         # Analyse exploratoire
├── src/                              # Scripts de collecte
├── docs/                             # Dashboard déployable
│   └── index.html
├── generate_multipage.py             # Générateur
└── requirements.txt
```

## 🚀 Installation

```bash
# Cloner et installer
git clone [votre-repo]
cd finance-banks-analysis
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Collecter les données
python src/prepare_data.py

# Générer le dashboard
python generate_multipage.py

# Visualiser
cd docs && python -m http.server 8080
```

## 🌐 Hébergement Gratuit

### GitHub Pages (Recommandé)
```bash
git add . && git commit -m "Add dashboard" && git push
# Settings > Pages > Source: main, /docs folder
```
URL : `https://[username].github.io/[repo-name]`

### Netlify
1. Compte sur netlify.com
2. "Deploy manually" 
3. Glisser-déposer `docs/`

### Cloudflare Pages
```bash
npm install -g wrangler
cd docs
wrangler pages publish . --project-name=finance-dashboard
```

### Render
1. render.com > "New Static Site"
2. Connecter GitHub repo
3. Publish directory: `docs`

## 📊 Indicateurs

| Indicateur | Formule | Seuil |
|-----------|---------|-------|
| **ROE** | Net Income / Equity | > 10% = Excellent |
| **Levier** | Liabilities / Equity | < 12 = Solide |
| **Equity Ratio** | Equity / Assets × 100 | > 8% = Bien capitalisé |

## 🛠️ Technologies

Python 3.11+ • pandas • yfinance • Plotly • Bootstrap 5

## 📝 Sources

- API Yahoo Finance • Données publiques 2021-2024
- BNP Paribas (BNP.PA), Société Générale (GLE.PA), Crédit Agricole (ACA.PA)

---

**Projet Portfolio** | Janvier 2026
