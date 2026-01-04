"""
Script pour préparer les données financières complètes
Ce script charge les données depuis yfinance et les sauvegarde pour le dashboard
"""

import yfinance as yf
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

# Définition des tickers des banques
TICKERS = {
    "BNP Paribas": "BNP.PA",
    "Société Générale": "GLE.PA",
    "Crédit Agricole": "ACA.PA"
}

def load_bank_financials(bank_name, ticker_symbol):
    """
    Charge les données financières d'une banque depuis Yahoo Finance
    """
    print(f"Chargement des données pour {bank_name}...")
    ticker = yf.Ticker(ticker_symbol)

    income_stmt = ticker.income_stmt
    balance_sheet = ticker.balance_sheet

    income_keys = [
        "Total Revenue",
        "Net Income"
    ]

    balance_keys = [
        "Total Assets",
        "Total Liabilities Net Minority Interest",
        "Stockholders Equity"
    ]

    income_selected = income_stmt.loc[income_keys]
    balance_selected = balance_sheet.loc[balance_keys]

    df = pd.concat(
        [income_selected.T, balance_selected.T],
        axis=1
    )

    df["bank"] = bank_name
    return df

def calculate_metrics(df):
    """
    Calcule tous les ratios et métriques financières
    """
    print("Calcul des métriques financières...")
    
    # Ratios de performance
    df["leverage_ratio"] = (
        df["Total Liabilities Net Minority Interest"] / df["Stockholders Equity"]
    )
    
    df["roe"] = (
        df["Net Income"] / df["Stockholders Equity"]
    )
    
    df["roa"] = (
        df["Net Income"] / df["Total Assets"]
    )
    
    # Marges bénéficiaires
    df["profit_margin"] = (df["Net Income"] / df["Total Revenue"]) * 100
    
    # Ratio de capitaux propres
    df["equity_ratio"] = (df["Stockholders Equity"] / df["Total Assets"]) * 100
    
    return df

def calculate_growth_rates(df):
    """
    Calcule les taux de croissance année par année
    """
    print("Calcul des taux de croissance...")
    
    df_sorted = df.sort_values(["bank", "year"]).reset_index(drop=True)
    growth_metrics = []

    for bank in df_sorted["bank"].unique():
        bank_data = df_sorted[df_sorted["bank"] == bank].copy()
        
        bank_data["revenue_growth"] = bank_data["Total Revenue"].pct_change() * 100
        bank_data["net_income_growth"] = bank_data["Net Income"].pct_change() * 100
        bank_data["assets_growth"] = bank_data["Total Assets"].pct_change() * 100
        
        growth_metrics.append(bank_data)

    df_growth = pd.concat(growth_metrics)
    return df_growth

def main():
    """
    Fonction principale pour préparer les données
    """
    print("=" * 60)
    print("Préparation des données financières des banques françaises")
    print("=" * 60)
    
    # Chargement des données pour toutes les banques
    dfs = []
    for bank, ticker in TICKERS.items():
        try:
            df_bank = load_bank_financials(bank, ticker)
            dfs.append(df_bank)
        except Exception as e:
            print(f"Erreur lors du chargement de {bank}: {e}")
    
    # Consolidation
    print("\nConsolidation des données...")
    df_all = pd.concat(dfs)
    df = df_all.dropna().copy()
    
    # Conversion des dates
    df.index = pd.to_datetime(df.index)
    df["year"] = df.index.year
    
    # Calcul des métriques
    df = calculate_metrics(df)
    
    # Calcul des taux de croissance
    df_complete = calculate_growth_rates(df)
    
    # Sauvegarde
    output_file = "data/banques_financials_complete.csv"
    df_complete.to_csv(output_file)
    
    print("\n" + "=" * 60)
    print(f"Données sauvegardées dans {output_file}")
    print(f"Total: {df_complete.shape[0]} lignes, {df_complete.shape[1]} colonnes")
    print("=" * 60)
    
    # Affichage d'un résumé
    print("\nRésumé des données:")
    print(f"Banques: {', '.join(df_complete['bank'].unique())}")
    print(f"Années: {df_complete['year'].min()} - {df_complete['year'].max()}")
    print("\nMétriques disponibles:")
    metrics = ['roe', 'roa', 'profit_margin', 'leverage_ratio', 'equity_ratio', 
               'revenue_growth', 'net_income_growth', 'assets_growth']
    for metric in metrics:
        print(f"  - {metric}")
    
    print("\nLes données sont prêtes pour le dashboard!")

if __name__ == "__main__":
    main()
