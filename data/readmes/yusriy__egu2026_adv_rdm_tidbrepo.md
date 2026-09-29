# Advanced Research Data Management to Enhance Reuse and Societal Impact of Flux Data
Presented at EGU 2026 under the registration number EGU26 BG8.3. Abstract at https://meetingorganizer.copernicus.org/EGU26/EGU26-11934.html.

## Abstract
Yusri Yusup ORCID 0000-0001-6703-22081, Andreas Rauber 2, Ehsan Jolous Jamshidi ORCID 0000-0002-6611-18331, Japareng Lalung ORCID 0000-0001-5134-64561, and Martin Weise ORCID 0000-0003-4216-302X2
1 School of Industrial Technology, Universiti Sains Malaysia, USM, Malaysia (yusriy@usm.my)
2 TU Wien, Vienna, Austria

Flux measurements play a critical role in informing climate mitigation, ecosystem management, and land–atmosphere interaction studies. However, their broader societal impact is often limited by fragmented data management, insufficient metadata, and unclear version histories that hinder reproducibility, citation, and effective reuse. Here, we demonstrate how the DBRepo data repository system can be used to operationalize principles, dataset versioning, precise identification of arbitrary subsets, and citation practices for flux data, while maintaining alignment with established standards such as those used by FLUXNET. Using flux datasets deposited in DBRepo, we illustrate how explicit versioning and persistent identifiers enable users to track updates, assess the impact of data revisions on analytical outcomes, and ensure that derived results remain interpretable and citable over time. This is particularly relevant for educational and applied contexts, where students, researchers, and non-academic stakeholders require clarity on which data version underpins a given conclusion. Mapping the data representations to established ontologies and FLUXNET conventions, to capture their semantics and units of measurements, further enhances interoperability and lowers the barrier for integrating locally managed flux datasets into broader analysis workflows. By framing versioned, FAIR flux data as a learning and decision-support resource rather than static research output, this work highlights how data infrastructure can directly enhance data literacy, analytical skills, and trust in flux-based evidence. Such practices are essential for translating flux observations into robust, actionable insights with immediate societal benefits.

How to cite: Yusup, Y., Rauber, A., Jamshidi, E. J., Lalung, J., and Weise, M.: Advanced Research Data Management to Enhance Reuse and Societal Impact of Flux Data, EGU General Assembly 2026, Vienna, Austria, 3–8 May 2026, EGU26-11934, https://doi.org/10.5194/egusphere-egu26-11934, 2026.

## Setup
```
python -m venv venv
source venv/bin/activate
pip install -r requirements_full.txt
```

## Overview
This repository demonstrates a **practical research data management (RDM) workflow** for eddy covariance (EC) data using:

- DBRepo → versioned, semantically annotated data storage  
- ERA5 → external reanalysis dataset for comparison  

Focus:
1. **Versioning** (temporal data evolution)  
2. **Interoperability** (semantic alignment EC ↔ ERA5)  

---

## Repository Contents
- `ec_tidbrepo_versioning.ipynb` — DBRepo temporal versioning demonstration  
- `ec_tidbrepo_interoperability.ipynb` — semantic mapping and EC–ERA5 comparison  
- `fec44b0aec5937106a8315efec5fcfbe.grib` — ERA5 data  

---

## Workflow

### 1. Versioning (DBRepo)
- Data is never overwritten  
- Updates create new row versions  
- Enables querying dataset at any time  

Key idea:
> Dataset = evolving system, not static file  

---

### 2. ERA5 Processing
- Load GRIB using `xarray + cfgrib`  
- Variables loaded separately (`t2m`, `slhf`, `sshf`)  
- Flatten `(time, step)` → `valid_time`  

---

### 3. Semantic Mapping

| Semantic Class      | EC Variable       | ERA5 Variable |
|--------------------|-----------------|--------------|
| air_temperature     | air_temperature  | t2m          |
| latent_heat_flux    | le               | slhf         |
| sensible_heat_flux  | h                | sshf         |

---

### 4. Unit Conversion

ERA5 fluxes are accumulated energy (J m⁻²):

    flux (W m⁻²) = flux / 3600

---

### 5. Time Alignment
- ERA5: UTC  
- EC: MYT (UTC+8)  

---

## Key Concepts

### Versioning
- Row-level history (`ts_add`, `ts_delete`)  
- Full reproducibility  
- No data loss  

### Semantics
- Concept URI + unit URI per variable  
- Enables machine-readable interoperability  

### Interoperability
- Mapping based on meaning, not variable names  

---

## Why This Matters
- Reproducible science  
- FAIR data principles  
- Robust EC–model comparison  

---

## Requirements

    pip install pandas xarray cfgrib cdsapi dbrepo

---

## Author
Yusri Yusup  
School of Industrial Technology  
Universiti Sains Malaysia
