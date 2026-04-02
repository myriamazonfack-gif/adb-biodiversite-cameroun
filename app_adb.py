import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
import io
import re
import os

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
# CSS
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
[data-testid="stSidebar"] .stMultiSelect label { color: #b7e4c7 !important; font-weight: 600; font-size: 0.8rem; letter-spacing: 0.08em; text-transform: uppercase; }
[data-testid="stSidebar"] h1, [data-testid="stSidebar"] h2, [data-testid="stSidebar"] h3 { color: #fff !important; }
[data-testid="stSidebar"] .stMarkdown p { color: #d8f3dc !important; }

.hero-header {
    background: linear-gradient(135deg, #1B4332 0%, #2D6A4F 50%, #52B788 100%);
    border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 1.5rem;
    position: relative; overflow: hidden;
}
.hero-header::before { content:"🌿"; position:absolute; right:2rem; top:50%; transform:translateY(-50%); font-size:5rem; opacity:0.15; }
.hero-title { font-family:'Playfair Display',serif; font-size:2.1rem; font-weight:900; color:#fff; margin:0; line-height:1.2; }
.hero-sub { color:#b7e4c7; font-size:0.95rem; margin-top:0.4rem; font-weight:300; }
.hero-badge { display:inline-block; background:rgba(255,255,255,0.18); color:#fff; border-radius:20px; padding:0.2rem 0.9rem; font-size:0.75rem; font-weight:600; margin-top:0.8rem; text-transform:uppercase; border:1px solid rgba(255,255,255,0.3); }

.kpi-card { background:#fff; border-radius:14px; padding:1.3rem 1.5rem; border-left:5px solid #52B788; box-shadow:0 2px 12px rgba(27,67,50,0.08); height:100%; }
.kpi-card.orange { border-left-color:#F4A261; }
.kpi-card.blue   { border-left-color:#457B9D; }
.kpi-card.purple { border-left-color:#9B5DE5; }
.kpi-label { font-size:0.72rem; color:#6B7280; font-weight:600; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:0.3rem; }
.kpi-value { font-family:'Playfair Display',serif; font-size:1.9rem; font-weight:700; color:#1B4332; line-height:1.1; }
.kpi-delta { font-size:0.78rem; color:#52B788; font-weight:500; margin-top:0.2rem; }
.kpi-delta.neg { color:#E76F51; }

.section-title { font-family:'Playfair Display',serif; font-size:1.25rem; font-weight:700; color:#1B4332; margin:1.5rem 0 0.8rem 0; padding-bottom:0.5rem; border-bottom:2px solid #d8f3dc; }

.stTabs [data-baseweb="tab-list"] { gap:0.3rem; background:#e9f5e9; padding:0.4rem; border-radius:12px; }
.stTabs [data-baseweb="tab"] { border-radius:8px; padding:0.4rem 1.2rem; font-weight:500; color:#2D6A4F; font-size:0.88rem; }
.stTabs [aria-selected="true"] { background:#2D6A4F !important; color:white !important; }

.footer { text-align:center; color:#9CA3AF; font-size:0.75rem; margin-top:2rem; padding-top:1rem; border-top:1px solid #e5e7eb; }

#MainMenu {visibility:hidden;} footer {visibility:hidden;} header {visibility:hidden;}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTES
# ─────────────────────────────────────────────────────────────────────────────
PALETTE_CATEGORIES = ["#1B4332","#2D6A4F","#40916C","#52B788","#74C69D","#95D5B2","#F4A261","#E76F51","#457B9D"]
PALETTE_SECTEURS   = {"Public":"#2D6A4F","ONG / OSC":"#457B9D","Secteur Privé":"#9B5DE5","PTF":"#F4A261"}

# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT
# ─────────────────────────────────────────────────────────────────────────────
@st.cache_data(show_spinner="Chargement des données…")
def charger_donnees(fichier_bytes: bytes):
    """Charge depuis des bytes bruts. Un BytesIO frais par lecture pour éviter
    les problèmes de curseur (bug historique de l'app)."""
    def _bx():
        return io.BytesIO(fichier_bytes)

    xls      = pd.ExcelFile(_bx())
    feuilles = xls.sheet_names
    df = macro = None

    # Feuille principale
    if "PowerBI_Data" in feuilles:
        df = pd.read_excel(_bx(), sheet_name="PowerBI_Data", header=1)
        df = df.dropna(how="all")

    # Fallback : feuilles sectorielles
    if df is None:
        mapping = {
            "D. Publiques":"Public","D. Publiques ":"Public",
            "ONG OSC":"ONG / OSC","ONG OSC ":"ONG / OSC",
            "Secteur Prive":"Secteur Privé","Secteur Prive.":"Secteur Privé",
            "Secteur Privé":"Secteur Privé","PTF":"PTF",
        }
        frames = []
        for feuille, secteur_val in mapping.items():
            if feuille in feuilles:
                tmp = pd.read_excel(_bx(), sheet_name=feuille, header=2)
                tmp = tmp.dropna(how="all")
                tmp["Secteur"] = secteur_val
                frames.append(tmp)
        if frames:
            df = pd.concat(frames, ignore_index=True)

    # Macro
    for nom in ["Donnees Macro", "Données Macro"]:
        if nom in feuilles:
            macro = pd.read_excel(_bx(), sheet_name=nom, header=1)
            macro = macro.dropna(how="all")
            break

    return df, macro, feuilles


def kpi_card(label, value, delta=None, couleur=""):
    dh = ""
    if delta is not None:
        cls = "neg" if delta < 0 else ""
        s   = "▲" if delta >= 0 else "▼"
        dh  = f'<div class="kpi-delta {cls}">{s} {abs(delta):.1f}% sur la période</div>'
    return f'<div class="kpi-card {couleur}"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div>{dh}</div>'


def court(s, n=30):
    s = re.sub(r"^\d+\.\s*", "", str(s))
    return s[:n]+"…" if len(s) > n else s


# ─────────────────────────────────────────────────────────────────────────────
# SIDEBAR — tout dans un seul bloc pour garantir l'ordre d'exécution
# ─────────────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 🌿 ADB Biodiversité")
    st.markdown("**Analyse des Dépenses pour la Biodiversité**")
    st.markdown("---")

    fichier_charge = st.file_uploader(
        "📂 Charger un autre fichier Excel",
        type=["xlsx","xls"],
        help="Laissez vide pour les données de démonstration",
    )

    # ── Résolution du fichier ──────────────────────────────────────────────
    if fichier_charge is not None:
        _bytes    = fichier_charge.read()
        mode_demo = False
    else:
        _candidates = [
            os.path.join(os.path.dirname(os.path.abspath(__file__)), "ADB_Cameroun_Simulation.xlsx"),
            os.path.join(os.getcwd(), "ADB_Cameroun_Simulation.xlsx"),
            "ADB_Cameroun_Simulation.xlsx",
        ]
        _bytes = None
        for _p in _candidates:
            if os.path.isfile(_p):
                with open(_p, "rb") as _f:
                    _bytes = _f.read()
                break
        mode_demo = True

    if _bytes is None:
        st.error("Fichier Excel introuvable. Chargez-le via le bouton ci-dessus.")
        st.stop()

    df_brut, macro_brut, _ = charger_donnees(_bytes)

    if df_brut is None:
        st.error("❌ Impossible de lire les données. Vérifiez la feuille 'PowerBI_Data'.")
        st.stop()

    # ── Nettoyage colonnes ─────────────────────────────────────────────────
    df = df_brut.copy()
    col_map = {}
    for c in df.columns:
        cl = str(c).lower().strip()
        if   "secteur"    in cl:                       col_map[c] = "Secteur"
        elif "institution" in cl:                      col_map[c] = "Institution"
        elif "programme"   in cl:                      col_map[c] = "Programme"
        elif "catégorie"   in cl or "categorie" in cl: col_map[c] = "Catégorie BIOFIN"
        elif "coefficient" in cl:                      col_map[c] = "Coefficient"
        elif "année"       in cl or "annee"     in cl: col_map[c] = "Année"
        elif "totale"      in cl:                      col_map[c] = "Dép. Totale"
        elif "bd"          in cl or "biodiv"    in cl: col_map[c] = "Dép. BD"
    df = df.rename(columns=col_map)

    for req in ["Secteur", "Catégorie BIOFIN", "Année", "Dép. BD"]:
        if req not in df.columns:
            st.error(f"Colonne manquante : « {req} »")
            st.stop()

    df["Année"]   = pd.to_numeric(df["Année"],   errors="coerce").astype("Int64")
    df["Dép. BD"] = pd.to_numeric(df["Dép. BD"], errors="coerce")
    if "Dép. Totale" in df.columns:
        df["Dép. Totale"] = pd.to_numeric(df["Dép. Totale"], errors="coerce")
    df = df.dropna(subset=["Année", "Dép. BD"])

    # ── FILTRES ────────────────────────────────────────────────────────────
    st.markdown("---")
    st.markdown("### 🎛️ Filtres")

    annees_dispo  = sorted(df["Année"].dropna().unique().tolist())
    annees_sel    = st.multiselect("📅 Années",           annees_dispo,  default=annees_dispo)

    secteurs_dispo = sorted(df["Secteur"].dropna().unique().tolist())
    secteurs_sel   = st.multiselect("🏛️ Secteurs",        secteurs_dispo, default=secteurs_dispo)

    cats_dispo = sorted(df["Catégorie BIOFIN"].dropna().unique().tolist())
    cats_sel   = st.multiselect("🌱 Catégories BIOFIN", cats_dispo,     default=cats_dispo)

    if "Institution" in df.columns:
        insts_dispo = sorted(df["Institution"].dropna().unique().tolist())
        inst_sel    = st.multiselect("🏢 Institutions", insts_dispo, default=insts_dispo)
    else:
        inst_sel = None

    st.markdown("---")
    st.markdown("**📊 Unité d'affichage**")
    unite       = st.radio("", ["Millions FCFA","Milliards FCFA"], index=0, horizontal=True)
    diviseur    = 1_000 if unite == "Milliards FCFA" else 1
    unite_label = "Mds FCFA" if unite == "Milliards FCFA" else "MFCFA"

    st.markdown("---")
    if mode_demo:
        st.info("🔬 **Mode démonstration**\nDonnées fictives simulées pour le Cameroun")

# ─────────────────────────────────────────────────────────────────────────────
# FILTRAGE — sécurisé (sélection vide = tout afficher)
# ─────────────────────────────────────────────────────────────────────────────
if not annees_sel:   annees_sel   = annees_dispo
if not secteurs_sel: secteurs_sel = secteurs_dispo
if not cats_sel:     cats_sel     = cats_dispo

dff = df[
    df["Année"].isin(annees_sel) &
    df["Secteur"].isin(secteurs_sel) &
    df["Catégorie BIOFIN"].isin(cats_sel)
].copy()

if inst_sel is not None and len(inst_sel) > 0 and "Institution" in dff.columns:
    dff = dff[dff["Institution"].isin(inst_sel)]

if dff.empty:
    st.warning("⚠️ Aucune donnée pour les filtres sélectionnés. Ajustez les filtres.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# HERO
# ─────────────────────────────────────────────────────────────────────────────
badge = "🔬 Données de démonstration" if mode_demo else "📊 Données réelles"
st.markdown(f"""
<div class="hero-header">
    <p class="hero-title">Analyse des Dépenses<br>Biodiversité — Cameroun</p>
    <p class="hero-sub">Initiative BIOFIN · Tableau de bord interactif · {min(annees_sel)}–{max(annees_sel)}</p>
    <span class="hero-badge">{badge}</span>
</div>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# KPIs
# ─────────────────────────────────────────────────────────────────────────────
total_bd    = dff["Dép. BD"].sum() / diviseur
secteur_top = dff.groupby("Secteur")["Dép. BD"].sum().idxmax()
cat_top     = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().idxmax()
nb_acteurs  = dff["Institution"].nunique() if "Institution" in dff.columns else dff["Secteur"].nunique()

delta_pct = None
if len(annees_sel) >= 2:
    v0 = dff[dff["Année"] == min(annees_sel)]["Dép. BD"].sum()
    v1 = dff[dff["Année"] == max(annees_sel)]["Dép. BD"].sum()
    if v0 > 0:
        delta_pct = (v1 - v0) / v0 * 100

coeff_str = None
if "Coefficient" in dff.columns:
    coeff_str = f"{dff['Coefficient'].mean() * 100:.1f} %"

c1, c2, c3, c4 = st.columns(4)
with c1: st.markdown(kpi_card(f"Total Dépenses BD ({unite_label})", f"{total_bd:,.1f}", delta_pct),            unsafe_allow_html=True)
with c2: st.markdown(kpi_card("Secteur dominant",     secteur_top,          couleur="blue"),   unsafe_allow_html=True)
with c3: st.markdown(kpi_card("Catégorie BIOFIN #1",  court(cat_top, 26),   couleur="orange"), unsafe_allow_html=True)
with c4: st.markdown(kpi_card("Coefficient moyen" if coeff_str else "Acteurs", coeff_str or str(nb_acteurs), couleur="purple"), unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# ONGLETS  (4 — Données brutes supprimées)
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Catégories BIOFIN",
    "📈 Évolution temporelle",
    "🏛️ Par secteur",
    "🔍 Analyse détaillée",
])

# ══════════════════════════════════════════════════════════════════════════════
# TAB 1 — CATÉGORIES BIOFIN
# ══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-title">🌱 Dépenses BD par catégorie BIOFIN</div>', unsafe_allow_html=True)

    cat_df = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
    cat_df["Dép. BD"]    = cat_df["Dép. BD"] / diviseur
    cat_df["Cat. courte"] = cat_df["Catégorie BIOFIN"].apply(court)
    cat_df["Part (%)"]   = (cat_df["Dép. BD"] / cat_df["Dép. BD"].sum() * 100).round(1)
    cat_df = cat_df.sort_values("Dép. BD", ascending=True)

    col_left, col_right = st.columns([3, 2])
    with col_left:
        fig_bar = px.bar(
            cat_df, x="Dép. BD", y="Cat. courte", orientation="h",
            color="Dép. BD", color_continuous_scale=["#d8f3dc","#52B788","#1B4332"],
            text=cat_df["Dép. BD"].apply(lambda v: f"{v:,.0f}"),
            labels={"Dép. BD":f"({unite_label})","Cat. courte":""},
            title=f"Dépenses BD par catégorie ({unite_label})",
        )
        fig_bar.update_traces(textposition="outside", textfont_size=11, marker_line_width=0)
        fig_bar.update_layout(
            height=440, coloraxis_showscale=False, plot_bgcolor="white", paper_bgcolor="white",
            font_family="DM Sans", title_font=dict(size=14,color="#1B4332"),
            margin=dict(l=10,r=90,t=40,b=20),
            xaxis=dict(gridcolor="#f0f0f0"), yaxis=dict(gridcolor="rgba(0,0,0,0)"),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

    with col_right:
        fig_pie = px.pie(
            cat_df, values="Dép. BD", names="Cat. courte",
            color_discrete_sequence=PALETTE_CATEGORIES, hole=0.52,
            title="Répartition en % du total",
        )
        fig_pie.update_traces(textposition="outside", textinfo="percent", textfont_size=11, pull=[0.03]*len(cat_df))
        fig_pie.update_layout(
            height=440, font_family="DM Sans", title_font=dict(size=14,color="#1B4332"),
            paper_bgcolor="white", showlegend=True, legend=dict(font_size=10,x=1.0),
            margin=dict(l=0,r=130,t=40,b=20),
        )
        fig_pie.add_annotation(text=f"<b>{total_bd:,.0f}</b><br>{unite_label}", x=0.5, y=0.5,
                               font_size=13, font_color="#1B4332", showarrow=False)
        st.plotly_chart(fig_pie, use_container_width=True)

    # Heatmap lisible
    st.markdown('<div class="section-title">🔥 Heatmap : Catégories × Années</div>', unsafe_allow_html=True)
    pivot = dff.pivot_table(index="Catégorie BIOFIN", columns="Année", values="Dép. BD", aggfunc="sum") / diviseur
    pivot.index = pivot.index.str.replace(r"^\d+\.\s*", "", regex=True)
    z_arr  = np.array(pivot.values, dtype=float)
    z_max  = float(np.nanmax(z_arr)) if np.nanmax(z_arr) > 0 else 1.0

    # Texte blanc sur cellules foncées, vert foncé sur cellules claires
    text_matrix = [[f"{v:.1f}" for v in row] for row in z_arr]

    fig_heat = go.Figure(go.Heatmap(
        z=z_arr,
        x=[str(c) for c in pivot.columns],
        y=pivot.index.tolist(),
        colorscale=[[0,"#e8f5e9"],[0.4,"#74C69D"],[1,"#1B4332"]],
        text=text_matrix, texttemplate="%{text}",
        hoverongaps=False, colorbar=dict(title=unite_label, tickfont=dict(size=10)),
    ))
    fig_heat.update_layout(
        height=380, font_family="DM Sans", paper_bgcolor="white", plot_bgcolor="white",
        margin=dict(l=10,r=20,t=20,b=20), xaxis=dict(side="top"),
    )
    st.plotly_chart(fig_heat, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 2 — ÉVOLUTION TEMPORELLE
# ══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.markdown('<div class="section-title">📈 Évolution des dépenses BD dans le temps</div>', unsafe_allow_html=True)

    evol = dff.groupby("Année")["Dép. BD"].sum().reset_index()
    evol["Dép. BD"] = evol["Dép. BD"] / diviseur
    evol["Année"]   = evol["Année"].astype(str)

    col_a, col_b = st.columns(2)
    with col_a:
        fig_l = go.Figure()
        fig_l.add_trace(go.Scatter(
            x=evol["Année"], y=evol["Dép. BD"], mode="lines+markers+text",
            line=dict(color="#2D6A4F",width=3),
            marker=dict(size=10,color="#2D6A4F",line=dict(color="white",width=2)),
            fill="tozeroy", fillcolor="rgba(82,183,136,0.15)",
            text=evol["Dép. BD"].apply(lambda v: f"{v:,.1f}"),
            textposition="top center", textfont=dict(size=11,color="#1B4332"),
        ))
        fig_l.update_layout(
            title=f"Évolution totale ({unite_label})", height=340,
            font_family="DM Sans", plot_bgcolor="white", paper_bgcolor="white",
            title_font=dict(size=14,color="#1B4332"),
            xaxis=dict(gridcolor="#f5f5f5"), yaxis=dict(gridcolor="#f5f5f5",title=unite_label),
            margin=dict(l=20,r=20,t=40,b=20), showlegend=False,
        )
        st.plotly_chart(fig_l, use_container_width=True)

    with col_b:
        evol_g = dff.groupby("Année")["Dép. BD"].sum().reset_index()
        evol_g["Croissance (%)"] = evol_g["Dép. BD"].pct_change() * 100
        evol_g = evol_g.dropna()
        evol_g["Année"] = evol_g["Année"].astype(str)
        fig_g = go.Figure(go.Bar(
            x=evol_g["Année"], y=evol_g["Croissance (%)"],
            marker_color=["#2D6A4F" if v >= 0 else "#E76F51" for v in evol_g["Croissance (%)"]],
            text=evol_g["Croissance (%)"].apply(lambda v: f"{v:.1f}%"),
            textposition="outside", textfont=dict(size=11),
        ))
        fig_g.update_layout(
            title="Taux de croissance annuel (%)", height=340,
            font_family="DM Sans", plot_bgcolor="white", paper_bgcolor="white",
            title_font=dict(size=14,color="#1B4332"),
            xaxis=dict(gridcolor="#f5f5f5"),
            yaxis=dict(gridcolor="#f5f5f5",title="%",zeroline=True,zerolinecolor="#ccc"),
            margin=dict(l=20,r=20,t=40,b=20), showlegend=False,
        )
        st.plotly_chart(fig_g, use_container_width=True)

    st.markdown('<div class="section-title">📊 Évolution par catégorie BIOFIN</div>', unsafe_allow_html=True)
    ec = dff.groupby(["Année","Catégorie BIOFIN"])["Dép. BD"].sum().reset_index()
    ec["Dép. BD"]     = ec["Dép. BD"] / diviseur
    ec["Cat. courte"] = ec["Catégorie BIOFIN"].apply(court)
    ec["Année"]       = ec["Année"].astype(str)
    fig_area = px.area(ec, x="Année", y="Dép. BD", color="Cat. courte",
                       color_discrete_sequence=PALETTE_CATEGORIES,
                       labels={"Dép. BD":f"Dépenses BD ({unite_label})","Cat. courte":"Catégorie"},
                       title=f"Évolution empilée par catégorie BIOFIN ({unite_label})")
    fig_area.update_layout(height=380, font_family="DM Sans", plot_bgcolor="white", paper_bgcolor="white",
                           title_font=dict(size=14,color="#1B4332"),
                           xaxis=dict(gridcolor="#f5f5f5"), yaxis=dict(gridcolor="#f5f5f5"),
                           margin=dict(l=20,r=20,t=40,b=20), legend=dict(font_size=10))
    st.plotly_chart(fig_area, use_container_width=True)

    es = dff.groupby(["Année","Secteur"])["Dép. BD"].sum().reset_index()
    es["Dép. BD"] = es["Dép. BD"] / diviseur
    es["Année"]   = es["Année"].astype(str)
    fig_ls = px.line(es, x="Année", y="Dép. BD", color="Secteur",
                     color_discrete_map=PALETTE_SECTEURS, markers=True,
                     labels={"Dép. BD":f"Dépenses BD ({unite_label})"},
                     title=f"Évolution par secteur ({unite_label})")
    fig_ls.update_traces(line_width=2.5, marker_size=9)
    fig_ls.update_layout(height=340, font_family="DM Sans", plot_bgcolor="white", paper_bgcolor="white",
                         title_font=dict(size=14,color="#1B4332"),
                         xaxis=dict(gridcolor="#f5f5f5"), yaxis=dict(gridcolor="#f5f5f5"),
                         margin=dict(l=20,r=20,t=40,b=20), legend=dict(font_size=11))
    st.plotly_chart(fig_ls, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 3 — PAR SECTEUR
# ══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-title">🏛️ Répartition par secteur de financement</div>', unsafe_allow_html=True)

    sd = dff.groupby("Secteur")["Dép. BD"].sum().reset_index()
    sd["Dép. BD"]  = sd["Dép. BD"] / diviseur
    sd["Part (%)"] = (sd["Dép. BD"] / sd["Dép. BD"].sum() * 100).round(1)
    sd = sd.sort_values("Dép. BD", ascending=False)

    c1_, c2_ = st.columns(2)
    with c1_:
        fig_sb = px.bar(sd, x="Secteur", y="Dép. BD", color="Secteur",
                        color_discrete_map=PALETTE_SECTEURS,
                        text=sd["Dép. BD"].apply(lambda v: f"{v:,.1f}"),
                        labels={"Dép. BD":f"Dépenses BD ({unite_label})"},
                        title=f"Total BD par secteur ({unite_label})")
        fig_sb.update_traces(textposition="outside", textfont_size=12, marker_line_width=0)
        fig_sb.update_layout(height=380, showlegend=False, font_family="DM Sans",
                             plot_bgcolor="white", paper_bgcolor="white",
                             title_font=dict(size=14,color="#1B4332"),
                             xaxis=dict(gridcolor="rgba(0,0,0,0)"), yaxis=dict(gridcolor="#f5f5f5"),
                             margin=dict(l=20,r=20,t=40,b=20))
        st.plotly_chart(fig_sb, use_container_width=True)

    with c2_:
        fig_sp = px.pie(sd, values="Dép. BD", names="Secteur", color="Secteur",
                        color_discrete_map=PALETTE_SECTEURS, hole=0.5,
                        title="Part de chaque secteur (%)")
        fig_sp.update_traces(textposition="outside", textinfo="label+percent", textfont_size=11, pull=[0.04]*len(sd))
        fig_sp.update_layout(height=380, font_family="DM Sans", paper_bgcolor="white",
                             showlegend=False, title_font=dict(size=14,color="#1B4332"),
                             margin=dict(l=0,r=0,t=40,b=20))
        st.plotly_chart(fig_sp, use_container_width=True)

    st.markdown('<div class="section-title">🌐 Vue hiérarchique : Secteur → Catégorie BIOFIN</div>', unsafe_allow_html=True)
    hd = dff.groupby(["Secteur","Catégorie BIOFIN"])["Dép. BD"].sum().reset_index()
    hd["Dép. BD"]     = hd["Dép. BD"] / diviseur
    hd["Cat. courte"] = hd["Catégorie BIOFIN"].apply(court)
    fig_sun = px.sunburst(hd, path=["Secteur","Cat. courte"], values="Dép. BD",
                          color="Secteur", color_discrete_map=PALETTE_SECTEURS,
                          title="Répartition hiérarchique Secteur → Catégorie BIOFIN")
    fig_sun.update_traces(textfont_size=12)
    fig_sun.update_layout(height=520, font_family="DM Sans", paper_bgcolor="white",
                          title_font=dict(size=14,color="#1B4332"),
                          margin=dict(l=20,r=20,t=40,b=20))
    st.plotly_chart(fig_sun, use_container_width=True)

    if "Institution" in dff.columns:
        st.markdown('<div class="section-title">🏆 Top 10 Institutions</div>', unsafe_allow_html=True)
        id_ = dff.groupby(["Institution","Secteur"])["Dép. BD"].sum().reset_index()
        id_["Dép. BD"] = id_["Dép. BD"] / diviseur
        id_ = id_.sort_values("Dép. BD", ascending=False).head(10).sort_values("Dép. BD")
        fig_i = px.bar(id_, x="Dép. BD", y="Institution", color="Secteur",
                       color_discrete_map=PALETTE_SECTEURS, orientation="h",
                       text=id_["Dép. BD"].apply(lambda v: f"{v:,.1f}"),
                       labels={"Dép. BD":f"Dépenses BD ({unite_label})"},
                       title=f"Top 10 acteurs — Dépenses BD ({unite_label})")
        fig_i.update_traces(textposition="outside", textfont_size=11)
        fig_i.update_layout(height=420, font_family="DM Sans", plot_bgcolor="white",
                            paper_bgcolor="white", title_font=dict(size=14,color="#1B4332"),
                            legend=dict(font_size=11), margin=dict(l=20,r=90,t=40,b=20))
        st.plotly_chart(fig_i, use_container_width=True)


# ══════════════════════════════════════════════════════════════════════════════
# TAB 4 — ANALYSE DÉTAILLÉE
# ══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-title">🔍 Analyse croisée & Coefficients</div>', unsafe_allow_html=True)

    cd1, cd2 = st.columns(2)
    with cd1:
        if "Dép. Totale" in dff.columns:
            grp = "Institution" if "Institution" in dff.columns else "Secteur"
            sc  = dff.groupby([grp,"Secteur"]).agg({"Dép. Totale":"sum","Dép. BD":"sum"}).reset_index()
            sc.columns = ["Nom","Secteur","Dép. Totale","Dép. BD"]
            sc["Dép. Totale"] = sc["Dép. Totale"] / diviseur
            sc["Dép. BD"]     = sc["Dép. BD"]     / diviseur
            sc["Coeff (%)"]   = (sc["Dép. BD"] / sc["Dép. Totale"].replace(0, np.nan) * 100).round(1)
            fig_sc = px.scatter(sc, x="Dép. Totale", y="Dép. BD", color="Secteur",
                                color_discrete_map=PALETTE_SECTEURS, size="Dép. BD", size_max=35,
                                hover_name="Nom", hover_data={"Coeff (%)":True},
                                labels={"Dép. Totale":f"Dépense Totale ({unite_label})","Dép. BD":f"Dépense BD ({unite_label})"},
                                title="Dépense Totale vs Dépense BD par acteur")
            mv = max(sc["Dép. Totale"].max(), sc["Dép. BD"].max())
            fig_sc.add_trace(go.Scatter(x=[0,mv],y=[0,mv],mode="lines",
                                        line=dict(dash="dash",color="#ccc",width=1),name="100% BD"))
            fig_sc.update_layout(height=380, font_family="DM Sans", plot_bgcolor="white",
                                 paper_bgcolor="white", title_font=dict(size=13,color="#1B4332"),
                                 legend=dict(font_size=10), margin=dict(l=20,r=20,t=40,b=20))
            st.plotly_chart(fig_sc, use_container_width=True)

    with cd2:
        if "Coefficient" in dff.columns:
            cf = dff[["Secteur","Coefficient","Catégorie BIOFIN"]].copy()
            cf["Coefficient (%)"] = (cf["Coefficient"] * 100).round(1)
            fig_bx = px.box(cf, x="Secteur", y="Coefficient (%)", color="Secteur",
                            color_discrete_map=PALETTE_SECTEURS, points="all",
                            title="Distribution des coefficients par secteur")
            fig_bx.update_layout(height=380, font_family="DM Sans", plot_bgcolor="white",
                                 paper_bgcolor="white", title_font=dict(size=13,color="#1B4332"),
                                 showlegend=False, margin=dict(l=20,r=20,t=40,b=20),
                                 yaxis=dict(range=[0,110],title="Coefficient (%)"))
            st.plotly_chart(fig_bx, use_container_width=True)

    # Tableau croisé — compatible pandas ≥ 2.1 (utilise .map au lieu de .applymap)
    st.markdown('<div class="section-title">📊 Tableau croisé : Catégories × Secteurs</div>', unsafe_allow_html=True)

    pv = dff.pivot_table(index="Catégorie BIOFIN", columns="Secteur", values="Dép. BD",
                         aggfunc="sum", margins=True, margins_name="TOTAL") / diviseur
    pv.index = [re.sub(r"^\d+\.\s*","",i) if i != "TOTAL" else i for i in pv.index]
    pv = pv.round(1).fillna(0)

    vmax = float(pv.replace(0, np.nan).stack().max() or 1)

    def colorier(val):
        try:
            v = float(val)
            if v <= 0: return "background-color:#f9f9f9;color:#bbb"
            t = min(int(v / vmax * 200), 200)
            txt = "#fff" if t > 100 else "#1B4332"
            return f"background-color:rgb({255-t},{255},{255-t});color:{txt};font-weight:500"
        except (ValueError, TypeError):
            return ""

    styler = pv.style.format("{:,.1f}")
    # Compatibilité : .map() en pandas ≥ 2.1, sinon .applymap()
    try:
        styler = styler.map(colorier)
    except AttributeError:
        styler = styler.applymap(colorier)

    st.dataframe(styler.set_properties(**{"font-size":"12px"}), use_container_width=True, height=400)

    # Macro
    if macro_brut is not None:
        st.markdown('<div class="section-title">🌍 Contexte macro-économique</div>', unsafe_allow_html=True)
        try:
            md = macro_brut.copy()
            md.columns = [str(c) for c in md.columns]
            ac = [c for c in md.columns if str(c).isdigit() and int(c) in annees_dispo]
            if "Indicateur" in md.columns and ac:
                pr = md[md["Indicateur"].str.contains("PIB.*Milliards",na=False,case=False)]
                if not pr.empty:
                    pv2 = [float(v) for v in pr[ac].values.flatten() if pd.notna(v)]
                    bpa = dff.groupby("Année")["Dép. BD"].sum()
                    rows = []
                    for i,an in enumerate(ac):
                        ai = int(an)
                        if ai in bpa.index and i < len(pv2):
                            rows.append({"Année":str(ai),"Part BD/PIB (%)":round(bpa[ai]/(pv2[i]*1000)*100,4)})
                    if rows:
                        bdf = pd.DataFrame(rows)
                        fmac = go.Figure(go.Bar(
                            x=bdf["Année"], y=bdf["Part BD/PIB (%)"],
                            marker_color="#52B788",
                            text=bdf["Part BD/PIB (%)"].apply(lambda v: f"{v:.3f}%"),
                            textposition="outside",
                        ))
                        fmac.update_layout(
                            title="Part des dépenses BD dans le PIB (%)", height=320,
                            font_family="DM Sans", plot_bgcolor="white", paper_bgcolor="white",
                            title_font=dict(size=13,color="#1B4332"),
                            yaxis=dict(title="%",gridcolor="#f5f5f5"),
                            xaxis=dict(gridcolor="rgba(0,0,0,0)"),
                            margin=dict(l=20,r=20,t=40,b=20), showlegend=False,
                        )
                        st.plotly_chart(fmac, use_container_width=True)
        except Exception:
            pass

# ─────────────────────────────────────────────────────────────────────────────
# FOOTER
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    🌿 ADB Biodiversité Cameroun &nbsp;·&nbsp; Initiative BIOFIN &nbsp;·&nbsp; PNUD
    &nbsp;|&nbsp; Données : 2020–2024 &nbsp;|&nbsp; Unité par défaut : Millions FCFA
</div>
""", unsafe_allow_html=True)
