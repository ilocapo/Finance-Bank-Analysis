# 📊 Analyse Financière des Banques Françaises

Dashboard interactif professionnel d'analyse comparative des principales banques françaises (BNP Paribas, Société Générale, Crédit Agricole) avec benchmarks sectoriels et projections.

## 🎯 Présentation

Analyse financière approfondie des trois principales banques françaises sur la période 2021-2024. Ce projet évalue la rentabilité, la solidité financière et les tendances stratégiques à travers 8+ indicateurs clés, des visualisations interactives, et une analyse complète des risques bancaires incluant les normes Bâle III.

## ✨ Fonctionnalités Principales

### 📈 Analyses Financières Complètes
- **Ratios de Rentabilité** : ROE, ROA, Marge bénéficiaire
- **Structure Financière** : Ratio de levier, Equity ratio, Conformité Bâle III
- **Dynamique de Croissance** : Revenus, Bénéfices nets, Actifs
- **Analyse de Volatilité** : Écart-types, Coefficient de variation
- **Score Global** : Évaluation comparative multi-critères

### 🎨 Dashboard Web Professionnel Multi-Pages
- **Synthèse** : Vue d'ensemble avec KPIs et graphiques d'évolution historique
- **Comparaison** : Tableaux détaillés, graphiques radar, analyse risque-rendement
- **Analyses Détaillées** : Profils enrichis par banque avec forces/faiblesses/recommandations narratives
- **Risques & Solidité** : Analyse des risques bancaires, conformité réglementaire, profils de risque
- **Projections 3 Ans** : Prédictions linéaires des métriques clés avec scénarios
- **Données Complètes** : Tables interactives avec tous les indicateurs
- **Méthodologie** : Guide complet des calculs et seuils d'interprétation

### 📊 Visualisations Interactives Avancées
- Graphiques Plotly interactifs avec hover details
- **Box plots** de distribution et volatilité
- **Graphiques radar** multi-dimensionnels
- **Matrices de corrélation** et heatmaps
- **Benchmark charts** vs moyenne européenne
- **Projections graphiques** avec lignes de tendance

### 🔥 Améliorations Récentes (V2.0)

#### ✅ Benchmarks Sectoriels
- Comparaison vs benchmarks bancaires européens 2023-2024
- ROE, Levier, Equity Ratio, Bâle III compliance
- Identification automatique des sur/sous-performances

#### ✅ Analyse Avancée des Risques
- **Volatilité des rendements** : stabilité de la performance
- **Profils de levier** : risque financier vs benchmark
- **Conformité Bâle III** : adéquation du capital
- **Score de risque intégré** : évaluation multi-critères
- **AI/Tech Impact** : implications de la transformation digitale

#### ✅ Projections Temporelles
- **Forecast 3 ans** : projections linéaires ROE, levier, marge
- **Analyse de tendances** : hausse/baisse des indicateurs clés
- **Scénarios** : cas positifs et risques potentiels
- **Illustratif** : prévisions basées sur données historiques

#### ✅ Méthodologie Enrichie
- **Sources** : Yahoo Finance API, données officielles annuelles
- **Formules détaillées** : calcul transparent de chaque ratio
- **Seuils d'interprétation** : repères pour l'analyse qualitative
- **FAQ méthodologique** : guide pour non-experts

#### ✅ Storytelling Visuel
- **Analyses narratives** : interprétations stratégiques par banque
- **Contexte réglementaire** : impacts Bâle III, contraintes de capital
- **Recommandations actionables** : points d'amélioration concrets

## 📂 Structure du Projet

```
finance-banks-analysis/
├── data/                              # Données financières (CSV)
│   └── banques_financials_complete.csv
├── notebooks/                         # Analyse exploratoire Jupyter
│   └── financial_analysis_full.ipynb
├── src/                               # Scripts de collecte & préparation
│   ├── fetch_data.py
│   └── prepare_data.py
├── docs/                              # Dashboard déployable
│   └── index.html (GÉNÉRÉ)
├── generate_multipage.py              # Générateur principal
├── requirements.txt                   # Dépendances Python
└── README.md
```

## 🚀 Installation & Utilisation

### Prérequis
- Python 3.8+
- pip ou conda

### Installation

```bash
# Cloner le repository
git clone [votre-repo]
cd finance-banks-analysis

# Créer un environnement virtuel (optionnel)
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate      # Windows

# Installer les dépendances
pip install -r requirements.txt
```

### Générer le Dashboard

```bash
python generate_multipage.py
```

Le dashboard est généré dans `docs/index.html`. Ouvrez le fichier dans un navigateur web.

### Déployer en ligne

