import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np

# ─────────────────────────────────────────────────────────────────────────────
# CONFIGURATION DE LA PAGE
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ADB Biodiversité — Cameroun",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Styles CSS personnalisés
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
.main { background: #F7F5F0; }
.block-container { padding: 1.2rem 1.5rem 2rem 1.5rem; max-width: 1600px; }

.hero {
    background: linear-gradient(120deg, #1C3A2B 0%, #2E6B47 55%, #4CAF76 100%);
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    border-left: 6px solid #6FCF97;
}
.hero-title {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.8rem; font-weight: 700;
    color: #FFFFFF; margin: 0 0 0.2rem 0;
}
.hero-sub { color: #A5D6A7; font-size: 0.88rem; letter-spacing: 0.04em; }
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    color: #E8F5E9; border-radius: 4px;
    padding: 0.15rem 0.7rem; font-size: 0.7rem;
    font-weight: 700; margin-top: 0.6rem;
    letter-spacing: 0.1em; text-transform: uppercase;
    border: 1px solid rgba(255,255,255,0.2);
}

.filtre-bar {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    margin-bottom: 1.2rem;
    box-shadow: 0 2px 8px rgba(28,58,43,0.07);
    border-left: 4px solid #2E6B47;
}
.filtre-title {
    font-size: 0.75rem; font-weight: 700;
    color: #2E6B47; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.5rem;
}

.kpi-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    border-top: 4px solid #2E6B47;
    box-shadow: 0 2px 8px rgba(28,58,43,0.07);
    height: 100%;
}
.kpi-card.orange { border-top-color: #E07B39; }
.kpi-card.blue    { border-top-color: #2B6CB0; }
.kpi-card.purple  { border-top-color: #6B46C1; }

.kpi-label { font-size: 0.68rem; color: #718096; font-weight: 700; text-transform: uppercase; }
.kpi-value { font-family: 'Libre Baskerville', serif; font-size: 1.4rem; font-weight: 700; color: #1C3A2B; }

.section-title {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.1rem; font-weight: 700;
    color: #1C3A2B; margin: 1.4rem 0 0.7rem 0;
    padding-bottom: 0.4rem; border-bottom: 2px solid #C8E6C9;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CONSTANTES ET CHARGEMENT
# ─────────────────────────────────────────────────────────────────────────────
PALETTE_CAT = ["#1C3A2B","#2E6B47","#3D8B5E","#4CAF76","#6FCF97","#95E0B4","#E07B39","#C53030","#2B6CB0"]
PALETTE_SECT = {"Public":"#2E6B47","ONG / OSC":"#2B6CB0","Secteur Privé":"#6B46C1","PTF":"#E07B39"}
LAYOUT_BASE = dict(font_family="Source Sans 3", plot_bgcolor="white", paper_bgcolor="white")

@st.cache_data
def charger_donnees(fichier):
    xls = pd.ExcelFile(fichier)
    df = pd.read_excel(xls, sheet_name="PowerBI_Data", header=1)
    macro = None
    if any(n in xls.sheet_names for n in ["Donnees Macro", "Données Macro"]):
        macro = pd.read_excel(xls, sheet_name="Donnees Macro", header=1)
    return df, macro

# ─────────────────────────────────────────────────────────────────────────────
# INTERFACE PRINCIPALE
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-title">Analyse des Dépenses Biodiversité — Cameroun</p>
    <p class="hero-sub">Initiative BIOFIN / PNUD · Tableau de bord interactif</p>
    <span class="hero-badge">BIOFIN · 2020–2024</span>
</div>
""", unsafe_allow_html=True)

col_up, _ = st.columns([2, 5])
with col_up:
    fichier_charge = st.file_uploader("📂 Charger le fichier Excel", type=["xlsx"])

if not fichier_charge:
    st.info("Veuillez charger un fichier Excel pour afficher les analyses.")
    st.stop()

# Traitement des données
df_brut, macro_brut = charger_donnees(fichier_charge)
df = df_brut.copy()

# Mapping des colonnes flexible
col_map = {}
for c in df.columns:
    cl = str(c).lower().strip()
    if "secteur" in cl: col_map[c] = "Secteur"
    elif "institution" in cl: col_map[c] = "Institution"
    elif "année" in cl or "annee" in cl: col_map[c] = "Année"
    elif "catégorie" in cl or "categorie" in cl: col_map[c] = "Catégorie BIOFIN"
    elif "bd" in cl or "biodiv" in cl: col_map[c] = "Dép. BD"
    elif "totale" in cl: col_map[c] = "Dép. Totale"

df = df.rename(columns=col_map)
df["Année"] = pd.to_numeric(df["Année"], errors='coerce').fillna(0).astype(int)
df["Dép. BD"] = pd.to_numeric(df["Dép. BD"], errors='coerce').fillna(0)
df = df[df["Année"] > 0] # Nettoyage

# ─────────────────────────────────────────────────────────────────────────────
# ZONE DE FILTRES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown('<div class="filtre-bar"><div class="filtre-title">🎛️ Filtres Dynamiques</div>', unsafe_allow_html=True)
f1, f2, f3, f4 = st.columns([2, 2, 4, 2])

with f1:
    list_ans = sorted(df["Année"].unique())
    sel_ans = st.multiselect("Années", list_ans, default=list_ans)
with f2:
    list_sect = sorted(df["Secteur"].unique())
    sel_sect = st.multiselect("Secteurs", list_sect, default=list_sect)
with f3:
    list_cat = sorted(df["Catégorie BIOFIN"].dropna().unique())
    sel_cat = st.multiselect("Catégories", list_cat, default=list_cat)
with f4:
    unite = st.radio("Unité", ["Millions FCFA", "Milliards FCFA"])

st.markdown('</div>', unsafe_allow_html=True)

# Application des filtres
dff = df.copy()
if sel_ans: dff = dff[dff["Année"].isin(sel_ans)]
if sel_sect: dff = dff[dff["Secteur"].isin(sel_sect)]
if sel_cat: dff = dff[dff["Catégorie BIOFIN"].isin(sel_cat)]

if dff.empty:
    st.warning("Aucune donnée pour ces filtres.")
    st.stop()

div = 1000 if unite == "Milliards FCFA" else 1
lab_u = "Mds FCFA" if unite == "Milliards FCFA" else "M FCFA"

# ─────────────────────────────────────────────────────────────────────────────
# AFFICHAGE DES RÉSULTATS
# ─────────────────────────────────────────────────────────────────────────────
# KPIs
tot_val = dff["Dép. BD"].sum() / div
sec_dom = dff.groupby("Secteur")["Dép. BD"].sum().idxmax()

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(f'<div class="kpi-card"><div class="kpi-label">Total Dépenses BD</div><div class="kpi-value">{tot_val:,.1f} {lab_u}</div></div>', unsafe_allow_html=True)
with c2: st.markdown(f'<div class="kpi-card blue"><div class="kpi-label">Secteur Principal</div><div class="kpi-value">{sec_dom}</div></div>', unsafe_allow_html=True)
with c3: st.markdown(f'<div class="kpi-card orange"><div class="kpi-label">Nombre de Catégories</div><div class="kpi-value">{dff["Catégorie BIOFIN"].nunique()}</div></div>', unsafe_allow_html=True)
with c4: st.markdown(f'<div class="kpi-card purple"><div class="kpi-label">Nombre d\'Acteurs</div><div class="kpi-value">{dff["Institution"].nunique() if "Institution" in dff else "N/A"}</div></div>', unsafe_allow_html=True)

# Onglets
tab1, tab2 = st.tabs(["📊 Analyses Graphiques", "📋 Table de données"])

with tab1:
    col_l, col_r = st.columns(2)
    
    with col_l:
        st.markdown('<div class="section-title">Répartition par Secteur</div>', unsafe_allow_html=True)
        fig_s = px.bar(dff.groupby("Secteur")["Dép. BD"].sum().reset_index(), x="Secteur", y="Dép. BD", color="Secteur", color_discrete_map=PALETTE_SECT)
        fig_s.update_layout(height=350, **LAYOUT_BASE, showlegend=False)
        st.plotly_chart(fig_s, use_container_width=True)

    with col_r:
        st.markdown('<div class="section-title">Évolution Temporelle</div>', unsafe_allow_html=True)
        fig_e = px.line(dff.groupby("Année")["Dép. BD"].sum().reset_index(), x="Année", y="Dép. BD", markers=True)
        fig_e.update_layout(height=350, **LAYOUT_BASE)
        st.plotly_chart(fig_e, use_container_width=True)

    st.markdown('<div class="section-title">Intensité des Dépenses par Catégorie et Année</div>', unsafe_allow_html=True)
    pivot = dff.pivot_table(index="Catégorie BIOFIN", columns="Année", values="Dép. BD", aggfunc="sum").fillna(0) / div
    fig_h = go.Figure(data=go.Heatmap(z=pivot.values, x=[str(c) for c in pivot.columns], y=pivot.index.tolist(), colorscale="Greens"))
    fig_h.update_layout(height=450, **LAYOUT_BASE)
    st.plotly_chart(fig_h, use_container_width=True)

with tab2:
    st.dataframe(dff, use_container_width=True)