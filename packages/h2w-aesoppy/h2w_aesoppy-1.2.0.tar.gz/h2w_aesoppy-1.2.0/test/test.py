import aesoppy.gurufocus as gf
from dotenv import load_dotenv
import os
import pandas as pd


load_dotenv()
gt = os.getenv('guru_token')
ticker = 'txn'

div_data = gf.GuruDividendHistory(ticker=ticker, token=gt)
price_data = gf.GuruPriceHistory(ticker=ticker, token=gt)

div_data = gf.GuruDividendHistory(ticker=ticker, token=gt).aesop_normalized
div_data.to_csv('div.csv', index=False)
price_data = gf.GuruPriceHistory(ticker=ticker, token=gt).aesop_normalized
price_data.to_csv('price.csv', index=False)
fin_data = gf.GuruStockAnnualTenK(ticker=ticker, token=gt).aesop_normalized
fin_data.to_csv('fin.csv', index=False)