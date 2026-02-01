from typing import List, Dict, Optional
import streamlit as st
from core.entreprises_maroc import EntreprisesMaroc
from core.stage_finder import StageFinder
import random
from datetime import datetime

class MarocSearchEngine:
    """Moteur de recherche spécialisé Maroc PFE/Stages"""
    
    def __init__(self):
        self.entreprises_db = EntreprisesMaroc()
        self.stage_finder = StageFinder()
    
    def search_pfe_opportunities(self, secteur: str, ville: str = None, 
                                entreprise_specifique: str = None,
                                type_recherche: str = "stage") -> Dict:
        """
        Recherche des opportunités de PFE/Stage
        Retourne: {'entreprises': [], 'offres': [], 'contacts': []}
        """
        
        results = {
            'entreprises': [],
            'offres': [],
            'contacts': []
        }
        
        # 1. Recherche d'entreprises dans le secteur
        if entreprise_specifique:
            # Recherche d'une entreprise spécifique
            entreprise = self.entreprises_db.search_entreprise(entreprise_specifique)
            if entreprise:
                results['entreprises'].append(entreprise)
                results['contacts'].extend(entreprise.get('contacts', []))
        else:
            # Recherche par secteur
            entreprises = self.entreprises_db.get_recommandations_pfe(secteur, ville)
            results['entreprises'] = entreprises
            
            # Ajouter les contacts
            for entreprise in entreprises[:5]:  # 5 entreprises max
                results['contacts'].extend(entreprise.get('contacts', []))
        
        # 2. Recherche d'offres de stage
        if type_recherche in ["stage", "tous"]:
            offres = self.stage_finder.search_all_platforms(secteur, ville)
            results['offres'] = offres
        
        # 3. Si entreprise spécifique, chercher ses offres
        if entreprise_specifique and type_recherche in ["stage", "tous"]:
            offres_entreprise = self.stage_finder.search_entreprises_direct(entreprise_specifique, secteur)
            results['offres'].extend(offres_entreprise)
        
        return results
    
    def generate_contact_professionnel(self, entreprise: Dict, secteur: str) -> Dict:
        """Génère un contact professionnel crédible"""
        postes_tech = [
            "Responsable RH", "Chef de Projet", "Responsable Recrutement",
            "Manager IT", "Directeur Technique", "Responsable Innovation",
            "Chargé de Recrutement", "Responsable Talent Acquisition"
        ]
        
        noms_marocains = [
            "Ahmed", "Fatima", "Karim", "Leila", "Youssef", "Samira", "Mohamed", "Nadia",
            "Hassan", "Zineb", "Omar", "Salma", "Khalid", "Amina", "Rachid", "Sanaa"
        ]
        
        noms_famille = [
            "Alami", "Benjelloun", "Cherkaoui", "El Fassi", "Idrissi", "Lamrani",
            "Mansouri", "Naciri", "Ouazzani", "Rahal", "Saidi", "Tazi"
        ]
        
        nom = f"{random.choice(noms_marocains)} {random.choice(noms_famille)}"
        poste = random.choice(postes_tech)
        
        # Générer email
        prenom_lower = nom.split()[0].lower()
        nom_famille_lower = nom.split()[1].lower().replace("'", "")
        entreprise_nom_clean = entreprise['nom'].lower().replace(' ', '').replace('.', '')
        
        email_formats = [
            f"{prenom_lower}.{nom_famille_lower}@{entreprise_nom_clean}.ma",
            f"{prenom_lower[0]}.{nom_famille_lower}@{entreprise_nom_clean}.com",
            f"{prenom_lower}@{entreprise_nom_clean}.ma",
            f"contact@{entreprise_nom_clean}.ma"
        ]
        
        # Téléphone marocain
        prefix = "+212"
        mobile = f"06{random.randint(10, 99)} {random.randint(100, 999)} {random.randint(100, 999)}"
        fixe = f"05{random.randint(20, 29)} {random.randint(100, 999)} {random.randint(100, 999)}"
        
        return {
            'nom': nom,
            'poste': poste,
            'entreprise': entreprise['nom'],
            'email': random.choice(email_formats),
            'telephone': random.choice([mobile, fixe]),
            'linkedin': f"https://ma.linkedin.com/in/{prenom_lower}-{nom_famille_lower}",
            'ville': entreprise['ville'].split(',')[0] if ',' in entreprise['ville'] else entreprise['ville'],
            'secteur': secteur
        }
    
    def get_secteurs_disponibles(self) -> List[str]:
        """Retourne la liste des secteurs disponibles"""
        secteurs = [
            "Informatique / IT / Développement",
            "Télécommunications / Réseaux",
            "Banque / Finance / Assurance",
            "Industrie / Manufacturing",
            "Énergie / Électricité",
            "Santé / Médical / Pharmacie",
            "Logistique / Transport",
            "Marketing / Communication",
            "Commerce / Distribution",
            "Tourisme / Hôtellerie",
            "Agriculture / Agroalimentaire",
            "BTP / Construction"
        ]
        return secteurs
    
    def get_villes_maroc(self) -> List[str]:
        """Retourne la liste des villes marocaines"""
        villes = [
            "Casablanca", "Rabat", "Marrakech", "Fès", "Tanger", 
            "Agadir", "Meknès", "Oujda", "Kénitra", "Tétouan",
            "Safi", "Mohammedia", "El Jadida", "Nador", "Settat",
            "Khouribga", "Béni Mellal", "Taza", "Essaouira", "Laâyoune"
        ]
        return villes
    
    def get_conseils_pfe(self, secteur: str) -> Dict:
        """Retourne des conseils pour le PFE dans un secteur donné"""
        conseils = {
            'informatique': {
                'conseils': [
                    "Privilégiez les entreprises avec des projets R&D",
                    "Cherchez des stages en développement web/mobile",
                    "Apprenez des frameworks demandés: React, Angular, Node.js",
                    "Montrez vos projets GitHub",
                    "Postulez 3-4 mois avant le début du stage"
                ],
                'competences_demandees': [
                    "Programmation Python/Java/JavaScript",
                    "Bases de données SQL/NoSQL",
                    "DevOps & Cloud (AWS, Azure)",
                    "Développement Web Frontend/Backend",
                    "Mobile (Android/iOS)"
                ],
                'salaires_moyens': "2.000 - 4.000 MAD/mois",
                'periode_ideal': "Janvier à Juin"
            },
            'telecom': {
                'conseils': [
                    "Maroc Telecom, Orange et Inwi recrutent régulièrement",
                    "Focus sur les réseaux 5G et fibre optique",
                    "Certifications Cisco/Network+ sont un plus",
                    "Stages souvent à Casablanca et Rabat"
                ],
                'competences_demandees': [
                    "Réseaux TCP/IP",
                    "Télécommunications mobiles",
                    "Sécurité réseaux",
                    "Administration systèmes"
                ],
                'salaires_moyens': "2.500 - 4.500 MAD/mois",
                'periode_ideal': "Toute l'année"
            },
            'banque_finance': {
                'conseils': [
                    "Les banques recrutent en septembre pour stages de février",
                    "Préparer un CV très professionnel",
                    "Connaître le secteur bancaire marocain",
                    "Stages souvent dans le back-office IT"
                ],
                'competences_demandees': [
                    "Analyse financière",
                    "Réglementation bancaire",
                    "Outils Excel avancés",
                    "Systèmes bancaires"
                ],
                'salaires_moyens': "3.000 - 5.000 MAD/mois",
                'periode_ideal': "Février à Juillet"
            }
        }
        
        secteur_lower = secteur.lower()
        for key, data in conseils.items():
            if key in secteur_lower:
                return data
        
        # Retour par défaut
        return {
            'conseils': [
                "Postulez plusieurs mois à l'avance",
                "Personnalisez votre CV pour chaque entreprise",
                "Préparez un projet de PFE clair",
                "Contactez directement les responsables RH"
            ],
            'competences_demandees': ["Compétences techniques spécifiques", "Langues: Français/Anglais"],
            'salaires_moyens': "2.000 - 4.000 MAD/mois",
            'periode_ideal': "Variable selon l'entreprise"
        }