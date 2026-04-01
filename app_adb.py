import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
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

html, body, [class*="css"] {
    font-family: 'Source Sans 3', sans-serif;
}

.main { background: #F7F5F0; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1500px; }

/* ── SIDEBAR ── */
[data-testid="stSidebar"] {
    background: #1C3A2B;
    border-right: 3px solid #2E6B47;
}
[data-testid="stSidebar"] * { color: #C8E6C9 !important; }
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #FFFFFF !important; font-family: 'Libre Baskerville', serif !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #A5D6A7 !important; font-size: 0.85rem; }
[data-testid="stSidebar"] label {
    color: #81C784 !important;
    font-weight: 600;
    font-size: 0.78rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
}
[data-testid="stSidebar"] .stMultiSelect span,
[data-testid="stSidebar"] .stSelectbox span { color: #1C3A2B !important; }
[data-testid="stSidebar"] hr { border-color: #2E6B47 !important; opacity: 0.5; }

/* ── HERO ── */
.hero-header {
    background: linear-gradient(120deg, #1C3A2B 0%, #2E6B47 55%, #4CAF76 100%);
    border-radius: 12px;
    padding: 2rem 2.5rem;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
    border-left: 6px solid #6FCF97;
}
.hero-header::after {
    content: "🌿";
    position: absolute;
    right: 2.5rem;
    top: 50%;
    transform: translateY(-50%);
    font-size: 6rem;
    opacity: 0.08;
}
.hero-title {
    font-family: 'Libre Baskerville', serif;
    font-size: 2rem;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 0.3rem 0;
    line-height: 1.2;
}
.hero-sub {
    color: #A5D6A7;
    font-size: 0.9rem;
    font-weight: 400;
    letter-spacing: 0.05em;
}
.hero-badge {
    display: inline-block;
    background: rgba(255,255,255,0.12);
    color: #E8F5E9;
    border-radius: 4px;
    padding: 0.2rem 0.8rem;
    font-size: 0.72rem;
    font-weight: 700;
    margin-top: 0.8rem;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    border: 1px solid rgba(255,255,255,0.2);
}

/* ── KPI CARDS ── */
.kpi-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.2rem 1.4rem;
    border-top: 4px solid #2E6B47;
    box-shadow: 0 2px 10px rgba(28,58,43,0.08);
    height: 100%;
}
.kpi-card.orange { border-top-color: #E07B39; }
.kpi-card.blue   { border-top-color: #2B6CB0; }
.kpi-card.purple { border-top-color: #6B46C1; }
.kpi-label {
    font-size: 0.7rem;
    color: #718096;
    font-weight: 700;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    margin-bottom: 0.5rem;
}
.kpi-value {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: #1C3A2B;
    line-height: 1.1;
    word-break: break-word;
}
.kpi-delta {
    font-size: 0.78rem;
    color: #2E6B47;
    font-weight: 600;
    margin-top: 0.3rem;
}
.kpi-delta.neg { color: #C53030; }

/* ── SECTION TITLES ── */
.section-title {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.2rem;
    font-weight: 700;
    color: #1C3A2B;
    margin: 1.5rem 0 0.8rem 0;
    padding-bottom: 0.5rem;
    border-bottom: 2px solid #C8E6C9;
}

/* ── TABS ── */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.2rem;
    background: #E8F5E9;
    padding: 0.35rem;
    border-radius: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px;
    padding: 0.4rem 1rem;
    font-weight: 600;
    color: #2E6B47;
    font-size: 0.85rem;
}
.stTabs [aria-selected="true"] {
    background: #1C3A2B !important;
    color: white !important;
}

/* ── TABLES ── */
.dataframe { font-size: 0.83rem !important; }
thead tr th {
    background-color: #1C3A2B !important;
    color: white !important;
    font-weight: 700 !important;
    font-size: 0.8rem !important;
}

/* ── METRICS ── */
[data-testid="metric-container"] {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}

/* ── FOOTER ── */
.footer {
    text-align: center;
    color: #A0AEC0;
    font-size: 0.75rem;
    margin-top: 2rem;
    padding-top: 1rem;
    border-top: 1px solid #E2E8F0;
}

/* ── HIDE STREAMLIT BRANDING ── */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTES
# ─────────────────────────────────────────────────────────────────────────────
PALETTE_CATEGORIES = [
    "#1C3A2B", "#2E6B47", "#3D8B5E", "#4CAF76",
    "#6FCF97", "#95E0B4", "#E07B39", "#C53030",
    "#2B6CB0"
]
PALETTE_SECTEURS = {
    "Public":         "#2E6B47",
    "ONG / OSC":      "#2B6CB0",
    "Secteur Privé":  "#6B46C1",
    "PTF":            "#E07B39",
}

# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def charger_donnees(fichier):
    xls = pd.ExcelFile(fichier)
    feuilles = xls.sheet_names
    df = None
    macro = None

    for nom in ["PowerBI_Data", "D. Publiques"]:
        if nom in feuilles:
            if nom == "PowerBI_Data":
                df = pd.read_excel(fichier, sheet_name=nom, header=1)
                df = df.dropna(subset=["Secteur", "Année"])
            break

    if df is None:
        frames = []
        mapping = {
            "D. Publiques":   "Public",
            "D. Publiques ":  "Public",
            "ONG OSC":        "ONG / OSC",
            "ONG OSC ":       "ONG / OSC",
            "Secteur Prive":  "Secteur Privé",
            "Secteur Prive.": "Secteur Privé",
            "Secteur Privé":  "Secteur Privé",
            "PTF":            "PTF",
        }
        for feuille, secteur in mapping.items():
            if feuille in feuilles:
                tmp = pd.read_excel(fichier, sheet_name=feuille, header=2)
                tmp = tmp.dropna(how="all")
                frames.append((secteur, tmp))

    for nom in ["Donnees Macro", "Données Macro"]:
        if nom in feuilles:
            macro = pd.read_excel(fichier, sheet_name=nom, header=1)
            macro = macro.dropna(subset=["Indicateur"])
            break

    return df, macro, feuilles


def kpi_card(label, value, delta=None, couleur=""):
    delta_html = ""
    if delta is not None:
        cls = "neg" if delta < 0 else ""
        signe = "▲" if delta >= 0 else "▼"
        delta_html = f'<div class="kpi-delta {cls}">{signe} {abs(delta):.1f}% vs année de référence</div>'
    return f"""
    <div class="kpi-card {couleur}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 ADB Biodiversité")
    st.markdown("**Analyse des Dépenses pour la Biodiversité**")
    st.markdown("---")

    fichier_charge = st.file_uploader(
        "📂 Charger votre fichier Excel",
        type=["xlsx", "xls"],
        help="Fichier ADB au format Excel (.xlsx)"
    )

    st.markdown("---")
    st.markdown("### 🎛️ Filtres")

# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT
# ─────────────────────────────────────────────────────────────────────────────
if fichier_charge is None:
    try:
        df_brut, macro_brut, feuilles_dispo = charger_donnees(
            "ADB_Cameroun_Simulation.xlsx"
        )
        mode_demo = True
    except Exception:
        st.markdown("""
        <div class="hero-header">
            <p class="hero-title">Analyse des Dépenses<br>Biodiversité — Cameroun</p>
            <p class="hero-sub">Initiative BIOFIN · Tableau de bord interactif</p>
            <span class="hero-badge">ADB · 2020–2024</span>
        </div>
        """, unsafe_allow_html=True)
        st.warning("Utilisez le panneau latéral pour charger votre fichier Excel ADB.")
        st.stop()
else:
    df_brut, macro_brut, feuilles_dispo = charger_donnees(fichier_charge)
    mode_demo = False

if df_brut is None:
    st.error("❌ Impossible de lire les données. Vérifiez que votre fichier contient la feuille 'PowerBI_Data'.")
    st.stop()

df = df_brut.copy()

# Nettoyage colonnes
col_map = {}
for c in df.columns:
    cl = str(c).lower().strip()
    if "secteur" in cl:         col_map[c] = "Secteur"
    elif "institution" in cl:   col_map[c] = "Institution"
    elif "programme" in cl:     col_map[c] = "Programme"
    elif "catégorie" in cl or "categorie" in cl: col_map[c] = "Catégorie BIOFIN"
    elif "coefficient" in cl:   col_map[c] = "Coefficient"
    elif "année" in cl or "annee" in cl: col_map[c] = "Année"
    elif "totale" in cl:        col_map[c] = "Dép. Totale"
    elif "bd" in cl or "biodiv" in cl:   col_map[c] = "Dép. BD"
df = df.rename(columns=col_map)

req = ["Secteur", "Catégorie BIOFIN", "Année", "Dép. BD"]
for r in req:
    if r not in df.columns:
        st.error(f"Colonne manquante : '{r}'. Vérifiez la structure du fichier.")
        st.stop()

df["Année"] = pd.to_numeric(df["Année"], errors="coerce").astype("Int64")
df["Dép. BD"] = pd.to_numeric(df["Dép. BD"], errors="coerce")
if "Dép. Totale" in df.columns:
    df["Dép. Totale"] = pd.to_numeric(df["Dép. Totale"], errors="coerce")
df = df.dropna(subset=["Année", "Dép. BD"])

# ─────────────────────────────────────────────────────────────────────────────
# FILTRES SIDEBAR — placés ici pour être TOUJOURS visibles
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    annees_dispo = sorted(df["Année"].dropna().unique().tolist())
    annees_sel = st.multiselect("📅 Années", annees_dispo, default=annees_dispo)

    secteurs_dispo = sorted(df["Secteur"].dropna().unique().tolist())
    secteurs_sel = st.multiselect("🏛️ Secteurs", secteurs_dispo, default=secteurs_dispo)

    cats_dispo = sorted(df["Catégorie BIOFIN"].dropna().unique().tolist())
    cats_sel = st.multiselect("🌱 Catégories BIOFIN", cats_dispo, default=cats_dispo)

    st.markdown("---")
    if "Institution" in df.columns:
        insts_dispo = sorted(df["Institution"].dropna().unique().tolist())
        inst_sel = st.multiselect("🏢 Institutions", insts_dispo, default=insts_dispo)
    else:
        inst_sel = None

    st.markdown("---")
    st.markdown("**📊 Unité d'affichage**")
    unite = st.radio("", ["Millions FCFA", "Milliards FCFA"], index=0, horizontal=True)
    diviseur = 1000 if unite == "Milliards FCFA" else 1
    unite_label = "Mds FCFA" if unite == "Milliards FCFA" else "M FCFA"

# ─────────────────────────────────────────────────────────────────────────────
# FILTRAGE
# ─────────────────────────────────────────────────────────────────────────────
if not annees_sel:
    annees_sel = annees_dispo
if not secteurs_sel:
    secteurs_sel = secteurs_dispo
if not cats_sel:
    cats_sel = cats_dispo

dff = df[
    df["Année"].isin(annees_sel) &
    df["Secteur"].isin(secteurs_sel) &
    df["Catégorie BIOFIN"].isin(cats_sel)
].copy()
if inst_sel and "Institution" in dff.columns:
    dff = dff[dff["Institution"].isin(inst_sel)]

if dff.empty:
    st.warning("⚠️ Aucune donnée pour les filtres sélectionnés.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
periode = f"{min(annees_sel)}–{max(annees_sel)}" if annees_sel else ""
st.markdown(f"""
<div class="hero-header">
    <p class="hero-title">Analyse des Dépenses Biodiversité — Cameroun</p>
    <p class="hero-sub">Initiative BIOFIN / PNUD · Tableau de bord interactif · {periode}</p>
    <span class="hero-badge">ADB · Données {periode}</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────────────────────────────────
total_bd = dff["Dép. BD"].sum() / diviseur
nb_institutions = len(dff["Institution"].unique()) if "Institution" in dff.columns else 0
cat_top = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().idxmax()
# Nom complet de la catégorie, nettoyé du numéro
cat_top_nom = cat_top.split(". ", 1)[-1] if ". " in cat_top else cat_top

if len(annees_sel) >= 2:
    an_min, an_max = min(annees_sel), max(annees_sel)
    v_min = dff[dff["Année"] == an_min]["Dép. BD"].sum() / diviseur
    v_max = dff[dff["Année"] == an_max]["Dép. BD"].sum() / diviseur
    delta_pct = ((v_max - v_min) / v_min * 100) if v_min > 0 else 0
else:
    delta_pct = None

secteur_top = dff.groupby("Secteur")["Dép. BD"].sum().idxmax()
part_top = dff.groupby("Secteur")["Dép. BD"].sum().max() / dff["Dép. BD"].sum() * 100

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(kpi_card(
        f"Total Dépenses BD ({unite_label})",
        f"{total_bd:,.1f}",
        delta_pct, ""
    ), unsafe_allow_html=True)
with c2:
    st.markdown(kpi_card(
        "Secteur dominant",
        f"{secteur_top} ({part_top:.0f}%)",
        None, "blue"
    ), unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card(
        "Catégorie BIOFIN principale",
        cat_top_nom,
        None, "orange"
    ), unsafe_allow_html=True)
with c4:
    st.markdown(kpi_card(
        "Institutions / Acteurs",
        str(nb_institutions) if nb_institutions > 0 else str(len(secteurs_sel)),
        None, "purple"
    ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ONGLETS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Catégories BIOFIN",
    "📈 Évolution temporelle",
    "🏛️ Par secteur",
    "🔍 Analyse détaillée",
    "📋 Données brutes",
])

LAYOUT_COMMUN = dict(
    font_family="Source Sans 3",
    font_size=13,
    plot_bgcolor="white",
    paper_bgcolor="white",
    title_font_size=15,
    title_font_color="#1C3A2B",
    title_font_family="Libre Baskerville",
    margin=dict(l=15, r=15, t=45, b=15),
)

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 — CATÉGORIES BIOFIN
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">🌱 Dépenses BD par catégorie BIOFIN</div>', unsafe_allow_html=True)

    cat_df = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
    cat_df["Dép. BD"] = cat_df["Dép. BD"] / diviseur
    cat_df = cat_df.sort_values("Dép. BD", ascending=True)
    cat_df["Part (%)"] = (cat_df["Dép. BD"] / cat_df["Dép. BD"].sum() * 100).round(1)
    # Nom court : retirer le numéro en début
    cat_df["Cat. courte"] = cat_df["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        fig_bar = px.bar(
            cat_df,
            x="Dép. BD",
            y="Cat. courte",
            orientation="h",
            color="Dép. BD",
            color_continuous_scale=["#C8E6C9", "#4CAF76", "#1C3A2B"],
            text=cat_df["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
            labels={"Dép. BD": f"Dépenses BD ({unite_label})", "Cat. courte": ""},
            title=f"Dépenses BD par catégorie ({unite_label})"
        )
        fig_bar.update_traces(
            textposition="outside",
            textfont_size=12,
            textfont_color="#1C3A2B",
            marker_line_width=0,
        )
        fig_bar.update_layout(
            **LAYOUT_COMMUN,
            height=440,
            coloraxis_showscale=False,
            xaxis=dict(gridcolor="#F0F0F0", showline=False, title=unite_label),
            yaxis=dict(gridcolor="rgba(0,0,0,0)", automargin=True, tickfont_size=12),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        fig_pie = px.pie(
            cat_df,
            values="Dép. BD",
            names="Cat. courte",
            color_discrete_sequence=PALETTE_CATEGORIES,
            hole=0.5,
            title="Répartition en % du total"
        )
        fig_pie.update_traces(
            textposition="outside",
            textinfo="percent+label",
            textfont_size=11,
            pull=[0.02]*len(cat_df),
        )
        fig_pie.update_layout(
            **LAYOUT_COMMUN,
            height=440,
            showlegend=False,
        )
        fig_pie.add_annotation(
            text=f"<b>{total_bd:,.1f}</b><br>{unite_label}",
            x=0.5, y=0.5,
            font_size=13,
            font_color="#1C3A2B",
            showarrow=False,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Heatmap
    st.markdown('<div class="section-title">🔥 Heatmap : Catégories × Années</div>', unsafe_allow_html=True)
    pivot = dff.pivot_table(
        index="Catégorie BIOFIN", columns="Année",
        values="Dép. BD", aggfunc="sum"
    ) / diviseur
    pivot.index = pivot.index.str.replace(r"^\d+\.\s*", "", regex=True)

    fig_heat = go.Figure(data=go.Heatmap(
        z=pivot.values,
        x=[str(c) for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0, "#E8F5E9"], [0.5, "#4CAF76"], [1, "#1C3A2B"]],
        text=np.round(pivot.values, 1),
        texttemplate="%{text}",
        textfont={"size": 12},
        hoverongaps=False,
        colorbar=dict(title=unite_label),
    ))
    fig_heat.update_layout(
        **LAYOUT_COMMUN,
        height=380,
        xaxis=dict(side="top", tickfont_size=13),
        yaxis=dict(automargin=True, tickfont_size=12),
    )
    st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 — ÉVOLUTION TEMPORELLE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📈 Évolution des dépenses BD dans le temps</div>', unsafe_allow_html=True)

    evol_total = dff.groupby("Année")["Dép. BD"].sum().reset_index()
    evol_total["Dép. BD"] = evol_total["Dép. BD"] / diviseur
    evol_total["Année"] = evol_total["Année"].astype(str)

    col_a, col_b = st.columns(2)

    with col_a:
        fig_line = go.Figure()
        fig_line.add_trace(go.Scatter(
            x=evol_total["Année"],
            y=evol_total["Dép. BD"],
            mode="lines+markers+text",
            line=dict(color="#2E6B47", width=3),
            marker=dict(size=10, color="#2E6B47", line=dict(color="white", width=2)),
            fill="tozeroy",
            fillcolor="rgba(76,175,118,0.12)",
            text=evol_total["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
            textposition="top center",
            textfont=dict(size=12, color="#1C3A2B"),
            name="Total BD"
        ))
        fig_line.update_layout(
            **LAYOUT_COMMUN,
            title=f"Évolution totale dépenses BD ({unite_label})",
            height=360,
            xaxis=dict(gridcolor="#F5F5F5", showline=True, linecolor="#E0E0E0", tickfont_size=13),
            yaxis=dict(gridcolor="#F5F5F5", title=unite_label, tickfont_size=12),
            showlegend=False,
        )
        st.plotly_chart(fig_line, use_container_width=True)

    with col_b:
        evol_total_num = dff.groupby("Année")["Dép. BD"].sum().reset_index()
        evol_total_num["Croissance (%)"] = evol_total_num["Dép. BD"].pct_change() * 100
        evol_total_num = evol_total_num.dropna()
        evol_total_num["Année"] = evol_total_num["Année"].astype(str)

        couleurs_croiss = ["#2E6B47" if v >= 0 else "#C53030" for v in evol_total_num["Croissance (%)"]]
        fig_growth = go.Figure(go.Bar(
            x=evol_total_num["Année"],
            y=evol_total_num["Croissance (%)"],
            marker_color=couleurs_croiss,
            text=evol_total_num["Croissance (%)"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside",
            textfont=dict(size=12),
        ))
        fig_growth.update_layout(
            **LAYOUT_COMMUN,
            title="Taux de croissance annuel (%)",
            height=360,
            xaxis=dict(gridcolor="#F5F5F5", tickfont_size=13),
            yaxis=dict(gridcolor="#F5F5F5", title="%", zeroline=True, zerolinecolor="#CCC", tickfont_size=12),
            showlegend=False,
        )
        st.plotly_chart(fig_growth, use_container_width=True)

    st.markdown('<div class="section-title">📊 Évolution par catégorie BIOFIN</div>', unsafe_allow_html=True)

    evol_cat = dff.groupby(["Année", "Catégorie BIOFIN"])["Dép. BD"].sum().reset_index()
    evol_cat["Dép. BD"] = evol_cat["Dép. BD"] / diviseur
    evol_cat["Cat. courte"] = evol_cat["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)
    evol_cat["Année"] = evol_cat["Année"].astype(str)

    fig_area = px.area(
        evol_cat,
        x="Année", y="Dép. BD", color="Cat. courte",
        color_discrete_sequence=PALETTE_CATEGORIES,
        labels={"Dép. BD": f"Dépenses BD ({unite_label})", "Cat. courte": "Catégorie"},
        title=f"Évolution empilée par catégorie BIOFIN ({unite_label})"
    )
    fig_area.update_layout(
        **LAYOUT_COMMUN,
        height=400,
        xaxis=dict(gridcolor="#F5F5F5", tickfont_size=13),
        yaxis=dict(gridcolor="#F5F5F5", tickfont_size=12),
        legend=dict(font_size=11),
    )
    st.plotly_chart(fig_area, use_container_width=True)

    evol_sect = dff.groupby(["Année", "Secteur"])["Dép. BD"].sum().reset_index()
    evol_sect["Dép. BD"] = evol_sect["Dép. BD"] / diviseur
    evol_sect["Année"] = evol_sect["Année"].astype(str)

    fig_line_sect = px.line(
        evol_sect, x="Année", y="Dép. BD", color="Secteur",
        color_discrete_map=PALETTE_SECTEURS,
        markers=True,
        labels={"Dép. BD": f"Dépenses BD ({unite_label})"},
        title=f"Évolution par secteur ({unite_label})"
    )
    fig_line_sect.update_traces(line_width=2.5, marker_size=9)
    fig_line_sect.update_layout(
        **LAYOUT_COMMUN,
        height=360,
        xaxis=dict(gridcolor="#F5F5F5", tickfont_size=13),
        yaxis=dict(gridcolor="#F5F5F5", tickfont_size=12),
        legend=dict(font_size=12),
    )
    st.plotly_chart(fig_line_sect, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 3 — PAR SECTEUR
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🏛️ Répartition par secteur de financement</div>', unsafe_allow_html=True)

    sect_df = dff.groupby("Secteur")["Dép. BD"].sum().reset_index()
    sect_df["Dép. BD"] = sect_df["Dép. BD"] / diviseur
    sect_df["Part (%)"] = (sect_df["Dép. BD"] / sect_df["Dép. BD"].sum() * 100).round(1)
    sect_df = sect_df.sort_values("Dép. BD", ascending=False)

    col1, col2 = st.columns(2)

    with col1:
        fig_sect_bar = px.bar(
            sect_df, x="Secteur", y="Dép. BD", color="Secteur",
            color_discrete_map=PALETTE_SECTEURS,
            text=sect_df["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
            labels={"Dép. BD": f"Dépenses BD ({unite_label})"},
            title=f"Total BD par secteur ({unite_label})"
        )
        fig_sect_bar.update_traces(textposition="outside", textfont_size=13, marker_line_width=0)
        fig_sect_bar.update_layout(
            **LAYOUT_COMMUN,
            height=400,
            showlegend=False,
            xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont_size=13),
            yaxis=dict(gridcolor="#F5F5F5", tickfont_size=12),
        )
        st.plotly_chart(fig_sect_bar, use_container_width=True)

    with col2:
        fig_sect_pie = px.pie(
            sect_df, values="Dép. BD", names="Secteur",
            color="Secteur", color_discrete_map=PALETTE_SECTEURS,
            hole=0.5, title="Part de chaque secteur (%)"
        )
        fig_sect_pie.update_traces(
            textposition="outside",
            textinfo="label+percent",
            textfont_size=12,
            pull=[0.04]*len(sect_df),
        )
        fig_sect_pie.update_layout(
            **LAYOUT_COMMUN,
            height=400,
            showlegend=False,
        )
        st.plotly_chart(fig_sect_pie, use_container_width=True)

    st.markdown('<div class="section-title">🌐 Vue hiérarchique : Secteur → Catégorie BIOFIN</div>', unsafe_allow_html=True)

    hier_df = dff.groupby(["Secteur", "Catégorie BIOFIN"])["Dép. BD"].sum().reset_index()
    hier_df["Dép. BD"] = hier_df["Dép. BD"] / diviseur
    hier_df["Cat. courte"] = hier_df["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)

    fig_sun = px.sunburst(
        hier_df, path=["Secteur", "Cat. courte"], values="Dép. BD",
        color="Secteur", color_discrete_map=PALETTE_SECTEURS,
        title="Répartition hiérarchique Secteur → Catégorie BIOFIN"
    )
    fig_sun.update_traces(textfont_size=12)
    fig_sun.update_layout(**LAYOUT_COMMUN, height=520)
    st.plotly_chart(fig_sun, use_container_width=True)

    if "Institution" in dff.columns:
        st.markdown('<div class="section-title">🏆 Top 10 Institutions</div>', unsafe_allow_html=True)
        inst_df = dff.groupby(["Institution", "Secteur"])["Dép. BD"].sum().reset_index()
        inst_df["Dép. BD"] = inst_df["Dép. BD"] / diviseur
        inst_df = inst_df.sort_values("Dép. BD", ascending=False).head(10)
        inst_df = inst_df.sort_values("Dép. BD", ascending=True)

        fig_inst = px.bar(
            inst_df, x="Dép. BD", y="Institution",
            color="Secteur", color_discrete_map=PALETTE_SECTEURS,
            orientation="h",
            text=inst_df["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
            labels={"Dép. BD": f"Dépenses BD ({unite_label})"},
            title=f"Top 10 acteurs — Dépenses BD cumulées ({unite_label})"
        )
        fig_inst.update_traces(textposition="outside", textfont_size=12)
        fig_inst.update_layout(
            **LAYOUT_COMMUN,
            height=420,
            legend=dict(font_size=12),
            yaxis=dict(automargin=True, tickfont_size=12),
            xaxis=dict(tickfont_size=12),
        )
        st.plotly_chart(fig_inst, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 4 — ANALYSE DÉTAILLÉE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🔍 Analyse croisée & Coefficients</div>', unsafe_allow_html=True)

    col_d1, col_d2 = st.columns(2)

    with col_d1:
        if "Dép. Totale" in dff.columns:
            scatter_df = dff.groupby(
                ["Institution" if "Institution" in dff.columns else "Secteur", "Secteur"]
            ).agg({"Dép. Totale": "sum", "Dép. BD": "sum"}).reset_index()
            scatter_df.columns = ["Nom", "Secteur", "Dép. Totale", "Dép. BD"]
            scatter_df["Dép. Totale"] = scatter_df["Dép. Totale"] / diviseur
            scatter_df["Dép. BD"] = scatter_df["Dép. BD"] / diviseur
            scatter_df["Coeff moyen (%)"] = (scatter_df["Dép. BD"] / scatter_df["Dép. Totale"] * 100).round(1)

            fig_scatter = px.scatter(
                scatter_df, x="Dép. Totale", y="Dép. BD",
                color="Secteur", color_discrete_map=PALETTE_SECTEURS,
                size="Dép. BD", size_max=35,
                hover_name="Nom",
                hover_data={"Coeff moyen (%)": True},
                labels={
                    "Dép. Totale": f"Dépense Totale ({unite_label})",
                    "Dép. BD": f"Dépense BD ({unite_label})",
                },
                title="Dépense Totale vs Dépense BD par acteur"
            )
            max_val = max(scatter_df["Dép. Totale"].max(), scatter_df["Dép. BD"].max())
            fig_scatter.add_trace(go.Scatter(
                x=[0, max_val], y=[0, max_val],
                mode="lines",
                line=dict(dash="dash", color="#CCC", width=1),
                name="100% BD", showlegend=True
            ))
            fig_scatter.update_layout(**LAYOUT_COMMUN, height=400, legend=dict(font_size=11))
            st.plotly_chart(fig_scatter, use_container_width=True)

    with col_d2:
        if "Coefficient" in dff.columns:
            coef_df = dff[["Secteur", "Coefficient", "Catégorie BIOFIN"]].copy()
            coef_df["Coefficient (%)"] = (coef_df["Coefficient"] * 100).round(0)

            fig_box = px.box(
                coef_df, x="Secteur", y="Coefficient (%)",
                color="Secteur", color_discrete_map=PALETTE_SECTEURS,
                points="all",
                title="Distribution des coefficients d'attribution par secteur"
            )
            fig_box.update_layout(
                **LAYOUT_COMMUN,
                height=400,
                showlegend=False,
                yaxis=dict(range=[0, 110], title="Coefficient (%)"),
            )
            st.plotly_chart(fig_box, use_container_width=True)

    st.markdown('<div class="section-title">📊 Tableau croisé : Catégories × Secteurs</div>', unsafe_allow_html=True)

    pivot2 = dff.pivot_table(
        index="Catégorie BIOFIN",
        columns="Secteur",
        values="Dép. BD",
        aggfunc="sum",
        margins=True,
        margins_name="TOTAL"
    ) / diviseur

    pivot2.index = [i.replace(r"^\d+\.\s*", "", 1) if i != "TOTAL" else i for i in pivot2.index]
    pivot2 = pivot2.round(1)

    val_max = pivot2.replace(0, float("nan")).stack().max()
    if pd.isna(val_max) or val_max == 0:
        val_max = 1

    def colorier_cellule(val):
        try:
            v = float(val)
            if v <= 0:
                return "background-color: #F9F9F9; color: #AAA"
            intensite = min(int(v / val_max * 180), 180)
            r = 255 - intensite
            g = 255
            b = 255 - intensite
            couleur_texte = "#1C3A2B" if intensite > 80 else "#333"
            return f"background-color: rgb({r},{g},{b}); color: {couleur_texte}; font-weight: 600"
        except (ValueError, TypeError):
            return ""

    st.dataframe(
        pivot2.style
            .applymap(colorier_cellule)
            .format("{:,.1f}")
            .set_properties(**{"font-size": "13px"}),
        use_container_width=True,
        height=400,
    )

    if macro_brut is not None:
        st.markdown('<div class="section-title">🌍 Contexte macro-économique</div>', unsafe_allow_html=True)
        try:
            macro_df = macro_brut.copy()
            macro_df.columns = [str(c) for c in macro_df.columns]
            annee_cols = [c for c in macro_df.columns if c.isdigit() and int(c) in annees_dispo]

            if annee_cols:
                pib_row = macro_df[macro_df["Indicateur"].str.contains("PIB.*Milliards", na=False, case=False)]
                if not pib_row.empty:
                    pib_vals = pib_row[annee_cols].values.flatten().tolist()
                    pib_vals_f = [float(v) for v in pib_vals if pd.notna(v)]

                    bd_par_an = dff.groupby("Année")["Dép. BD"].sum()
                    bd_pib_data = []
                    for i, an in enumerate(annee_cols):
                        an_int = int(an)
                        if an_int in bd_par_an.index and i < len(pib_vals_f):
                            pib_mfcfa = pib_vals_f[i] * 1000
                            bd = bd_par_an[an_int]
                            bd_pib_data.append({
                                "Année": str(an_int),
                                "Part BD/PIB (%)": round(bd / pib_mfcfa * 100, 4)
                            })

                    if bd_pib_data:
                        bd_pib_df = pd.DataFrame(bd_pib_data)
                        fig_macro = go.Figure()
                        fig_macro.add_trace(go.Bar(
                            x=bd_pib_df["Année"],
                            y=bd_pib_df["Part BD/PIB (%)"],
                            marker_color="#4CAF76",
                            text=bd_pib_df["Part BD/PIB (%)"].apply(lambda x: f"{x:.3f}%"),
                            textposition="outside",
                            textfont_size=12,
                        ))
                        fig_macro.update_layout(
                            **LAYOUT_COMMUN,
                            title="Part des dépenses BD dans le PIB (%)",
                            height=340,
                            yaxis=dict(title="%", gridcolor="#F5F5F5"),
                            xaxis=dict(gridcolor="rgba(0,0,0,0)", tickfont_size=13),
                            showlegend=False,
                        )
                        st.plotly_chart(fig_macro, use_container_width=True)
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 5 — DONNÉES BRUTES
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">📋 Données détaillées</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        search = st.text_input("🔎 Rechercher", placeholder="Ministère, programme...")
    with col_f2:
        sort_col = st.selectbox("Trier par", ["Dép. BD", "Année", "Secteur", "Catégorie BIOFIN"])
    with col_f3:
        ordre = st.radio("Ordre", ["Décroissant", "Croissant"], horizontal=True)

    table_df = dff.copy()
    if "Dép. Totale" in table_df.columns:
        table_df["Dép. Totale"] = (table_df["Dép. Totale"] / diviseur).round(2)
    table_df["Dép. BD"] = (table_df["Dép. BD"] / diviseur).round(2)

    if search:
        mask = table_df.apply(lambda row: any(search.lower() in str(v).lower() for v in row), axis=1)
        table_df = table_df[mask]

    asc = ordre == "Croissant"
    if sort_col in table_df.columns:
        table_df = table_df.sort_values(sort_col, ascending=asc)

    st.markdown(f"**{len(table_df):,} lignes** | Unité : {unite_label}")
    st.dataframe(table_df, use_container_width=True, height=460)

    st.markdown("---")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            dff.to_excel(writer, index=False, sheet_name="Données filtrées")
            cat_df_exp = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
            cat_df_exp.to_excel(writer, index=False, sheet_name="Synthèse BIOFIN")
        st.download_button(
            label="⬇️ Exporter les données filtrées (.xlsx)",
            data=buffer.getvalue(),
            file_name="ADB_Export_filtre.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col_e2:
        csv = dff.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="⬇️ Exporter en CSV",
            data=csv,
            file_name="ADB_Export.csv",
            mime="text/csv",
        )

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌿 ADB Biodiversité Cameroun &nbsp;|&nbsp; Initiative BIOFIN / PNUD &nbsp;|&nbsp; Données 2020–2024 &nbsp;|&nbsp; Unité : Millions FCFA
</div>
""", unsafe_allow_html=True)
