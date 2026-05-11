"""WASH Access PySpark Pipeline — Azure Databricks."""
from pyspark.sql import SparkSession
from pyspark.sql import functions as F
import os


def get_spark():
    return SparkSession.builder.appName("WASHPipeline").getOrCreate()


def compute_wash_index(coverage_df):
    return (
        coverage_df
        .withColumn(
            "wash_composite_index",
            (F.col("improved_water_pct") * 0.40 +
             F.col("basic_sanitation_pct") * 0.35 +
             F.col("handwashing_facility_pct") * 0.25) / 100
        )
        .withColumn(
            "wash_tier",
            F.when(F.col("wash_composite_index") >= 0.70, "Adequate")
             .when(F.col("wash_composite_index") >= 0.50, "Developing")
             .when(F.col("wash_composite_index") >= 0.30, "Limited")
             .otherwise("Critical")
        )
    )


def compute_water_point_status(water_df):
    return (
        water_df
        .groupBy("state", "zone")
        .agg(
            F.count("*").alias("total_points"),
            F.sum(F.col("is_functional").cast("int")).alias("functional_points"),
            F.sum(F.col("is_safe").cast("int")).alias("safe_points"),
            F.avg("population_served").alias("avg_pop_served"),
            F.avg("distance_to_households_km").alias("avg_distance_km"),
        )
        .withColumn(
            "functionality_rate",
            F.col("functional_points") / F.col("total_points")
        )
    )


if __name__ == "__main__":
    spark = get_spark()
    coverage = spark.read.csv("data/wash_coverage.csv", header=True, inferSchema=True)
    water = spark.read.csv("data/water_points.csv", header=True, inferSchema=True)
    wash_idx = compute_wash_index(coverage)
    wash_idx.show(10)
    wp_status = compute_water_point_status(water)
    wp_status.show(10)
    spark.stop()
