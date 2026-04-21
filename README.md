# AIDA — AI Decision Assistant

## 🎯 Objectif

AIDA est un assistant d'aide à la décision pour managers. À partir d'un fichier client CSV, l'application :
- Visualise les KPIs clés (clients, CA, clients à risque)
- Segmente et filtre la base clients
- Propose des recommandations automatiques pour les clients à risque
- Permet de créer et suivre des actions opérationnelles

## 🛠️ Stack technique

- **Python 3.10+**
- **Streamlit** — interface et dashboard
- **pandas** — manipulation de données
- **Plotly** — visualisations
- **streamlit-authenticator** — authentification et rôles

## 📦 Installation

```bash
git clone https://github.com/LaNuggets/PM_PO.git
cd PM_PO
python -m venv .venv
source .venv/bin/activate  # Windows : .venv\Scripts\activate
pip install -r requirements.txt
```

## ▶️ Lancement

```bash
streamlit run app.py
```

Application disponible sur `http://localhost:8501`

### Comptes de test

| Utilisateur | Mot de passe | Rôle |
|-------------|--------------|------|
| `admin` | `admin123` | admin |
| `user` | `user123` | user |

## 🧭 Workflow Scrum

### Board GitHub Project

Cycle imposé : `Product Backlog → Sprint Backlog → In Progress → In Review → Done`

### Convention de nommage des branches

```
type/US-XX-githubuser-nom-court
```

Exemples :
- `feature/US-01-Baptistebdy1-upload-csv`
- `fix/US-03-dcleooo-data-cleaning`
- `docs/US-21-LaNuggets-readme`

### Workflow par user story

1. Créer une issue GitHub avec le template
2. Créer la branche dédiée depuis `dev`
3. Développer la fonctionnalité
4. Ouvrir une PR vers `dev` avec :
   - le numéro de l'issue
   - un résumé du travail
   - ce qu'il reste à faire
   - une demande explicite de review
5. Après review → merge → déplacer la carte en `Done`

## 👥 Équipe

| Membre | Rôle | Scope |
|--------|------|-------|
| Baptiste (`Baptistebdy1`) | Dev Data | Ingestion & qualité des données |
| Alvin (`AlvinDiesel09`) | Dev Front | Visualisation & KPIs |
| Cléo (`dcleooo`) | Dev IA | Recommandations & actions |
| Aurélien (`LaNuggets`) | Cyber / SM | Sécurité, rôles, documentation |

## 📐 Structure du projet

```
PM_PO/
├── app.py                    # Point d'entrée Streamlit
├── modules/
│   ├── ingestion.py          # Import CSV, validation
│   ├── kpi.py                # Calculs de KPIs
│   ├── filters.py            # Filtres segment / risque
│   ├── recommendations.py    # Moteur de reco
│   ├── actions.py            # Gestion des actions
│   └── auth.py               # Authentification et rôles
├── data/
│   ├── sample.csv
│   ├── actions.json
│   ├── users.json
│   └── audit.log.jsonl
├── requirements.txt
└── README.md
```

## 🧪 Démonstration

1. Importer un CSV (`data/sample.csv` fourni)
2. Vérifier l'aperçu des données
3. Consulter le dashboard (KPIs + répartition)
4. Filtrer par segment ou niveau de risque
5. Ouvrir la fiche d'un client à risque → voir la recommandation
6. Créer une action à partir de la reco
7. Changer le statut de l'action
8. (Admin) Consulter le journal d'audit

## 📄 Definition of Done (Phase 1)

- [x] Branche dédiée existe
- [x] Code poussé
- [x] PR vers `dev` ouverte
- [x] Issue mise à jour
- [x] Fonctionnalité démontrable
- [x] Carte déplacée dans le Project
- [x] Critères d'acceptation respectés

## 🔗 Liens utiles

- **Repo :** https://github.com/LaNuggets/PM_PO
- **Board :** https://github.com/LaNuggets/PM_PO/projects
- **Issues :** https://github.com/LaNuggets/PM_PO/issues
