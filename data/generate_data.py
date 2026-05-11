import pandas as pd
import numpy as np
import os

STATES = [
    ("Lagos", 6.5244, 3.3792, "SW", 15388000),
    ("Kano", 12.0022, 8.5920, "NW", 13076000),
    ("Kaduna", 10.5222, 7.4383, "NW", 8252000),
    ("Rivers", 4.8156, 7.0498, "SS", 7303000),
    ("Oyo", 7.3775, 3.9470, "SW", 7840000),
    ("Abuja FCT", 9.0765, 7.3986, "NC", 3564000),
    ("Anambra", 6.2104, 6.9623, "SE", 5527000),
    ("Borno", 11.8846, 13.1571, "NE", 5860000),
    ("Imo", 5.4527, 7.0201, "SE", 4856000),
    ("Delta", 5.5320, 5.8987, "SS", 5663000),
    ("Adamawa", 9.3265, 12.3984, "NE", 4253000),
    ("Plateau", 9.2182, 9.5179, "NC", 4200000),
    ("Bauchi", 10.3158, 9.8442, "NE", 6537000),
    ("Sokoto", 13.0059, 5.2476, "NW", 4998000),
    ("Katsina", 12.9908, 7.6018, "NW", 8036000),
    ("Jigawa", 12.2280, 9.5616, "NW", 5829000),
    ("Kebbi", 11.4943, 4.2333, "NW", 4459000),
    ("Zamfara", 12.1222, 6.2236, "NW", 4515000),
    ("Niger", 10.0008, 5.5981, "NC", 5559000),
    ("Kwara", 8.9669, 4.3873, "NC", 3194000),
    ("Nassarawa", 8.4994, 8.1997, "NC", 2523000),
    ("Kogi", 7.7337, 6.6906, "NC", 4473000),
    ("Benue", 7.3369, 8.7404, "NC", 5741000),
    ("Taraba", 7.9993, 10.7741, "NE", 3066000),
    ("Yobe", 12.2939, 11.4390, "NE", 3294000),
    ("Gombe", 10.2791, 11.1673, "NE", 3256000),
    ("Ogun", 6.9980, 3.4737, "SW", 5217000),
    ("Osun", 7.5629, 4.5624, "SW", 4705000),
    ("Ekiti", 7.6218, 5.2311, "SW", 3270000),
    ("Ondo", 7.0003, 5.0000, "SW", 4671000),
    ("Edo", 6.3350, 5.6037, "SS", 4737000),
    ("Bayelsa", 4.7719, 6.0699, "SS", 2278000),
    ("Cross River", 5.9631, 8.3305, "SS", 4059000),
    ("Akwa Ibom", 5.0527, 7.9335, "SS", 5450000),
    ("Enugu", 6.4584, 7.5464, "SE", 4411000),
    ("Ebonyi", 6.2649, 8.0137, "SE", 2880000),
    ("Abia", 5.3671, 7.4948, "SE", 3728000),
]

WATER_SOURCE_TYPES = ["Borehole", "Pipe-borne", "Hand Pump", "Surface Water",
                       "Sachet/Bottled", "Well", "Rainwater Harvesting"]
SANITATION_TYPES = ["Flush Toilet", "Pit Latrine", "VIP Latrine",
                    "Open Defecation", "Communal Toilet"]


def generate_water_points(n: int = 600) -> pd.DataFrame:
    np.random.seed(42)
    records = []
    for i in range(n):
        state_info = STATES[np.random.randint(len(STATES))]
        state, slat, slon, zone, pop = state_info
        records.append({
            "point_id": f"WP-{i+1:05d}",
            "state": state, "zone": zone,
            "lat": slat + np.random.uniform(-0.8, 0.8),
            "lon": slon + np.random.uniform(-0.8, 0.8),
            "source_type": np.random.choice(WATER_SOURCE_TYPES,
                           p=[0.30, 0.20, 0.15, 0.15, 0.10, 0.07, 0.03]),
            "is_functional": np.random.choice([True, False], p=[0.72, 0.28]),
            "is_safe": np.random.choice([True, False], p=[0.60, 0.40]),
            "population_served": int(np.random.exponential(2000)),
            "year_installed": int(np.random.randint(1990, 2024)),
            "distance_to_households_km": round(np.random.exponential(1.5), 2),
            "seasonal_availability": np.random.choice(["Year-round", "Seasonal"], p=[0.65, 0.35]),
        })
    return pd.DataFrame(records)


def generate_wash_coverage() -> pd.DataFrame:
    np.random.seed(42)
    records = []
    for state, slat, slon, zone, pop in STATES:
        improved_water = np.random.uniform(35, 95) if zone in ("SW", "SS", "SE") else np.random.uniform(20, 75)
        basic_sanitation = np.random.uniform(20, 80) if zone in ("SW", "SS", "SE") else np.random.uniform(10, 55)
        records.append({
            "state": state, "zone": zone, "lat": slat, "lon": slon, "population": pop,
            "improved_water_pct": round(improved_water, 1),
            "basic_sanitation_pct": round(basic_sanitation, 1),
            "open_defecation_pct": round(max(0, np.random.uniform(5, 50) if zone in ("NW", "NE") else np.random.uniform(0, 20)), 1),
            "handwashing_facility_pct": round(np.random.uniform(20, 85), 1),
            "water_stress_index": round(np.random.uniform(0.2, 0.9), 3),
            "diarrhea_prevalence_pct": round(np.random.uniform(5, 35), 1),
            "waterborne_disease_rate": round(np.random.uniform(10, 120), 0),
        })
    return pd.DataFrame(records)


def save_all(output_dir: str = "data"):
    os.makedirs(output_dir, exist_ok=True)
    generate_water_points().to_csv(f"{output_dir}/water_points.csv", index=False)
    generate_wash_coverage().to_csv(f"{output_dir}/wash_coverage.csv", index=False)
    print("WASH data generated.")


if __name__ == "__main__":
    save_all()
