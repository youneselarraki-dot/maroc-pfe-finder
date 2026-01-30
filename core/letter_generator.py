import streamlit as st
from datetime import datetime
import json
from typing import Dict, List, Optional
import os

class LetterGenerator:
    """Générateur intelligent de lettres de motivation"""
    
    def __init__(self):
        self.templates = self._load_templates()
        self.sector_keywords = self._load_sector_keywords()
    
    def _load_templates(self) -> Dict:
        """Charge les templates de lettres par secteur"""
        return {
            'informatique': {
                'title': "Lettre de Motivation - Stage PFE Développement",
                'template': """{header}

{date}

{company_info}

Objet : Candidature pour un stage de fin d'études - {position}

Madame, Monsieur,

Étudiant(e) en {degree} à {school}, je suis actuellement à la recherche d'un stage de fin d'études dans le domaine du développement {specialization}. Votre annonce pour le poste de "{position}" a particulièrement retenu mon attention et je souhaite vivement intégrer votre entreprise pour mon projet de fin d'études.

Au cours de ma formation, j'ai acquis des compétences solides en :
{technical_skills}

J'ai également réalisé plusieurs projets académiques incluant :
{projects}

Mon intérêt pour {company_name} repose sur votre expertise dans {company_expertise}. Je suis persuadé(e) que votre entreprise constitue un environnement idéal pour mettre en pratique mes connaissances et contribuer à vos projets innovants.

Disponible à partir du {start_date} pour une période de {duration}, je serais honoré(e) de vous rencontrer afin de vous exposer plus en détail ma motivation et mes compétences.

Dans l'attente de votre réponse, je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{signature}"""
            },
            
            'telecom': {
                'title': "Lettre de Motivation - Stage Ingénieur Réseaux",
                'template': """{header}

{date}

{company_info}

Objet : Candidature pour un stage PFE - {position}

Madame, Monsieur,

Actuellement en dernière année d'ingénierie en Télécommunications à {school}, je me permets de vous adresser ma candidature pour le stage de fin d'études "{position}" au sein de {company_name}.

Passionné(e) par les technologies des télécommunications et plus particulièrement par {specialization}, je souhaite approfondir mes connaissances pratiques dans un environnement professionnel tel que le vôtre.

Mes compétences techniques incluent :
{technical_skills}

Mon parcours académique m'a permis de travailler sur :
{projects}

L'excellente réputation de {company_name} dans le secteur des télécommunications au Maroc et vos projets innovants dans le domaine du {company_expertise} m'incitent à vous proposer ma candidature.

Je serais disponible à partir du {start_date} pour une durée de {duration}. Mon stage de fin d'études portera sur "{project_title}".

Je reste à votre disposition pour un entretien afin de vous exposer plus en détail mes motivations.

Veuillez agréer, Madame, Monsieur, l'expression de mes salutations les plus respectueuses.

{signature}"""
            },
            
            'finance': {
                'title': "Lettre de Motivation - Stage Analyse Financière",
                'template': """{header}

{header}

{date}

{company_info}

Objet : Candidature pour un stage PFE - {position}

Madame, Monsieur,

Étudiant(e) en Master {degree} à {school}, je suis à la recherche d'un stage de fin d'études dans le secteur {specialization}. Votre annonce pour le poste de "{position}" correspond parfaitement à mes aspirations professionnelles.

Au cours de ma formation, j'ai développé des compétences en :
{technical_skills}

Mes projets académiques incluent :
{projects}

L'expertise de {company_name} dans le domaine {company_expertise} et votre position de leader dans le secteur bancaire marocain représentent pour moi une opportunité unique d'apprentissage.

Je serais disponible à partir du {start_date} pour une période de {duration}. Mon projet de fin d'études traitera de "{project_title}".

Dans l'espoir que ma candidature retienne votre attention, je me tiens à votre disposition pour un entretien.

Je vous prie d'agréer, Madame, Monsieur, l'expression de mes salutations distinguées.

{signature}"""
            },
            
            'default': {
                'title': "Lettre de Motivation - Stage PFE",
                'template': """{header}

{date}

{company_info}

Objet : Candidature pour un stage de fin d'études - {position}

Madame, Monsieur,

Étudiant(e) en {degree} à {school}, je suis actuellement à la recherche d'un stage de fin d'études dans le domaine {specialization}. Votre annonce pour le poste de "{position}" a retenu toute mon attention.

Mes compétences acquises au cours de ma formation :
{technical_skills}

Projets réalisés :
{projects}

Mon intérêt pour {company_name} est motivé par votre expertise dans {company_expertise}. Je suis convaincu(e) que votre entreprise me permettra de mettre en pratique mes connaissances et de contribuer à vos projets.

Disponible à partir du {start_date} pour une durée de {duration}, je serais ravi(e) de vous rencontrer pour discuter de ma candidature.

Dans l'attente de votre réponse, je vous prie d'agréer, Madame, Monsieur, mes salutations respectueuses.

{signature}"""
            }
        }
    
    def _load_sector_keywords(self) -> Dict:
        """Mots-clés par secteur pour personnalisation"""
        return {
            'informatique': {
                'technical_skills': [
                    "Développement Full-Stack (React, Node.js, Python)",
                    "Bases de données SQL et NoSQL",
                    "Architecture microservices et APIs REST",
                    "Méthodes Agile et DevOps",
                    "Cloud Computing (AWS, Azure)",
                    "Sécurité informatique et bonnes pratiques"
                ],
                'projects': [
                    "Développement d'une application web de gestion",
                    "Création d'une API REST pour service e-commerce",
                    "Migration d'application vers le cloud",
                    "Projet de machine learning pour analyse de données"
                ],
                'specializations': [
                    "développement web", 
                    "développement mobile",
                    "data science", 
                    "cybersécurité",
                    "cloud computing",
                    "intelligence artificielle"
                ]
            },
            'telecom': {
                'technical_skills': [
                    "Réseaux TCP/IP et architectures réseau",
                    "Technologies 4G/5G et réseaux mobiles",
                    "Sécurité des réseaux et firewall",
                    "Virtualisation et SDN",
                    "Administration systèmes Linux/Windows",
                    "Protocoles de routage (OSPF, BGP)"
                ],
                'projects': [
                    "Simulation de réseau d'entreprise",
                    "Étude de déploiement fibre optique",
                    "Sécurisation de réseau local",
                    "Analyse de performances réseau"
                ],
                'specializations': [
                    "réseaux et télécommunications",
                    "sécurité réseau",
                    "téléphonie mobile",
                    "fibre optique",
                    "ingénierie réseau"
                ]
            },
            'finance': {
                'technical_skills': [
                    "Analyse financière et modélisation",
                    "Gestion de portefeuille et risque",
                    "Outils Excel avancés et VBA",
                    "Logiciels bancaires (SAP, Bloomberg)",
                    "Réglementation bancaire Maroc",
                    "Analyse de données financières"
                ],
                'projects': [
                    "Étude de marché financier",
                    "Modélisation de risque de crédit",
                    "Analyse de performance d'entreprise",
                    "Projet de fintech"
                ],
                'specializations': [
                    "analyse financière",
                    "banque d'investissement",
                    "gestion de risque",
                    "fintech",
                    "audit financier"
                ]
            }
        }
    
    def generate_letter(self, offer_data: Dict, student_info: Dict) -> str:
        """Génère une lettre de motivation personnalisée"""
        
        # Déterminer le secteur
        secteur = self._detect_sector(offer_data.get('secteur', ''))
        
        # Récupérer le template adapté
        template_info = self.templates.get(secteur, self.templates['default'])
        template = template_info['template']
        
        # Préparer les données de remplacement
        replacement_data = self._prepare_replacement_data(offer_data, student_info, secteur)
        
        # Appliquer les remplacements
        letter = template.format(**replacement_data)
        
        return {
            'content': letter,
            'title': template_info['title'],
            'filename': f"Lettre_Motivation_{offer_data['entreprise'].replace(' ', '_')}_{datetime.now().strftime('%Y%m%d')}.txt"
        }
    
    def _detect_sector(self, secteur: str) -> str:
        """Détecte le secteur à partir du texte"""
        secteur_lower = secteur.lower()
        
        if any(word in secteur_lower for word in ['informatique', 'it', 'développement', 'programmation', 'software']):
            return 'informatique'
        elif any(word in secteur_lower for word in ['telecom', 'télécom', 'réseau', 'téléphonie']):
            return 'telecom'
        elif any(word in secteur_lower for word in ['finance', 'banque', 'bancaire', 'assurance']):
            return 'finance'
        else:
            return 'default'
    
    def _prepare_replacement_data(self, offer: Dict, student: Dict, secteur: str) -> Dict:
        """Prépare les données de remplacement pour le template"""
        
        # Informations étudiant (par défaut si non fournies)
        default_student = {
            'full_name': 'Prénom NOM',
            'address': 'Adresse, Ville, Maroc',
            'phone': '+212 6 XX XX XX XX',
            'email': 'email@domain.com',
            'linkedin': 'linkedin.com/in/votrenom',
            'degree': 'Ingénierie en Informatique',
            'school': 'École/Université',
            'start_date': '01 février 2024',
            'duration': '6 mois',
            'project_title': 'Développement d\'application innovante'
        }
        
        # Fusionner avec les infos étudiant fournies
        student_info = {**default_student, **student}
        
        # Informations entreprise
        company_info = f"""
{offer.get('entreprise', 'Entreprise')}
Service RH / Recrutement
{offer.get('lieu', 'Casablanca')}, Maroc
"""
        
        # Compétences techniques selon le secteur
        sector_keywords = self.sector_keywords.get(secteur, self.sector_keywords.get('informatique', {}))
        technical_skills_list = sector_keywords.get('technical_skills', [])
        projects_list = sector_keywords.get('projects', [])
        specializations = sector_keywords.get('specializations', ['développement'])
        
        # Choix aléatoire pour varier les lettres
        import random
        technical_skills = "\n".join([f"- {skill}" for skill in random.sample(technical_skills_list, min(4, len(technical_skills_list)))])
        projects = "\n".join([f"- {project}" for project in random.sample(projects_list, min(2, len(projects_list)))])
        specialization = random.choice(specializations)
        
        # Expertises entreprise
        company_expertise_options = [
            "les technologies innovantes",
            "la transformation digitale",
            "le développement de solutions sur mesure",
            "l'excellence opérationnelle",
            "l'innovation technologique"
        ]
        company_expertise = random.choice(company_expertise_options)
        
        # En-tête
        header = f"""
{student_info['full_name']}
{student_info['address']}
Tél : {student_info['phone']}
Email : {student_info['email']}
LinkedIn : {student_info['linkedin']}
"""
        
        # Signature
        signature = f"""
Cordialement,

{student_info['full_name']}
"""
        
        return {
            'header': header,
            'date': datetime.now().strftime("Fait à %Ville, le %d/%m/%Y"),
            'company_info': company_info,
            'position': offer.get('titre', 'Stage PFE'),
            'degree': student_info['degree'],
            'school': student_info['school'],
            'specialization': specialization,
            'technical_skills': technical_skills,
            'projects': projects,
            'company_name': offer.get('entreprise', 'votre entreprise'),
            'company_expertise': company_expertise,
            'start_date': student_info['start_date'],
            'duration': student_info['duration'],
            'project_title': student_info['project_title'],
            'signature': signature
        }
    
    def get_student_form_fields(self) -> List[Dict]:
        """Retourne les champs du formulaire étudiant"""
        return [
            {
                'key': 'full_name',
                'label': 'Nom complet',
                'type': 'text',
                'placeholder': 'Prénom NOM',
                'required': True
            },
            {
                'key': 'address',
                'label': 'Adresse',
                'type': 'text',
                'placeholder': 'Adresse, Ville, Maroc',
                'required': True
            },
            {
                'key': 'phone',
                'label': 'Téléphone',
                'type': 'text',
                'placeholder': '+212 6 XX XX XX XX',
                'required': True
            },
            {
                'key': 'email',
                'label': 'Email',
                'type': 'email',
                'placeholder': 'email@domain.com',
                'required': True
            },
            {
                'key': 'linkedin',
                'label': 'Profil LinkedIn',
                'type': 'text',
                'placeholder': 'linkedin.com/in/votrenom',
                'required': False
            },
            {
                'key': 'degree',
                'label': 'Diplôme en cours',
                'type': 'text',
                'placeholder': 'Ex: Master en Informatique',
                'required': True
            },
            {
                'key': 'school',
                'label': 'École/Université',
                'type': 'text',
                'placeholder': 'Nom de votre établissement',
                'required': True
            },
            {
                'key': 'start_date',
                'label': 'Date de début du stage',
                'type': 'text',
                'placeholder': 'Ex: 01 février 2024',
                'required': True
            },
            {
                'key': 'duration',
                'label': 'Durée du stage',
                'type': 'text',
                'placeholder': 'Ex: 6 mois',
                'required': True
            },
            {
                'key': 'project_title',
                'label': 'Titre du projet PFE (optionnel)',
                'type': 'text',
                'placeholder': 'Titre de votre projet de fin d\'études',
                'required': False
            }
        ]