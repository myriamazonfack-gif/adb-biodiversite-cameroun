# 🌿 ADB Biodiversité Cameroun — Application Streamlit

Tableau de bord interactif pour l'Analyse des Dépenses Biodiversité (ADB)
basé sur la méthodologie BIOFIN / PNUD.

---

## 🚀 Lancement en 3 étapes

### Étape 1 — Installer les dépendances
```bash
pip install -r requirements.txt
```

### Étape 2 — Lancer l'application
```bash
streamlit run app_adb.py
```

### Étape 3 — Ouvrir dans le navigateur
L'application s'ouvre automatiquement à :
```
http://localhost:8501
```

---

## 📁 Fichiers nécessaires

| Fichier | Rôle |
|---|---|
| `app_adb.py` | Application principale Streamlit |
| `requirements.txt` | Dépendances Python |
| `ADB_Cameroun_Simulation.xlsx` | Données fictives pour tester |

---

## 📂 Comment utiliser vos vraies données

1. Ouvrez votre fichier Excel ADB rempli
2. Dans l'application, utilisez le bouton **"📂 Charger votre fichier Excel"** dans la barre latérale
3. L'application chargera automatiquement la feuille **PowerBI_Data**

> ✅ Le fichier doit contenir une feuille "PowerBI_Data" avec les colonnes :
> Secteur | Institution | Programme | Catégorie BIOFIN | Coefficient (%) | Année | Dépense Totale | Dépense BD

---

## 🗂️ Pages du tableau de bord

1. **📊 Catégories BIOFIN** — Barres + camembert + heatmap des 9 catégories
2. **📈 Évolution temporelle** — Courbes + taux de croissance + zones empilées
3. **🏛️ Par secteur** — Public / ONG / Privé / PTF + sunburst hiérarchique
4. **🔍 Analyse détaillée** — Scatter, boxplots coefficients, tableau croisé, part PIB
5. **📋 Données brutes** — Tableau filtrable + export Excel/CSV

---

## ⚙️ Filtres disponibles

- Années (2020–2024)
- Secteurs (Public, ONG/OSC, Secteur Privé, PTF)
- Catégories BIOFIN (9 catégories)
- Institutions / Acteurs
- Unité : Millions FCFA ou Milliards FCFA
