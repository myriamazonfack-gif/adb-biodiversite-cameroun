import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# 1. CONFIGURATION
st.set_page_config(page_title="ADB Biodiversité", layout="wide")

# 2. INTÉGRATION DES DONNÉES (Simulation des données du fichier pour autonomie)
# Note : Ces données sont extraites de votre structure PowerBI_Data
@st.cache_data
def get_data():
    data = {
        'Année': [2020, 2020, 2021, 2021, 2022, 2022, 2023, 2023, 2024, 2024],
        'Secteur': ['Public', 'ONG / OSC', 'Public', 'PTF', 'Public', 'Secteur Privé', 'Public', 'ONG / OSC', 'Public', 'PTF'],
        'Catégorie BIOFIN': ['Gestion de la biodiversité', 'Protection', 'Restauration', 'Gestion de la biodiversité', 'Protection', 'Restauration', 'Protection', 'Restauration', 'Gestion de la biodiversité', 'Protection'],
        'Dép. BD': [1200, 450, 1350, 800, 1100, 300, 1500, 600, 1400, 950],
        'Institution': ['MINEDDUB', 'WWF', 'MINFOF', 'PNUD', 'MINFOF', 'Entreprise X', 'MINEDDUB', 'IUCN', 'MINFOF', 'Banque Mondiale']
    }
    df = pd.DataFrame(data)
    # Sécurité : Forcer les types pour le filtrage
    df['Année'] = df['Année'].astype(int)
    df['Secteur'] = df['Secteur'].astype(str)
    return df

df = get_data()

# 3. DESIGN (CSS)
st.markdown("""
<style>
    .kpi-box { background: white; padding: 20px; border-radius: 10px; border-left: 5px solid #2E6B47; box-shadow: 2px 2px 10px rgba(0,0,0,0.1); }
    .stMultiSelect [data-baseweb="tag"] { background-color: #2E6B47 !important; }
</style>
""", unsafe_allow_html=True)

st.title("🌿 Analyse des Dépenses Biodiversité — Cameroun")

# 4. FILTRES (CORRIGÉS)
st.sidebar.header("🔍 Paramètres d'affichage")

# On s'assure que les listes de filtres sont propres
options_annee = sorted(df['Année'].unique().tolist())
options_secteur = sorted(df['Secteur'].unique().tolist())

sel_ans = st.sidebar.multiselect("Sélectionner les Années", options_annee, default=options_annee)
sel_sect = st.sidebar.multiselect("Sélectionner les Secteurs", options_secteur, default=options_secteur)

# Logique de filtrage robuste
# On filtre SEULEMENT si l'utilisateur a fait un choix, sinon on garde tout
dff = df.copy()
if sel_ans:
    dff = dff[dff['Année'].isin(sel_ans)]
if sel_sect:
    dff = dff[dff['Secteur'].isin(sel_sect)]

# 5. AFFICHAGE DES RÉSULTATS
if dff.empty:
    st.error("Désolé, aucune donnée ne correspond à cette combinaison de filtres.")
else:
    # KPIs
    c1, c2, c3 = st.columns(3)
    with c1:
        st.markdown(f'<div class="kpi-box"><b>Total Dépenses</b><br><h2>{dff["Dép. BD"].sum():,.0f} M FCFA</h2></div>', unsafe_allow_html=True)
    with c2:
        top_sec = dff.groupby('Secteur')['Dép. BD'].sum().idxmax()
        st.markdown(f'<div class="kpi-box"><b>Secteur Dominant</b><br><h2>{top_sec}</h2></div>', unsafe_allow_html=True)
    with c3:
        st.markdown(f'<div class="kpi-box"><b>Nombre de Projets</b><br><h2>{len(dff)}</h2></div>', unsafe_allow_html=True)

    st.write("---")

    # Graphiques
    col_left, col_right = st.columns(2)

    with col_left:
        fig_bar = px.bar(dff.groupby('Année')['Dép. BD'].sum().reset_index(), 
                         x='Année', y='Dép. BD', 
                         title="Évolution des Dépenses par An",
                         color_discrete_sequence=['#2E6B47'])
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        fig_pie = px.pie(dff, values='Dép. BD', names='Secteur', 
                         title="Répartition par Secteur",
                         color_discrete_sequence=px.colors.qualitative.Greens)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Table de données
    st.subheader("📋 Détails des enregistrements")
    st.dataframe(dff, use_container_width=True)