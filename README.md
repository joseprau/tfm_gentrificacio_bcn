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
- **Renda neta Mitjana per Persona i barri:** [Open Data](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/renda-tributaria-per-persona-atlas-distribucio)
- **Index Gini per barri:** [Open Data](https://opendata-ajuntament.barcelona.cat/data/ca/dataset/atles-renda-index-gini)
## Dades Urbanes
- **Incidents per barri:** [Portal de dades Barcelona](https://portaldades.ajuntament.barcelona.cat/ca/microdades/8181e647-083e-48ec-b8a3-68b25b91ab83)
- **Nombre de locals comercials actius per sector d’activitat i grup d’activitat:**  [Portal de dades Barcelona](Nombre de locals comercials actius per sector d’activitat i grup d’activitat)
## Dades Habitatge
- **Preu mitjà per superfície (€/m²) del lloguer d'habitatges:** [Portal de dades Barcelona](https://portaldades.ajuntament.barcelona.cat/ca/estad%C3%ADstiques/5ibudgqbrb)
- **Nombre d’habitatges d’ús turístic:** [Portal de dades Barcelona](https://portaldades.ajuntament.barcelona.cat/ca/estad%C3%ADstiques/z1wuyvykvf)
- **Nombre dels locals d'habitatge segons superfície de la ciutat de Barcelona:** [Portal de dades Barcelona](Nombre dels locals d'habitatge segons superfície de la ciutat de Barcelona)
# EDA - Exploratory Data Analysis
