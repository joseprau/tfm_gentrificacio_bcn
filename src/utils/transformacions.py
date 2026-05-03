import pandas as pd
import geopandas as gpd
from shapely import wkt

def prepare_geodata(df: pd.DataFrame, dim_barris: pd.DataFrame) -> gpd.GeoDataFrame:
    dim = dim_barris[["codi_barri", "nom_barri", "geometria_wgs84"]].copy()
    dim["geometry"] = dim["geometria_wgs84"].apply(wkt.loads)

    merged = dim.merge(df, on="codi_barri", how="left")

    return gpd.GeoDataFrame(merged, geometry="geometry", crs="EPSG:4326")


def get_numeric_columns(df: pd.DataFrame) -> list[str]:
    return [
        col
        for col in df.select_dtypes(include="number").columns
        if col not in "codi_barri"
    ]