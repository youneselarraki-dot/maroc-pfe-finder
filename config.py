import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    # API Keys (gratuites)
    SERPAPI_KEY = os.getenv("SERPAPI_KEY", "demo")  # Clé gratuite: 100 requêtes/mois
    GOOGLE_CSE_ID = os.getenv("GOOGLE_CSE_ID", "")
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "")
    
    # Application
    APP_NAME = "Contact Agent Pro"
    VERSION = "2.0.0"
    
    # Recherche
    MAX_RESULTS = 15
    REQUEST_DELAY = 3
    TIMEOUT = 30
    
    # Sources alternatives
    USE_GOOGLE_SEARCH = True
    USE_SERPAPI = True  # 100 requêtes/mois gratuites
    USE_MANUAL_SCRAPING = True
    
    # Fichiers
    DATA_DIR = "data"
    EXPORTS_DIR = "exports"
    
    @property
    def data_path(self):
        path = os.path.join(os.path.dirname(__file__), self.DATA_DIR)
        os.makedirs(path, exist_ok=True)
        return path

settings = Settings()