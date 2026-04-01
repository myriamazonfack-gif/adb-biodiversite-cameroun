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
)

# ─────────────────────────────────────────────────────────────────────────────
# CSS SIMPLIFIÉ
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
.main { background: #F7F5F0; }
.kpi-card {
    background: white;
    border-radius: 10px;
    padding: 1rem;
    border-left: 4px solid #2E6B47;
    box-shadow: 0 2px 4px rgba(0,0,0,0.1);
}
.kpi-label { font-size: 0.8rem; color: #666; text-transform: uppercase; }
.kpi-value { font-size: 1.8rem; font-weight: bold; color: #1C3A2B; }
.section-title {
    font-size: 1.2rem;
    font-weight: bold;
    color: #1C3A2B;
    margin: 1rem 0;
    border-bottom: 2px solid #C8E6C9;
}
.insight {
    background: #E8F5E9;
    padding: 0.8rem;
    border-radius: 8px;
    margin: 0.5rem 0;
}
</style>
""", unsafe_allow_html=True)

# ─────────────────────────────────────────────────────────────────────────────
# PALETTES
# ─────────────────────────────────────────────────────────────────────────────
PALETTE_SECT = {"Public": "#2E6B47", "ONG / OSC": "#2B6CB0", "Secteur Privé": "#6B46C1", "PTF": "#E07B39"}
PALETTE_CAT = ["#1C3A2B", "#2E6B47", "#3D8B5E", "#4CAF76", "#6FCF97"]


# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT DES DONNÉES
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

    return df


# Titre principal
st.title("🌿 Analyse des Dépenses Biodiversité — Cameroun")
st.markdown("Initiative BIOFIN / PNUD")

# ─────────────────────────────────────────────────────────────────────────────
# CHARGEMENT FICHIER
# ─────────────────────────────────────────────────────────────────────────────
col1, col2 = st.columns([2, 3])
with col1:
    fichier_charge = st.file_uploader("📂 Charger votre fichier Excel", type=["xlsx", "xls"])

# Chargement des données
try:
    source = fichier_charge if fichier_charge else "ADB_Cameroun_Simulation.xlsx"
    df_brut = charger_donnees(source)
except Exception as e:
    st.error(f"Erreur : {e}")
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
    elif "année" in cl or "annee" in cl:
        col_map[c] = "Année"
    elif "bd" in cl or "biodiv" in cl:
        col_map[c] = "Dép. BD"

df = df.rename(columns=col_map)

# Conversion des types
df["Année"] = pd.to_numeric(df["Année"], errors="coerce")
df["Dép. BD"] = pd.to_numeric(df["Dép. BD"], errors="coerce")
df = df.dropna(subset=["Année", "Dép. BD"])
df["Année"] = df["Année"].astype(int)

# ─────────────────────────────────────────────────────────────────────────────
# FILTRES - SIMPLES ET VISIBLES
# ─────────────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown("### 🎛️ Filtres")

# Récupération des options
annees_options = sorted(df["Année"].unique())
secteurs_options = sorted(df["Secteur"].unique())
categories_options = sorted(df["Catégorie BIOFIN"].unique())

# Création des filtres en colonnes
fcol1, fcol2, fcol3 = st.columns(3)

with fcol1:
    annees_sel = st.multiselect(
        "📅 Années",
        options=annees_options,
        default=annees_options
    )

with fcol2:
    secteurs_sel = st.multiselect(
        "🏛️ Secteurs",
        options=secteurs_options,
        default=secteurs_options
    )

with fcol3:
    categories_sel = st.multiselect(
        "🌱 Catégories BIOFIN",
        options=categories_options,
        default=categories_options
    )

# Unité
unite = st.radio("💰 Unité d'affichage", ["Millions FCFA", "Milliards FCFA"], horizontal=True)
diviseur = 1000 if unite == "Milliards FCFA" else 1
unite_label = "Mds FCFA" if unite == "Milliards FCFA" else "M FCFA"

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# APPLICATION DES FILTRES
# ─────────────────────────────────────────────────────────────────────────────
dff = df[
    df["Année"].isin(annees_sel) &
    df["Secteur"].isin(secteurs_sel) &
    df["Catégorie BIOFIN"].isin(categories_sel)
    ].copy()

# Vérification
if dff.empty:
    st.warning("⚠️ Aucune donnée pour ces filtres. Veuillez élargir votre sélection.")
    st.stop()

# ─────────────────────────────────────────────────────────────────────────────
# INDICATEURS (KPIs)
# ─────────────────────────────────────────────────────────────────────────────
total = dff["Dép. BD"].sum() / diviseur
secteur_top = dff.groupby("Secteur")["Dép. BD"].sum().idxmax()
part_top = (dff[dff["Secteur"] == secteur_top]["Dép. BD"].sum() / dff["Dép. BD"].sum() * 100)
nb_projets = len(dff)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Total Dépenses BD</div>
        <div class="kpi-value">{total:,.1f} {unite_label}</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Secteur dominant</div>
        <div class="kpi-value">{secteur_top}</div>
        <div style="font-size:0.8rem;">{part_top:.0f}% du total</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    cat_top = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().idxmax()
    cat_top_nom = cat_top.split(". ", 1)[-1] if ". " in cat_top else cat_top
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Priorité BIOFIN</div>
        <div class="kpi-value">{cat_top_nom[:30]}</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-label">Projets/Programmes</div>
        <div class="kpi-value">{nb_projets}</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ─────────────────────────────────────────────────────────────────────────────
# GRAPHIQUES
# ─────────────────────────────────────────────────────────────────────────────
tab1, tab2, tab3 = st.tabs(["📊 Vue d'ensemble", "📈 Évolution", "📋 Données"])

# ─────────────────────────────────────────────────────────────────────────────
# TAB 1 - VUE D'ENSEMBLE
# ─────────────────────────────────────────────────────────────────────────────
with tab1:
    col_g1, col_g2 = st.columns(2)

    with col_g1:
        st.subheader("Dépenses par secteur")
        sect_df = dff.groupby("Secteur")["Dép. BD"].sum().reset_index()
        sect_df["Dép. BD"] = sect_df["Dép. BD"] / diviseur
        fig = px.pie(
            sect_df, values="Dép. BD", names="Secteur",
            color="Secteur", color_discrete_map=PALETTE_SECT,
            hole=0.4
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)

    with col_g2:
        st.subheader("Dépenses par catégorie BIOFIN")
        cat_df = dff.groupby("Catégorie BIOFIN")["Dép. BD"].sum().reset_index()
        cat_df["Dép. BD"] = cat_df["Dép. BD"] / diviseur
        cat_df["Catégorie"] = cat_df["Catégorie BIOFIN"].str.replace(r"^\d+\.\s*", "", regex=True)
        fig = px.bar(
            cat_df, x="Catégorie", y="Dép. BD",
            color="Dép. BD", color_continuous_scale="Greens",
            title=f"Dépenses ({unite_label})"
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 2 - ÉVOLUTION
# ─────────────────────────────────────────────────────────────────────────────
with tab2:
    st.subheader("Évolution temporelle")

    evol = dff.groupby("Année")["Dép. BD"].sum().reset_index()
    evol["Dép. BD"] = evol["Dép. BD"] / diviseur

    fig = px.line(
        evol, x="Année", y="Dép. BD",
        markers=True, line_shape="linear",
        title=f"Évolution des dépenses ({unite_label})"
    )
    fig.update_traces(line=dict(color="#2E6B47", width=3), marker=dict(size=10, color="#2E6B47"))
    fig.update_layout(height=450)
    st.plotly_chart(fig, use_container_width=True)

    # Évolution par secteur
    st.subheader("Évolution par secteur")
    evol_sect = dff.groupby(["Année", "Secteur"])["Dép. BD"].sum().reset_index()
    evol_sect["Dép. BD"] = evol_sect["Dép. BD"] / diviseur

    fig2 = px.line(
        evol_sect, x="Année", y="Dép. BD", color="Secteur",
        color_discrete_map=PALETTE_SECT, markers=True
    )
    fig2.update_layout(height=450)
    st.plotly_chart(fig2, use_container_width=True)

# ─────────────────────────────────────────────────────────────────────────────
# TAB 3 - DONNÉES
# ─────────────────────────────────────────────────────────────────────────────
with tab3:
    st.subheader("Données détaillées")

    # Recherche
    search = st.text_input("🔎 Rechercher", placeholder="Ex: MINFOF, WWF...")

    table_df = dff.copy()
    table_df["Dép. BD"] = (table_df["Dép. BD"] / diviseur).round(2)

    if search:
        mask = table_df.apply(lambda row: any(search.lower() in str(v).lower() for v in row), axis=1)
        table_df = table_df[mask]

    st.dataframe(table_df, use_container_width=True, height=500)

    # Export
    col_exp1, col_exp2 = st.columns(2)
    with col_exp1:
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine="openpyxl") as writer:
            dff.to_excel(writer, index=False, sheet_name="Données filtrées")
        st.download_button(
            "⬇️ Exporter en Excel",
            data=buffer.getvalue(),
            file_name="ADB_Export.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
    with col_exp2:
        st.download_button(
            "⬇️ Exporter en CSV",
            data=dff.to_csv(index=False).encode("utf-8"),
            file_name="ADB_Export.csv",
            mime="text/csv",
        )

# Footer
st.markdown("---")
st.markdown("🌿 ADB Biodiversité Cameroun | Initiative BIOFIN / PNUD")