# Automotive Supply Chain & Commercial BI System

[![Power BI](https://img.shields.io/badge/Power_BI-Semantic_Model-F2C811?logo=powerbi&logoColor=black)](https://powerbi.microsoft.com/)
[![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-ETL_Pipeline-150458?logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![DAX](https://img.shields.io/badge/DAX-Analytics_Measures-yellowgreen)](https://learn.microsoft.com/dax/)
[![Architecture](https://img.shields.io/badge/Model-Star_Schema-blue)](#-data-architecture--star-schema)

An end-to-end Business Intelligence System developed for **Caminos Autopartes S.L.**, a synthetic enterprise case study representing an automotive spare parts distributor. The project simulates real-world enterprise operations, covering the entire lifecycle: data ingestion from heterogeneous sources (MySQL, CSV, JSON), an automated ETL pipeline implemented in Python, dimensional modeling under a Star Schema, business logic engineering in DAX, and executive reporting in Power BI.

---

## 📌 Executive Overview (STAR Methodology)

### Situation
In dynamic distribution operations, sales, procurement, and warehouse transactions are frequently siloed across transactional relational databases, manual purchase sheets, and semi-structured inventory feeds. In this case study, Caminos Autopartes faced missing pricing records in historical purchase orders and lacked an integrated view of margin contribution, stock turnover, and supplier performance.

### Task
Design and deploy a complete Business Intelligence system to:
1. Ingest simulated multi-source business data (relational MySQL database, procurement CSVs, and nested JSON inventory logs).
2. Automate data extraction, cleaning, and foreign-key price imputation using a modular Python pipeline.
3. Architect an analytical dimensional model (Star Schema) in Power BI with optimized relationship cardinalities.
4. Engineer analytical business measures using DAX to track commercial revenue, procurement spend, and inventory turnover.

### Action
* **Automated Data Engineering (`src/etl.py`):** Built a standalone Python ETL engine using Pandas to normalize JSON structures, resolve schema variations, and impute missing historical purchase values (`PrecioCompra`) via catalog lookups.
* **Dimensional Data Modeling:** Implemented a multi-fact **Star Schema** in Power BI, connecting transactional facts (`ventas2020-2024`, `compras2023-2024`) with core dimension tables (`productos`, `clientes`, `vendedores`, `proveedores`, `ubicaciones`, `categorias`).
* **Analytical DAX Formulation (`dax/`):** Created version-controlled analytical measures for cumulative sales, dynamic average ticket size, annual procurement budget execution, and inventory rotation velocity (`RotacionInventario`).
* **Report Delivery:** Designed an executive dashboard consolidating sales, costs, stock rotation, and product profitability tiers.

### Result
* Delivered a unified semantic model consolidating **€3.77M** in multi-year revenue and **€200.37k** in purchasing volume.
* Enabled automated stock health tracking to pinpoint capital tied up in slow-moving spare parts versus high-velocity consumables.
* Established an extensible, production-ready BI pipeline that decouples heavy transformation logic from front-end visuals.

---

## 🏛️ Data Architecture & Star Schema

The semantic model adheres to a Kimball Star Schema architecture, ensuring analytical query performance and clean filter propagation:

```text
                  +------------------+
                  |    Categorías    |
                  +------------------+
                           |
  +---------------+        |        +------------------+
  |  Proveedores  |  +------------+  |    Vendedores    |
  +---------------+  | Productos  |  +------------------+
          \          +------------+          /
           \         /            \         /
         +---------------+    +---------------+
         | Fact_Compras  |    |  Fact_Ventas  |
         +---------------+    +---------------+
                              /               \
               +---------------+             +---------------+
               |   Clientes    |             |  Ubicaciones  |
               +---------------+             +---------------+
```
---

## 📊 Executive Dashboard & Key Metrics

* Commercial Trajectory: Historical gross revenue (€3.77M, 2020–2024) and transaction value averaging €375.65.
* Procurement Expenditure: Longitudinal visibility into purchasing outlays across suppliers (€200.37k).
* Inventory Rotation: Turnover ratios per SKU to mitigate overstock risks and prevent stockouts.
* Margin Categorization: Rule-based classification of components into High, Medium, and Low profitability brackets.
---

## 📂 Repository Organization

automotive-supplychain-bi-system/
├── .env.example
├── .gitattributes
├── .gitignore
├── Makefile
├── requirements.txt
├── README.md
├── data/
│   ├── raw/                  # Local CSV and JSON files (excluded by .gitignore)
│   │   └── .gitkeep
│   └── processed/            # Tables cleaned up by Python (excluded by .gitignore)
│       └── .gitkeep
├── dax/
│   └── business-measures.dax # DAX Catalog Versioned in Plain Text
├── reports/
│   ├── caminos-autopartes-bi-model.pbix # PBIX file with model and dashboard
│   └── figures/
│       ├── executive_dashboard.pdf       # Screenshot of the dashboard
│       └── star_schema_model.png         # Screenshot of the relational model
├── src/
│   ├── __init__.py
│   ├── config.py             # Dynamic paths and environment variables
│   └── etl.py                # Python Pipeline with Imputation and Calculations
└── tests/
    ├── __init__.py
    └── test-etl-parity.py    # Unit Test for Transformation Parity

---

## 🚀 Reproduction & Setup

### 1. Data Pipeline Execution (Python ETL)
Prerequisites: Python 3.11+

```bash
# Clone the repository
git clone [https://github.com/carladdm/automotive-supplychain-bi-system.git](https://github.com/carladdm/automotive-supplychain-bi-system.git)
cd automotive-supplychain-bi-system

# Create and activate a virtual environment
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# Install dependencies and execute the ETL pipeline
pip install -r requirements.txt
python -m src.etl
```
### 2. Analytical Model Exploration (Power BI)
* Launch Power BI Desktop.  
* Open reports/caminos_autopartes_bi_model.pbix to explore the semantic Star Schema, evaluate DAX measures, and interact with the executive canvas visuals.