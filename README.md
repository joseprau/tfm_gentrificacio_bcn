# Introducció
Treball de fi de Master centrat en la gentrificació als barris de Barcelona.
# Estructura del projecte
```bash
├── data
│   ├── raw
│   ├── processed
│   ├── dimensions
│   ├── modelling
├── notebooks
│   └── ingestio_demografiques.ipynb
│   └── ingestio_economiques.ipynb
├── src
│   └── utils.py
│   └── __init__.py
├── env
├── requirements.txt
├── README.md
├── LICENSE
└── .gitignore
```
# Fonts
S' han integrat diferents fonts de dades de tipologia socio econòmica i d' habitatge. En el procés d' ingesta i de preprocessament, s' han combinat per obtenir un dataset per construir el model de ML i un altre per enriquir l'anàlisi de dades.
## Dades Demogràfiques
- **Població Total per barri:**
- **Població per nacionalitat (Espanya, Resta UE i Resta del món) per barri:**
- **Població per regió de continent per barri:**
- **Població per nivell d'estudis i nacionalitat (Espanya, Resta UE i Resta del Món) per barri:**
- **Població per grup d'edat i nacionalitat (Espanya, Resta UE i Resta del Món) per Barri:**  
## Dades Econòmiques
- **Renda neta Mitjana per Persona i barri:** [Idescat](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/renda-tributaria-per-persona-atlas-distribucio)
- **Index Gini per barri:** [Idescat](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/atles-renda-index-gini)
## Dades Urbanes
# EDA - Exploratory Data Analysis
