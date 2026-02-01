import requests
import json
from typing import List, Dict

class BackupAPIs:
    """APIs de secours pour offres d'emploi"""
    
    def __init__(self):
        self.session = requests.Session()
    
    def search_adzuna(self, secteur: str, pays: str = "ma") -> List[Dict]:
        """Adzuna API (gratuite - 100 requêtes/jour)"""
        try:
            # Clé API gratuite
            app_id = "YOUR_APP_ID"  # S'inscrire sur adzuna.com
            app_key = "YOUR_APP_KEY"
            
            url = f"http://api.adzuna.com/v1/api/jobs/{pays}/search/1"
            params = {
                'app_id': app_id,
                'app_key': app_key,
                'what': f"stage {secteur}",
                'content-type': 'application/json'
            }
            
            response = self.session.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                offres = []
                
                for result in data.get('results', [])[:10]:
                    offres.append({
                        'titre': result.get('title', ''),
                        'entreprise': result.get('company', {}).get('display_name', ''),
                        'lieu': result.get('location', {}).get('display_name', 'Maroc'),
                        'date_publication': result.get('created', ''),
                        'lien': result.get('redirect_url', ''),
                        'source': 'Adzuna',
                        'type': 'Stage',
                        'valide': True
                    })
                
                return offres
            return []
            
        except:
            return []
    
    def search_reed_co_uk(self, secteur: str) -> List[Dict]:
        """Reed.co.uk API (gratuite pour quelques requêtes)"""
        try:
            # API publique limitée
            url = f"https://www.reed.co.uk/api/1.0/search?keywords=internship+{secteur}"
            
            response = self.session.get(url, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                offres = []
                
                for result in data.get('results', [])[:5]:
                    offres.append({
                        'titre': result.get('jobTitle', ''),
                        'entreprise': result.get('employerName', ''),
                        'lieu': result.get('locationName', ''),
                        'date_publication': 'Récente',
                        'lien': result.get('jobUrl', ''),
                        'source': 'Reed.co.uk',
                        'type': 'Stage',
                        'valide': True
                    })
                
                return offres
            return []
            
        except:
            return []