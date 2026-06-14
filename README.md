# Pipeline de Machine learning - Modèle de prediction de consomation electrique de la ville de Seattle (2016)
***
![Python](https://img.shields.io/badge/Python-3.13-blue)
![scikit-learn](https://img.shields.io/badge/scikit--learn-1.8.0-orange)
![BentoML](https://img.shields.io/badge/BentoML-1.4.39-purple)
![Pydantic](https://img.shields.io/badge/Pydantic-2.13.4-green)
![Docker](https://img.shields.io/badge/Docker-✓-blue)
![Render](https://img.shields.io/badge/Cloud-Render-46E3B7)
______

## Présentation
La municipalité américaine de Seattle souhaite prédire sa consommation électrique de ses bâtiments en se basant uniquement sur leurs caractéristiques.Pour satisfaire cette mission,  nous avons développé un modèle de prediction à partir d'un dataset composé des détails et de mesures en 2016 sur l'ensemble des infrastuctures majeures de la ville. Le modèle de prediction sera disponible via une API en cloud computing. Nous pourrons au final executer des requêtes avec des détails differents afin de prédir la consommation d'un bâtiment particulier.
La procedure est faite via des scripts python, le modèle est ensuite pousser sur docker hub et déployé via l'API de render.

______

## Architecture

Techniquement cela c'est presque entièrement sous Python sur differends notebook et scripts, et les librairies nécessaires. Afin d'accelerer la tache, le modele a été enregistrer avec bentoml et l'image du du container pousser sur docker hub pour ensuite être déployé vias l'API render.

```
[Dataset Seattle 2016 — 3376 bâtiments]
        │
        ▼
[Notebooks Jupyter]
  bloc1_EDA → bloc2_FE → bloc3_model
  (1668 non-résidentiels → 16 features → GradientBoosting R²=0.637)
        │
        ▼
[BentoML Model Store]
  model_nr_seattle_v1 (Pipeline + feature_names)
        │
        ▼
[bentoml build + containerize]
        │
        ▼
[Docker Hub — mohandab/energy_prediction:latest]
        │
        ▼
[Render Cloud — Plan Free]
  URL : https://energy-prediction-mq7rbuthgo5h7lyd.onrender.com
  Port : 3000
        │
        ▼
Utilisateur
  POST /predict (JSON 13 champs)
        │
        ▼
validation.py (Pydantic — types, bornes, valeurs autorisées)
        │
        ▼
service.py (recalcul features dérivées → DataFrame → predict → expm1)
        │
        ▼
Réponse : {"consommation_estimee_kbtu": ______}

```
______

## Données

Source : [Seattle Building Energy Benchmarking 2016](https://data.seattle.gov/dataset/2016-Building-Energy-Benchmarking/2bpz-gwpy)
3 376 bâtiments → 1 668 non-résidentiels retenus · 16 features sélectionnées après feature engineering

______

## Prérequis

| Outil | Version | Remarque |
|---|---|---|
| Python | 3.13 | local |
| Docker | Latest | local |
| BentoML | 1.4.39 | local |
| Cloud computing | - | Render, GCP, AWS ou autre au choix |

______

## Installation

```bash
# 1. Dans la racine du projet, pour produire le dockerfile.yaml et le requirements.txt
bentoml build

# 2. Produit l'image qu'il faudraensuite pousser sur docker hub
bentoml containerize <nom du service bento>

# 3. S'authentifier sur docker
docker login 

# 4. Tager l'image avec son nom d'utilisateur
docker tag <nom du service> <username/nom du service>

# 5. Pousser l'image sur docker hub
docker push <username/nom du service>

# 6. Se connecter à son compte cloud (Render, GCP, AWS...)
# et déployer l'image en renseignant : docker.io/<username/nom du service>
# Port : 3000
```
______

## Utilisation

| Commande | Description |
|---|---|
| `bentoml serve py.service:EnergyPrediction` | Lancer le serveur en local |
| `bentoml list` | Lister les Bentos construits |
| `bentoml models list` | Lister les modèles sauvegardés |
| `docker run -p 3000:3000 energy_prediction:latest` | Lancer le container Docker |
| `docker ps` | Voir les containers en cours |
| `docker stop <container_id>` | Arrêter un container |

## Exemple de requête

```bash
curl -X POST https://energy-prediction-mq7rbuthgo5h7lyd.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{
    "input_data": {
      "BuildingType": "NonResidential",
      "PrimaryPropertyType": "Large Office",
      "Neighborhood": "DOWNTOWN",
      "NumberofBuildings": 1,
      "NumberofFloors": 10,
      "YearBuilt": 1985,
      "sum_energy_use": 2,
      "sum_types_use": 1,
      "PrimaryPropertyUseTypeGFA": 50000,
      "SecondLargestPropertyUseTypeGFA": 0,
      "ThirdLargestPropertyUseTypeGFA": 0,
      "use_steam": 0,
      "has_third_use": 0
    }
  }'
```

**Réponse :**
```json
{"consommation_estimee_kbtu": 219062753.89}
```
______

## Structure du projet
<!-- INDICE : Arbre du répertoire avec un commentaire par fichier/dossier important -->
<!-- Utilise la commande tree pour générer la base puis commente -->

```
.
├── bentofile.yaml
├── data
│   ├── 2016_Building_Energy_Benchmarking.csv
│   ├── df_s4.csv
│   ├── feat_corr_cleaning.csv
│   └── feat_corr_lp2.csv
├── docs
│   ├── feat_corr_lp2.ods
│   └── feat_corr_lp2.ods.bak
├── exit
├── main.py
├── models
├── notebooks
│   ├── p6-bloc1-EDA.ipynb
│   ├── p6-bloc2-fe.ipynb
│   ├── p6-bloc3-model.ipynb
│   └── p6-profiling.ipynb
├── p6-ml.code-workspace
├── py
│   ├── __init__.py
│   ├── service.py
│   └── validation.py
├── pyproject.toml
├── README.md
└── uv.lock
```
______

## Tests

**Validation des données (Pydantic)**
```bash
python py/validation.py
```
Vérifie qu'une requête valide est acceptée et qu'une requête invalide (ex : BuildingType="Maison") est rejetée.

**API locale**
```bash
bentoml serve py.service:EnergyPrediction
# Ouvrir http://localhost:3000 → Swagger → Try it out → Execute
```
Vérifie que l'endpoint /predict retourne un code 200 avec une prédiction en kBtu.

**Container Docker**
```bash
docker run -p 3000:3000 energy_prediction:latest
# Tester via curl ou Swagger sur http://localhost:3000
```
Vérifie que le container se lance et répond comme en local.

**API Cloud (Render)**
```bash
curl -X POST https://energy-prediction-mq7rbuthgo5h7lyd.onrender.com/predict \
  -H "Content-Type: application/json" \
  -d '{"input_data": {"BuildingType": "NonResidential", ...}}'
```
Vérifie que l'API déployée retourne un code 200.

______

## Limites connues
1. Données estimées K-12 - Dans la variable estimée, 76.5% étaient des écoles de la ville, elles était conserver car elle constituait une donnée importante du dataset. Par conséquent le Le modèle a potentiellement appris un pattern artificiel. Il est neessaie de recuperer les vraies mesures et relancerla modélisation vu le poids de K12 dans les features importances.

2. "Non-résidentiel" est une catégorie trop large. Il existe des différences significative et notables à l'interieure même du decoupage. Cela génère des outliers de bonne natures et des informations essentielles. Un entrepôt frigorifique et un store, un un bureau au sont tous les trois non-résidentiels mais n'ont rien à voir en consommation. En production, il faut revoir l'approche de ou des modelisations sur le dataset, isoler les infrastructures.

3. Le projet doit être daa centric. En effet, 39% de variance reste inexpliquée, les features structurelles ne suffisent pas. Il manque des variables comme le type d'isolation, le taux d'occupation, la météo, le comportements des usagers. Il faut enrichir le dataset de ses données pour atteindre un prediction bien plus élevée.

4. Cold start Render, pour mon plan gratuit, render éteint le serveur après inactivité, et la première requête est lente (~30s), il faut anticiper pour des demos.

______

## Auteur
Mohand Abaran - Data Engineer 
GitHub: [mohandab-dataeng](https://github.com/mohandab-dataeng)

______