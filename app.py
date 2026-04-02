import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
import base64

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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;900&family=DM+Sans:wght@300;400;500;600&display=swap');

html, body, [class*="css"] { font-family: 'DM Sans', sans-serif; }
.main { background: #f4f6f0; }
.block-container { padding: 1.5rem 2rem 2rem 2rem; max-width: 1400px; }

[data-testid="stSidebar"] {
    background: linear-gradient(160deg, #1B4332 0%, #2D6A4F 60%, #40916C 100%);
    border-right: none;
}
[data-testid="stSidebar"] * { color: #d8f3dc !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stSlider label {
    color: #b7e4c7 !important; font-weight: 600; font-size: 0.8rem;
    letter-spacing: 0.08em; text-transform: uppercase;
}
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3 { color: #ffffff !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #d8f3dc !important; }

.hero-header {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 50%, #52B788 100%);
    border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero-header::before {
    content: "🌿"; position: absolute; right: 2rem; top: 50%;
    transform: translateY(-50%); font-size: 5rem; opacity: 0.15;
}
.hero-title {
    font-family: 'Playfair Display', serif; font-size: 2.1rem; font-weight: 900;
    color: #ffffff; margin: 0; line-height: 1.2; letter-spacing: -0.02em;
}
.hero-sub {
    font-family: 'DM Sans', sans-serif; color: #b7e4c7; font-size: 0.95rem;
    margin-top: 0.4rem; font-weight: 300; letter-spacing: 0.04em;
}
.hero-badge {
    display: inline-block; background: rgba(255,255,255,0.18); color: #ffffff;
    border-radius: 20px; padding: 0.2rem 0.9rem; font-size: 0.75rem;
    font-weight: 600; margin-top: 0.8rem; letter-spacing: 0.06em;
    text-transform: uppercase; border: 1px solid rgba(255,255,255,0.3);
}
.kpi-card {
    background: #ffffff; border-radius: 14px; padding: 1.3rem 1.5rem;
    border-left: 5px solid #52B788; box-shadow: 0 2px 12px rgba(27,67,50,0.08);
    height: 100%; transition: transform 0.2s, box-shadow 0.2s;
}
.kpi-card:hover { transform: translateY(-3px); box-shadow: 0 6px 20px rgba(27,67,50,0.13); }
.kpi-card.orange { border-left-color: #F4A261; }
.kpi-card.blue   { border-left-color: #457B9D; }
.kpi-card.purple { border-left-color: #9B5DE5; }
.kpi-label {
    font-size: 0.72rem; color: #6B7280; font-weight: 600;
    letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 0.3rem;
}
.kpi-value {
    font-family: 'Playfair Display', serif; font-size: 2rem;
    font-weight: 700; color: #1B4332; line-height: 1.1;
}
.kpi-delta { font-size: 0.78rem; color: #52B788; font-weight: 500; margin-top: 0.2rem; }
.kpi-delta.neg { color: #E76F51; }
.section-title {
    font-family: 'Playfair Display', serif; font-size: 1.35rem; font-weight: 700;
    color: #1B4332; margin: 1.5rem 0 0.8rem 0; padding-bottom: 0.5rem;
    border-bottom: 2px solid #d8f3dc; display: flex; align-items: center; gap: 0.5rem;
}
.chart-container {
    background: #ffffff; border-radius: 14px; padding: 1.2rem;
    box-shadow: 0 2px 12px rgba(27,67,50,0.07); margin-bottom: 1rem;
}
.stTabs [data-baseweb="tab-list"] {
    gap: 0.3rem; background: #e9f5e9; padding: 0.4rem; border-radius: 12px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 8px; padding: 0.4rem 1.2rem;
    font-weight: 500; color: #2D6A4F; font-size: 0.88rem;
}
.stTabs [aria-selected="true"] { background: #2D6A4F !important; color: white !important; }
.dataframe { font-size: 0.82rem !important; }
thead tr th {
    background-color: #1B4332 !important; color: white !important; font-weight: 600 !important;
}
.footer {
    text-align: center; color: #9CA3AF; font-size: 0.75rem;
    margin-top: 2rem; padding-top: 1rem; border-top: 1px solid #e5e7eb;
}
[data-testid="metric-container"] {
    background: white; border-radius: 12px; padding: 1rem;
    box-shadow: 0 2px 8px rgba(0,0,0,0.06);
}
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTES
# ─────────────────────────────────────────────────────────────────────────────
PALETTE_CATEGORIES = [
    "#1B4332", "#2D6A4F", "#40916C", "#52B788",
    "#74C69D", "#95D5B2", "#F4A261", "#E76F51", "#457B9D"
]
PALETTE_SECTEURS = {
    "Public":        "#2D6A4F",
    "ONG / OSC":     "#457B9D",
    "Secteur Privé": "#9B5DE5",
    "PTF":           "#F4A261",
}

# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT DES DONNÉES — depuis Streamlit Secrets (base64)
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def charger_donnees():
    """
    Charge le fichier Excel depuis les Secrets Streamlit (clé DATA_B64).
    La donnée est encodée en base64 pour ne jamais être exposée directement.
    """
    try:
        b64 = st.secrets["DATA_B64"]
        raw = base64.b64decode(b64)
        fichier = io.BytesIO(raw)
    except (KeyError, Exception) as e:
        st.error(
            "❌ Données introuvables. "
            "Vérifiez que la clé `DATA_B64` est bien définie dans les Secrets Streamlit."
        )
        st.stop()

    xls = pd.ExcelFile(fichier)
    feuilles = xls.sheet_names
    df = None
    macro = None

    # Feuille principale
    for nom in ["PowerBI_Data", "D. Publiques"]:
        if nom in feuilles:
            if nom == "PowerBI_Data":
                df = pd.read_excel(fichier, sheet_name=nom, header=1)
                df = df.dropna(subset=["Secteur", "Année"])
            break

    # Fallback : construire depuis les feuilles source
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
                tmp["Secteur"] = secteur
                frames.append(tmp)
        if frames:
            df = pd.concat(frames, ignore_index=True)

    # Données macro
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
        delta_html = f'<div class="kpi-delta {cls}">{signe} {abs(delta):.1f}% vs première année</div>'
    return f"""
    <div class="kpi-card {couleur}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """


# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT
# ─────────────────────────────────────────────────────────────────────────────
df_brut, macro_brut, feuilles_dispo = charger_donnees()

if df_brut is None:
    st.error("❌ Impossible de lire les données. Vérifiez que votre fichier contient la feuille 'PowerBI_Data'.")
    st.stop()

df = df_brut.copy()

# ─────────────────────────────────────────────────────────────────────────────
# NORMALISATION DES COLONNES
# ─────────────────────────────────────────────────────────────────────────────
col_map = {}
for c in df.columns:
    cl = str(c).lower().strip()
    if "secteur" in cl:                             col_map[c] = "Secteur"
    elif "institution" in cl:                       col_map[c] = "Institution"
    elif "programme" in cl:                         col_map[c] = "Programme"
    elif "catégorie" in cl or "categorie" in cl:    col_map[c] = "Catégorie BIOFIN"
    elif "coefficient" in cl:                       col_map[c] = "Coefficient"
    elif "année" in cl or "annee" in cl:            col_map[c] = "Année"
    elif "totale" in cl:                            col_map[c] = "Dép. Totale"
    elif "bd" in cl or "biodiv" in cl:              col_map[c] = "Dép. BD"
df = df.rename(columns=col_map)

# Vérification colonnes obligatoires
colonnes_req = ["Secteur", "Catégorie BIOFIN", "Année", "Dép. BD"]
cols_manquantes = [c for c in colonnes_req if c not in df.columns]
if cols_manquantes:
    st.error(f"Colonnes manquantes : {', '.join(cols_manquantes)}. Vérifiez la structure du fichier.")
    st.stop()

# Nettoyage types
df["Année"] = pd.to_numeric(df["Année"], errors="coerce").astype("Int64")
df["Dép. BD"] = pd.to_numeric(df["Dép. BD"], errors="coerce")
if "Dép. Totale" in df.columns:
    df["Dép. Totale"] = pd.to_numeric(df["Dép. Totale"], errors="coerce")
if "Coefficient" in df.columns:
    df["Coefficient"] = pd.to_numeric(df["Coefficient"], errors="coerce")
df = df.dropna(subset=["Année", "Dép. BD"])

# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — FILTRES
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 ADB Biodiversité")
    st.markdown("**Analyse des Dépenses pour la Biodiversité**")
    st.markdown("---")
    st.markdown("### 🎛️ Filtres")

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
    unite_label = "Mds FCFA" if unite == "Milliards FCFA" else "MFCFA"

    st.markdown("---")
    st.info("🔬 **Mode démonstration**\nDonnées fictives simulées pour le Cameroun")

# ─────────────────────────────────────────────────────────────────────────────
# APPLICATION DES FILTRES — CORRIGÉ
# ─────────────────────────────────────────────────────────────────────────────
# Gestion des filtres vides : si aucune sélection, afficher avertissement
if not annees_sel or not secteurs_sel or not cats_sel:
    st.warning("⚠️ Veuillez sélectionner au moins une valeur dans chaque filtre (Années, Secteurs, Catégories).")
    st.stop()

# Filtrage principal
mask = (
    df["Année"].isin(annees_sel) &
    df["Secteur"].isin(secteurs_sel) &
    df["Catégorie BIOFIN"].isin(cats_sel)
)
dff = df[mask].copy()

# Filtre institutions — CORRIGÉ : liste vide = aucune institution = résultat vide
if inst_sel is not None:
    if len(inst_sel) == 0:
        st.warning("⚠️ Aucune institution sélectionnée. Veuillez en choisir au moins une.")
        st.stop()
    if "Institution" in dff.columns:
        dff = dff[dff["Institution"].isin(inst_sel)]

if dff.empty:
    st.warning("⚠️ Aucune donnée pour les filtres sélectionnés. Essayez d'élargir votre sélection.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# HERO HEADER
# ─────────────────────────────────────────────────────────────────────────────
an_min = min(annees_sel)
an_max = max(annees_sel)

st.markdown(f"""
<div class="hero-header">
    <p class="hero-title">Analyse des Dépenses<br>Biodiversité — Cameroun</p>
    <p class="hero-sub">Initiative BIOFIN · Tableau de bord interactif · {an_min}–{an_max}</p>
    <span class="hero-badge">🔬 Données de démonstration</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────────────────────────────────
total_bd = dff["Dép. BD"].sum() / diviseur
nb_institutions = dff["Institution"].nunique() if "Institution" in dff.columns else len(secteurs_sel)

cat_top = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().idxmax()
cat_top_court = cat_top.split(". ")[-1]
cat_top_court = cat_top_court[:25] + "…" if len(cat_top_court) > 25 else cat_top_court

secteur_top = dff.groupby("Secteur")["Dép. BD"].sum().idxmax()

# Tendance entre première et dernière année
delta_pct = None
if len(annees_sel) >= 2:
    v_min = dff[dff["Année"] == an_min]["Dép. BD"].sum() / diviseur
    v_max = dff[dff["Année"] == an_max]["Dép. BD"].sum() / diviseur
    if v_min > 0:
        delta_pct = (v_max - v_min) / v_min * 100

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(kpi_card(f"Total Dépenses BD ({unite_label})", f"{total_bd:,.1f}", delta_pct), unsafe_allow_html=True)
with c2:
    st.markdown(kpi_card("Secteur dominant", secteur_top, couleur="blue"), unsafe_allow_html=True)
with c3:
    st.markdown(kpi_card("Catégorie BIOFIN #1", cat_top_court, couleur="orange"), unsafe_allow_html=True)
with c4:
    lbl = "Institutions" if "Institution" in dff.columns else "Secteurs actifs"
    st.markdown(kpi_card(lbl, str(nb_institutions), couleur="purple"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ONGLETS PRINCIPAUX
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Catégories BIOFIN",
    "📈 Évolution temporelle",
    "🏛️ Par secteur",
    "🔍 Analyse détaillée",
    "📋 Données brutes",
])

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 — CATÉGORIES BIOFIN
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">🌱 Dépenses BD par catégorie BIOFIN</div>', unsafe_allow_html=True)

    cat_df = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
    cat_df["Dép. BD"] = cat_df["Dép. BD"] / diviseur
    cat_df = cat_df.sort_values("Dép. BD", ascending=True)
    cat_df["Part (%)"] = (cat_df["Dép. BD"] / cat_df["Dép. BD"].sum() * 100).round(1)
    cat_df["Cat. courte"] = cat_df["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)

    col_left, col_right = st.columns([3, 2])

    with col_left:
        fig_bar = px.bar(
            cat_df, x="Dép. BD", y="Cat. courte", orientation="h",
            color="Dép. BD",
            color_continuous_scale=["#d8f3dc", "#52B788", "#1B4332"],
            text=cat_df["Dép. BD"].apply(lambda x: f"{x:,.0f}"),
            labels={"Dép. BD": f"Dépenses BD ({unite_label})", "Cat. courte": ""},
            title=f"Dépenses BD par catégorie ({unite_label})"
        )
        fig_bar.update_traces(textposition="outside", textfont_size=11, marker_line_width=0)
        fig_bar.update_layout(
            height=420, coloraxis_showscale=False, plot_bgcolor="white",
            paper_bgcolor="white", font_family="DM Sans", title_font_size=14,
            title_font_color="#1B4332", margin=dict(l=10, r=80, t=40, b=20),
            xaxis=dict(gridcolor="#f0f0f0", showline=False),
            yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        fig_pie = px.pie(
            cat_df, values="Dép. BD", names="Cat. courte",
            color_discrete_sequence=PALETTE_CATEGORIES, hole=0.52,
            title="Répartition en % du total"
        )
        fig_pie.update_traces(
            textposition="outside", textinfo="percent", textfont_size=11,
            pull=[0.03] * len(cat_df),
        )
        fig_pie.update_layout(
            height=420, font_family="DM Sans", title_font_size=14,
            title_font_color="#1B4332", paper_bgcolor="white",
            showlegend=True, legend=dict(font_size=10, x=1.05),
            margin=dict(l=0, r=120, t=40, b=20),
        )
        fig_pie.add_annotation(
            text=f"<b>{total_bd:,.0f}</b><br>{unite_label}",
            x=0.5, y=0.5, font_size=13, font_color="#1B4332",
            showarrow=False, font_family="DM Sans",
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # Heatmap catégories × années
    if len(annees_sel) > 1:
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
            colorscale=[[0, "#e8f5e9"], [0.5, "#52B788"], [1, "#1B4332"]],
            text=np.round(pivot.values, 1),
            texttemplate="%{text}",
            textfont={"size": 11, "color": "white"},
            hoverongaps=False,
            colorbar=dict(title=unite_label),
        ))
        fig_heat.update_layout(
            height=360, font_family="DM Sans", paper_bgcolor="white",
            plot_bgcolor="white", margin=dict(l=10, r=20, t=20, b=20),
            xaxis=dict(side="top"),
        )
        st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 — ÉVOLUTION TEMPORELLE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    if len(annees_sel) < 2:
        st.info("📅 Sélectionnez au moins 2 années pour afficher l'évolution temporelle.")
    else:
        st.markdown('<div class="section-title">📈 Évolution des dépenses BD dans le temps</div>', unsafe_allow_html=True)

        evol_total = dff.groupby("Année")["Dép. BD"].sum().reset_index()
        evol_total["Dép. BD"] = evol_total["Dép. BD"] / diviseur
        evol_total["Année"] = evol_total["Année"].astype(str)

        col_a, col_b = st.columns(2)

        with col_a:
            fig_line = go.Figure()
            fig_line.add_trace(go.Scatter(
                x=evol_total["Année"], y=evol_total["Dép. BD"],
                mode="lines+markers+text",
                line=dict(color="#2D6A4F", width=3),
                marker=dict(size=10, color="#2D6A4F", symbol="circle",
                            line=dict(color="white", width=2)),
                fill="tozeroy", fillcolor="rgba(82,183,136,0.15)",
                text=evol_total["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
                textposition="top center",
                textfont=dict(size=11, color="#1B4332"),
                name="Total BD"
            ))
            fig_line.update_layout(
                title=f"Évolution totale dépenses BD ({unite_label})",
                height=340, font_family="DM Sans", plot_bgcolor="white",
                paper_bgcolor="white", title_font_size=14, title_font_color="#1B4332",
                xaxis=dict(gridcolor="#f5f5f5", showline=True, linecolor="#e0e0e0"),
                yaxis=dict(gridcolor="#f5f5f5", title=unite_label),
                margin=dict(l=20, r=20, t=40, b=20), showlegend=False,
            )
            st.plotly_chart(fig_line, use_container_width=True)

        with col_b:
            evol_num = dff.groupby("Année")["Dép. BD"].sum().reset_index()
            evol_num["Croissance (%)"] = evol_num["Dép. BD"].pct_change() * 100
            evol_num = evol_num.dropna()
            evol_num["Année"] = evol_num["Année"].astype(str)

            couleurs_croiss = ["#2D6A4F" if v >= 0 else "#E76F51" for v in evol_num["Croissance (%)"]]
            fig_growth = go.Figure(go.Bar(
                x=evol_num["Année"], y=evol_num["Croissance (%)"],
                marker_color=couleurs_croiss,
                text=evol_num["Croissance (%)"].apply(lambda x: f"{x:.1f}%"),
                textposition="outside", textfont=dict(size=11),
            ))
            fig_growth.update_layout(
                title="Taux de croissance annuel (%)",
                height=340, font_family="DM Sans", plot_bgcolor="white",
                paper_bgcolor="white", title_font_size=14, title_font_color="#1B4332",
                xaxis=dict(gridcolor="#f5f5f5"),
                yaxis=dict(gridcolor="#f5f5f5", title="%", zeroline=True, zerolinecolor="#ccc"),
                margin=dict(l=20, r=20, t=40, b=20), showlegend=False,
            )
            st.plotly_chart(fig_growth, use_container_width=True)

        # Évolution par catégorie
        st.markdown('<div class="section-title">📊 Évolution par catégorie BIOFIN</div>', unsafe_allow_html=True)
        evol_cat = dff.groupby(["Année", "Catégorie BIOFIN"])["Dép. BD"].sum().reset_index()
        evol_cat["Dép. BD"] = evol_cat["Dép. BD"] / diviseur
        evol_cat["Cat. courte"] = evol_cat["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)
        evol_cat["Année"] = evol_cat["Année"].astype(str)

        fig_area = px.area(
            evol_cat, x="Année", y="Dép. BD", color="Cat. courte",
            color_discrete_sequence=PALETTE_CATEGORIES,
            labels={"Dép. BD": f"Dépenses BD ({unite_label})", "Cat. courte": "Catégorie"},
            title=f"Évolution empilée par catégorie BIOFIN ({unite_label})"
        )
        fig_area.update_layout(
            height=380, font_family="DM Sans", plot_bgcolor="white",
            paper_bgcolor="white", title_font_size=14, title_font_color="#1B4332",
            xaxis=dict(gridcolor="#f5f5f5"), yaxis=dict(gridcolor="#f5f5f5"),
            margin=dict(l=20, r=20, t=40, b=20), legend=dict(font_size=10),
        )
        st.plotly_chart(fig_area, use_container_width=True)

        # Évolution par secteur
        evol_sect = dff.groupby(["Année", "Secteur"])["Dép. BD"].sum().reset_index()
        evol_sect["Dép. BD"] = evol_sect["Dép. BD"] / diviseur
        evol_sect["Année"] = evol_sect["Année"].astype(str)

        fig_line_sect = px.line(
            evol_sect, x="Année", y="Dép. BD", color="Secteur",
            color_discrete_map=PALETTE_SECTEURS, markers=True,
            labels={"Dép. BD": f"Dépenses BD ({unite_label})"},
            title=f"Évolution par secteur ({unite_label})"
        )
        fig_line_sect.update_traces(line_width=2.5, marker_size=8)
        fig_line_sect.update_layout(
            height=340, font_family="DM Sans", plot_bgcolor="white",
            paper_bgcolor="white", title_font_size=14, title_font_color="#1B4332",
            xaxis=dict(gridcolor="#f5f5f5"), yaxis=dict(gridcolor="#f5f5f5"),
            margin=dict(l=20, r=20, t=40, b=20), legend=dict(font_size=11),
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
        fig_sect_bar.update_traces(textposition="outside", textfont_size=12, marker_line_width=0)
        fig_sect_bar.update_layout(
            height=380, showlegend=False, font_family="DM Sans",
            plot_bgcolor="white", paper_bgcolor="white",
            title_font_size=14, title_font_color="#1B4332",
            xaxis=dict(gridcolor="rgba(0,0,0,0)"), yaxis=dict(gridcolor="#f5f5f5"),
            margin=dict(l=20, r=20, t=40, b=20),
        )
        st.plotly_chart(fig_sect_bar, use_container_width=True)

    with col2:
        fig_sect_pie = px.pie(
            sect_df, values="Dép. BD", names="Secteur",
            color="Secteur", color_discrete_map=PALETTE_SECTEURS,
            hole=0.5, title="Part de chaque secteur (%)"
        )
        fig_sect_pie.update_traces(
            textposition="outside", textinfo="label+percent",
            textfont_size=11, pull=[0.04] * len(sect_df),
        )
        fig_sect_pie.update_layout(
            height=380, font_family="DM Sans", paper_bgcolor="white",
            showlegend=False, title_font_size=14, title_font_color="#1B4332",
            margin=dict(l=0, r=0, t=40, b=20),
        )
        st.plotly_chart(fig_sect_pie, use_container_width=True)

    # Sunburst
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
    fig_sun.update_layout(
        height=500, font_family="DM Sans", paper_bgcolor="white",
        title_font_size=14, title_font_color="#1B4332",
        margin=dict(l=20, r=20, t=40, b=20),
    )
    st.plotly_chart(fig_sun, use_container_width=True)

    # Top institutions
    if "Institution" in dff.columns:
        st.markdown('<div class="section-title">🏆 Top 10 Institutions</div>', unsafe_allow_html=True)
        inst_df = dff.groupby(["Institution", "Secteur"])["Dép. BD"].sum().reset_index()
        inst_df["Dép. BD"] = inst_df["Dép. BD"] / diviseur
        inst_df = inst_df.sort_values("Dép. BD", ascending=False).head(10)
        inst_df = inst_df.sort_values("Dép. BD", ascending=True)

        fig_inst = px.bar(
            inst_df, x="Dép. BD", y="Institution", color="Secteur",
            color_discrete_map=PALETTE_SECTEURS, orientation="h",
            text=inst_df["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
            labels={"Dép. BD": f"Dépenses BD ({unite_label})"},
            title=f"Top 10 acteurs — Dépenses BD cumulées ({unite_label})"
        )
        fig_inst.update_traces(textposition="outside", textfont_size=11)
        fig_inst.update_layout(
            height=400, font_family="DM Sans", plot_bgcolor="white",
            paper_bgcolor="white", title_font_size=14, title_font_color="#1B4332",
            legend=dict(font_size=11), margin=dict(l=20, r=80, t=40, b=20),
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
            grp_col = "Institution" if "Institution" in dff.columns else "Secteur"
            scatter_df = dff.groupby([grp_col, "Secteur"]).agg(
                {"Dép. Totale": "sum", "Dép. BD": "sum"}
            ).reset_index()
            scatter_df.columns = ["Nom", "Secteur", "Dép. Totale", "Dép. BD"]
            scatter_df["Dép. Totale"] = scatter_df["Dép. Totale"] / diviseur
            scatter_df["Dép. BD"] = scatter_df["Dép. BD"] / diviseur
            scatter_df["Coeff moyen (%)"] = (
                scatter_df["Dép. BD"] / scatter_df["Dép. Totale"].replace(0, np.nan) * 100
            ).round(1)

            fig_scatter = px.scatter(
                scatter_df, x="Dép. Totale", y="Dép. BD",
                color="Secteur", color_discrete_map=PALETTE_SECTEURS,
                size="Dép. BD", size_max=35, hover_name="Nom",
                hover_data={"Coeff moyen (%)": True},
                labels={
                    "Dép. Totale": f"Dépense Totale ({unite_label})",
                    "Dép. BD": f"Dépense BD ({unite_label})",
                },
                title="Dépense Totale vs Dépense BD par acteur"
            )
            max_val = max(scatter_df["Dép. Totale"].max(), scatter_df["Dép. BD"].max())
            fig_scatter.add_trace(go.Scatter(
                x=[0, max_val], y=[0, max_val], mode="lines",
                line=dict(dash="dash", color="#ccc", width=1),
                name="100% BD", showlegend=True
            ))
            fig_scatter.update_layout(
                height=380, font_family="DM Sans", plot_bgcolor="white",
                paper_bgcolor="white", title_font_size=13, title_font_color="#1B4332",
                legend=dict(font_size=10), margin=dict(l=20, r=20, t=40, b=20),
            )
            st.plotly_chart(fig_scatter, use_container_width=True)

    with col_d2:
        if "Coefficient" in dff.columns:
            coef_df = dff[["Secteur", "Coefficient"]].copy()
            coef_df["Coefficient (%)"] = (coef_df["Coefficient"] * 100).round(0)

            fig_box = px.box(
                coef_df, x="Secteur", y="Coefficient (%)", color="Secteur",
                color_discrete_map=PALETTE_SECTEURS, points="all",
                title="Distribution des coefficients d'attribution par secteur"
            )
            fig_box.update_layout(
                height=380, font_family="DM Sans", plot_bgcolor="white",
                paper_bgcolor="white", title_font_size=13, title_font_color="#1B4332",
                showlegend=False, margin=dict(l=20, r=20, t=40, b=20),
                yaxis=dict(range=[0, 110], title="Coefficient (%)"),
            )
            st.plotly_chart(fig_box, use_container_width=True)

    # Tableau croisé
    st.markdown('<div class="section-title">📊 Tableau croisé : Catégories × Secteurs</div>', unsafe_allow_html=True)
    pivot2 = dff.pivot_table(
        index="Catégorie BIOFIN", columns="Secteur",
        values="Dép. BD", aggfunc="sum", margins=True, margins_name="TOTAL"
    ) / diviseur
    pivot2.index = [
        i.replace(r"^\d+\.\s*", "", 1) if i != "TOTAL" else i
        for i in pivot2.index
    ]
    pivot2 = pivot2.round(1)

    val_max = pivot2.replace(0, float("nan")).stack().max()
    if pd.isna(val_max) or val_max == 0:
        val_max = 1

    def colorier_cellule(val):
        try:
            v = float(val)
            if v <= 0:
                return "background-color: #f9f9f9; color: #aaa"
            intensite = min(int(v / val_max * 180), 180)
            r = 255 - intensite
            couleur_texte = "#1B4332" if intensite > 80 else "#333"
            return f"background-color: rgb({r},255,{r}); color: {couleur_texte}; font-weight: 500"
        except (ValueError, TypeError):
            return ""

    # Compatible pandas 2.0+ et 2.1+
    try:
        styled = pivot2.style.map(colorier_cellule).format("{:,.1f}").set_properties(**{"font-size": "12px"})
    except AttributeError:
        styled = pivot2.style.applymap(colorier_cellule).format("{:,.1f}").set_properties(**{"font-size": "12px"})

    st.dataframe(styled, use_container_width=True, height=380)

    # Contexte macro
    if macro_brut is not None:
        st.markdown('<div class="section-title">🌍 Contexte macro-économique</div>', unsafe_allow_html=True)
        try:
            macro_df = macro_brut.copy()
            macro_df.columns = [str(c) for c in macro_df.columns]
            annee_cols = [c for c in macro_df.columns if c.isdigit() and int(c) in annees_dispo]

            if annee_cols:
                pib_row = macro_df[macro_df["Indicateur"].str.contains("PIB.*Milliards", na=False, case=False)]
                if not pib_row.empty:
                    pib_vals = pib_row[annee_cols].values.flatten()
                    pib_vals_f = [float(v) for v in pib_vals if pd.notna(v)]
                    bd_par_an = dff.groupby("Année")["Dép. BD"].sum()
                    bd_pib_data = []
                    for i, an in enumerate(annee_cols):
                        an_int = int(an)
                        if an_int in bd_par_an.index and i < len(pib_vals_f) and pib_vals_f[i] > 0:
                            pib_mfcfa = pib_vals_f[i] * 1000
                            bd_pib_data.append({
                                "Année": str(an_int),
                                "Part BD/PIB (%)": round(bd_par_an[an_int] / pib_mfcfa * 100, 4)
                            })

                    if bd_pib_data:
                        bd_pib_df = pd.DataFrame(bd_pib_data)
                        fig_macro = go.Figure()
                        fig_macro.add_trace(go.Bar(
                            x=bd_pib_df["Année"], y=bd_pib_df["Part BD/PIB (%)"],
                            marker_color="#52B788",
                            text=bd_pib_df["Part BD/PIB (%)"].apply(lambda x: f"{x:.3f}%"),
                            textposition="outside", name="Dép. BD / PIB"
                        ))
                        fig_macro.update_layout(
                            title="Part des dépenses BD dans le PIB (%)",
                            height=320, font_family="DM Sans", plot_bgcolor="white",
                            paper_bgcolor="white", title_font_size=13, title_font_color="#1B4332",
                            yaxis=dict(title="%", gridcolor="#f5f5f5"),
                            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                            margin=dict(l=20, r=20, t=40, b=20), showlegend=False,
                        )
                        st.plotly_chart(fig_macro, use_container_width=True)
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 5 — DONNÉES BRUTES (export filtré uniquement, pas la BDD brute)
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">📋 Données détaillées</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        search = st.text_input("🔎 Rechercher", placeholder="Ministère, programme...")
    with col_f2:
        cols_tri_dispo = [c for c in ["Dép. BD", "Année", "Secteur", "Catégorie BIOFIN"] if c in dff.columns]
        sort_col = st.selectbox("Trier par", cols_tri_dispo)
    with col_f3:
        ordre = st.radio("Ordre", ["Décroissant", "Croissant"], horizontal=True)

    table_df = dff.copy()
    if "Dép. Totale" in table_df.columns:
        table_df["Dép. Totale"] = (table_df["Dép. Totale"] / diviseur).round(2)
    table_df["Dép. BD"] = (table_df["Dép. BD"] / diviseur).round(2)

    # Recherche texte
    if search:
        mask_search = table_df.apply(
            lambda row: any(search.lower() in str(v).lower() for v in row), axis=1
        )
        table_df = table_df[mask_search]

    # Tri
    asc = ordre == "Croissant"
    if sort_col in table_df.columns:
        table_df = table_df.sort_values(sort_col, ascending=asc)

    st.markdown(f"**{len(table_df):,} lignes** | Unité : {unite_label}")
    st.dataframe(table_df, use_container_width=True, height=450)

    # Export des données filtrées uniquement (pas la BDD source)
    st.markdown("---")
    st.markdown("**📥 Exporter la sélection filtrée**")
    col_e1, col_e2 = st.columns(2)

    with col_e1:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            table_df.to_excel(writer, index=False, sheet_name="Données filtrées")
            synth = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
            synth["Dép. BD"] = (synth["Dép. BD"] / diviseur).round(2)
            synth.to_excel(writer, index=False, sheet_name="Synthèse BIOFIN")
        st.download_button(
            label="⬇️ Exporter en Excel (.xlsx)",
            data=buffer.getvalue(),
            file_name="ADB_Export_filtre.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )

    with col_e2:
        csv = table_df.to_csv(index=False).encode("utf-8")
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
    🌿 ADB Biodiversité Cameroun · Initiative BIOFIN · PNUD
    &nbsp;|&nbsp; Données : 2020–2024 &nbsp;|&nbsp; Unité : Millions FCFA
</div>
""", unsafe_allow_html=True)
