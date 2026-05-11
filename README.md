[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://share.streamlit.io/deploy?repository=Momahmoses%2Fng-wash-access-monitor&branch=main&mainModule=app.py)

# 💧 Nigeria WASH Access Monitor

SDG 6 progress tracker for Water, Sanitation, and Hygiene (WASH) across Nigeria's 37 states, mapping water point functionality, open defecation zones, and coverage gaps with **GIS**, **PySpark**, **Azure Data Lake**, and **Streamlit**.

## Problem Statement
60+ million Nigerians lack safe drinking water. Open defecation affects 47 million people. North-West and North-East zones have the worst coverage. This platform tracks SDG 6 progress and helps RUWASSA, UNICEF, and state governments prioritize interventions.

## Quick Start
```bash
pip install -r requirements.txt
streamlit run app.py
```

## Data Sources (Production)
- **UNICEF MICS** — Multiple Indicator Cluster Survey
- **NBS NDHS** — Nigeria Demographic and Health Survey
- **JMP/WHO-UNICEF** — Joint Monitoring Programme
- **RUWASSA** — Rural Water Supply and Sanitation Agency
