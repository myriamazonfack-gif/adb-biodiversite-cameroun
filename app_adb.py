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
    initial_sidebar_state="collapsed",
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Libre+Baskerville:wght@400;700&family=Source+Sans+3:wght@300;400;500;600;700&display=swap');

html, body, [class*="css"] { font-family: 'Source Sans 3', sans-serif; }
.main { background: #F7F5F0; }
.block-container { padding: 1.2rem 1.5rem 2rem 1.5rem; max-width: 1600px; }

/* HERO */
.hero {
    background: linear-gradient(120deg, #1C3A2B 0%, #2E6B47 55%, #4CAF76 100%);
    border-radius: 12px;
    padding: 1.6rem 2rem;
    margin-bottom: 1.2rem;
    position: relative;
    overflow: hidden;
    border-left: 6px solid #6FCF97;
}
.hero::after {
    content: "🌿";
    position: absolute; right: 2rem; top: 50%;
    transform: translateY(-50%);
    font-size: 5rem; opacity: 0.08;
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

/* FILTRE BAR */
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

/* KPI CARDS */
.kpi-card {
    background: #FFFFFF;
    border-radius: 10px;
    padding: 1.1rem 1.3rem;
    border-top: 4px solid #2E6B47;
    box-shadow: 0 2px 8px rgba(28,58,43,0.07);
    height: 100%;
}
.kpi-card.orange { border-top-color: #E07B39; }
.kpi-card.blue   { border-top-color: #2B6CB0; }
.kpi-card.purple { border-top-color: #6B46C1; }
.kpi-card.red    { border-top-color: #C53030; }
.kpi-label {
    font-size: 0.68rem; color: #718096;
    font-weight: 700; letter-spacing: 0.1em;
    text-transform: uppercase; margin-bottom: 0.4rem;
}
.kpi-value {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.6rem; font-weight: 700;
    color: #1C3A2B; line-height: 1.1; word-break: break-word;
}
.kpi-sub { font-size: 0.78rem; color: #718096; margin-top: 0.2rem; }
.kpi-delta { font-size: 0.78rem; font-weight: 600; margin-top: 0.2rem; }
.kpi-delta.pos { color: #2E6B47; }
.kpi-delta.neg { color: #C53030; }

/* SECTION TITLES */
.section-title {
    font-family: 'Libre Baskerville', serif;
    font-size: 1.1rem; font-weight: 700;
    color: #1C3A2B;
    margin: 1.4rem 0 0.7rem 0;
    padding-bottom: 0.4rem;
    border-bottom: 2px solid #C8E6C9;
}

/* TABS */
.stTabs [data-baseweb="tab-list"] {
    gap: 0.2rem; background: #E8F5E9;
    padding: 0.3rem; border-radius: 8px;
}
.stTabs [data-baseweb="tab"] {
    border-radius: 6px; padding: 0.35rem 0.9rem;
    font-weight: 600; color: #2E6B47; font-size: 0.83rem;
}
.stTabs [aria-selected="true"] {
    background: #1C3A2B !important; color: white !important;
}

/* INSIGHT BOXES */
.insight {
    background: #E8F5E9; border-left: 4px solid #2E6B47;
    border-radius: 6px; padding: 0.7rem 1rem;
    margin: 0.5rem 0; font-size: 0.88rem; color: #1C3A2B;
}
.insight.warning {
    background: #FFF3E0; border-left-color: #E07B39; color: #7B3F00;
}

/* HIDE BRANDING */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}
[data-testid="stSidebar"] {display: none;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTES
# ─────────────────────────────────────────────────────────────────────────────
PALETTE_CAT = ["#1C3A2B","#2E6B47","#3D8B5E","#4CAF76","#6FCF97","#95E0B4","#E07B39","#C53030","#2B6CB0"]
PALETTE_SECT = {"Public":"#2E6B47","ONG / OSC":"#2B6CB0","Secteur Privé":"#6B46C1","PTF":"#E07B39"}
LAYOUT = dict(
    font_family="Source Sans 3", font_size=13,
    plot_bgcolor="white", paper_bgcolor="white",
    title_font_size=14, title_font_color="#1C3A2B",
    title_font_family="Libre Baskerville",
    margin=dict(l=15, r=15, t=45, b=15),
)

# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data
def charger_donnees(fichier):
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

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <p class="hero-title">Analyse des Dépenses Biodiversité — Cameroun</p>
    <p class="hero-sub">Initiative BIOFIN / PNUD · Tableau de bord interactif</p>
    <span class="hero-badge">ADB · 2020–2024</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT FICHIER
# ─────────────────────────────────────────────────────────────────────────────
col_up, _ = st.columns([2, 5])
with col_up:
    fichier_charge = st.file_uploader("📂 Charger votre fichier Excel (optionnel)", type=["xlsx","xls"])

try:
    source = fichier_charge if fichier_charge else "ADB_Cameroun_Simulation.xlsx"
    df_brut, macro_brut = charger_donnees(source)
    mode_demo = fichier_charge is None
except Exception as e:
    st.error(f"Erreur de chargement : {e}")
    st.stop()

if df_brut is None:
    st.error("❌ Feuille 'PowerBI_Data' introuvable.")
    st.stop()

df = df_brut.copy()
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
df["Année"] = pd.to_numeric(df["Année"], errors="coerce").astype("Int64")
df["Dép. BD"] = pd.to_numeric(df["Dép. BD"], errors="coerce")
if "Dép. Totale" in df.columns:
    df["Dép. Totale"] = pd.to_numeric(df["Dép. Totale"], errors="coerce")
if "Coefficient" in df.columns:
    df["Coefficient"] = pd.to_numeric(df["Coefficient"], errors="coerce")
df = df.dropna(subset=["Année", "Dép. BD"])

# ─────────────────────────────────────────────────────────────────────────────
# FILTRES — VISIBLES SUR LA PAGE
# ─────────────────────────────────────────────────────────────────────────────
annees_dispo = sorted(df["Année"].dropna().unique().tolist())
secteurs_dispo = sorted(df["Secteur"].dropna().unique().tolist())
cats_dispo = sorted(df["Catégorie BIOFIN"].dropna().unique().tolist())
insts_dispo = sorted(df["Institution"].dropna().unique().tolist()) if "Institution" in df.columns else []

with st.expander("🎛️ Filtres — Cliquez pour ouvrir / fermer", expanded=True):
    f1, f2, f3 = st.columns(3)
    with f1:
        annees_sel = st.multiselect("📅 Années", annees_dispo, default=annees_dispo, key="annees")
        unite = st.radio("💰 Unité", ["Millions FCFA", "Milliards FCFA"], index=0, key="unite")
    with f2:
        secteurs_sel = st.multiselect("🏛️ Secteurs", secteurs_dispo, default=secteurs_dispo, key="secteurs")
        insts_sel = st.multiselect("🏢 Institutions (optionnel)", insts_dispo, default=[], key="insts",
                                    help="Laissez vide pour tout afficher")
    with f3:
        cats_sel = st.multiselect("🌱 Catégories BIOFIN", cats_dispo, default=cats_dispo, key="cats")


diviseur = 1000 if unite == "Milliards FCFA" else 1
unite_label = "Mds FCFA" if unite == "Milliards FCFA" else "M FCFA"

# Valeurs par défaut si rien sélectionné
if not annees_sel: annees_sel = annees_dispo
if not secteurs_sel: secteurs_sel = secteurs_dispo
if not cats_sel: cats_sel = cats_dispo
if not insts_sel: insts_sel = insts_dispo

# Filtrage
dff = df[
    df["Année"].isin(annees_sel) &
    df["Secteur"].isin(secteurs_sel) &
    df["Catégorie BIOFIN"].isin(cats_sel)
].copy()
if insts_sel and "Institution" in dff.columns:
    dff = dff[dff["Institution"].isin(insts_sel)]

if dff.empty:
    st.warning("⚠️ Aucune donnée pour les filtres sélectionnés. Élargissez vos critères.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# CALCULS GLOBAUX
# ─────────────────────────────────────────────────────────────────────────────
total_bd = dff["Dép. BD"].sum() / diviseur
total_tot = dff["Dép. Totale"].sum() / diviseur if "Dép. Totale" in dff.columns else None
nb_institutions = dff["Institution"].nunique() if "Institution" in dff.columns else 0
nb_programmes = dff["Programme"].nunique() if "Programme" in dff.columns else 0
cat_top = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().idxmax()
cat_top_nom = cat_top.split(". ", 1)[-1] if ". " in cat_top else cat_top
secteur_top = dff.groupby("Secteur")["Dép. BD"].sum().idxmax()
part_top = dff.groupby("Secteur")["Dép. BD"].sum().max() / dff["Dép. BD"].sum() * 100

# Tendance
an_min, an_max = min(annees_sel), max(annees_sel)
v_min = dff[dff["Année"] == an_min]["Dép. BD"].sum() / diviseur
v_max = dff[dff["Année"] == an_max]["Dép. BD"].sum() / diviseur
delta_pct = ((v_max - v_min) / v_min * 100) if v_min > 0 and len(annees_sel) >= 2 else None
taux_moyen = ((v_max / v_min) ** (1 / (len(annees_sel) - 1)) - 1) * 100 if v_min > 0 and len(annees_sel) >= 2 else None

# Part BD / Total
part_bd = (dff["Dép. BD"].sum() / dff["Dép. Totale"].sum() * 100) if total_tot and total_tot > 0 else None

# ─────────────────────────────────────────────────────────────────────────────
# KPIs PRINCIPAUX
# ─────────────────────────────────────────────────────────────────────────────
def kpi(label, val, sub="", delta=None, couleur=""):
    d_html = ""
    if delta is not None:
        cls = "pos" if delta >= 0 else "neg"
        signe = "▲" if delta >= 0 else "▼"
        d_html = f'<div class="kpi-delta {cls}">{signe} {abs(delta):.1f}%</div>'
    s_html = f'<div class="kpi-sub">{sub}</div>' if sub else ""
    return f"""<div class="kpi-card {couleur}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{val}</div>
        {s_html}{d_html}
    </div>"""

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    st.markdown(kpi(
        f"Total Dépenses BD ({unite_label})",
        f"{total_bd:,.1f}",
        f"sur {an_min}–{an_max}",
        delta_pct
    ), unsafe_allow_html=True)
with c2:
    st.markdown(kpi(
        "Secteur dominant",
        secteur_top,
        f"{part_top:.0f}% du total",
        couleur="blue"
    ), unsafe_allow_html=True)
with c3:
    st.markdown(kpi(
        "Catégorie prioritaire",
        cat_top_nom,
        "Plus grande dépense BD",
        couleur="orange"
    ), unsafe_allow_html=True)
with c4:
    st.markdown(kpi(
        "Institutions actives",
        str(nb_institutions),
        f"{nb_programmes} programmes",
        couleur="purple"
    ), unsafe_allow_html=True)
with c5:
    if part_bd:
        st.markdown(kpi(
            "Taux d'attribution BD",
            f"{part_bd:.1f}%",
            "Dép. BD / Dép. Totale",
            couleur="red" if part_bd < 70 else ""
        ), unsafe_allow_html=True)
    elif taux_moyen:
        st.markdown(kpi(
            "Croissance annuelle moy.",
            f"+{taux_moyen:.1f}%/an",
            "Taux moyen sur la période",
            couleur="red"
        ), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ONGLETS
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Vue d'ensemble",
    "📈 Tendances",
    "🏛️ Secteurs",
    "🌱 Catégories BIOFIN",
    "🔍 Analyse avancée",
    "📋 Données",
])

# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 1 — VUE D'ENSEMBLE
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">📊 Répartition globale des dépenses biodiversité</div>', unsafe_allow_html=True)

    col_a, col_b = st.columns(2)

    with col_a:
        # Dépenses par secteur — barres horizontales
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
        fig.update_traces(textposition="outside", textfont_size=12, marker_line_width=0)
        fig.update_layout(**LAYOUT, height=320, showlegend=False,
            xaxis=dict(title=unite_label, gridcolor="#F0F0F0"),
            yaxis=dict(title="", tickfont_size=13))
        st.plotly_chart(fig, use_container_width=True)

        st.markdown(f"""<div class="insight">
        💡 <b>Le secteur {secteur_top}</b> représente <b>{part_top:.0f}%</b> des dépenses biodiversité totales.
        Le secteur privé est le moins contributeur, ce qui suggère un potentiel de mobilisation important.
        </div>""", unsafe_allow_html=True)

    with col_b:
        # Camembert par catégorie
        cat_df = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
        cat_df["Dép. BD"] = cat_df["Dép. BD"] / diviseur
        cat_df["Cat. courte"] = cat_df["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)
        cat_df = cat_df.sort_values("Dép. BD", ascending=False)

        fig2 = px.pie(
            cat_df, values="Dép. BD", names="Cat. courte",
            color_discrete_sequence=PALETTE_CAT, hole=0.5,
            title="Répartition par catégorie BIOFIN"
        )
        fig2.update_traces(
            textposition="outside", textinfo="percent+label",
            textfont_size=11, pull=[0.03]*len(cat_df)
        )
        fig2.update_layout(**LAYOUT, height=320, showlegend=False)
        fig2.add_annotation(
            text=f"<b>{total_bd:,.0f}</b><br>{unite_label}",
            x=0.5, y=0.5, font_size=13, font_color="#1C3A2B", showarrow=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Tableau récapitulatif simple
    st.markdown('<div class="section-title">📋 Résumé par secteur et catégorie</div>', unsafe_allow_html=True)

    pivot_resume = dff.pivot_table(
        index="Secteur", columns="Catégorie BIOFIN",
        values="Dép. BD", aggfunc="sum", margins=True, margins_name="TOTAL"
    ) / diviseur
    pivot_resume.columns = [c.split(". ", 1)[-1] if ". " in str(c) else str(c) for c in pivot_resume.columns]
    pivot_resume = pivot_resume.round(1)

    def colorier(val):
        try:
            v = float(val)
            if v <= 0:
                return "background-color: #f9f9f9; color: #aaa"
            intensite = min(int(v / pivot_resume.values.max() * 200), 200)
            r = 255 - intensite
            g = 255
            b = 255 - intensite
            couleur_texte = "#1C3A2B" if intensite > 100 else "#333"
            return f"background-color: rgb({r},{g},{b}); color: {couleur_texte}; font-weight: 600"
        except:
            return ""
    st.dataframe(
        pivot_resume.style.applymap(colorier).format("{:,.1f}").set_properties(**{"font-size": "12px"}),
        use_container_width=True, height=220
    )

    # KPI macro si disponible
    if macro_brut is not None:
        st.markdown('<div class="section-title">🌍 Contexte économique du Cameroun</div>', unsafe_allow_html=True)
        macro = macro_brut.copy()
        macro.columns = [str(c) for c in macro.columns]

        m1, m2, m3, m4 = st.columns(4)
        annee_str = str(max(annees_sel))
        try:
            pib_row = macro[macro["Indicateur"].str.contains("PIB.*Milliards", na=False, case=False)]
            croiss_row = macro[macro["Indicateur"].str.contains("Croissance", na=False, case=False)]
            budget_row = macro[macro["Indicateur"].str.contains("Budget", na=False, case=False)]
            infla_row = macro[macro["Indicateur"].str.contains("inflation", na=False, case=False)]

            if annee_str in macro.columns:
                with m1:
                    pib_val = float(pib_row[annee_str].values[0]) if not pib_row.empty else None
                    if pib_val:
                        st.markdown(kpi("PIB Cameroun", f"{pib_val:,.0f} Mds", "FCFA en "+annee_str, couleur="blue"), unsafe_allow_html=True)
                with m2:
                    cr_val = float(croiss_row[annee_str].values[0]) if not croiss_row.empty else None
                    if cr_val:
                        st.markdown(kpi("Croissance PIB", f"{cr_val:.1f}%", annee_str, delta=cr_val, couleur=""), unsafe_allow_html=True)
                with m3:
                    bud_val = float(budget_row[annee_str].values[0]) if not budget_row.empty else None
                    if bud_val:
                        st.markdown(kpi("Budget de l'État", f"{bud_val:,.0f} Mds", "FCFA en "+annee_str, couleur="orange"), unsafe_allow_html=True)
                with m4:
                    inf_val = float(infla_row[annee_str].values[0]) if not infla_row.empty else None
                    if inf_val:
                        st.markdown(kpi("Inflation", f"{inf_val:.1f}%", annee_str, couleur="red" if inf_val > 5 else ""), unsafe_allow_html=True)
        except Exception:
            pass


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 2 — TENDANCES
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📈 Comment les dépenses évoluent-elles chaque année ?</div>', unsafe_allow_html=True)

    evol = dff.groupby("Année")["Dép. BD"].sum().reset_index()
    evol["Dép. BD"] = evol["Dép. BD"] / diviseur
    evol["Croissance (%)"] = evol["Dép. BD"].pct_change() * 100
    evol["Année_str"] = evol["Année"].astype(str)

    col1, col2 = st.columns(2)
    with col1:
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=evol["Année_str"], y=evol["Dép. BD"],
            mode="lines+markers+text",
            line=dict(color="#2E6B47", width=3),
            marker=dict(size=11, color="#2E6B47", line=dict(color="white", width=2)),
            fill="tozeroy", fillcolor="rgba(76,175,118,0.1)",
            text=evol["Dép. BD"].apply(lambda x: f"{x:,.1f}"),
            textposition="top center", textfont=dict(size=12, color="#1C3A2B"),
        ))
        fig.update_layout(**LAYOUT, title=f"Évolution totale ({unite_label})", height=340,
            xaxis=dict(gridcolor="#F5F5F5", tickfont_size=13),
            yaxis=dict(gridcolor="#F5F5F5", title=unite_label, tickfont_size=12),
            showlegend=False)
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        evol_c = evol.dropna(subset=["Croissance (%)"])
        couleurs = ["#2E6B47" if v >= 0 else "#C53030" for v in evol_c["Croissance (%)"]]
        fig2 = go.Figure(go.Bar(
            x=evol_c["Année_str"], y=evol_c["Croissance (%)"],
            marker_color=couleurs,
            text=evol_c["Croissance (%)"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside", textfont_size=12,
        ))
        fig2.update_layout(**LAYOUT, title="Taux de croissance annuel (%)", height=340,
            xaxis=dict(gridcolor="#F5F5F5", tickfont_size=13),
            yaxis=dict(gridcolor="#F5F5F5", title="%", zeroline=True, zerolinecolor="#CCC"),
            showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    if taux_moyen:
        st.markdown(f"""<div class="insight">
        📈 Les dépenses biodiversité ont augmenté de <b>{delta_pct:.1f}%</b> entre {an_min} et {an_max},
        soit un taux de croissance annuel moyen de <b>+{taux_moyen:.1f}%/an</b>.
        Cette tendance reflète un engagement croissant du Cameroun pour la biodiversité.
        </div>""", unsafe_allow_html=True)

    st.markdown('<div class="section-title">📊 Évolution par secteur année par année</div>', unsafe_allow_html=True)

    evol_sect = dff.groupby(["Année", "Secteur"])["Dép. BD"].sum().reset_index()
    evol_sect["Dép. BD"] = evol_sect["Dép. BD"] / diviseur
    evol_sect["Année_str"] = evol_sect["Année"].astype(str)

    fig3 = px.line(
        evol_sect, x="Année_str", y="Dép. BD", color="Secteur",
        color_discrete_map=PALETTE_SECT, markers=True,
        labels={"Dép. BD": f"Dépenses BD ({unite_label})", "Année_str": "Année"},
        title=f"Dépenses BD par secteur ({unite_label})"
    )
    fig3.update_traces(line_width=2.5, marker_size=9)
    fig3.update_layout(**LAYOUT, height=360,
        xaxis=dict(gridcolor="#F5F5F5", tickfont_size=13),
        yaxis=dict(gridcolor="#F5F5F5", tickfont_size=12),
        legend=dict(font_size=12))
    st.plotly_chart(fig3, use_container_width=True)

    st.markdown('<div class="section-title">📊 Évolution cumulée par catégorie BIOFIN</div>', unsafe_allow_html=True)

    evol_cat = dff.groupby(["Année", "Catégorie BIOFIN"])["Dép. BD"].sum().reset_index()
    evol_cat["Dép. BD"] = evol_cat["Dép. BD"] / diviseur
    evol_cat["Cat. courte"] = evol_cat["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)
    evol_cat["Année_str"] = evol_cat["Année"].astype(str)

    fig4 = px.area(
        evol_cat, x="Année_str", y="Dép. BD", color="Cat. courte",
        color_discrete_sequence=PALETTE_CAT,
        labels={"Dép. BD": f"Dépenses BD ({unite_label})", "Cat. courte": "Catégorie", "Année_str": "Année"},
        title=f"Dépenses cumulées par catégorie ({unite_label})"
    )
    fig4.update_layout(**LAYOUT, height=380,
        xaxis=dict(gridcolor="#F5F5F5", tickfont_size=13),
        yaxis=dict(gridcolor="#F5F5F5", tickfont_size=12),
        legend=dict(font_size=11))
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 3 — SECTEURS
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🏛️ Qui finance la biodiversité au Cameroun ?</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        sect_df = dff.groupby("Secteur").agg(
            BD=("Dép. BD", "sum"),
            Totale=("Dép. Totale", "sum") if "Dép. Totale" in dff.columns else ("Dép. BD", "sum"),
        ).reset_index()
        sect_df["BD"] = sect_df["BD"] / diviseur
        sect_df["Totale"] = sect_df["Totale"] / diviseur
        sect_df["Part (%)"] = (sect_df["BD"] / sect_df["BD"].sum() * 100).round(1)
        sect_df = sect_df.sort_values("BD", ascending=False)

        fig = px.bar(
            sect_df, x="Secteur", y="BD", color="Secteur",
            color_discrete_map=PALETTE_SECT,
            text=sect_df.apply(lambda r: f"{r['BD']:,.1f}\n({r['Part (%)']:.0f}%)", axis=1),
            title=f"Dépenses BD par secteur ({unite_label})"
        )
        fig.update_traces(textposition="outside", textfont_size=12, marker_line_width=0)
        fig.update_layout(**LAYOUT, height=360, showlegend=False,
            xaxis=dict(tickfont_size=13),
            yaxis=dict(gridcolor="#F5F5F5", title=unite_label))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            sect_df, values="BD", names="Secteur",
            color="Secteur", color_discrete_map=PALETTE_SECT,
            hole=0.5, title="Part de chaque secteur"
        )
        fig2.update_traces(
            textposition="outside", textinfo="label+percent",
            textfont_size=12, pull=[0.04]*len(sect_df)
        )
        fig2.update_layout(**LAYOUT, height=360, showlegend=False)
        st.plotly_chart(fig2, use_container_width=True)

    # Taux d'attribution moyen par secteur
    if "Coefficient" in dff.columns:
        st.markdown('<div class="section-title">📐 Taux d\'attribution biodiversité par secteur</div>', unsafe_allow_html=True)
        st.markdown("""<div class="insight">
        ℹ️ <b>Le taux d'attribution</b> indique quelle part des dépenses totales est réellement consacrée à la biodiversité.
        Un taux de 100% signifie que toute la dépense bénéficie à la biodiversité.
        </div>""", unsafe_allow_html=True)

        coef_sect = dff.groupby("Secteur")["Coefficient"].mean().reset_index()
        coef_sect["Coefficient (%)"] = (coef_sect["Coefficient"] * 100).round(1)
        coef_sect = coef_sect.sort_values("Coefficient (%)", ascending=False)

        fig3 = px.bar(
            coef_sect, x="Secteur", y="Coefficient (%)",
            color="Secteur", color_discrete_map=PALETTE_SECT,
            text=coef_sect["Coefficient (%)"].apply(lambda x: f"{x:.0f}%"),
            title="Taux d'attribution moyen par secteur (%)"
        )
        fig3.update_traces(textposition="outside", textfont_size=13, marker_line_width=0)
        fig3.update_layout(**LAYOUT, height=320, showlegend=False,
            yaxis=dict(range=[0, 115], title="%", gridcolor="#F5F5F5"),
            xaxis=dict(tickfont_size=13))
        st.plotly_chart(fig3, use_container_width=True)

    # Top 10 institutions
    if "Institution" in dff.columns:
        st.markdown('<div class="section-title">🏆 Les 10 principaux acteurs</div>', unsafe_allow_html=True)

        inst_df = dff.groupby(["Institution", "Secteur"])["Dép. BD"].sum().reset_index()
        inst_df["Dép. BD"] = inst_df["Dép. BD"] / diviseur
        inst_df["Part (%)"] = (inst_df["Dép. BD"] / inst_df["Dép. BD"].sum() * 100).round(1)
        inst_df = inst_df.sort_values("Dép. BD", ascending=False).head(10)
        inst_df = inst_df.sort_values("Dép. BD", ascending=True)

        fig4 = px.bar(
            inst_df, x="Dép. BD", y="Institution",
            color="Secteur", color_discrete_map=PALETTE_SECT, orientation="h",
            text=inst_df.apply(lambda r: f"{r['Dép. BD']:,.1f} ({r['Part (%)']:.1f}%)", axis=1),
            title=f"Top 10 institutions — Dépenses BD ({unite_label})"
        )
        fig4.update_traces(textposition="outside", textfont_size=11)
        fig4.update_layout(**LAYOUT, height=420,
            legend=dict(font_size=12),
            yaxis=dict(automargin=True, tickfont_size=12),
            xaxis=dict(title=unite_label, tickfont_size=12))
        st.plotly_chart(fig4, use_container_width=True)

    # Vue hiérarchique sunburst
    st.markdown('<div class="section-title">🌐 Vue hiérarchique : Secteur → Institution → Programme</div>', unsafe_allow_html=True)
    if "Institution" in dff.columns:
        hier = dff.groupby(["Secteur", "Institution"])["Dép. BD"].sum().reset_index()
        hier["Dép. BD"] = hier["Dép. BD"] / diviseur
        fig5 = px.sunburst(
            hier, path=["Secteur", "Institution"], values="Dép. BD",
            color="Secteur", color_discrete_map=PALETTE_SECT,
            title="Répartition hiérarchique par secteur et institution"
        )
        fig5.update_traces(textfont_size=12)
        fig5.update_layout(**LAYOUT, height=500)
        st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 4 — CATÉGORIES BIOFIN
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🌱 Quelles sont les priorités de financement biodiversité ?</div>', unsafe_allow_html=True)
    st.markdown("""<div class="insight">
    ℹ️ <b>Les 9 catégories BIOFIN</b> classifient les types de dépenses biodiversité selon la méthode internationale BIOFIN/PNUD.
    Chaque catégorie représente un domaine d'intervention spécifique pour la protection de la nature.
    </div>""", unsafe_allow_html=True)

    cat_df = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
    cat_df["Dép. BD"] = cat_df["Dép. BD"] / diviseur
    cat_df["Part (%)"] = (cat_df["Dép. BD"] / cat_df["Dép. BD"].sum() * 100).round(1)
    cat_df["Cat. courte"] = cat_df["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)
    cat_df = cat_df.sort_values("Dép. BD", ascending=True)

    col1, col2 = st.columns([3, 2])
    with col1:
        fig = px.bar(
            cat_df, x="Dép. BD", y="Cat. courte", orientation="h",
            color="Dép. BD",
            color_continuous_scale=["#C8E6C9", "#4CAF76", "#1C3A2B"],
            text=cat_df.apply(lambda r: f"{r['Dép. BD']:,.1f} ({r['Part (%)']:.0f}%)", axis=1),
            title=f"Dépenses BD par catégorie BIOFIN ({unite_label})"
        )
        fig.update_traces(textposition="outside", textfont_size=11, textfont_color="#1C3A2B", marker_line_width=0)
        fig.update_layout(**LAYOUT, height=440, coloraxis_showscale=False,
            xaxis=dict(title=unite_label, gridcolor="#F0F0F0"),
            yaxis=dict(automargin=True, tickfont_size=12))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        fig2 = px.pie(
            cat_df, values="Dép. BD", names="Cat. courte",
            color_discrete_sequence=PALETTE_CAT, hole=0.5,
            title="Part de chaque catégorie"
        )
        fig2.update_traces(
            textposition="outside", textinfo="percent",
            textfont_size=11, pull=[0.02]*len(cat_df)
        )
        fig2.update_layout(**LAYOUT, height=440,
            legend=dict(font_size=10, x=1.0),
            margin=dict(l=15, r=120, t=45, b=15))
        fig2.add_annotation(
            text=f"<b>{total_bd:,.0f}</b><br>{unite_label}",
            x=0.5, y=0.5, font_size=12, font_color="#1C3A2B", showarrow=False
        )
        st.plotly_chart(fig2, use_container_width=True)

    # Heatmap catégories × années
    st.markdown('<div class="section-title">🔥 Heatmap : Intensité des dépenses par catégorie et par année</div>', unsafe_allow_html=True)
    st.markdown("""<div class="insight">
    ℹ️ Plus la couleur est foncée, plus les dépenses sont élevées. Cela permet d'identifier quelles catégories ont progressé ou stagné.
    </div>""", unsafe_allow_html=True)

    pivot_heat = dff.pivot_table(
        index="Catégorie BIOFIN", columns="Année",
        values="Dép. BD", aggfunc="sum"
    ) / diviseur
    pivot_heat.index = pivot_heat.index.str.replace(r"^\d+\.\s*", "", regex=True)

    fig3 = go.Figure(data=go.Heatmap(
        z=pivot_heat.values,
        x=[str(c) for c in pivot_heat.columns],
        y=pivot_heat.index.tolist(),
        colorscale=[[0, "#E8F5E9"], [0.5, "#4CAF76"], [1, "#1C3A2B"]],
        text=np.round(pivot_heat.values, 1),
        texttemplate="%{text}",
        textfont={"size": 12},
        colorbar=dict(title=unite_label),
    ))
    fig3.update_layout(**LAYOUT, height=400,
        xaxis=dict(side="top", tickfont_size=13),
        yaxis=dict(automargin=True, tickfont_size=12))
    st.plotly_chart(fig3, use_container_width=True)

    # Catégorie × secteur
    st.markdown('<div class="section-title">📊 Quelle catégorie est financée par quel secteur ?</div>', unsafe_allow_html=True)

    cat_sect = dff.groupby(["Catégorie BIOFIN", "Secteur"])["Dép. BD"].sum().reset_index()
    cat_sect["Dép. BD"] = cat_sect["Dép. BD"] / diviseur
    cat_sect["Cat. courte"] = cat_sect["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)

    fig4 = px.bar(
        cat_sect, x="Cat. courte", y="Dép. BD", color="Secteur",
        color_discrete_map=PALETTE_SECT, barmode="stack",
        text_auto=False,
        labels={"Dép. BD": f"Dépenses BD ({unite_label})", "Cat. courte": ""},
        title=f"Dépenses par catégorie BIOFIN, décomposées par secteur ({unite_label})"
    )
    fig4.update_layout(**LAYOUT, height=400,
        xaxis=dict(tickfont_size=11, tickangle=-25),
        yaxis=dict(gridcolor="#F5F5F5", title=unite_label),
        legend=dict(font_size=12))
    st.plotly_chart(fig4, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 5 — ANALYSE AVANCÉE
# ══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.markdown('<div class="section-title">🔍 Analyses statistiques avancées</div>', unsafe_allow_html=True)

    # 1. Part BD dans le budget de l'État et le PIB
    if macro_brut is not None:
        st.markdown("#### 💰 Les dépenses biodiversité représentent quelle part du PIB et du budget national ?")
        st.markdown("""<div class="insight">
        ℹ️ Cet indicateur permet de comparer l'effort financier du Cameroun pour la biodiversité avec les standards internationaux.
        Les pays développés consacrent généralement entre 0,5% et 1,5% de leur PIB à la biodiversité.
        </div>""", unsafe_allow_html=True)

        macro = macro_brut.copy()
        macro.columns = [str(c) for c in macro.columns]
        annee_cols = [c for c in macro.columns if c.isdigit() and int(c) in annees_sel]

        if annee_cols:
            try:
                pib_row = macro[macro["Indicateur"].str.contains("PIB.*Milliards", na=False, case=False)]
                budget_row = macro[macro["Indicateur"].str.contains("Budget", na=False, case=False)]
                bd_par_an = dff.groupby("Année")["Dép. BD"].sum()

                rows = []
                for an in annee_cols:
                    an_int = int(an)
                    if an_int in bd_par_an.index:
                        bd = bd_par_an[an_int]
                        pib_mfcfa = float(pib_row[an].values[0]) * 1000 if not pib_row.empty else None
                        budget_mfcfa = float(budget_row[an].values[0]) * 1000 if not budget_row.empty else None
                        rows.append({
                            "Année": str(an_int),
                            "Dép. BD (M FCFA)": round(bd, 1),
                            "% du PIB": round(bd / pib_mfcfa * 100, 4) if pib_mfcfa else None,
                            "% du Budget État": round(bd / budget_mfcfa * 100, 3) if budget_mfcfa else None,
                        })

                if rows:
                    df_macro = pd.DataFrame(rows)
                    col1, col2 = st.columns(2)
                    with col1:
                        fig = go.Figure()
                        fig.add_trace(go.Bar(
                            x=df_macro["Année"], y=df_macro["% du PIB"],
                            marker_color="#4CAF76",
                            text=df_macro["% du PIB"].apply(lambda x: f"{x:.3f}%" if x else ""),
                            textposition="outside", textfont_size=12,
                        ))
                        fig.update_layout(**LAYOUT, title="Dépenses BD en % du PIB", height=320,
                            yaxis=dict(title="%", gridcolor="#F5F5F5"),
                            xaxis=dict(tickfont_size=13), showlegend=False)
                        st.plotly_chart(fig, use_container_width=True)

                    with col2:
                        fig2 = go.Figure()
                        fig2.add_trace(go.Bar(
                            x=df_macro["Année"], y=df_macro["% du Budget État"],
                            marker_color="#2B6CB0",
                            text=df_macro["% du Budget État"].apply(lambda x: f"{x:.2f}%" if x else ""),
                            textposition="outside", textfont_size=12,
                        ))
                        fig2.update_layout(**LAYOUT, title="Dépenses BD en % du Budget de l'État", height=320,
                            yaxis=dict(title="%", gridcolor="#F5F5F5"),
                            xaxis=dict(tickfont_size=13), showlegend=False)
                        st.plotly_chart(fig2, use_container_width=True)
            except Exception:
                pass

    # 2. Efficacité : rapport Dép. BD / Dép. Totale par institution
    if "Dép. Totale" in dff.columns and "Institution" in dff.columns:
        st.markdown('<div class="section-title">📐 Efficacité d\'attribution : Dépense BD vs Dépense Totale</div>', unsafe_allow_html=True)
        st.markdown("""<div class="insight">
        ℹ️ Ce graphique montre pour chaque institution combien elle dépense au total et quelle part va réellement à la biodiversité.
        Les bulles au-dessus de la ligne diagonale dépasseraient 100% — impossible par définition.
        <b>Plus la bulle est grande et proche de la diagonale, plus l'institution est engagée pour la biodiversité.</b>
        </div>""", unsafe_allow_html=True)

        scatter_df = dff.groupby(["Institution", "Secteur"]).agg({
            "Dép. Totale": "sum", "Dép. BD": "sum"
        }).reset_index()
        scatter_df["Dép. Totale"] = scatter_df["Dép. Totale"] / diviseur
        scatter_df["Dép. BD"] = scatter_df["Dép. BD"] / diviseur
        scatter_df["Taux (%)"] = (scatter_df["Dép. BD"] / scatter_df["Dép. Totale"] * 100).round(1)

        fig3 = px.scatter(
            scatter_df, x="Dép. Totale", y="Dép. BD",
            color="Secteur", color_discrete_map=PALETTE_SECT,
            size="Dép. BD", size_max=40,
            hover_name="Institution",
            hover_data={"Taux (%)": True, "Dép. Totale": ":.1f", "Dép. BD": ":.1f"},
            labels={
                "Dép. Totale": f"Dépense Totale ({unite_label})",
                "Dép. BD": f"Dépense BD ({unite_label})",
            },
            title="Dépense Totale vs Dépense BD par institution"
        )
        max_val = max(scatter_df["Dép. Totale"].max(), scatter_df["Dép. BD"].max())
        fig3.add_trace(go.Scatter(
            x=[0, max_val], y=[0, max_val], mode="lines",
            line=dict(dash="dash", color="#CCC", width=1),
            name="100% BD", showlegend=True
        ))
        fig3.update_layout(**LAYOUT, height=420, legend=dict(font_size=12))
        st.plotly_chart(fig3, use_container_width=True)

    # 3. Concentration des financements (indice)
    st.markdown('<div class="section-title">📊 Concentration des financements par institution</div>', unsafe_allow_html=True)
    st.markdown("""<div class="insight">
    ℹ️ Ce graphique montre la part cumulée des financements. Si les 5 premières institutions représentent 80% des dépenses,
    les financements sont très concentrés — ce qui peut être un risque de dépendance.
    </div>""", unsafe_allow_html=True)

    if "Institution" in dff.columns:
        inst_cumul = dff.groupby("Institution")["Dép. BD"].sum().reset_index()
        inst_cumul = inst_cumul.sort_values("Dép. BD", ascending=False)
        inst_cumul["Part (%)"] = inst_cumul["Dép. BD"] / inst_cumul["Dép. BD"].sum() * 100
        inst_cumul["Part cumulée (%)"] = inst_cumul["Part (%)"].cumsum().round(1)
        inst_cumul["Rang"] = range(1, len(inst_cumul) + 1)

        fig4 = go.Figure()
        fig4.add_trace(go.Bar(
            x=inst_cumul["Institution"], y=inst_cumul["Part (%)"],
            name="Part individuelle (%)", marker_color="#4CAF76",
            text=inst_cumul["Part (%)"].apply(lambda x: f"{x:.1f}%"),
            textposition="outside", textfont_size=10,
        ))
        fig4.add_trace(go.Scatter(
            x=inst_cumul["Institution"], y=inst_cumul["Part cumulée (%)"],
            mode="lines+markers", name="Part cumulée (%)",
            line=dict(color="#C53030", width=2.5),
            marker=dict(size=7, color="#C53030"),
            yaxis="y2"
        ))
        fig4.update_layout(
            **LAYOUT, height=400,
            title="Part et part cumulée des financements par institution",
            xaxis=dict(tickfont_size=10, tickangle=-35),
            yaxis=dict(title="Part individuelle (%)", gridcolor="#F5F5F5"),
            yaxis2=dict(title="Part cumulée (%)", overlaying="y", side="right",
                        range=[0, 110], showgrid=False),
            legend=dict(font_size=12),
        )
        st.plotly_chart(fig4, use_container_width=True)

        # Alerte concentration
        top5_part = inst_cumul.head(5)["Part (%)"].sum()
        if top5_part > 70:
            st.markdown(f"""<div class="insight warning">
            ⚠️ Les <b>5 premières institutions</b> concentrent <b>{top5_part:.0f}%</b> des financements biodiversité.
            Cette concentration élevée représente un risque : si l'une d'elles se retire, l'impact serait majeur.
            Il est recommandé de diversifier les sources de financement.
            </div>""", unsafe_allow_html=True)

    # 4. Distribution des coefficients
    if "Coefficient" in dff.columns:
        st.markdown('<div class="section-title">📐 Distribution des taux d\'attribution par catégorie</div>', unsafe_allow_html=True)
        st.markdown("""<div class="insight">
        ℹ️ Le taux d'attribution indique quelle fraction d'une dépense est attribuée à la biodiversité.
        Un coefficient de 1,0 (100%) signifie que la dépense est entièrement dédiée à la biodiversité.
        </div>""", unsafe_allow_html=True)

        coef_df = dff.copy()
        coef_df["Coefficient (%)"] = (coef_df["Coefficient"] * 100).round(0)
        coef_df["Cat. courte"] = coef_df["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)

        fig5 = px.box(
            coef_df, x="Cat. courte", y="Coefficient (%)",
            color="Cat. courte", color_discrete_sequence=PALETTE_CAT,
            points="all",
            title="Distribution des taux d'attribution par catégorie BIOFIN"
        )
        fig5.update_layout(**LAYOUT, height=400,
            showlegend=False,
            xaxis=dict(tickfont_size=10, tickangle=-25, title=""),
            yaxis=dict(range=[0, 115], title="Taux d'attribution (%)", gridcolor="#F5F5F5"))
        st.plotly_chart(fig5, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# ONGLET 6 — DONNÉES BRUTES
# ══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.markdown('<div class="section-title">📋 Données détaillées</div>', unsafe_allow_html=True)

    col_f1, col_f2, col_f3 = st.columns(3)
    with col_f1:
        search = st.text_input("🔎 Rechercher", placeholder="Ex : Ministère, WWF, forêt...")
    with col_f2:
        cols_tri = [c for c in ["Dép. BD", "Dép. Totale", "Année", "Secteur", "Catégorie BIOFIN"] if c in dff.columns]
        sort_col = st.selectbox("Trier par", cols_tri)
    with col_f3:
        ordre = st.radio("Ordre", ["Décroissant", "Croissant"], horizontal=True)

    table_df = dff.copy()
    if "Dép. Totale" in table_df.columns:
        table_df["Dép. Totale"] = (table_df["Dép. Totale"] / diviseur).round(2)
    table_df["Dép. BD"] = (table_df["Dép. BD"] / diviseur).round(2)
    if "Coefficient" in table_df.columns:
        table_df["Coefficient"] = (table_df["Coefficient"] * 100).round(0).astype(int).astype(str) + "%"

    if search:
        mask = table_df.apply(lambda row: any(search.lower() in str(v).lower() for v in row), axis=1)
        table_df = table_df[mask]

    if sort_col in table_df.columns:
        table_df = table_df.sort_values(sort_col, ascending=(ordre == "Croissant"))

    st.markdown(f"**{len(table_df):,} lignes affichées** | Unité : {unite_label}")
    st.dataframe(table_df, use_container_width=True, height=460)

    st.markdown("---")
    col_e1, col_e2 = st.columns(2)
    with col_e1:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            dff.to_excel(writer, index=False, sheet_name="Données filtrées")
            dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index().to_excel(
                writer, index=False, sheet_name="Synthèse BIOFIN"
            )
        st.download_button(
            "⬇️ Exporter en Excel (.xlsx)",
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

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<hr style="border:1px solid #E2E8F0; margin-top:2rem;">
<p style="text-align:center; color:#A0AEC0; font-size:0.75rem; margin:0.5rem 0;">
    🌿 ADB Biodiversité Cameroun &nbsp;|&nbsp; Initiative BIOFIN / PNUD &nbsp;|&nbsp; Données 2020–2024 &nbsp;|&nbsp; Unité : Millions FCFA
</p>
""", unsafe_allow_html=True)
