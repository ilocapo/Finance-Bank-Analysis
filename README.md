Analyse Comparative de Trois Banques Françaises

BNP Paribas • Société Générale • Crédit Agricole

1. Contexte et objectif

Ce projet a pour objectif d’analyser et de comparer la performance financière de trois grandes banques françaises :
BNP Paribas, Société Générale et Crédit Agricole.

L’étude s’appuie sur leurs états financiers publics afin d’évaluer :

leur rentabilité,

leur solidité bilancielle,

l’évolution de leur taille,

leur profil de risque,

ainsi que leur trajectoire stratégique.

Ce projet illustre une réflexion d’analyste financier junior appliquée sur des données réelles.

2. Sources et données

Les données proviennent de Yahoo Finance (via la bibliothèque yfinance), incluant :

Compte de résultat

Bilan

Historique des résultats par année

Les indicateurs utilisés incluent notamment :

Total Revenue

Net Income

Total Assets

Total Liabilities Net Minority Interest

Total Stockholders Equity

Leverage Ratio (Liabilities / Equity)

3. Méthodologie

Extraction des données avec yfinance

Nettoyage et structuration via pandas

Visualisations et comparaisons temporelles

Analyse qualitative et interprétation métier

Formulation d’insights orientés décision

4. Principaux résultats
Rentabilité (Net Income)

BNP Paribas présente le profit le plus élevé et la plus grande stabilité, illustrant une rentabilité structurée sur un modèle mature.

Crédit Agricole affiche un Net Income inférieur mais régulier, associé à une expansion prudente.

Société Générale montre davantage de volatilité, avec un choc significatif en 2021–2022 suivi d’un rebond, traduisant une résilience mais aussi une exposition plus forte aux évènements macro-financiers.

Taille et solidité (Total Assets)

BNP Paribas dispose du bilan le plus important, reflétant son envergure internationale.

Crédit Agricole a un bilan légèrement plus modeste mais régulier, cohérent avec un modèle mutualiste prudent.

Société Générale reste structurellement plus petite, avec des variations reflétant ajustements et repositionnements.

Structure financière (Leverage Ratio)

Les trois banques présentent des ratios de levier relativement stables.

Cela suggère une gestion prudente de l’effet de levier, une dépendance maîtrisée aux financements externes et une discipline réglementaire forte.

5. Interprétation métier

Les résultats convergent vers plusieurs observations structurantes :

Le secteur bancaire français est profondément régulé, ce qui limite les dérives d’endettement.

BNP Paribas incarne un modèle de banque universelle internationalisée, performant et stable.

Crédit Agricole se distingue par une croissance modérée mais cohérente et rentable, alignée avec son modèle de banque mutualiste.

Société Générale présente un profil plus sensible aux chocs externes, mais sa capacité de rebond indique une flexibilité opérationnelle.

6. Limites

Les données proviennent de sources publiques et ne tiennent pas compte d’éléments hors bilan.

Des analyses plus fines (marges segmentées, provisions, coût du risque) pourraient enrichir l’étude.

La période observée reste courte pour certaines métriques.

7. Pistes d’amélioration

Pour une version future du projet :

intégrer des ratios de solvabilité réglementaires (CET1, Tier 1 capital),

comparer le coût du risque et les dépôts clients,

analyser les performances par segments (banque de détail, corporate, marchés financiers).

8. Technologies utilisées

Python

yfinance

pandas

matplotlib / seaborn

9. Structure du projet
📁 projet_banques_francaises
│── 01_comparaison_banques_francaises.ipynb
│── README.md

10. Auteur

Projet réalisé par Ilona Capo, dans une démarche d’apprentissage appliquée à l’analyse financière et au traitement de données.

French Banking Sector Comparative Financial Analysis
Overview

This project presents a comparative financial analysis of three major French banking institutions:

BNP Paribas

Société Générale

Crédit Agricole

The objective is to evaluate performance, risk positioning, and balance-sheet strength using publicly available financial statements retrieved via yfinance.

The analysis is intended to illustrate practical financial reasoning, data manipulation, visualization, and insight generation from publicly listed firms.

Data Sources

Data was retrieved programmatically via the Yahoo Finance API using yfinance, including:

Income statements

Balance sheet items

Stock market price history

Units and reporting dates follow issuer disclosure formats.

Methodology
1. Data Acquisition

Ticker symbols for each bank were queried through yfinance.
Financial statements were extracted, formatted, and merged into panel-style datasets.

2. Financial Indicators Studied

Key performance indicators include:

Total Revenue

Net Income

Total Assets

Liabilities

Total Stockholders Equity

Leverage Ratio (Liabilities / Equity)

3. Data Visualization

Custom Matplotlib plots were created to illustrate:

Net Income evolution

Total Asset growth

Liabilities vs Equity

Leverage trajectory over time

Key Insights
BNP Paribas

The largest and most stable institution among the sample.
Consistently rising Net Income and relatively steady asset base suggest a mature universal banking model delivering resilient profitability on a large balance sheet.

Crédit Agricole

Displays controlled expansion supported by rising assets and improving profitability.
Its cooperative structure aligns with a conservative risk posture, reflected in smoother performance metrics.

Société Générale

A smaller and structurally more volatile bank.
Asset contraction in 2022 alongside sharply lower Net Income corresponds with divestment and geopolitical impacts (notably Russia exit).
Subsequent recovery highlights resilience but exposes vulnerability to exogenous shocks.

Leverage Dynamics

All banks maintain relatively stable leverage levels.
Liabilities have grown moderately faster than equity, suggesting externally-financed expansion, but stability over time indicates sound capital discipline rather than aggressive risk accumulation.

Technologies & Tools

Python

Pandas

Matplotlib

yfinance

Business Interpretation Value

This project demonstrates:

Ability to source and process financial statements programmatically

Understanding of core bank valuation metrics

Capacity to articulate financial insights rather than only compute figures

Practical business analysis applied to a regulated industry

The style and reasoning are relevant for roles in:

Data Analytics

Business Analytics

Financial Analysis

Risk / Banking Insight roles

Next Steps / Future Work

Integrating stock price correlations with earnings changes

Adding profitability ratios (ROE, ROA)

Extending analysis to international peers