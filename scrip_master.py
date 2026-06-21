import pandas as pd
import requests
import logging

class TokenManager:
    def __init__(self):
        self.dataframe = None
        # Example: Dhan's daily scrip master URL
        self.scrip_url = "https://images.dhan.co/api-data/api-scrip-master.csv"

    def load_scrip_master(self):
        """Downloads the NSE/BSE Scrip Master into a Pandas DataFrame."""
        try:
            logging.info("Downloading Scrip Master to RAM...")
            # We only load the columns we need to save memory
            self.dataframe = pd.read_csv(self.scrip_url, usecols=['SEM_TRADING_SYMBOL', 'SEM_EXM_EXCH_ID', 'SEM_SMST_SECURITY_ID'])
            
            # Set the symbol as the index for O(1) lookup speed
            self.dataframe.set_index('SEM_TRADING_SYMBOL', inplace=True)
            logging.info("RAM-Cache initialized successfully.")
        except Exception as e:
            logging.error(f"Failed to load Scrip Master: {str(e)}")

    def get_token(self, symbol):
        """Fetches the static exchange token instantly."""
        if self.dataframe is None:
            self.load_scrip_master()
            
        try:
            # Locate the strict security ID required by the broker API
            token = self.dataframe.loc[symbol, 'SEM_SMST_SECURITY_ID']
            return int(token)
        except KeyError:
            return None
