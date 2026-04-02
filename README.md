# 🌿 ADB Biodiversité Cameroun — Tableau de bord interactif

Tableau de bord Streamlit pour l'**Analyse des Dépenses Biodiversité (ADB)** selon la méthodologie BIOFIN / PNUD.

---

## 🚀 Déploiement sur Streamlit Cloud (recommandé)

### Étape 1 — Préparer le secret DATA_B64

Le fichier Excel est **encodé en base64** et stocké comme secret Streamlit.  
Il ne sera **jamais visible** des utilisateurs qui accèdent à l'application.

Pour générer la valeur `DATA_B64` depuis votre fichier Excel :

```python
import base64
with open("ADB_Cameroun_Simulation.xlsx", "rb") as f:
    print(base64.b64encode(f.read()).decode())
```

### Étape 2 — Déployer sur Streamlit Cloud

1. Poussez ce dépôt sur GitHub (**sans** le fichier `.streamlit/secrets.toml`)
2. Allez sur [share.streamlit.io](https://share.streamlit.io)
3. Connectez votre repo GitHub et sélectionnez `app.py`
4. Dans **Settings → Secrets**, ajoutez :

```toml
DATA_B64 = "votre_chaine_base64_ici"
```

5. Cliquez **Deploy** — votre app est en ligne 🎉

---

## 💻 Lancement en local

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Créer le fichier de secrets local
mkdir -p .streamlit
# Copiez votre secrets.toml dans .streamlit/secrets.toml

# 3. Lancer l'application
streamlit run app.py
```

---

## 📁 Structure du projet

```
.
├── app.py                    # Application principale
├── requirements.txt          # Dépendances Python
├── .gitignore                # Protège les données sensibles
├── README.md                 # Ce fichier
└── .streamlit/
    └── secrets.toml          # ⚠️ GITIGNORE — ne pas pousser
```

> ⚠️ **Le fichier `.streamlit/secrets.toml` est protégé par `.gitignore`.**  
> Ne le committez jamais. Configurez les secrets directement dans Streamlit Cloud.

---

## 🗂️ Pages du tableau de bord

| Onglet | Contenu |
|---|---|
| 📊 Catégories BIOFIN | Barres + camembert + heatmap |
| 📈 Évolution temporelle | Courbes, taux de croissance, aires empilées |
| 🏛️ Par secteur | Public / ONG / Privé / PTF + sunburst |
| 🔍 Analyse détaillée | Scatter, boxplots, tableau croisé, part PIB |
| 📋 Données brutes | Tableau filtrable + export Excel/CSV |

## 🎛️ Filtres disponibles

- Années (2020–2024)
- Secteurs (Public, ONG/OSC, Secteur Privé, PTF)
- Catégories BIOFIN (9 catégories)
- Institutions / Acteurs
- Unité : Millions FCFA ou Milliards FCFA

---

## 🔒 Sécurité des données

- La base de données n'est **jamais exposée directement** — elle est chargée depuis les Secrets Streamlit
- Les utilisateurs peuvent uniquement **exporter leurs données filtrées**
- Le fichier source Excel n'est pas accessible via l'interface

---

*🌿 Initiative BIOFIN · PNUD · Données 2020–2024*
