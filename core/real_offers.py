import requests
from bs4 import BeautifulSoup
import json
from typing import List, Dict, Optional
import streamlit as st
from datetime import datetime
import re

class RealOffersFinder:
    """Trouve des offres RÉELLES de stage au Maroc"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'fr,fr-FR;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive'
        })
    
    def search_rekrute_real(self, secteur: str, ville: str = "Casablanca") -> List[Dict]:
        """Recherche RÉELLE sur Rekrute.com (site marocain d'emploi)"""
        try:
            # Encodage des paramètres
            search_terms = {
                'informatique': ['développeur', 'programmeur', 'informaticien', 'stage informatique'],
                'telecom': ['telecom', 'réseaux', 'stage telecom'],
                'finance': ['finance', 'banque', 'stage finance'],
                'marketing': ['marketing', 'communication', 'stage marketing']
            }
            
            keywords = search_terms.get(secteur.lower(), [secteur])
            
            all_offres = []
            
            for keyword in keywords[:2]:  # Essayer 2 keywords
                # Construction URL
                url = f"https://www.rekrute.com/offres.html?p={keyword}&s=1&o=1&l={ville}"
                
                st.write(f"🔍 Recherche Rekrute.com: {keyword} à {ville}")
                
                try:
                    response = self.session.get(url, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Recherche des offres
                        offre_elements = soup.select('.job-item, .emploi-item, .offer-item')
                        
                        if not offre_elements:
                            # Essayer un autre sélecteur
                            offre_elements = soup.select('.titreJob, .emploi-title')
                        
                        for element in offre_elements[:10]:  # Limiter à 10
                            try:
                                # Extraire titre
                                titre_elem = element.select_one('.titreJob, .emploi-title, .job-title')
                                titre = titre_elem.get_text(strip=True) if titre_elem else f"Stage {secteur}"
                                
                                # Extraire entreprise
                                entreprise_elem = element.select_one('.entreprise, .company-name, .societe')
                                entreprise = entreprise_elem.get_text(strip=True) if entreprise_elem else "Entreprise"
                                
                                # Extraire lieu
                                lieu_elem = element.select_one('.lieu, .location, .ville')
                                lieu = lieu_elem.get_text(strip=True) if lieu_elem else ville
                                
                                # Extraire lien
                                lien_elem = element.select_one('a[href*="/offres/"], a[href*="/emploi/"]')
                                lien = ""
                                if lien_elem and 'href' in lien_elem.attrs:
                                    lien = f"https://www.rekrute.com{lien_elem['href']}"
                                else:
                                    # Chercher un lien dans l'élément parent
                                    parent_link = element.find_parent('a', href=True)
                                    if parent_link:
                                        lien = f"https://www.rekrute.com{parent_link['href']}"
                                
                                # Vérifier si c'est un stage
                                if any(mot in titre.lower() for mot in ['stage', 'stagiare', 'pfe', 'intern', 'alternance']):
                                    offre = {
                                        'titre': titre,
                                        'entreprise': entreprise,
                                        'lieu': lieu,
                                        'date_publication': 'Récente',
                                        'lien': lien if lien else url,
                                        'source': 'Rekrute.com',
                                        'type': 'Stage',
                                        'secteur': secteur,
                                        'valide': bool(lien)  # Marquer si lien valide
                                    }
                                    all_offres.append(offre)
                                    
                            except Exception as e:
                                continue
                    
                except Exception as e:
                    st.warning(f"⚠️ Erreur Rekrute.com ({keyword}): {str(e)[:50]}")
                    continue
            
            return all_offres[:15]  # Limiter à 15 offres
            
        except Exception as e:
            st.error(f"❌ Erreur générale Rekrute: {e}")
            return []
    
    def search_emploi_ma_real(self, secteur: str) -> List[Dict]:
        """Recherche sur Emploi.ma (site marocain)"""
        try:
            url = f"https://www.emploi.ma/recherche-emploi-maroc?mots={secteur}"
            
            st.write(f"🔍 Recherche Emploi.ma: {secteur}")
            
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                offres = []
                
                # Rechercher les offres de stage
                stage_keywords = ['stage', 'stagiare', 'pfe', 'alternance']
                
                # Chercher dans tout le texte
                text = soup.get_text().lower()
                
                # Extraire les offres
                job_items = soup.select('.job-item, .offer, .annonce')
                
                for item in job_items[:10]:
                    try:
                        # Extraire titre
                        titre_elem = item.select_one('.titre, .title, h3, h4')
                        titre = titre_elem.get_text(strip=True) if titre_elem else f"Offre {secteur}"
                        
                        # Vérifier si c'est un stage
                        titre_lower = titre.lower()
                        if any(keyword in titre_lower for keyword in stage_keywords):
                            # Extraire entreprise
                            entreprise_elem = item.select_one('.entreprise, .company, .societe')
                            entreprise = entreprise_elem.get_text(strip=True) if entreprise_elem else "Entreprise"
                            
                            # Extraire lieu
                            lieu_elem = item.select_one('.lieu, .ville, .location')
                            lieu = lieu_elem.get_text(strip=True) if lieu_elem else "Maroc"
                            
                            # Extraire lien
                            lien_elem = item.select_one('a[href*="/offre/"], a[href*="/emploi/"]')
                            lien = lien_elem['href'] if lien_elem and 'href' in lien_elem.attrs else ""
                            if lien and not lien.startswith('http'):
                                lien = f"https://www.emploi.ma{lien}"
                            
                            offres.append({
                                'titre': titre,
                                'entreprise': entreprise,
                                'lieu': lieu,
                                'date_publication': '2024',
                                'lien': lien if lien else url,
                                'source': 'Emploi.ma',
                                'type': 'Stage',
                                'secteur': secteur,
                                'valide': bool(lien)
                            })
                            
                    except:
                        continue
                
                return offres
            else:
                return []
                
        except Exception as e:
            st.warning(f"⚠️ Erreur Emploi.ma: {e}")
            return []
    
    def search_marocannonces(self, secteur: str) -> List[Dict]:
        """Recherche sur MarocAnnonces.com"""
        try:
            url = f"https://www.marocannonces.com/categorie/309/Emploi-et-Formation/Offres-d-emploi.html?filtre={secteur}"
            
            st.write(f"🔍 Recherche MarocAnnonces: {secteur}")
            
            response = self.session.get(url, timeout=15)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                offres = []
                
                # Chercher les annonces
                annonces = soup.select('.annonce, .item, .listing-item')[:10]
                
                for annonce in annonces:
                    try:
                        titre_elem = annonce.select_one('.titre, .title, h3')
                        titre = titre_elem.get_text(strip=True) if titre_elem else ""
                        
                        # Vérifier si c'est un stage
                        if titre and any(mot in titre.lower() for mot in ['stage', 'stagiare', 'pfe']):
                            lien_elem = annonce.select_one('a[href*=".html"]')
                            lien = lien_elem['href'] if lien_elem and 'href' in lien_elem.attrs else ""
                            
                            if lien and not lien.startswith('http'):
                                lien = f"https://www.marocannonces.com{lien}"
                            
                            # Extraire entreprise du titre ou description
                            entreprise = "Entreprise"
                            desc_elem = annonce.select_one('.description, .desc')
                            if desc_elem:
                                desc_text = desc_elem.get_text()
                                # Chercher un nom d'entreprise
                                entreprise_match = re.search(r'(?:chez|à|dans|pour)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*)', desc_text)
                                if entreprise_match:
                                    entreprise = entreprise_match.group(1)
                            
                            offres.append({
                                'titre': titre,
                                'entreprise': entreprise,
                                'lieu': "Maroc",
                                'date_publication': 'Récente',
                                'lien': lien if lien else url,
                                'source': 'MarocAnnonces',
                                'type': 'Stage',
                                'secteur': secteur,
                                'valide': bool(lien)
                            })
                            
                    except:
                        continue
                
                return offres
            else:
                return []
                
        except Exception as e:
            st.warning(f"⚠️ Erreur MarocAnnonces: {e}")
            return []
    
    def search_linkedin_api(self, secteur: str, ville: str = "Casablanca") -> List[Dict]:
        """Recherche via l'API LinkedIn (approche alternative)"""
        try:
            # Note: LinkedIn API nécessite un token
            # Cette méthode utilise une approche simplifiée
            
            # URLs de recherche LinkedIn pour le Maroc
            linkedin_urls = [
                f"https://www.linkedin.com/jobs/search/?keywords=stage%20{secteur}&location=Maroc",
                f"https://www.linkedin.com/jobs/search/?keywords=pfe%20{secteur}&location=Maroc",
                f"https://www.linkedin.com/jobs/search/?keywords=alternance%20{secteur}&location={ville}%2C%20Maroc"
            ]
            
            offres = []
            
            for url in linkedin_urls[:2]:  # Essayer 2 URLs
                try:
                    response = self.session.get(url, timeout=15)
                    
                    if response.status_code == 200:
                        soup = BeautifulSoup(response.content, 'html.parser')
                        
                        # Chercher les jobs (sélecteurs LinkedIn)
                        job_cards = soup.select('.job-card-container, .result-card')[:5]
                        
                        for card in job_cards:
                            try:
                                titre_elem = card.select_one('.job-card-list__title, .result-card__title')
                                titre = titre_elem.get_text(strip=True) if titre_elem else f"Stage {secteur}"
                                
                                entreprise_elem = card.select_one('.job-card-container__company-name, .result-card__subtitle')
                                entreprise = entreprise_elem.get_text(strip=True) if entreprise_elem else "Entreprise"
                                
                                lieu_elem = card.select_one('.job-card-container__metadata-item, .job-result-card__location')
                                lieu = lieu_elem.get_text(strip=True) if lieu_elem else ville
                                
                                # Construire lien LinkedIn
                                lien = url  # Par défaut
                                link_elem = card.select_one('a[href*="/jobs/view/"]')
                                if link_elem and 'href' in link_elem.attrs:
                                    lien = f"https://www.linkedin.com{link_elem['href']}"
                                
                                offres.append({
                                    'titre': titre,
                                    'entreprise': entreprise,
                                    'lieu': lieu,
                                    'date_publication': 'Récente',
                                    'lien': lien,
                                    'source': 'LinkedIn',
                                    'type': 'Stage',
                                    'secteur': secteur,
                                    'valide': True
                                })
                                
                            except:
                                continue
                                
                except:
                    continue
            
            return offres
            
        except Exception as e:
            st.warning(f"⚠️ Erreur LinkedIn: {e}")
            return []
    
    def search_all_real_offers(self, secteur: str, ville: str = "Casablanca") -> List[Dict]:
        """Recherche sur TOUTES les plateformes réelles"""
        st.info(f"🔍 Recherche d'offres RÉELLES: {secteur} à {ville}")
        
        all_offres = []
        
        # 1. Rekrute.com (Maroc)
        try:
            offres_rekrute = self.search_rekrute_real(secteur, ville)
            if offres_rekrute:
                st.success(f"✅ {len(offres_rekrute)} offres sur Rekrute.com")
                all_offres.extend(offres_rekrute)
        except Exception as e:
            st.warning(f"⚠️ Rekrute.com inaccessible: {e}")
        
        # 2. Emploi.ma (Maroc)
        try:
            offres_emploi = self.search_emploi_ma_real(secteur)
            if offres_emploi:
                st.success(f"✅ {len(offres_emploi)} offres sur Emploi.ma")
                all_offres.extend(offres_emploi)
        except Exception as e:
            st.warning(f"⚠️ Emploi.ma inaccessible: {e}")
        
        # 3. MarocAnnonces
        try:
            offres_annonces = self.search_marocannonces(secteur)
            if offres_annonces:
                st.success(f"✅ {len(offres_annonces)} offres sur MarocAnnonces")
                all_offres.extend(offres_annonces)
        except Exception as e:
            st.warning(f"⚠️ MarocAnnonces inaccessible: {e}")
        
        # 4. LinkedIn (alternative)
        if len(all_offres) < 5:  # Si pas assez d'offres
            try:
                offres_linkedin = self.search_linkedin_api(secteur, ville)
                if offres_linkedin:
                    st.success(f"✅ {len(offres_linkedin)} offres sur LinkedIn")
                    all_offres.extend(offres_linkedin)
            except Exception as e:
                st.warning(f"⚠️ LinkedIn inaccessible: {e}")
        
        # Supprimer les doublons
        unique_offres = []
        seen = set()
        
        for offre in all_offres:
            key = (offre['titre'][:50], offre['entreprise'][:30])
            if key not in seen:
                seen.add(key)
                unique_offres.append(offre)
        
        # Trier par validité (liens valides d'abord)
        valid_offres = [o for o in unique_offres if o.get('valide', False)]
        other_offres = [o for o in unique_offres if not o.get('valide', False)]
        
        return valid_offres + other_offres[:20]  # 20 offres max
    
    def verify_offer_link(self, url: str) -> bool:
        """Vérifie si un lien d'offre est accessible"""
        try:
            if not url or url == "Non disponible":
                return False
            
            # Vérifier que c'est une URL valide
            if not url.startswith('http'):
                return False
            
            # Essayer d'accéder à la page
            response = self.session.head(url, timeout=10, allow_redirects=True)
            
            # Codes HTTP acceptables: 200, 301, 302
            return response.status_code in [200, 301, 302]
            
        except:
            return False