Le dashboard peut être hébergé gratuitement sur :
- **GitHub Pages** : Poussez `docs/` sur votre repo
- **Netlify** : Déploiement automatique depuis GitHub
- **Vercel** : Hébergement statique ultra-rapide

Consulter `HEBERGEMENT.md` pour les instructions détaillées.

## 📊 Données & Méthodologie

### Sources
- **API** : Yahoo Finance via `yfinance`
- **Données** : Income Statement + Balance Sheet (annuelles)
- **Période** : 2021-2024 (4 années complètes)
- **Tickers** : BNP.PA, GLE.PA, ACA.PA

### Indicateurs Clés (8+)

| Indicateur | Formule | Interprétation |
|-----------|---------|-----------------|
| **ROE** | Net Income / Equity | Rentabilité des capitaux propres (>10% = excellent) |
| **ROA** | Net Income / Assets | Efficacité de l'utilisation des actifs |
| **Marge** | Net Income / Revenue (%) | Rentabilité opérationnelle (bancaire: 15-25%) |
| **Levier** | Total Liabilities / Equity | Risque financier (<12 = robuste) |
| **Equity Ratio** | Equity / Assets (%) | Capitalisation (>6% = conforme Bâle III) |
| **Croissance** | YoY variation (%) | Dynamique de croissance |
| **Volatilité** | StdDev de ROE | Stabilité de la performance |
| **Score Global** | Composite multi-critères | Évaluation synthétique |

### Seuils d'Interprétation
- **ROE** : >10% Excellent | 8-10% Bon | 5-8% Acceptable | <5% Faible
- **Levier** : <10 Très solide | 10-15 Équilibré | >15 Risqué
- **Equity Ratio** : >8% Forte cap. | 5-8% Acceptable | <5% Vulnérable

## 🎯 Key Insights (2021-2024)

### BNP Paribas
- **Performance** : ROE en amélioration (8.0% → 9.1%), tendance positive
- **Solidité** : Levier bien contrôlé (21.3 → 20.1), profil conservateur
- **Stratégie** : Croissance profitable, optimisation des marges

### Société Générale
- **Performance** : Volatilité élevée (ROE: 8.7% → 6.0% → 3.8% → 6.0%)
- **Défis** : Rebond post-2022, impact de la crise énergétique
- **Opportunité** : Normalisation attendue avec stabilisation des taux

### Crédit Agricole
- **Performance** : Croissance constante du ROE (8.6% → 9.5%)
- **Risque** : Levier élevé (29.3), modèle mutualiste spécifique
- **Force** : Marge très solide (27%), efficacité opérationnelle

## 🔒 Conformité Réglementaire

Tous les indicateurs respectent les normes :
- **Bâle III** : CET1 ratio, Leverage ratio, ratios de liquidité
- **SOLVABILITÉ II** : Pour les activités d'assurance (CAA)
- **Reporting CECABANK** : Données officielles CCR

## 📱 Responsivité & Accessibilité

Le dashboard est optimisé pour :
- ✅ Desktop (1920x1080+)
- ✅ Tablet (768-1024px)
- ✅ Mobile (320px+)
- ✅ Lecteurs d'écran (ARIA labels)
- ✅ Contraste élevé (WCAG AA)

## 🛠 Technologies Utilisées

- **Backend** : Python 3, pandas, numpy, scipy
- **Visualisations** : Plotly (interactif), Matplotlib
- **Frontend** : HTML5, CSS3, Bootstrap 5, Font Awesome
- **Données** : yfinance, CSV
- **Déploiement** : GitHub Pages, Netlify

## 📈 Roadmap Future

- [ ] Intégration données temps réel (WebSocket)
- [ ] Machine Learning : prédictions ARIMA/Prophet
- [ ] Dashboard Tableau/Power BI interactif
- [ ] Analyse sentiments actualités bancaires
- [ ] Comparaison vs banques internationales (EU, US, Asia)
- [ ] Module stress test (scénarios de crise)
- [ ] Export PDF personnalisé

## 📞 Support & Questions

Pour toute question ou suggestion d'amélioration :
- 📧 Email: [votre email]
- 🐙 GitHub Issues: [lien repo]
- 💼 LinkedIn: [votre profil]

## 📄 Licence

MIT License - Libre d'utilisation pour projets commerciaux et personnels.

## 🙏 Remerciements

- **Yahoo Finance** : Données financières
- **Plotly** : Visualisations interactives
- **Bootstrap** : Framework CSS
- **Banques Françaises** : Rapports annuels publics

---

**Dernière mise à jour** : Janvier 2026
**Version** : 2.0 (Améliorations V2 - Benchmarks, Risques, Projections)
**Status** : ✅ Productionpip install -r requirements.txt

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
