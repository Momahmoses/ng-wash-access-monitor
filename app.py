"""Nigeria WASH Access Monitor — Streamlit Dashboard"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import folium
from streamlit_folium import st_folium
import sys, os

sys.path.insert(0, os.path.dirname(__file__))
from data.generate_data import generate_water_points, generate_wash_coverage
from gis.spatial_analysis import build_wash_map

st.set_page_config(page_title="NG WASH Monitor", page_icon="💧", layout="wide")
st.markdown("""<style>
.kpi{background:#0d47a1;color:white;padding:14px;border-radius:8px;text-align:center;}
.kpi-val{font-size:1.9rem;font-weight:700;}
.kpi-lbl{font-size:.8rem;opacity:.85;}
</style>""", unsafe_allow_html=True)


@st.cache_data
def load_data():
    return generate_water_points(500), generate_wash_coverage()


def main():
    water_df, coverage_df = load_data()
    coverage_df["wash_index"] = (
        coverage_df["improved_water_pct"] * 0.4 +
        coverage_df["basic_sanitation_pct"] * 0.35 +
        coverage_df["handwashing_facility_pct"] * 0.25
    ) / 100

    with st.sidebar:
        st.title("💧 WASH Monitor")
        st.caption("Nigeria Water & Sanitation")
        st.divider()
        zone_filter = st.multiselect("Zone", coverage_df["zone"].unique().tolist(),
                                     default=coverage_df["zone"].unique().tolist())
        water_source = st.multiselect("Water Source Type",
                                      water_df["source_type"].unique().tolist(),
                                      default=water_df["source_type"].unique().tolist())
        st.divider()
        st.markdown("**WHO/UNICEF Targets (SDG 6)**")
        st.info("100% safe water by 2030")
        st.info("0% open defecation by 2025")

    cov_filtered = coverage_df[coverage_df["zone"].isin(zone_filter)]
    wp_filtered = water_df[water_df["source_type"].isin(water_source)]

    st.title("💧 Nigeria WASH Access Monitor")
    st.caption("Water · Sanitation · Hygiene gap analysis · GIS + PySpark + Azure Data Lake")
    st.divider()

    c1, c2, c3, c4 = st.columns(4)
    national_water = coverage_df["improved_water_pct"].mean()
    national_san = coverage_df["basic_sanitation_pct"].mean()
    od_states = len(coverage_df[coverage_df["open_defecation_pct"] > 20])
    functional_wp = len(water_df[water_df["is_functional"] == True])
    for col, val, lbl in zip(
        [c1, c2, c3, c4],
        [f"{national_water:.1f}%", f"{national_san:.1f}%", od_states, functional_wp],
        ["Improved Water Access", "Basic Sanitation", "High OD States", "Functional Water Points"]
    ):
        col.markdown(f'<div class="kpi"><div class="kpi-val">{val}</div>'
                     f'<div class="kpi-lbl">{lbl}</div></div>', unsafe_allow_html=True)

    st.divider()
    col_map, col_chart = st.columns([3, 2])

    with col_map:
        st.subheader("🗺 WASH Coverage & Water Points")
        m = build_wash_map(cov_filtered, wp_filtered)
        st_folium(m, width=700, height=460)

    with col_chart:
        st.subheader("📊 WASH Index by State")
        fig = px.bar(
            cov_filtered.sort_values("wash_index"),
            x="wash_index", y="state", orientation="h",
            color="wash_index", color_continuous_scale="Blues",
            labels={"wash_index": "WASH Index", "state": ""},
            height=460,
        )
        fig.update_layout(coloraxis_showscale=False,
                          plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                          margin=dict(l=0, r=10, t=5, b=10))
        st.plotly_chart(fig, use_container_width=True)

    st.divider()
    col_radar, col_src = st.columns(2)

    with col_radar:
        st.subheader("📊 Water vs Sanitation by Zone")
        zone_avg = (cov_filtered.groupby("zone")
                    .agg(water=("improved_water_pct", "mean"),
                         sanitation=("basic_sanitation_pct", "mean"),
                         handwashing=("handwashing_facility_pct", "mean"))
                    .reset_index())
        fig_z = px.bar(zone_avg.melt(id_vars="zone", var_name="Indicator", value_name="Pct"),
                       x="zone", y="Pct", color="Indicator", barmode="group",
                       labels={"zone": "Zone", "Pct": "Coverage (%)"},
                       color_discrete_sequence=["#1565c0", "#43a047", "#f57c00"])
        fig_z.update_layout(plot_bgcolor="rgba(0,0,0,0)", paper_bgcolor="rgba(0,0,0,0)",
                            margin=dict(l=0, r=0, t=5, b=0))
        st.plotly_chart(fig_z, use_container_width=True)

    with col_src:
        st.subheader("🚰 Water Source Type")
        src = wp_filtered["source_type"].value_counts().reset_index()
        src.columns = ["source", "count"]
        fig_src = px.pie(src, names="source", values="count", hole=0.4,
                         color_discrete_sequence=px.colors.sequential.Blues_r)
        fig_src.update_layout(margin=dict(l=0, r=0, t=10, b=0))
        st.plotly_chart(fig_src, use_container_width=True)

    st.divider()
    st.subheader("📋 State WASH Details")
    st.dataframe(
        cov_filtered[["state", "zone", "population", "improved_water_pct",
                      "basic_sanitation_pct", "open_defecation_pct",
                      "diarrhea_prevalence_pct", "wash_index"]]
        .sort_values("wash_index")
        .style.background_gradient(subset=["wash_index"], cmap="Blues")
               .background_gradient(subset=["open_defecation_pct"], cmap="Reds"),
        use_container_width=True, height=300,
    )
    st.caption("Data: Synthetic — replace with UNICEF MICS, NBS NDHS, JMP/WHO-UNICEF data. "
               "Pipeline: Azure Databricks PySpark. Storage: Azure Data Lake.")


if __name__ == "__main__":
    main()
