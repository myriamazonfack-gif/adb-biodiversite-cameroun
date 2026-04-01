import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io

# ─────────────────────────────────────────────────────────────────────────────
# CONFIG PAGE
# ─────────────────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="ADB Biodiversité — Cameroun",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS PERSONNALISÉ AVANCÉ
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=Playfair+Display:wght@400;500;600;700;800&display=swap');

/* Base */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}
.main {
    background: linear-gradient(135deg, #F8FAF5 0%, #F0F4EA 100%);
}
.block-container {
    padding: 1.2rem 2rem 2rem 2rem;
    max-width: 1600px;
}

/* Sidebar moderne */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2F1F 0%, #1C3A2B 100%);
    border-right: none;
    box-shadow: 4px 0 20px rgba(0,0,0,0.08);
}
[data-testid="stSidebar"] * { color: #E8F5E9 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { 
    font-family: 'Playfair Display', serif !important;
    color: #FFFFFF !important;
    font-weight: 600;
}
[data-testid="stSidebar"] .stMarkdown p { 
    color: #C8E6C9 !important; 
    font-size: 0.85rem;
    line-height: 1.4;
}
[data-testid="stSidebar"] label {
    color: #9CCC65 !important;
    font-weight: 600;
    font-size: 0.75rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] hr {
    border-color: #2E6B47 !important;
    margin: 1rem 0;
}
[data-testid="stSidebar"] .stMultiSelect [data-baseweb="tag"] {
    background-color: #2E6B47 !important;
}

