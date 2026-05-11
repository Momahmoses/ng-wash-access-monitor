"""GIS: Water point mapping, WASH coverage choropleth, open defecation zones."""
import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
import folium
from folium.plugins import HeatMap, MarkerCluster
import sys, os

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from data.generate_data import generate_water_points, generate_wash_coverage


def build_wash_map(coverage_df: pd.DataFrame, water_df: pd.DataFrame) -> folium.Map:
    m = folium.Map(location=[9.08, 8.67], zoom_start=6, tiles="CartoDB positron")

    for _, row in coverage_df.iterrows():
        wash_idx = (row["improved_water_pct"] * 0.4 + row["basic_sanitation_pct"] * 0.35 +
                    row["handwashing_facility_pct"] * 0.25) / 100
        color = ("#1565c0" if wash_idx >= 0.70 else "#43a047" if wash_idx >= 0.50
                 else "#f57c00" if wash_idx >= 0.30 else "#d32f2f")
        folium.CircleMarker(
            location=[row.lat, row.lon],
            radius=max(8, (1 - wash_idx) * 28),
            color=color, fill=True, fill_opacity=0.6,
            popup=(f"<b>{row['state']}</b><br>"
                   f"Water Access: {row['improved_water_pct']}%<br>"
                   f"Sanitation: {row['basic_sanitation_pct']}%<br>"
                   f"OD Rate: {row['open_defecation_pct']}%"),
            tooltip=row["state"],
        ).add_to(m)

    cluster = MarkerCluster(name="Water Points").add_to(m)
    for _, wp in water_df[water_df["is_safe"] == True].head(200).iterrows():
        source_colors = {"Borehole": "blue", "Pipe-borne": "green",
                         "Hand Pump": "lightblue", "Surface Water": "red"}
        folium.CircleMarker(
            location=[wp.lat, wp.lon], radius=3,
            color=source_colors.get(wp["source_type"], "gray"),
            fill=True, fill_opacity=0.8,
            popup=f"{wp['source_type']} | Pop: {wp['population_served']:,}",
        ).add_to(cluster)

    heat = [[r.lat, r.lon, r["open_defecation_pct"] / 100] for _, r in coverage_df.iterrows()]
    HeatMap(heat, radius=20, blur=18, min_opacity=0.3,
            gradient={"0.3": "yellow", "0.6": "orange", "1.0": "red"},
            name="OD Heatmap").add_to(m)

    folium.LayerControl().add_to(m)
    return m


if __name__ == "__main__":
    coverage = generate_wash_coverage()
    water = generate_water_points()
    m = build_wash_map(coverage, water)
    os.makedirs("app", exist_ok=True)
    m.save("app/wash_map.html")
    print("Map saved.")
