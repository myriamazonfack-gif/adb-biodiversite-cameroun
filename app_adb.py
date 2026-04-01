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
# CSS PERSONNALISÉ
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
.main { background: #F7F5F0; }
.block-container { padding: 1.2rem 1.5rem 2rem 1.5rem; max-width: 1600px; }

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0A2F1F 0%, #1C3A2B 100%);
    border-right: none;
}
[data-testid="stSidebar"] * { color: #E8F5E9 !important; }
[data-testid="stSidebar"] label { color: #9CCC65 !important; font-weight: 600; }

/* Hero */
.hero {
    background: linear-gradient(120deg, #1C3A2B 0%, #2E6B47 55%, #4CAF76 100%);
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.2rem;
    border-left: 6px solid #6FCF97;
}
.hero-title {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.8rem; font-weight: 700;
    color: #FFFFFF; margin: 0;
}
.hero-sub { color: #A5D6A7; font-size: 0.88rem; }

/* KPI Cards */
.kpi-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1rem;
    border-top: 4px solid #2E6B47;
    box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    height: 100%;
}
.kpi-card.orange { border-top-color: #E07B39; }
.kpi-card.blue { border-top-color: #2B6CB0; }
.kpi-card.purple { border-top-color: #6B46C1; }
.kpi-label {
    font-size: 0.7rem; color: #718096;
    font-weight: 700; text-transform: uppercase;
}
.kpi-value {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.6rem; font-weight: 700;
    color: #1C3A2B;
}

/* Section Titles */
.section-title {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.1rem; font-weight: 700;
    color: #1C3A2B;
    margin: 1rem 0 0.7rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #C8E6C9;
}

/* Tabs */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.2rem; background: #E8F5E9;
    padding: 0.3rem; border-radius: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px; padding: 0.35rem 0.9rem;
    font-weight: 600; color: #2E6B47;
}
.stTabs [aria-selected="true"] {
    background: #1C3A2B !important; color: white !important;
}

/* Insight */
.insight {
    background: #E8F5E9; border-left: 4px solid #2E6B47;
    border-radius: 6px; padding: 0.7rem 1rem;
    margin: 0.5rem 0;
}

/* Hide Branding */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTES
# ─────────────────────────────────────────────────────────────────────────────
PALETTE_CAT = ["#1C3A2B", "#2E6B47", "#3D8B5E", "#4CAF76", "#6FCF97", "#95E0B4", "#E07B39", "#C53030", "#2B6CB0"]
PALETTE_SECT = {"Public": "#2E6B47", "ONG / OSC": "#2B6CB0", "Secteur Privé": "#6B46C1", "PTF": "#E07B39"}
LAYOUT = dict(
    font_family="Source Sans 3", font_size=13,
    plot_bgcolor="white", paper_bgcolor="white",
    title_font_size=14, title_font_color="#1C3A2B",
    title_font_family="Libre Baskerville",
    margin=dict(l=15, r=15, t=45, b=15),
)


# ─────────────────────────────────────────────────────────────────────────────
# FONCTIONS
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def charger_donnees(fichier):
    """Charge les données depuis le fichier Excel."""
    xls = pd.ExcelFile(fichier)
    feuilles = xls.sheet_names

    df = None
    for nom in ["PowerBI_Data"]:
        if nom in feuilles:
            df = pd.read_excel(fichier, sheet_name=nom, header=1)
            df = df.dropna(subset=["Secteur", "Année"])
            break

    macro = None
    for nom in ["Donnees Macro", "Données Macro"]:
        if nom in feuilles:
            macro = pd.read_excel(fichier, sheet_name=nom, header=1)
            break

    return df, macro


def kpi_card(label, value, sub="", delta=None, couleur=""):
    """Génère une carte KPI."""
    delta_html = f'<div class="kpi-delta" style="color:#2E6B47">{"▲" if delta >= 0 else "▼"} {abs(delta):.1f}%</div>' if delta is not None else ""
    sub_html = f'<div class="kpi-sub" style="font-size:0.7rem;color:#718096">{sub}</div>' if sub else ""
    return f"""<div class="kpi-card {couleur}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {sub_html}{delta_html}
    </div>"""


# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-title">Analyse des Dépenses Biodiversité — Cameroun</p>
    <p class="hero-sub">Initiative BIOFIN / PNUD · Tableau de bord interactif</p>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 ADB Biodiversité")
    st.markdown("**Analyse des Dépenses**")
    st.markdown("---")

    fichier_charge = st.file_uploader(
        "📂 Charger votre fichier Excel",
        type=["xlsx", "xls"],
        key="file_uploader"
    )
    st.markdown("---")

# Chargement
try:
    source = fichier_charge if fichier_charge else "ADB_Cameroun_Simulation.xlsx"
    df_brut, macro_brut = charger_donnees(source)
except Exception as e:
    st.error(f"❌ Erreur de chargement : {e}")
    st.stop()

if df_brut is None:
    st.error("❌ Feuille 'PowerBI_Data' introuvable.")
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

# Conversion des types
df["Année"] = pd.to_numeric(df["Année"], errors="coerce").astype("Int64")
df["Dép. BD"] = pd.to_numeric(df["Dép. BD"], errors="coerce")
if "Dép. Totale" in df.columns:
    df["Dép. Totale"] = pd.to_numeric(df["Dép. Totale"], errors="coerce")
if "Coefficient" in df.columns:
    df["Coefficient"] = pd.to_numeric(df["Coefficient"], errors="coerce")

df = df.dropna(subset=["Année", "Dép. BD"])

# ─────────────────────────────────────────────────────────────────────────────
# FILTRES - SOLUTION ROBUSTE AVEC SESSION STATE
# ─────────────────────────────────────────────────────────────────────────────
# Initialisation de session_state pour les filtres
if "filters_initialized" not in st.session_state:
    st.session_state.filters_initialized = True
    st.session_state.annees = None
    st.session_state.secteurs = None
    st.session_state.cats = None
    st.session_state.insts = None
    st.session_state.unite = "Millions FCFA"

with st.sidebar:
    st.markdown("### 🎛️ Filtres")

    # Options disponibles
    annees_dispo = sorted(df["Année"].dropna().unique().tolist())
    secteurs_dispo = sorted(df["Secteur"].dropna().unique().tolist())
    cats_dispo = sorted(df["Catégorie BIOFIN"].dropna().unique().tolist())
    insts_dispo = sorted(df["Institution"].dropna().unique().tolist()) if "Institution" in df.columns else []

    # Filtres avec gestion des defaults
    annees_sel = st.multiselect(
        "📅 Années",
        annees_dispo,
        default=annees_dispo,  # Par défaut toutes les années
        key="annees_filter"
    )

    secteurs_sel = st.multiselect(
        "🏛️ Secteurs",
        secteurs_dispo,
        default=secteurs_dispo,  # Par défaut tous les secteurs
        key="secteurs_filter"
    )

    cats_sel = st.multiselect(
        "🌱 Catégories BIOFIN",
        cats_dispo,
        default=cats_dispo,  # Par défaut toutes les catégories
        key="cats_filter"
    )

    if insts_dispo:
        insts_sel = st.multiselect(
            "🏢 Institutions",
            insts_dispo,
            default=insts_dispo,  # Par défaut toutes les institutions
            key="insts_filter"
        )
    else:
        insts_sel = insts_dispo

    st.markdown("---")

    unite = st.radio(
        "💰 Unité",
        ["Millions FCFA", "Milliards FCFA"],
        index=0,
        key="unite_filter"
    )

# Application des filtres (TRÈS IMPORTANT: on utilise les valeurs sélectionnées)
dff = df.copy()

# Appliquer chaque filtre seulement si des valeurs sont sélectionnées
if annees_sel:
    dff = dff[dff["Année"].isin(annees_sel)]
if secteurs_sel:
    dff = dff[dff["Secteur"].isin(secteurs_sel)]
if cats_sel:
    dff = dff[dff["Catégorie BIOFIN"].isin(cats_sel)]
if insts_sel and "Institution" in dff.columns:
    dff = dff[dff["Institution"].isin(insts_sel)]

# Vérification après filtrage
if dff.empty:
    st.warning("⚠️ Aucune donnée ne correspond aux filtres sélectionnés. Veuillez élargir vos critères.")
    st.stop()

# Calcul du diviseur
diviseur = 1000 if unite == "Milliards FCFA" else 1
unite_label = "Mds FCFA" if unite == "Milliards FCFA" else "M FCFA"

# ─────────────────────────────────────────────────────────────────────────────
# CALCULS DES INDICATEURS
# ─────────────────────────────────────────────────────────────────────────────
total_bd = dff["Dép. BD"].sum() / diviseur
nb_institutions = dff["Institution"].nunique() if "Institution" in dff.columns else 0

cat_top = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().idxmax()
cat_top_nom = cat_top.split(". ", 1)[-1] if ". " in cat_top else cat_top

secteur_top = dff.groupby("Secteur")["Dép. BD"].sum().idxmax()
part_top = dff.groupby("Secteur")["Dép. BD"].sum().max() / dff["Dép. BD"].sum() * 100

# Tendance
an_min, an_max = min(annees_sel), max(annees_sel)
v_min = dff[dff["Année"] == an_min]["Dép. BD"].sum() / diviseur
v_max = dff[dff["Année"] == an_max]["Dép. BD"].sum() / diviseur
delta_pct = ((v_max - v_min) / v_min * 100) if v_min > 0 and len(annees_sel) >= 2 else None

# ─────────────────────────────────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────────────────────────────────
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(kpi_card(
        f"Total Dépenses BD",
        f"{total_bd:,.1f} {unite_label}",
        f"sur {an_min}–{an_max}",
        delta_pct
    ), unsafe_allow_html=True)

with c2:
    st.markdown(kpi_card(
        "Secteur dominant",
        secteur_top,
        f"{part_top:.0f}% du total",
        couleur="blue"
    ), unsafe_allow_html=True)

with c3:
    st.markdown(kpi_card(
        "Priorité BIOFIN",
        cat_top_nom,
        "Plus grande dépense",
        couleur="orange"
    ), unsafe_allow_html=True)

with c4:
    st.markdown(kpi_card(
        "Acteurs impliqués",
        str(nb_institutions) if nb_institutions > 0 else str(len(secteurs_sel)),
        f"{len(dff)} projets",
        couleur="purple"
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ONGLETS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Vue d'ensemble",
    "📈 Tendances",
    "🏛️ Secteurs",
    "🌱 Catégories BIOFIN",
    "📋 Données"
])

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 — VUE D'ENSEMBLE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">📊 Répartition globale</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        sect_df = dff.groupby("Secteur")["Dép. BD"].sum().reset_index()
        sect_df["Dép. BD"] = sect_df["Dép. BD"] / diviseur
        sect_df["Part (%)"] = (sect_df["Dép. BD"] / sect_df["Dép. BD"].sum() * 100).round(1)
        sect_df = sect_df.sort_values("Dép. BD", ascending=True)

        fig = px.bar(
            sect_df, x="Dép. BD", y="Secteur", orientation="h",
            color="Secteur", color_discrete_map=PALETTE_SECT,
            text=sect_df.apply(lambda r: f"{r['Dép. BD']:,.1f} ({r['Part (%)']:.0f}%)", axis=1),
            title=f"Dépenses BD par secteur ({unite_label})"
        )
        fig.update_traces(textposition="outside", textfont_size=12)
        fig.update_layout(**LAYOUT, height=350, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col_b:
        cat_df = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
        cat_df["Dép. BD"] = cat_df["Dép. BD"] / diviseur
        cat_df["Cat. courte"] = cat_df["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)
        cat_df = cat_df.sort_values("Dép. BD", ascending=False)

        fig2 = px.pie(
            cat_df, values="Dép. BD", names="Cat. courte",
            color_discrete_sequence=PALETTE_CAT, hole=0.5,
            title="Répartition par catégorie BIOFIN"
        )
        fig2.update_traces(textposition="outside", textinfo="percent+label", textfont_size=11)
        fig2.update_layout(**LAYOUT, height=350, showlegend=False)
        fig2.add_annotation(
            text=f"<b>{total_bd:,.0f}</b><br>{unite_label}",
            x=0.5, y=0.5, font_size=12, showarrow=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tableau récapitulatif
    st.markdown('<div class="section-title">📋 Résumé par secteur et catégorie</div>', unsafe_allow_html=True)

    pivot_resume = dff.pivot_table(
        index="Secteur", columns="Catégorie BIOFIN",
        values="Dép. BD", aggfunc="sum", margins=True, margins_name="TOTAL"
    ) / diviseur
    pivot_resume.columns = [c.split(". ", 1)[-1] if ". " in str(c) else str(c) for c in pivot_resume.columns]
    pivot_resume = pivot_resume.round(1)

    st.dataframe(
        pivot_resume.style.background_gradient(cmap="Greens").format("{:,.1f}"),
        use_container_width=True, height=250
    )

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 — TENDANCES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📈 Évolution des dépenses</div>', unsafe_allow_html=True)

    evol = dff.groupby("Année")["Dép. BD"].sum().reset_index()
    evol["Dép. BD"] = evol["Dép. BD"] / diviseur
    evol["Année_str"] = evol["Année"].astype(str)

    fig = px.line(
        evol, x="Année_str", y="Dép. BD",
        markers=True, line_shape="linear",
        title=f"Évolution totale des dépenses ({unite_label})"
    )
    fig.update_traces(line=dict(color="#2E6B47", width=3), marker=dict(size=10, color="#2E6B47"))
    fig.update_layout(**LAYOUT, height=400)
    st.plotly_chart(fig, use_container_width=True)

    # Évolution par secteur
    st.markdown('<div class="section-title">📊 Évolution par secteur</div>', unsafe_allow_html=True)

    evol_sect = dff.groupby(["Année", "Secteur"])["Dép. BD"].sum().reset_index()
    evol_sect["Dép. BD"] = evol_sect["Dép. BD"] / diviseur
    evol_sect["Année_str"] = evol_sect["Année"].astype(str)

    fig2 = px.line(
        evol_sect, x="Année_str", y="Dép. BD", color="Secteur",
        color_discrete_map=PALETTE_SECT, markers=True,
        title=f"Évolution par secteur ({unite_label})"
    )
    fig2.update_layout(**LAYOUT, height=400)
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 3 — SECTEURS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🏛️ Analyse par secteur</div>', unsafe_allow_html=True)

    sect_df = dff.groupby("Secteur")["Dép. BD"].sum().reset_index()
    sect_df["Dép. BD"] = sect_df["Dép. BD"] / diviseur
    sect_df["Part (%)"] = (sect_df["Dép. BD"] / sect_df["Dép. BD"].sum() * 100).round(1)

    fig = px.pie(
        sect_df, values="Dép. BD", names="Secteur",
        color="Secteur", color_discrete_map=PALETTE_SECT,
        hole=0.4, title="Répartition par secteur"
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    fig.update_layout(**LAYOUT, height=450)
    st.plotly_chart(fig, use_container_width=True)

    # Top institutions
    if "Institution" in dff.columns:
        st.markdown('<div class="section-title">🏆 Top 10 institutions</div>', unsafe_allow_html=True)

        inst_df = dff.groupby("Institution")["Dép. BD"].sum().reset_index()
        inst_df["Dép. BD"] = inst_df["Dép. BD"] / diviseur
        inst_df = inst_df.sort_values("Dép. BD", ascending=False).head(10)
        inst_df = inst_df.sort_values("Dép. BD", ascending=True)

        fig2 = px.bar(
            inst_df, x="Dép. BD", y="Institution", orientation="h",
            text=inst_df["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
            title=f"Top 10 institutions ({unite_label})"
        )
        fig2.update_traces(marker_color="#2E6B47", textposition="outside")
        fig2.update_layout(**LAYOUT, height=450)
        st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 4 — CATÉGORIES BIOFIN
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🌱 Analyse par catégorie BIOFIN</div>', unsafe_allow_html=True)

    cat_df = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
    cat_df["Dép. BD"] = cat_df["Dép. BD"] / diviseur
    cat_df["Cat. courte"] = cat_df["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)
    cat_df = cat_df.sort_values("Dép. BD", ascending=True)

    fig = px.bar(
        cat_df, x="Dép. BD", y="Cat. courte", orientation="h",
        color="Dép. BD", color_continuous_scale="Greens",
        text=cat_df["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
        title=f"Dépenses par catégorie BIOFIN ({unite_label})"
    )
    fig.update_traces(textposition="outside", textfont_size=12)
    fig.update_layout(**LAYOUT, height=450, coloraxis_showscale=False)
    st.plotly_chart(fig, use_container_width=True)

    # Heatmap
    st.markdown('<div class="section-title">🔥 Heatmap par année</div>', unsafe_allow_html=True)

    pivot_heat = dff.pivot_table(
        index="Catégorie BIOFIN", columns="Année",
        values="Dép. BD", aggfunc="sum"
    ) / diviseur
    pivot_heat.index = pivot_heat.index.str.replace(r"^\d+\.\s*", "", regex=True)

    fig2 = go.Figure(data=go.Heatmap(
        z=pivot_heat.values,
        x=[str(c) for c in pivot_heat.columns],
        y=pivot_heat.index.tolist(),
        colorscale="Greens",
        text=np.round(pivot_heat.values, 1),
        texttemplate="%{text}",
        textfont={"size": 11}
    ))
    fig2.update_layout(**LAYOUT, height=400)
    st.plotly_chart(fig2, use_container_width=True)

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 5 — DONNÉES
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">📋 Données détaillées</div>', unsafe_allow_html=True)

    # Recherche
    search = st.text_input("🔎 Rechercher", placeholder="Ex: MINFOF, WWF...")

    table_df = dff.copy()
    table_df["Dép. BD"] = (table_df["Dép. BD"] / diviseur).round(2)
    if "Dép. Totale" in table_df.columns:
        table_df["Dép. Totale"] = (table_df["Dép. Totale"] / diviseur).round(2)

    if search:
        mask = table_df.apply(lambda row: any(search.lower() in str(v).lower() for v in row), axis=1)
        table_df = table_df[mask]

    st.markdown(f"**{len(table_df):,} lignes** | Unité : {unite_label}")
    st.dataframe(table_df, use_container_width=True, height=500)

    # Export
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            dff.to_excel(writer, index=False, sheet_name="Données filtrées")
        st.download_button(
            "⬇️ Exporter en Excel",
            data=buffer.getvalue(),
            file_name="ADB_Export.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col_e2:
        st.download_button(
            "⬇️ Exporter en CSV",
            data=dff.to_csv(index=False).encode("utf-8"),
            file_name="ADB_Export.csv",
            mime="text/csv",
        )

# Footer
st.markdown("""
<hr>
<p style="text-align:center; color:#A0AEC0; font-size:0.75rem;">
    🌿 ADB Biodiversité Cameroun | Initiative BIOFIN / PNUD
</p>
""", unsafe_allow_html=True)
