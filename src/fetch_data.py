from yfinance import Ticker

def get_bank_data(ticker):
    bank = Ticker(ticker)
    return bank.financials.transpose(), bank.balance_sheet.transpose()
