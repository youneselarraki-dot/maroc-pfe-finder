import json
import os
from typing import List, Dict, Optional
import streamlit as st

class EntreprisesMaroc:
    """Base de données des entreprises marocaines par secteur"""
    
    def __init__(self):
        self.data_file = os.path.join(os.path.dirname(__file__), '..', 'data', 'entreprises_maroc.json')
        self.entreprises = self._load_data()
    
    def _load_data(self):
        """Charge la base de données des entreprises"""
        entreprises_data = {
            'informatique': [
                {
                    'nom': 'Atos Maroc',
                    'ville': 'Casablanca',
                    'site_web': 'https://atos.net/maroc',
                    'specialite': 'Services IT, Consulting',
                    'contacts': [
                        {'nom': 'Service RH', 'email': 'rh.maroc@atos.net', 'telephone': '+212 5 22 XX XX XX'},
                        {'nom': 'Service Recrutement', 'email': 'recrutement.maroc@atos.net'}
                    ],
                    'offres_stage': True,
                    'type': 'ESN/SSII'
                },
                {
                    'nom': 'Capgemini Maroc',
                    'ville': 'Casablanca, Rabat',
                    'site_web': 'https://www.capgemini.com/ma-ma/',
                    'specialite': 'Transformation digitale, IT',
                    'contacts': [
                        {'nom': 'Service Carrières', 'email': 'maroc.careers@capgemini.com'},
                        {'nom': 'RH Maroc', 'email': 'rh.maroc@capgemini.com'}
                    ],
                    'offres_stage': True,
                    'type': 'ESN'
                },
                {
                    'nom': 'IBM Maroc',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.ibm.com/ma-fr',
                    'specialite': 'Cloud, IA, Solutions IT',
                    'contacts': [
                        {'nom': 'Recrutement Maroc', 'email': 'recrutement.ma@ibm.com'}
                    ],
                    'offres_stage': True,
                    'type': 'Éditeur Logiciel'
                },
                {
                    'nom': 'Microsoft Maroc',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.microsoft.com/fr-ma',
                    'specialite': 'Logiciels, Cloud Azure',
                    'contacts': [
                        {'nom': 'Contact Maroc', 'email': 'infoma@microsoft.com'}
                    ],
                    'offres_stage': True,
                    'type': 'Éditeur'
                },
                {
                    'nom': 'Oracle Maroc',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.oracle.com/ma/',
                    'specialite': 'Bases de données, ERP',
                    'contacts': [
                        {'nom': 'Service Client Maroc', 'email': 'ma-info_ww@oracle.com'}
                    ],
                    'offres_stage': True,
                    'type': 'Éditeur'
                },
                {
                    'nom': 'HPS Maroc',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.hps-worldwide.com/',
                    'specialite': 'Solutions de paiement',
                    'contacts': [
                        {'nom': 'RH Maroc', 'email': 'careers@hps-inc.com'}
                    ],
                    'offres_stage': True,
                    'type': 'Fintech'
                },
                {
                    'nom': 'SQLI Maroc',
                    'ville': 'Casablanca, Rabat',
                    'site_web': 'https://www.sqli.ma/',
                    'specialite': 'Digital, E-commerce',
                    'contacts': [
                        {'nom': 'Recrutement', 'email': 'recrutement.ma@sqli.com'}
                    ],
                    'offres_stage': True,
                    'type': 'Agence Web'
                },
                {
                    'nom': 'Sofrecom Maroc',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.sofrecom.com/fr/',
                    'specialite': 'Télécoms, Digital',
                    'contacts': [
                        {'nom': 'Carrières Maroc', 'email': 'maroc@sofrecom.com'}
                    ],
                    'offres_stage': True,
                    'type': 'ESN'
                }
            ],
            'telecom': [
                {
                    'nom': 'Maroc Telecom',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.iam.ma/',
                    'specialite': 'Télécommunications',
                    'contacts': [
                        {'nom': 'Recrutement', 'email': 'recrutement@iam.ma'},
                        {'nom': 'Service RH', 'email': 'drh@iam.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Opérateur Télécom'
                },
                {
                    'nom': 'Orange Maroc',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.orange.ma/',
                    'specialite': 'Télécommunications, Mobile',
                    'contacts': [
                        {'nom': 'Carrières', 'email': 'recrutement@orange.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Opérateur'
                },
                {
                    'nom': 'Inwi',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.inwi.ma/',
                    'specialite': 'Télécoms, Internet',
                    'contacts': [
                        {'nom': 'RH', 'email': 'rh@inwi.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Opérateur'
                }
            ],
            'banque_finance': [
                {
                    'nom': 'Attijariwafa Bank',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.attijariwafabank.com/',
                    'specialite': 'Banque, Finance',
                    'contacts': [
                        {'nom': 'Service RH', 'email': 'rh@attijariwafabank.com'}
                    ],
                    'offres_stage': True,
                    'type': 'Banque'
                },
                {
                    'nom': 'BMCE Bank',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.bmcebank.ma/',
                    'specialite': 'Banque Commerciale',
                    'contacts': [
                        {'nom': 'Recrutement', 'email': 'recrutement@bmcebank.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Banque'
                },
                {
                    'nom': 'Banque Populaire',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.gbp.ma/',
                    'specialite': 'Banque, Finance',
                    'contacts': [
                        {'nom': 'Direction RH', 'email': 'drh@gbp.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Banque'
                }
            ],
            'industrie': [
                {
                    'nom': 'OCP Group',
                    'ville': 'Casablanca, Khouribga',
                    'site_web': 'https://www.ocpgroup.ma/',
                    'specialite': 'Phosphates, Engrais',
                    'contacts': [
                        {'nom': 'Recrutement', 'email': 'recrutement@ocpgroup.ma'},
                        {'nom': 'Service Stages', 'email': 'stages@ocpgroup.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Industrie Chimique'
                },
                {
                    'nom': 'Managem',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.managemgroup.com/',
                    'specialite': 'Mines, Métaux',
                    'contacts': [
                        {'nom': 'RH', 'email': 'rh@managemgroup.com'}
                    ],
                    'offres_stage': True,
                    'type': 'Mining'
                },
                {
                    'nom': 'LafargeHolcim Maroc',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.lafargeholcim.ma/',
                    'specialite': 'Ciment, BTP',
                    'contacts': [
                        {'nom': 'Carrières', 'email': 'recrutement.ma@lafargeholcim.com'}
                    ],
                    'offres_stage': True,
                    'type': 'Matériaux Construction'
                }
            ],
            'energie': [
                {
                    'nom': 'ONEE',
                    'ville': 'Casablanca, Rabat',
                    'site_web': 'https://www.one.org.ma/',
                    'specialite': 'Eau, Électricité',
                    'contacts': [
                        {'nom': 'Service RH', 'email': 'drh@one.org.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Énergie'
                },
                {
                    'nom': 'MASEN',
                    'ville': 'Rabat',
                    'site_web': 'https://www.masen.ma/',
                    'specialite': 'Énergies Renouvelables',
                    'contacts': [
                        {'nom': 'Recrutement', 'email': 'recrutement@masen.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Énergie Solaire'
                }
            ],
            'sante': [
                {
                    'nom': 'Pharmalog',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.pharmalog.ma/',
                    'specialite': 'Pharmacie, Distribution',
                    'contacts': [
                        {'nom': 'RH', 'email': 'rh@pharmalog.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Santé'
                },
                {
                    'nom': 'Cooper Pharma',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.cooperpharma.com/',
                    'specialite': 'Pharmaceutique',
                    'contacts': [
                        {'nom': 'Recrutement', 'email': 'rh@cooperpharma.com'}
                    ],
                    'offres_stage': True,
                    'type': 'Pharma'
                }
            ],
            'logistique': [
                {
                    'nom': 'Marsa Maroc',
                    'ville': 'Casablanca',
                    'site_web': 'https://www.marsamaroc.co.ma/',
                    'specialite': 'Logistique Portuaire',
                    'contacts': [
                        {'nom': 'Service RH', 'email': 'rh@marsamaroc.co.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Logistique'
                },
                {
                    'nom': 'Tanger Med',
                    'ville': 'Tanger',
                    'site_web': 'https://www.tangermed.ma/',
                    'specialite': 'Port, Logistique',
                    'contacts': [
                        {'nom': 'Carrières', 'email': 'recrutement@tangermed.ma'}
                    ],
                    'offres_stage': True,
                    'type': 'Portuaire'
                }
            ]
        }
        return entreprises_data
    
    def get_entreprises_by_sector(self, secteur: str) -> List[Dict]:
        """Retourne les entreprises d'un secteur donné"""
        secteur_lower = secteur.lower()
        
        # Mapping des secteurs
        secteur_mapping = {
            'informatique': ['informatique', 'it', 'développement', 'programmation', 'software', 'technologie'],
            'telecom': ['telecom', 'télécommunications', 'réseaux', 'téléphonie'],
            'banque_finance': ['banque', 'finance', 'assurance', 'bancaire', 'fintech'],
            'industrie': ['industrie', 'manufacturing', 'production', 'usine'],
            'energie': ['énergie', 'électricité', 'pétrole', 'gaz', 'renouvelable'],
            'sante': ['santé', 'médical', 'pharmacie', 'médicale', 'hospitalier'],
            'logistique': ['logistique', 'transport', 'supply chain', 'distribution']
        }
        
        # Trouver le secteur correspondant
        for key, keywords in secteur_mapping.items():
            if any(kw in secteur_lower for kw in keywords):
                return self.entreprises.get(key, [])
        
        return []
    
    def search_entreprise(self, nom_entreprise: str) -> Optional[Dict]:
        """Recherche une entreprise par nom"""
        nom_lower = nom_entreprise.lower()
        
        for secteur, entreprises in self.entreprises.items():
            for entreprise in entreprises:
                if nom_lower in entreprise['nom'].lower():
                    return entreprise
        
        return None
    
    def get_all_sectors(self) -> List[str]:
        """Retourne tous les secteurs disponibles"""
        return list(self.entreprises.keys())
    
    def get_recommandations_pfe(self, secteur: str, ville: str = None) -> List[Dict]:
        """Retourne des recommandations pour PFE par secteur et ville"""
        entreprises = self.get_entreprises_by_sector(secteur)
        
        if ville:
            entreprises = [e for e in entreprises if ville.lower() in e['ville'].lower()]
        
        # Filtrer celles avec offres de stage
        entreprises_stage = [e for e in entreprises if e.get('offres_stage', False)]
        
        return entreprises_stage[:10]  # Limiter à 10