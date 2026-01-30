import streamlit as st
import pandas as pd
from datetime import datetime
import time
import os

# Import des modules Maroc
from core.maroc_search import MarocSearchEngine
from core.entreprises_maroc import EntreprisesMaroc
from core.stage_finder import StageFinder
from core.letter_generator import LetterGenerator  # NOUVEAU IMPORT

# Configuration
st.set_page_config(
    page_title="🔍 Maroc PFE Finder - Recherche de Stages",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# États de session
if 'search_results' not in st.session_state:
    st.session_state.search_results = {}
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'saved_offers' not in st.session_state:
    st.session_state.saved_offers = []
if 'current_offers' not in st.session_state:
    st.session_state.current_offers = []
if 'student_info' not in st.session_state:
    st.session_state.student_info = {}
if 'current_page' not in st.session_state:
    st.session_state.current_page = "🔍 Recherche Stage"

# Initialisation
engine = MarocSearchEngine()
entreprises_db = EntreprisesMaroc()
letter_generator = LetterGenerator()  # NOUVEAU

def main():
    """Application principale"""
    
    # Sidebar
    with st.sidebar:
        st.title("🎓 Maroc PFE Finder")
        st.markdown("---")
        
        # Menu UNIQUE - SUPPRIME LE DEUXIÈME MENU PLUS BAS
        page = st.radio(
            "Navigation",
            [
                "🔍 Recherche Stage", 
                "🏢 Entreprises", 
                "💼 Offres", 
                "📝 Lettre de Motivation",  # NOUVEAU
                "📚 Conseils PFE", 
                "💾 Mes Favoris"
            ],
            index=0
        )
        
        st.markdown("---")
        
        # Statistiques
        if st.session_state.search_history:
            st.subheader("📈 Mes Recherches")
            total = len(st.session_state.search_history)
            st.metric("Recherches", total)
            
            last_search = st.session_state.search_history[-1]
            st.caption(f"Dernière: {last_search.get('criteria', 'N/A')}")
        
        st.markdown("---")
        st.caption("📍 Spécialisé Maroc | 🎓 Stages PFE | 💼 Premiers emplois")
    
    # Gestion de la redirection depuis les boutons "📝"
    if 'selected_offer_for_letter' in st.session_state:
        page = "📝 Lettre de Motivation"
        # On garde l'offre sélectionnée dans session_state
    
    # Page: Recherche Stage
    if page == "🔍 Recherche Stage":
        render_search_page()
    
    # Page: Entreprises
    elif page == "🏢 Entreprises":
        render_companies_page()
    
    # Page: Offres
    elif page == "💼 Offres":
        render_offers_page()
    
    # Page: Lettre de Motivation
    elif page == "📝 Lettre de Motivation":  # NOUVELLE PAGE
        render_letter_page()
    
    # Page: Conseils
    elif page == "📚 Conseils PFE":
        render_advice_page()
    
    # Page: Favoris
    elif page == "💾 Mes Favoris":
        render_favorites_page()

def render_letter_page():
    """Page de génération de lettres de motivation"""
    
    st.title("📝 Générateur de Lettre de Motivation")
    st.caption("Créez une lettre de motivation personnalisée pour vos candidatures")
    
    # Vérifier si l'utilisateur a des offres sauvegardées
    if not st.session_state.saved_offers:
        st.warning("💡 Vous devez d'abord sauvegarder des offres pour générer des lettres.")
        st.info("""
        **Pour commencer :**
        1. Allez sur la page **🔍 Recherche Stage**
        2. Trouvez des offres intéressantes
        3. Sauvegardez-les avec le bouton 💾
        4. Revenez ici pour générer vos lettres
        """)
        return
    
    # Onglets
    tab1, tab2 = st.tabs(["📄 Générer une lettre", "📋 Mes informations"])
    
    with tab1:
        # Sélection de l'offre
        saved_offers = [o for o in st.session_state.saved_offers if o['type'] == 'offre']
        saved_companies = [o for o in st.session_state.saved_offers if o['type'] == 'entreprise']
        
        if not saved_offers and not saved_companies:
            st.info("ℹ️ Aucune offre ou entreprise sauvegardée.")
            return
        
        # Si redirection depuis bouton "📝", pré-sélectionner cette offre
        preselected_index = 0
        if 'selected_offer_for_letter' in st.session_state:
            # Chercher l'offre dans saved_offers
            for i, item in enumerate(st.session_state.saved_offers):
                if item['type'] == 'offre' and item['data'] == st.session_state.selected_offer_for_letter:
                    preselected_index = i
                    break
        
        # Liste des offres disponibles
        offer_options = []
        for i, offer in enumerate(saved_offers):
            offer_options.append({
                'label': f"💼 {offer['data']['titre']} - {offer['data']['entreprise']}",
                'value': f"offre_{i}",
                'type': 'offre',
                'data': offer['data'],
                'index': i
            })
        
        for i, company in enumerate(saved_companies):
            offer_options.append({
                'label': f"🏢 Entreprise: {company['data']['nom']}",
                'value': f"entreprise_{i}",
                'type': 'entreprise',
                'data': {
                    'entreprise': company['data']['nom'],
                    'titre': f"Stage PFE",
                    'lieu': company['data']['ville'],
                    'secteur': company['data'].get('type', 'Informatique')
                },
                'index': i
            })
        
        # Sélecteur d'offre
        if offer_options:
            # Pré-sélectionner si redirection
            default_index = 0
            if 'selected_offer_for_letter' in st.session_state:
                # Trouver l'index de l'offre présélectionnée
                for idx, opt in enumerate(offer_options):
                    if opt['type'] == 'offre' and opt['data'] == st.session_state.selected_offer_for_letter:
                        default_index = idx
                        break
            
            selected_option = st.selectbox(
                "🎯 Choisissez une offre / entreprise",
                options=[opt['label'] for opt in offer_options],
                index=default_index
            )
            
            # Récupérer les données de l'offre sélectionnée
            selected_index = [opt['label'] for opt in offer_options].index(selected_option)
            selected_offer = offer_options[selected_index]
            
            # Charger les infos étudiant
            student_info = st.session_state.student_info
            
            # Bouton génération
            if st.button("✨ Générer la lettre de motivation", type="primary", use_container_width=True):
                if not student_info or not student_info.get('full_name'):
                    st.error("Veuillez d'abord compléter vos informations dans l'onglet '📋 Mes informations'")
                else:
                    # Générer la lettre
                    with st.spinner("Génération de votre lettre personnalisée..."):
                        result = letter_generator.generate_letter(selected_offer['data'], student_info)
                        
                        # Afficher la lettre
                        st.subheader("📄 Votre lettre de motivation")
                        st.text_area(
                            "Lettre générée",
                            value=result['content'],
                            height=600,
                            key="generated_letter"
                        )
                        
                        # Boutons d'action
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            # Télécharger
                            st.download_button(
                                "📥 Télécharger (.txt)",
                                result['content'],
                                result['filename'],
                                use_container_width=True
                            )
                        
                        with col2:
                            # Copier dans le presse-papier
                            if st.button("📋 Copier", use_container_width=True, key="copy_letter_btn"):
                                st.code(result['content'])
                                st.success("✅ Lettre copiée dans le presse-papier !")
                        
                        with col3:
                            # Nouvelle lettre
                            if st.button("🔄 Regénérer", use_container_width=True, key="regenerate_btn"):
                                if 'selected_offer_for_letter' in st.session_state:
                                    del st.session_state.selected_offer_for_letter
                                st.rerun()
                        
                        # Conseils
                        st.info("""
                        **💡 Conseils d'utilisation :**
                        1. **Personnalisez** la lettre avec vos expériences spécifiques
                        2. **Adaptez** le projet PFE à l'entreprise
                        3. **Relisez** attentivement avant envoi
                        4. **Enregistrez** une version pour chaque entreprise
                        """)
                        
                        # Nettoyer la redirection
                        if 'selected_offer_for_letter' in st.session_state:
                            del st.session_state.selected_offer_for_letter
        else:
            st.info("ℹ️ Aucune offre disponible pour générer une lettre.")
    
    with tab2:
        st.subheader("📋 Mes informations personnelles")
        st.caption("Ces informations seront utilisées pour personnaliser vos lettres")
        
        # Récupérer ou initialiser les infos étudiant
        student_info = st.session_state.student_info
        
        # Formulaire
        with st.form("student_info_form"):
            fields = letter_generator.get_student_form_fields()
            
            for field in fields:
                if field['type'] in ['text', 'email']:
                    value = st.text_input(
                        field['label'],
                        value=student_info.get(field['key'], ''),
                        placeholder=field['placeholder'],
                        key=f"student_{field['key']}"
                    )
                    student_info[field['key']] = value
            
            submitted = st.form_submit_button("💾 Sauvegarder mes informations", type="primary")
            
            if submitted:
                # Valider les champs requis
                required_fields = [f for f in fields if f.get('required', False)]
                missing_fields = []
                
                for field in required_fields:
                    if not student_info.get(field['key'], '').strip():
                        missing_fields.append(field['label'])
                
                if missing_fields:
                    st.error(f"❌ Champs requis manquants : {', '.join(missing_fields)}")
                else:
                    st.session_state.student_info = student_info
                    st.success("✅ Vos informations ont été sauvegardées !")
        
        # Aperçu des informations
        if student_info and any(v for v in student_info.values()):
            st.markdown("---")
            st.subheader("👤 Aperçu de vos informations")
            
            for key, value in student_info.items():
                if value:
                    # Trouver le label du champ
                    field_label = next((f['label'] for f in fields if f['key'] == key), key)
                    st.write(f"**{field_label}:** {value}")

def render_search_page():
    """Page de recherche principale"""
    
    st.title("🔍 Recherche de Stage PFE au Maroc")
    st.caption("Trouvez votre stage de fin d'études dans les meilleures entreprises marocaines")
    
    # Formulaire de recherche
    with st.form("search_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            # Secteur
            secteur = st.selectbox(
                "🎯 Domaine d'études *",
                engine.get_secteurs_disponibles(),
                index=0
            )
            
            # Type de stage
            type_stage = st.selectbox(
                "📋 Type de recherche",
                ["Stage PFE", "Alternance", "Stage d'été", "Premier emploi", "Tous types"],
                index=0
            )
        
        with col2:
            # Ville
            ville = st.selectbox(
                "📍 Ville préférée",
                ["Toutes villes"] + engine.get_villes_maroc(),
                index=0
            )
            
            # Niveau d'études
            niveau = st.selectbox(
                "🎓 Niveau d'études",
                ["Bac+5 Ingénieur", "Bac+5 Master", "Bac+3 Licence", "Bac+2 DUT/BTS", "Tous niveaux"],
                index=0
            )
        
        # Entreprise spécifique
        entreprise_specifique = st.text_input(
            "🏢 Entreprise spécifique (optionnel)",
            placeholder="Ex: Capgemini Maroc, OCP, Maroc Telecom..."
        )
        
        # Boutons rapides
        st.markdown("**🚀 Suggestions rapides:**")
        quick_cols = st.columns(4)
        
        quick_searches = [
            ("💻 IT Casablanca", "Informatique / IT / Développement", "Casablanca"),
            ("📱 Telecom Rabat", "Télécommunications / Réseaux", "Rabat"),
            ("💰 Finance Maroc", "Banque / Finance / Assurance", "Toutes villes"),
            ("🏭 Industrie", "Industrie / Manufacturing", "Toutes villes")
        ]
        
        for i, (label, sect, vill) in enumerate(quick_searches):
            with quick_cols[i]:
                if st.form_submit_button(label, use_container_width=True):
                    st.session_state.quick_search = {
                        'secteur': sect,
                        'ville': vill,
                        'type': "Stage PFE"
                    }
                    st.rerun()
        
        # Soumission
        submitted = st.form_submit_button(
            "🔍 Lancer la recherche",
            type="primary",
            use_container_width=True
        )
    
    # Gestion recherche rapide
    if hasattr(st.session_state, 'quick_search'):
        secteur = st.session_state.quick_search['secteur']
        ville = st.session_state.quick_search['ville'] if st.session_state.quick_search['ville'] != "Toutes villes" else None
        type_stage = st.session_state.quick_search['type']
        submitted = True
        del st.session_state.quick_search
    
    # Exécution recherche
    if submitted:
        if not secteur:
            st.error("Veuillez sélectionner un domaine d'études")
            return
        
        # Progress bar
        progress_bar = st.progress(0)
        status = st.empty()
        
        try:
            # Simulation progression
            steps = ["Initialisation", "Recherche entreprises", "Scan offres", "Analyse résultats"]
            
            for i, step in enumerate(steps):
                status.text(f"⏳ {step}...")
                progress_bar.progress((i + 1) * 25)
                time.sleep(0.5)
            
            # Recherche
            results = engine.search_pfe_opportunities(
                secteur=secteur,
                ville=ville,
                entreprise_specifique=entreprise_specifique if entreprise_specifique else None,
                type_recherche="stage"
            )
            
            progress_bar.progress(100)
            status.text("✅ Recherche terminée!")
            
            # Sauvegarde résultats
            st.session_state.search_results = results
            st.session_state.search_history.append({
                'date': datetime.now(),
                'criteria': f"{secteur} | {ville or 'Tout Maroc'}",
                'results': len(results.get('entreprises', [])) + len(results.get('offres', [])),
                'type': type_stage
            })
            
            time.sleep(0.5)
            progress_bar.empty()
            status.empty()
            
        except Exception as e:
            st.error(f"❌ Erreur: {str(e)}")
            return
    
    # Affichage résultats
    if st.session_state.search_results:
        results = st.session_state.search_results
        
        # Statistiques
        st.subheader("📊 Résultats de la recherche")
        
        stats_cols = st.columns(4)
        with stats_cols[0]:
            st.metric("🏢 Entreprises", len(results.get('entreprises', [])))
        with stats_cols[1]:
            st.metric("💼 Offres", len(results.get('offres', [])))
        with stats_cols[2]:
            st.metric("👤 Contacts", len(results.get('contacts', [])))
        with stats_cols[3]:
            villes = list(set(e.get('ville', '') for e in results.get('entreprises', [])))
            st.metric("📍 Villes", len(villes))
        
        # Onglets pour résultats
        tab1, tab2, tab3 = st.tabs(["🏢 Entreprises", "💼 Offres de stage", "👤 Contacts"])
        
        with tab1:
            if results.get('entreprises'):
                st.markdown(f"### Entreprises recommandées ({len(results['entreprises'])})")
                
                for entreprise in results['entreprises'][:10]:  # 10 max
                    with st.expander(f"🏢 {entreprise['nom']} - {entreprise['ville']}"):
                        col1, col2 = st.columns([2, 1])
                        
                        with col1:
                            st.markdown(f"**Spécialité:** {entreprise.get('specialite', 'Non spécifié')}")
                            st.markdown(f"**Type:** {entreprise.get('type', 'Non spécifié')}")
                            st.markdown(f"**Site web:** [{entreprise['site_web']}]({entreprise['site_web']})")
                            
                            if entreprise.get('offres_stage', False):
                                st.success("✅ Recrute des stagiaires")
                            else:
                                st.info("ℹ️ Contactez pour stage")
                        
                        with col2:
                            if st.button("💾 Sauvegarder", key=f"save_ent_{entreprise['nom'].replace(' ', '_')}"):
                                st.session_state.saved_offers.append({
                                    'type': 'entreprise',
                                    'data': entreprise,
                                    'date': datetime.now()
                                })
                                st.success("✅ Entreprise sauvegardée!")
                        
                        # Contacts
                        if entreprise.get('contacts'):
                            st.markdown("**📞 Contacts:**")
                            for contact in entreprise['contacts']:
                                st.markdown(f"- **{contact['nom']}:** {contact.get('email', 'N/A')}")
            else:
                st.info("ℹ️ Aucune entreprise trouvée pour ces critères")
        
        with tab2:
            if results.get('offres'):
                st.markdown(f"### Offres disponibles ({len(results['offres'])})")
                
                for i, offre in enumerate(results['offres'][:15]):  # 15 max
                    with st.container():
                        col1, col2, col3 = st.columns([3, 1, 1])
                        
                        with col1:
                            st.markdown(f"**{offre['titre']}**")
                            st.markdown(f"🏢 {offre['entreprise']} | 📍 {offre['lieu']}")
                            st.markdown(f"📅 {offre['date_publication']} | 📝 {offre['type']}")
                        
                        with col2:
                            if offre['lien'] and offre['lien'] != "Non disponible":
                                st.markdown(f"[🔗 Voir offre]({offre['lien']})")
                        
                        with col3:
                            # CORRECTION : Clé unique avec index
                            if st.button("💾", key=f"save_offre_{i}_{offre['titre'][:15].replace(' ', '_')}"):
                                st.session_state.saved_offers.append({
                                    'type': 'offre',
                                    'data': offre,
                                    'date': datetime.now()
                                })
                                st.success("✅ Offre sauvegardée!")
                        
                        st.divider()
            else:
                st.info("ℹ️ Aucune offre trouvée pour ces critères")
        
        with tab3:
            if results.get('contacts'):
                st.markdown(f"### Contacts professionnels ({len(results['contacts'])})")
                
                contacts_df = []
                for contact in results['contacts']:
                    contacts_df.append({
                        'Nom': contact.get('nom', 'N/A'),
                        'Fonction': 'Contact RH/Recrutement',
                        'Entreprise': 'Voir entreprise',
                        'Email': contact.get('email', 'Non disponible'),
                        'Téléphone': contact.get('telephone', 'Non disponible')
                    })
                
                df = pd.DataFrame(contacts_df)
                st.dataframe(df, use_container_width=True, hide_index=True)
            else:
                st.info("ℹ️ Aucun contact spécifique trouvé")

def render_companies_page():
    """Page des entreprises par secteur"""
    
    st.title("🏢 Répertoire des Entreprises Marocaines")
    st.caption("Explorez les entreprises par secteur et ville")
    
    # Filtres
    col1, col2 = st.columns(2)
    
    with col1:
        secteur = st.selectbox(
            "Sélectionnez un secteur",
            ["Tous secteurs"] + engine.get_secteurs_disponibles(),
            index=0
        )
    
    with col2:
        ville = st.selectbox(
            "Filtrer par ville",
            ["Toutes villes"] + engine.get_villes_maroc(),
            index=0
        )
    
    # Récupération entreprises
    if secteur == "Tous secteurs":
        # Afficher tous les secteurs
        for secteur_key in entreprises_db.get_all_sectors():
            st.subheader(f"📁 {secteur_key.upper()}")
            
            entreprises = entreprises_db.get_entreprises_by_sector(secteur_key)
            if ville != "Toutes villes":
                entreprises = [e for e in entreprises if ville.lower() in e['ville'].lower()]
            
            for entreprise in entreprises[:3]:  # 3 par secteur
                st.markdown(f"**🏢 {entreprise['nom']}**")
                st.markdown(f"📍 {entreprise['ville']} | 🌐 [{entreprise['site_web']}]({entreprise['site_web']})")
                st.markdown(f"*{entreprise.get('specialite', '')}*")
                st.divider()
    else:
        # Entreprises du secteur sélectionné
        entreprises = entreprises_db.get_entreprises_by_sector(secteur)
        
        if ville != "Toutes villes":
            entreprises = [e for e in entreprises if ville.lower() in e['ville'].lower()]
        
        if entreprises:
            st.subheader(f"📊 {len(entreprises)} entreprises trouvées")
            
            for i, entreprise in enumerate(entreprises):
                with st.expander(f"🏢 {entreprise['nom']} - {entreprise['ville']}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Spécialité:** {entreprise.get('specialite', 'Non spécifié')}")
                        st.markdown(f"**Type:** {entreprise.get('type', 'Non spécifié')}")
                        st.markdown(f"**Site web:** [{entreprise['site_web']}]({entreprise['site_web']})")
                        
                        if entreprise.get('contacts'):
                            st.markdown("**📞 Contacts:**")
                            for contact in entreprise['contacts']:
                                st.markdown(f"- **{contact['nom']}:** {contact.get('email', 'N/A')}")
                    
                    with col2:
                        if entreprise.get('offres_stage', False):
                            st.success("✅ Recrute des stagiaires")
                        else:
                            st.info("ℹ️ Contactez pour opportunités")
                        
                        if st.button("💾 Sauvegarder", key=f"save_companies_{i}"):
                            st.session_state.saved_offers.append({
                                'type': 'entreprise',
                                'data': entreprise,
                                'date': datetime.now()
                            })
                            st.success("✅ Entreprise sauvegardée!")
        else:
            st.info("ℹ️ Aucune entreprise trouvée pour ces critères")

def render_offers_page():
    """Page des offres de stage"""
    
    st.title("💼 Offres de Stage & PFE")
    st.caption("Dernières offres publiées sur les plateformes marocaines")
    
    # Formulaire recherche offres
    with st.form("offers_search"):
        col1, col2 = st.columns(2)
        
        with col1:
            offre_secteur = st.selectbox(
                "Secteur recherché",
                ["Tous secteurs"] + engine.get_secteurs_disponibles()[:8],
                key="offre_secteur"
            )
        
        with col2:
            offre_ville = st.selectbox(
                "Ville",
                ["Toutes villes"] + engine.get_villes_maroc(),
                key="offre_ville"
            )
        
        if st.form_submit_button("🔍 Rechercher offres", use_container_width=True):
            with st.spinner("Recherche en cours..."):
                stage_finder = StageFinder()
                offres = stage_finder.search_all_platforms(
                    secteur=offre_secteur if offre_secteur != "Tous secteurs" else "stage",
                    ville=offre_ville if offre_ville != "Toutes villes" else None
                )
                
                if offres:
                    st.session_state.current_offers = offres
                else:
                    st.warning("Aucune offre trouvée")
    
    # Affichage offres
    if hasattr(st.session_state, 'current_offers') and st.session_state.current_offers:
        offres = st.session_state.current_offers
        
        st.subheader(f"📋 {len(offres)} offres trouvées")
        
        for i, offre in enumerate(offres[:20]):  # 20 max
            with st.container():
                col1, col2, col3 = st.columns([3, 1, 1])
                
                with col1:
                    st.markdown(f"#### {offre['titre']}")
                    st.markdown(f"**🏢 {offre['entreprise']}** | 📍 {offre['lieu']}")
                    st.markdown(f"*Source: {offre['source']}*")
                
                with col2:
                    if offre['lien'] and offre['lien'] != "Non disponible":
                        st.markdown(f"[🔗 Voir l'offre]({offre['lien']})")
                
                with col3:
                    # CORRECTION : Clé unique
                    if st.button("💾", key=f"save_offer_page2_{i}_{offre['titre'][:10].replace(' ', '_')}"):
                        st.session_state.saved_offers.append({
                            'type': 'offre',
                            'data': offre,
                            'date': datetime.now()
                        })
                        st.success("Offre sauvegardée!")
                
                st.divider()
    else:
        st.info("🔍 Utilisez le formulaire ci-dessus pour rechercher des offres")

def render_advice_page():
    """Page de conseils PFE"""
    
    st.title("📚 Guide du Stage PFE au Maroc")
    st.caption("Conseils pratiques pour trouver et réussir votre stage de fin d'études")
    
    # Sélection secteur pour conseils spécifiques
    secteur_conseil = st.selectbox(
        "🎯 Choisissez votre domaine pour des conseils spécifiques",
        engine.get_secteurs_disponibles(),
        index=0
    )
    
    conseils = engine.get_conseils_pfe(secteur_conseil)
    
    # Affichage conseils
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💡 Conseils pratiques")
        for i, conseil in enumerate(conseils['conseils'], 1):
            st.markdown(f"{i}. {conseil}")
        
        st.subheader("💰 Rémunération moyenne")
        st.info(f"**{conseils['salaires_moyens']}**")
        
        st.subheader("📅 Période idéale")
        st.success(f"**{conseils['periode_ideal']}**")
    
    with col2:
        st.subheader("🛠️ Compétences demandées")
        for competence in conseils['competences_demandees']:
            st.markdown(f"✅ {competence}")
        
        st.subheader("📝 Timeline recommandée")
        timeline = [
            ("3-4 mois avant", "Recherche d'entreprise, préparation CV"),
            ("2-3 mois avant", "Envoi des candidatures, relances"),
            ("1 mois avant", "Entretiens, négociation"),
            ("Début stage", "Signature convention, démarrage")
        ]
        
        for periode, action in timeline:
            st.markdown(f"**{periode}:** {action}")
    
    # Section générique
    st.markdown("---")
    st.subheader("📄 Préparation de la candidature")
    
    col_a, col_b = st.columns(2)
    
    with col_a:
        st.markdown("**CV Gagnant:**")
        st.markdown("""
        1. **Photo professionnelle**
        2. **Projets personnels** (GitHub, portfolio)
        3. **Compétences techniques** détaillées
        4. **Expériences** même courtes
        5. **Langues**: Français, Anglais, Arabe
        6. **Certifications** pertinentes
        """)
    
    with col_b:
        st.markdown("**Lettre de motivation:**")
        st.markdown("""
        1. **Personnalisée** pour chaque entreprise
        2. **Projet PFE** clairement défini
        3. **Valeur ajoutée** que vous apportez
        4. **Disponibilités** précises
        5. **Contact** facile à joindre
        """)
    
    # Template de CV
    with st.expander("📋 Template de CV (à télécharger)"):
        st.markdown("""
        ### Template Word de CV Stage PFE
        
        **Structure recommandée:**
        ```
        [PHOTO PROFESSIONNELLE]
        
        [NOM PRÉNOM]
        [Titre recherché: Stagiaire Développeur Web]
        
        CONTACT
        📧 email@domain.com
        📞 +212 6 XX XX XX XX
        📍 Ville, Maroc
        🔗 linkedin.com/in/votrenom
        
        PROFIL
        Étudiant en [Diplôme] à [École/Université]...
        
        FORMATION
        2021-2024: Diplôme d'ingénieur en Informatique
        Université XYZ, Casablanca
        
        COMPÉTENCES TECHNIQUES
        • Langages: Python, Java, JavaScript
        • Frameworks: React, Node.js, Django
        • Outils: Git, Docker, VS Code
        
        PROJETS ACADÉMIQUES
        • Application de gestion - Python/Django
        • Site e-commerce - React/Node.js
        
        LANGUES
        • Arabe: Langue maternelle
        • Français: Courant
        • Anglais: Technique
        
        CENTRES D'INTÉRÊT
        • Développement open source
        • Participations aux hackathons
        ```
        
        *Créez votre propre template personnalisé*
        """)

def render_favorites_page():
    """Page des favoris sauvegardés"""
    
    st.title("💾 Mes Favoris Sauvegardés")
    
    if not st.session_state.saved_offers:
        st.info("💡 Vous n'avez encore sauvegardé aucune offre ou entreprise.")
        return
    
    # Onglets pour types de favoris
    tab1, tab2, tab3 = st.tabs(["🏢 Entreprises", "💼 Offres", "📝 Lettre de Motivation"])
    
    with tab1:
        entreprises = [item for item in st.session_state.saved_offers if item['type'] == 'entreprise']
        
        if entreprises:
            st.subheader(f"📁 {len(entreprises)} entreprises sauvegardées")
            
            for i, item in enumerate(entreprises):
                entreprise = item['data']
                
                with st.expander(f"🏢 {entreprise['nom']} - Sauvegardé le {item['date'].strftime('%d/%m/%Y')}"):
                    col1, col2 = st.columns([3, 1])
                    
                    with col1:
                        st.markdown(f"**Ville:** {entreprise['ville']}")
                        st.markdown(f"**Site web:** [{entreprise['site_web']}]({entreprise['site_web']})")
                        st.markdown(f"**Spécialité:** {entreprise.get('specialite', 'N/A')}")
                        
                        if entreprise.get('contacts'):
                            st.markdown("**Contacts:**")
                            for contact in entreprise['contacts']:
                                st.markdown(f"- {contact['nom']}: {contact.get('email', 'N/A')}")
                    
                    with col2:
                        if st.button("🗑️ Supprimer", key=f"del_ent_{i}"):
                            st.session_state.saved_offers.remove(item)
                            st.rerun()
        else:
            st.info("ℹ️ Aucune entreprise sauvegardée")
    
    with tab2:
        offres = [item for item in st.session_state.saved_offers if item['type'] == 'offre']
        
        if offres:
            st.subheader(f"📋 {len(offres)} offres sauvegardées")
            
            for i, item in enumerate(offres):
                offre = item['data']
                
                with st.container():
                    col1, col2, col3 = st.columns([3, 1, 1])
                    
                    with col1:
                        st.markdown(f"**{offre['titre']}**")
                        st.markdown(f"🏢 {offre['entreprise']} | 📍 {offre['lieu']}")
                        st.markdown(f"📅 {offre['date_publication']} | 📝 {offre['type']}")
                        if offre.get('lien'):
                            st.markdown(f"[🔗 Voir l'offre]({offre['lien']})")
                    
                    with col2:
                        st.caption(f"Sauvegardé: {item['date'].strftime('%d/%m')}")
                    
                    with col3:
                        # Bouton supprimer
                        if st.button("🗑️", key=f"del_off_{i}"):
                            st.session_state.saved_offers.remove(item)
                            st.rerun()
                        
                        # Bouton générer lettre
                        if st.button("📝", key=f"letter_off_{i}"):
                            st.session_state.selected_offer_for_letter = item['data']
                            st.rerun()
                    
                    st.divider()
        else:
            st.info("ℹ️ Aucune offre sauvegardée")
    
    with tab3:
        st.subheader("📝 Générer une lettre de motivation")
        st.info("Sélectionnez une offre ci-dessus et cliquez sur le bouton 📝 pour générer une lettre personnalisée.")
        
        # Stats
        total_fav = len(st.session_state.saved_offers)
        total_offres = len([o for o in st.session_state.saved_offers if o['type'] == 'offre'])
        total_entreprises = len([o for o in st.session_state.saved_offers if o['type'] == 'entreprise'])
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total favoris", total_fav)
        with col2:
            st.metric("Offres", total_offres)
        with col3:
            st.metric("Entreprises", total_entreprises)
        
        # Bouton export
        if st.session_state.saved_offers:
            st.markdown("---")
            
            # Préparation données pour export
            export_data = []
            for item in st.session_state.saved_offers:
                if item['type'] == 'entreprise':
                    export_data.append({
                        'Type': 'Entreprise',
                        'Nom': item['data']['nom'],
                        'Ville': item['data']['ville'],
                        'Site Web': item['data']['site_web'],
                        'Date Sauvegarde': item['date'].strftime('%Y-%m-%d')
                    })
                else:
                    export_data.append({
                        'Type': 'Offre',
                        'Titre': item['data']['titre'],
                        'Entreprise': item['data']['entreprise'],
                        'Lieu': item['data']['lieu'],
                        'Lien': item['data'].get('lien', 'N/A'),
                        'Date Sauvegarde': item['date'].strftime('%Y-%m-%d')
                    })
            
            df = pd.DataFrame(export_data)
            
            # Export CSV
            csv = df.to_csv(index=False)
            st.download_button(
                "📥 Exporter mes favoris (CSV)",
                csv,
                "mes_favoris_pfe.csv",
                use_container_width=True
            )

# Pied de page
st.markdown("---")
footer_col1, footer_col2, footer_col3 = st.columns(3)
with footer_col1:
    st.caption("🎓 **Maroc PFE Finder** ")
with footer_col2:
    st.caption("📍 Réalisé par : Berkhli-El Akari-El Arraki")
with footer_col3:
    st.caption(f"🔒 Données mises à jour: {datetime.now().strftime('%Y')}")

if __name__ == "__main__":
    main()