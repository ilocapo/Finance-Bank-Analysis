# Analyse comparative de banques françaises (BNP • SG • Crédit Agricole)

## Objectif
Comparer la **rentabilité** et la **solidité bilancielle** de trois grandes banques françaises sur plusieurs années, à partir de données publiques, dans une démarche d’analyste junior (data + visualisation + interprétation métier).

## Questions
- Quelle banque est la plus rentable (Net Income, ROE/ROA) ?
- Quelle banque est la plus “solide” (structure bilan, levier) ?
- Quelles tendances ressortent sur 5–10 ans ?

## Données
- Source : **Yahoo Finance** via **yfinance**
- États financiers : **Income Statement** & **Balance Sheet** (annuel)

## Indicateurs & ratios
- Total Revenue, Net Income  
- Total Assets, Total Liabilities, Total Stockholders’ Equity  
- Leverage Ratio = Liabilities / Equity  
- (À venir) ROE, ROA, croissance (%), score global

## Méthodologie
1. Extraction automatisée (**yfinance**)
2. Nettoyage + structuration (**pandas**)
3. Analyse temporelle + comparaison
4. Visualisations (**matplotlib**)
5. Interprétation métier + synthèse

## Résultats (résumé)
- **BNP Paribas** : rentabilité la plus élevée et relativement stable ; bilan le plus important.
- **Crédit Agricole** : performance plus modérée mais régulière ; croissance progressive.
- **Société Générale** : volatilité plus marquée ; phase de choc puis redressement.

## Limites
- Données publiques (pas d’éléments hors-bilan)
- Pas de ratios réglementaires détaillés (CET1/Tier 1)
- Période parfois courte selon les métriques

## Pistes d’amélioration
- Ajouter **ROE/ROA**, croissance (%), score global
- Intégrer coût du risque/provisions (si dispo)
- Dashboard (Streamlit / Power BI)

## Tech
**Python**, **pandas**, **yfinance**, **matplotlib**

## Structure
projet_analyse_banques/
- bank_financial_analysis_fr.ipynb
- README.md

## Auteur
Ilona Capo
