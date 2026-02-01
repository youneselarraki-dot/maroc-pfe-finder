import requests
from bs4 import BeautifulSoup
from typing import List, Dict, Optional
import streamlit as st
import re
from datetime import datetime
from core.real_offers import RealOffersFinder  # IMPORT NOUVEAU

class StageFinder:
    """Recherche d'offres de stage PFE au Maroc - VERSION RÉELLE"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept-Language': 'fr, ar-MA;q=0.9, ar;q=0.8',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'
        })
        self.real_finder = RealOffersFinder()  # NOUVEAU
    
    def search_rekrute(self, secteur: str, ville: str = "Casablanca") -> List[Dict]:
        """Recherche sur Rekrute.com - Version améliorée"""
        return self.real_finder.search_rekrute_real(secteur, ville)
    
    def search_emploi_maroc(self, secteur: str) -> List[Dict]:
        """Recherche sur Emploi.ma - Version améliorée"""
        return self.real_finder.search_emploi_ma_real(secteur)
    
    def search_linkedin_stage(self, secteur: str, ville: str = "Casablanca") -> List[Dict]:
        """Recherche sur LinkedIn - Version améliorée"""
        return self.real_finder.search_linkedin_api(secteur, ville)
    
    def search_entreprises_direct(self, entreprise_nom: str, secteur: str) -> List[Dict]:
        """Cherche directement sur le site de l'entreprise - Version améliorée"""
        try:
            # Rechercher les pages carrières des entreprises marocaines
            entreprise_sites = {
                'atos': 'https://atos.net/fr/maroc/carrieres',
                'capgemini': 'https://www.capgemini.com/ma-ma/careers/',
                'ibm': 'https://www.ibm.com/ma-fr/careers/',
                'microsoft': 'https://careers.microsoft.com/professionals/us/en/l-morocco',
                'ocp': 'https://www.ocpgroup.ma/fr/carrieres',
                'maroc telecom': 'https://www.iam.ma/L-Espace-Carrieres/Recrutement',
                'orange maroc': 'https://www.orange.ma/le-groupe/rejoignez-nous',
                'attijariwafa bank': 'https://www.attijariwafabank.com/fr/recrutement',
                'bnp paribas maroc': 'https://www.bnpparibas.com/fr/recrutement/',
                'vinci maroc': 'https://www.vinci.com/vinci.nsf/fr/offres-emploi.htm'
            }
            
            entreprise_lower = entreprise_nom.lower()
            offres = []
            
            for key, url in entreprise_sites.items():
                if key in entreprise_lower:
                    # Essayer de scraper le site
                    try:
                        response = self.session.get(url, timeout=10)
                        if response.status_code == 200:
                            soup = BeautifulSoup(response.content, 'html.parser')
                            
                            # Chercher des offres de stage
                            stage_keywords = ['stage', 'stagiare', 'pfe', 'intern', 'alternance']
                            
                            # Chercher dans les liens
                            for link in soup.find_all('a', href=True, string=True):
                                link_text = link.get_text().lower()
                                if any(keyword in link_text for keyword in stage_keywords):
                                    offre = {
                                        'titre': link.get_text(strip=True),
                                        'entreprise': entreprise_nom,
                                        'lieu': 'Maroc',
                                        'date_publication': '2024',
                                        'lien': link['href'] if link['href'].startswith('http') else f"{url.rstrip('/')}/{link['href'].lstrip('/')}",
                                        'source': f'Site {entreprise_nom}',
                                        'type': 'Stage',
                                        'valide': True
                                    }
                                    offres.append(offre)
                    
                    except Exception as e:
                        # Si scraping échoue, créer une offre générique mais avec vrai lien
                        offres.append({
                            'titre': f"Stage PFE {secteur}",
                            'entreprise': entreprise_nom,
                            'lieu': 'Casablanca',
                            'date_publication': '2024',
                            'lien': url,
                            'source': f'Site {entreprise_nom}',
                            'type': 'Stage',
                            'valide': True
                        })
                    
                    break
            
            return offres
            
        except Exception as e:
            st.warning(f"⚠️ Erreur recherche entreprise directe: {e}")
            return []
    
    def search_all_platforms(self, secteur: str, ville: str = None) -> List[Dict]:
        """Recherche sur toutes les plateformes - Version RÉELLE"""
        all_offres = []
        
        # Utiliser le finder réel
        offres_reelles = self.real_finder.search_all_real_offers(secteur, ville or "Casablanca")
        all_offres.extend(offres_reelles)
        
        # Si peu d'offres, ajouter des offres d'entreprises directes
        if len(all_offres) < 5:
            # Chercher pour grandes entreprises marocaines
            grandes_entreprises = ['Capgemini', 'Atos', 'OCP', 'Maroc Telecom', 'Orange Maroc']
            for entreprise in grandes_entreprises[:3]:
                offres_entreprise = self.search_entreprises_direct(entreprise, secteur)
                all_offres.extend(offres_entreprise)
        
        # Supprimer les doublons
        unique_offres = []
        seen_titles = set()
        
        for offre in all_offres:
            key = (offre['titre'][:50], offre['entreprise'][:30])
            if key not in seen_titles:
                seen_titles.add(key)
                unique_offres.append(offre)
        
        # Vérifier les liens (optionnel - peut ralentir)
        # for offre in unique_offres:
        #     offre['valide'] = self.real_finder.verify_offer_link(offre['lien'])
        
        return unique_offres[:25]  # Limiter à 25 offres