/* Hero Header */
.hero-header {
    background: linear-gradient(135deg, #0A2F1F 0%, #1C3A2B 50%, #2E6B47 100%);
    border-radius: 20px;
    padding: 2rem 2.5rem;
    margin-bottom: 2rem;
    position: relative;
    overflow: hidden;
    box-shadow: 0 10px 30px rgba(0,0,0,0.1);
}
.hero-header::before {
    content: "🌿";
    position: absolute;
    right: 2rem;
    top: 1rem;
    font-size: 8rem;
    opacity: 0.08;
    font-family: monospace;
}
.hero-header::after {
    content: "";
    position: absolute;
    bottom: 0;
    left: 0;
    right: 0;
    height: 4px;
    background: linear-gradient(90deg, #6FCF97, #2E6B47, #0A2F1F);
}
.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 2.2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 0.4rem 0;
    line-height: 1.2;
    letter-spacing: -0.01em;
}
.hero-sub {
    color: #A5D6A7;
    font-size: 0.9rem;
    font-weight: 400;
    letter-spacing: 0.02em;
}
.hero-badge {
    display: inline-flex;
    background: rgba(111,207,151,0.2);
    backdrop-filter: blur(8px);
    color: #E8F5E9;
    border-radius: 20px;
    padding: 0.3rem 1rem;
    font-size: 0.7rem;
    font-weight: 600;
    margin-top: 0.8rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    border: 1px solid rgba(111,207,151,0.3);
}

/* KPI Cards */
.kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 1.2rem;
    margin-bottom: 1.5rem;
}
.kpi-card {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1.2rem 1.2rem;
    position: relative;
    overflow: hidden;
    transition: all 0.3s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    border: 1px solid rgba(46,107,71,0.1);
}
.kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 20px rgba(46,107,71,0.12);
}
.kpi-card::before {
    content: "";
    position: absolute;
    top: 0;
    left: 0;
    width: 4px;
    height: 100%;
    background: #2E6B47;
}
.kpi-card.green::before { background: #2E6B47; }
.kpi-card.blue::before { background: #2B6CB0; }
.kpi-card.orange::before { background: #E07B39; }
.kpi-card.purple::before { background: #6B46C1; }
.kpi-card.teal::before { background: #319795; }

.kpi-label {
    font-size: 0.7rem;
    color: #718096;
    font-weight: 600;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    margin-bottom: 0.6rem;
}
.kpi-value {
    font-family: 'Playfair Display', serif;
    font-size: 1.8rem;
    font-weight: 700;
    color: #1C3A2B;
    line-height: 1.1;
    margin-bottom: 0.3rem;
}
.kpi-delta {
    font-size: 0.7rem;
    font-weight: 600;
    margin-top: 0.3rem;
    display: inline-flex;
    align-items: center;
    gap: 0.2rem;
}
.kpi-delta.pos { color: #2E6B47; }
.kpi-delta.neg { color: #C53030; }
.kpi-sub {
    font-size: 0.7rem;
    color: #A0AEC0;
    margin-top: 0.2rem;
}

/* Section Titles */
.section-title {
    font-family: 'Playfair Display', serif;
    font-size: 1.2rem;
    font-weight: 600;
    color: #1C3A2B;
    margin: 1.5rem 0 1rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #C8E6C9;
    display: flex;
    align-items: center;
    gap: 0.5rem;
}

/* Tabs Modernes */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.3rem;
    background: #FFFFFF;
    padding: 0.4rem;
    border-radius: 12px;
    box-shadow: 0 1px 3px rgba(0,0,0,0.05);
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px;
    padding: 0.5rem 1.2rem;
    font-weight: 500;
    color: #4A5568;
    font-size: 0.85rem;
    transition: all 0.2s;
}
.stTabs [aria-selected="true"] {
    background: #1C3A2B !important;
    color: white !important;
    box-shadow: 0 2px 6px rgba(28,58,43,0.2);
}

/* Insight Boxes */
.insight-box {
    background: linear-gradient(135deg, #E8F5E9 0%, #F1F8E9 100%);
    border-radius: 12px;
    padding: 0.9rem 1.2rem;
    margin: 1rem 0;
    border-left: 4px solid #2E6B47;
}
.insight-box.warning {
    background: linear-gradient(135deg, #FFF3E0 0%, #FFEFD0 100%);
    border-left-color: #E07B39;
}
.insight-box.info {
    background: linear-gradient(135deg, #E3F2FD 0%, #E8F0FE 100%);
    border-left-color: #2B6CB0;
}

/* Filter Bar */
.filter-bar {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 1rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    border: 1px solid rgba(46,107,71,0.15);
}
.filter-title {
    font-size: 0.7rem;
    font-weight: 700;
    color: #2E6B47;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.8rem;
}

/* Chart Container */
.chart-container {
    background: #FFFFFF;
    border-radius: 16px;
    padding: 0.8rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    border: 1px solid #EDF2F7;
}

/* Data Table */
.stDataFrame {
    border-radius: 12px;
    overflow: hidden;
}
.dataframe thead tr th {
    background: #1C3A2B !important;
    color: white !important;
    font-weight: 600 !important;
    font-size: 0.8rem !important;
    padding: 0.8rem !important;
}

/* Footer */
.footer {
    text-align: center;
    color: #A0AEC0;
    font-size: 0.7rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #E2E8F0;
}

/* Hide Streamlit Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Custom Scrollbar */
::-webkit-scrollbar {
    width: 8px;
    height: 8px;
}
::-webkit-scrollbar-track {
    background: #F1F1F1;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb {
    background: #2E6B47;
    border-radius: 4px;
}
::-webkit-scrollbar-thumb:hover {
    background: #1C3A2B;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTES DE COULEURS
# ─────────────────────────────────────────────────────────────────────────────
PALETTE_CAT = [
    "#1C3A2B", "#2E6B47", "#3D8B5E", "#4CAF76",
    "#6FCF97", "#95E0B4", "#E07B39", "#C53030", "#2B6CB0"
]
PALETTE_SECT = {
    "Public": "#2E6B47",
    "ONG / OSC": "#2B6CB0",
    "Secteur Privé": "#6B46C1",
    "PTF": "#E07B39",
}

LAYOUT_COMMUN = dict(
    font_family="Inter",
    font_size=12,
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_font_size=14,
    title_font_color="#1C3A2B",
    title_font_family="Playfair Display",
    margin=dict(l=15, r=15, t=50, b=20),
    hoverlabel=dict(bgcolor="#1C3A2B", font_size=11, font_color="white"),
)


# ─────────────────────────────────────────────────────────────────────────────
# FONCTIONS UTILITAIRES
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def charger_donnees(fichier):
    """Charge les données depuis le fichier Excel."""
    xls = pd.ExcelFile(fichier)
    feuilles = xls.sheet_names
    df = None
    macro = None

    for nom in ["PowerBI_Data"]:
        if nom in feuilles:
            df = pd.read_excel(fichier, sheet_name=nom, header=1)
            df = df.dropna(subset=["Secteur", "Année"])
            break

    for nom in ["Donnees Macro", "Données Macro"]:
        if nom in feuilles:
            macro = pd.read_excel(fichier, sheet_name=nom, header=1)
            break

    return df, macro


def kpi_card(label, value, delta=None, delta_text=None, sub=None, color="green"):
    """Génère une carte KPI stylisée."""
    delta_html = ""
    if delta is not None:
        cls = "pos" if delta >= 0 else "neg"
        signe = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="kpi-delta {cls}">{signe} {abs(delta):.1f}% {delta_text or ""}</div>'

    sub_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""

    return f"""
    <div class="kpi-card {color}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_html}
        {delta_html}
    </div>
    """


def normalize_category_name(cat_name):
    """Normalise le nom de catégorie BIOFIN."""
    if isinstance(cat_name, str):
        return cat_name.split(". ", 1)[-1] if ". " in cat_name else cat_name
    return cat_name


# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 ADB Biodiversité")
    st.markdown("**Analyse des Dépenses pour la Biodiversité**")
    st.markdown("Cameroun · 2020–2024")
    st.markdown("---")

    fichier_charge = st.file_uploader(
        "📂 Charger votre fichier Excel",
        type=["xlsx", "xls"],
        help="Fichier ADB au format Excel (.xlsx)"
    )
    st.markdown("---")

# Chargement
if fichier_charge is None:
    try:
        df_brut, macro_brut = charger_donnees("ADB_Cameroun_Simulation.xlsx")
        mode_demo = True
    except Exception as e:
        st.markdown("""
        <div class="hero-header">
            <p class="hero-title">Analyse des Dépenses<br>Biodiversité — Cameroun</p>
            <p class="hero-sub">Initiative BIOFIN / PNUD · Tableau de bord interactif</p>
            <span class="hero-badge">ADB · 2020–2024</span>
        </div>
        """, unsafe_allow_html=True)
        st.warning("⚠️ Veuillez charger votre fichier Excel ADB via le panneau latéral.")
        st.stop()
else:
    df_brut, macro_brut = charger_donnees(fichier_charge)
    mode_demo = False

if df_brut is None:
    st.error("❌ Impossible de lire les données. Vérifiez que votre fichier contient la feuille 'PowerBI_Data'.")
    st.stop()

# Nettoyage des colonnes
df = df_brut.copy()
col_map = {}
for c in df.columns:
    cl = str(c).lower().strip()
    if "secteur" in cl:
        col_map[c] = "Secteur"
    elif "institution" in cl:
        col_map[c] = "Institution"
    elif "programme" in cl:
        col_map[c] = "Programme"
    elif "catégorie" in cl or "categorie" in cl:
        col_map[c] = "Catégorie BIOFIN"
    elif "coefficient" in cl:
        col_map[c] = "Coefficient"
    elif "année" in cl or "annee" in cl:
        col_map[c] = "Année"
    elif "totale" in cl:
        col_map[c] = "Dép. Totale"
    elif "bd" in cl or "biodiv" in cl:
        col_map[c] = "Dép. BD"

df = df.rename(columns=col_map)

# Vérification des colonnes requises
required_cols = ["Secteur", "Catégorie BIOFIN", "Année", "Dép. BD"]
for col in required_cols:
    if col not in df.columns:
        st.error(f"❌ Colonne requise manquante : '{col}'")
        st.stop()

# Conversion des types
df["Année"] = pd.to_numeric(df["Année"], errors="coerce").astype("Int64")
df["Dép. BD"] = pd.to_numeric(df["Dép. BD"], errors="coerce")
if "Dép. Totale" in df.columns:
    df["Dép. Totale"] = pd.to_numeric(df["Dép. Totale"], errors="coerce")
if "Coefficient" in df.columns:
    df["Coefficient"] = pd.to_numeric(df["Coefficient"], errors="coerce")

df = df.dropna(subset=["Année", "Dép. BD"])

# ─────────────────────────────────────────────────────────────────────────────
# FILTRES - GESTION ROBUSTE
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛️ Filtres")

    # Années
    annees_dispo = sorted(df["Année"].dropna().unique().tolist())
    annees_sel = st.multiselect(
        "📅 Années",
        annees_dispo,
        default=annees_dispo,
        help="Sélectionnez une ou plusieurs années"
    )

    # Secteurs
    secteurs_dispo = sorted(df["Secteur"].dropna().unique().tolist())
    secteurs_sel = st.multiselect(
        "🏛️ Secteurs",
        secteurs_dispo,
        default=secteurs_dispo,
        help="Filtrez par secteur d'activité"
    )

    # Catégories BIOFIN
    cats_dispo = sorted(df["Catégorie BIOFIN"].dropna().unique().tolist())
    cats_sel = st.multiselect(
        "🌱 Catégories BIOFIN",
        cats_dispo,
        default=cats_dispo,
        help="Filtrez par catégorie de dépense biodiversité"
    )

    st.markdown("---")

    # Institutions (si disponibles)
    if "Institution" in df.columns:
        insts_dispo = sorted(df["Institution"].dropna().unique().tolist())
        insts_sel = st.multiselect(
            "🏢 Institutions",
            insts_dispo,
            default=insts_dispo,
            help="Filtrez par institution spécifique"
        )
    else:
        insts_sel = None

    st.markdown("---")

    # Unité d'affichage
    st.markdown("### 📊 Unité d'affichage")
    unite = st.radio(
        "",
        ["Millions FCFA", "Milliards FCFA"],
        index=0,
        horizontal=True
    )
    diviseur = 1000 if unite == "Milliards FCFA" else 1
    unite_label = "Mds FCFA" if unite == "Milliards FCFA" else "M FCFA"

# Application des filtres (gestion des valeurs par défaut)
annees_sel = annees_sel if annees_sel else annees_dispo
secteurs_sel = secteurs_sel if secteurs_sel else secteurs_dispo
cats_sel = cats_sel if cats_sel else cats_dispo

# Filtrage principal
dff = df[
    df["Année"].isin(annees_sel) &
    df["Secteur"].isin(secteurs_sel) &
    df["Catégorie BIOFIN"].isin(cats_sel)
    ].copy()

if insts_sel and "Institution" in dff.columns:
    dff = dff[dff["Institution"].isin(insts_sel)]

# Vérification des données après filtrage
if dff.empty:
    st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés. Veuillez élargir vos critères.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
periode = f"{min(annees_sel)}–{max(annees_sel)}" if annees_sel else ""
st.markdown(f"""
<div class="hero-header">
    <p class="hero-title">Analyse des Dépenses<br>Biodiversité — Cameroun</p>
    <p class="hero-sub">Initiative BIOFIN / PNUD · Tableau de bord interactif · {periode}</p>
    <span class="hero-badge">🌿 ADB · Données {periode}</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────────────────────────────────
total_bd = dff["Dép. BD"].sum() / diviseur
nb_projets = len(dff)

# Catégorie principale
cat_top = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().idxmax()
cat_top_nom = normalize_category_name(cat_top)

# Secteur dominant
secteur_top = dff.groupby("Secteur")["Dép. BD"].sum().idxmax()
part_top = (dff[dff["Secteur"] == secteur_top]["Dép. BD"].sum() / dff["Dép. BD"].sum() * 100)

# Tendance
if len(annees_sel) >= 2:
    an_min, an_max = min(annees_sel), max(annees_sel)
    v_min = dff[dff["Année"] == an_min]["Dép. BD"].sum() / diviseur
    v_max = dff[dff["Année"] == an_max]["Dép. BD"].sum() / diviseur
    delta_pct = ((v_max - v_min) / v_min * 100) if v_min > 0 else 0
else:
    delta_pct = None

# Nombre d'institutions
nb_institutions = dff["Institution"].nunique() if "Institution" in dff.columns else len(secteurs_sel)

# Affichage KPIs
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(kpi_card(
        f"Total Dépenses BD",
        f"{total_bd:,.1f} {unite_label}",
        delta=delta_pct,
        delta_text="vs début période",
        sub=f"sur {periode}" if periode else ""
    ), unsafe_allow_html=True)

with col2:
    st.markdown(kpi_card(
        "Secteur dominant",
        secteur_top,
        sub=f"{part_top:.0f}% du total",
        color="blue"
    ), unsafe_allow_html=True)

with col3:
    st.markdown(kpi_card(
        "Priorité BIOFIN",
        cat_top_nom,
        sub="Plus grande dépense",
        color="orange"
    ), unsafe_allow_html=True)

with col4:
    st.markdown(kpi_card(
        "Acteurs impliqués",
        f"{nb_institutions:,}",
        sub=f"{nb_projets} projets/programmes",
        color="purple"
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ONGLETS PRINCIPAUX
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'ensemble",
    "📈 Tendances",
    "🏛️ Par secteur",
    "🌱 Catégories BIOFIN",
    "📋 Données détaillées"
])

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 - VUE D'ENSEMBLE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">📊 Répartition globale des dépenses</div>', unsafe_allow_html=True)

    colA, colB = st.columns(2)

    with colA:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Dépenses par secteur
            sect_df = dff.groupby("Secteur")["Dép. BD"].sum().reset_index()
            sect_df["Dép. BD"] = sect_df["Dép. BD"] / diviseur
            sect_df["Part (%)"] = (sect_df["Dép. BD"] / sect_df["Dép. BD"].sum() * 100).round(1)
            sect_df = sect_df.sort_values("Dép. BD", ascending=True)

            fig_sect = px.bar(
                sect_df,
                x="Dép. BD", y="Secteur", orientation="h",
                color="Secteur",
                color_discrete_map=PALETTE_SECT,
                text=sect_df.apply(lambda r: f"{r['Dép. BD']:,.1f} ({r['Part (%)']:.0f}%)", axis=1),
                labels={"Dép. BD": f"Dépenses BD ({unite_label})", "Secteur": ""},
                title=f"Dépenses par secteur"
            )
            fig_sect.update_traces(
                textposition="outside",
                textfont_size=11,
                marker_line_width=0,
                hovertemplate="%{y}: %{x:,.1f} " + unite_label + "<br>Part: %{customdata}%<extra></extra>",
                customdata=sect_df["Part (%)"]
            )
            fig_sect.update_layout(**LAYOUT_COMMUN, height=350, showlegend=False)
            st.plotly_chart(fig_sect, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            # Répartition par catégorie
            cat_df = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
            cat_df["Dép. BD"] = cat_df["Dép. BD"] / diviseur
            cat_df["Cat. courte"] = cat_df["Catégorie BIOFIN"].apply(normalize_category_name)
            cat_df = cat_df.sort_values("Dép. BD", ascending=False)

            fig_cat = px.pie(
                cat_df,
                values="Dép. BD",
                names="Cat. courte",
                color_discrete_sequence=PALETTE_CAT,
                hole=0.5,
                title="Répartition par catégorie BIOFIN"
            )
            fig_cat.update_traces(
                textposition="outside",
                textinfo="percent+label",
                textfont_size=10,
                pull=[0.02] * len(cat_df)
            )
            fig_cat.update_layout(**LAYOUT_COMMUN, height=350, showlegend=False)
            fig_cat.add_annotation(
                text=f"<b>{total_bd:,.0f}</b><br>{unite_label}",
                x=0.5, y=0.5,
                font_size=12,
                font_color="#1C3A2B",
                showarrow=False
            )
            st.plotly_chart(fig_cat, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Tableau récapitulatif
    st.markdown('<div class="section-title">📋 Synthèse par secteur et catégorie</div>', unsafe_allow_html=True)

    pivot_summary = dff.pivot_table(
        index="Secteur",
        columns="Catégorie BIOFIN",
        values="Dép. BD",
        aggfunc="sum",
        margins=True,
        margins_name="TOTAL"
    ) / diviseur

    pivot_summary.columns = [normalize_category_name(c) for c in pivot_summary.columns]
    pivot_summary = pivot_summary.round(1)

    st.dataframe(
        pivot_summary.style
        .format("{:,.1f}")
        .background_gradient(cmap="Greens", subset=[c for c in pivot_summary.columns if c != "TOTAL"])
        .set_properties(**{"font-size": "12px"}),
        use_container_width=True,
        height=300
    )

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 - TENDANCES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📈 Évolution temporelle des dépenses</div>', unsafe_allow_html=True)

    # Évolution totale
    evol = dff.groupby("Année")["Dép. BD"].sum().reset_index()
    evol["Dép. BD"] = evol["Dép. BD"] / diviseur
    evol["Croissance (%)"] = evol["Dép. BD"].pct_change() * 100
    evol["Année_str"] = evol["Année"].astype(str)

    colA, colB = st.columns(2)

    with colA:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=evol["Année_str"],
                y=evol["Dép. BD"],
                mode="lines+markers+text",
                line=dict(color="#2E6B47", width=3),
                marker=dict(size=12, color="#2E6B47", line=dict(color="white", width=2)),
                fill="tozeroy",
                fillcolor="rgba(76,175,118,0.1)",
                text=evol["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
                textposition="top center",
                textfont=dict(size=11, color="#1C3A2B")
            ))
            fig_line.update_layout(
                **LAYOUT_COMMUN,
                title=f"Évolution totale ({unite_label})",
                height=350,
                xaxis=dict(title="Année", tickfont_size=12),
                yaxis=dict(title=unite_label, tickfont_size=12),
                showlegend=False
            )
            st.plotly_chart(fig_line, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    with colB:
        with st.container():
            st.markdown('<div class="chart-container">', unsafe_allow_html=True)
            evol_croiss = evol.dropna(subset=["Croissance (%)"])
            couleurs = ["#2E6B47" if v >= 0 else "#C53030" for v in evol_croiss["Croissance (%)"]]

            fig_growth = go.Figure(go.Bar(
                x=evol_croiss["Année_str"],
                y=evol_croiss["Croissance (%)"],
                marker_color=couleurs,
                text=evol_croiss["Croissance (%)"].apply(lambda x: f"{x:.1f}%"),
                textposition="outside",
                textfont_size=11
            ))
            fig_growth.update_layout(
                **LAYOUT_COMMUN,
                title="Taux de croissance annuel (%)",
                height=350,
                xaxis=dict(title="Année", tickfont_size=12),
                yaxis=dict(title="%", tickfont_size=12, zeroline=True, zerolinecolor="#CCC"),
                showlegend=False
            )
            st.plotly_chart(fig_growth, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

    # Évolution par secteur
    st.markdown('<div class="section-title">📊 Évolution par secteur</div>', unsafe_allow_html=True)

    evol_sect = dff.groupby(["Année", "Secteur"])["Dép. BD"].sum().reset_index()
    evol_sect["Dép. BD"] = evol_sect["Dép. BD"] / diviseur
    evol_sect["Année_str"] = evol_sect["Année"].astype(str)

    fig_sect_evol = px.line(
        evol_sect,
        x="Année_str", y="Dép. BD",
        color="Secteur",
        color_discrete_map=PALETTE_SECT,
        markers=True,
        labels={"Dép. BD": f"Dépenses BD ({unite_label})", "Année_str": "Année"},
        title=f"Évolution des dépenses par secteur ({unite_label})"
    )
    fig_sect_evol.update_traces(line_width=2.5, marker_size=8)
    fig_sect_evol.update_layout(**LAYOUT_COMMUN, height=380)
    st.plotly_chart(fig_sect_evol, use_container_width=True)

    # Évolution par catégorie
    st.markdown('<div class="section-title">📊 Évolution par catégorie BIOFIN</div>', unsafe_allow_html=True)

    evol_cat = dff.groupby(["Année", "Catégorie BIOFIN"])["Dép. BD"].sum().reset_index()
    evol_cat["Dép. BD"] = evol_cat["Dép. BD"] / diviseur
    evol_cat["Cat. courte"] = evol_cat["Catégorie BIOFIN"].apply(normalize_category_name)
    evol_cat["Année_str"] = evol_cat["Année"].astype(str)

    fig_cat_evol = px.area(
        evol_cat,
        x="Année_str", y="Dép. BD",
        color="Cat. courte",
        color_discrete_sequence=PALETTE_CAT