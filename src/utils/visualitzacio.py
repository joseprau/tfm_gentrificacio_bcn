import geopandas as gpd
import pandas as pd

import plotly.express as px
import streamlit as st

from utils.transformacions import get_numeric_columns


def plot_cluster_map(gdf: gpd.GeoDataFrame, selected_period: str) -> None:

    map_data = gdf.dropna(subset=["cluster"]).copy()
        
    map_data["cluster_label"] = "Cluster " + map_data["cluster"].astype(str)
    map_data["tooltip_cluster"] = map_data["cluster"].astype(str)

    center = map_data.geometry.unary_union.centroid
    fig = px.choropleth_mapbox(
        map_data,
        geojson=map_data.__geo_interface__,
        locations="codi_barri",
        featureidkey="properties.codi_barri",
        color="cluster_label",
        hover_name="nom_barri",
        hover_data={
            "codi_barri": True,
            "tooltip_cluster": True,
            "cluster_label": False,
        },
        mapbox_style="carto-positron",
        center={"lat": center.y, "lon": center.x},
        zoom=11,
        opacity=0.72,
        title=f"Clusters dels barris de Barcelona ({selected_period})",
    )
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        legend_title_text="Cluster",
        height=620,
    )
    fig.update_traces(marker_line_width=0.8, marker_line_color="white")
    st.plotly_chart(fig, use_container_width=True)



def show_cluster_profile(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame | None:
    st.subheader("Perfil mitja dels clusters")

    if not numeric_cols:
        st.info("No s'han trobat variables numeriques per resumir.")
        return None

    profile = (
        df[numeric_cols].groupby("cluster", dropna=False)
        .mean()
        .round(3)
        .T
        .reset_index()
    )
    st.dataframe(profile, use_container_width=True, hide_index=True)
    return profile


def show_neighborhood_detail(gdf: gpd.GeoDataFrame) -> None:
    st.subheader("Detall del barri")

    options = (
        gdf[["codi_barri", "nom_barri"]]
        .dropna(subset=["nom_barri"])
        .sort_values("nom_barri")
        .assign(label=lambda data: data["nom_barri"] + " (" + data["codi_barri"].astype(str) + ")")
    )

    selected_label = st.selectbox("Escull un barri", options["label"])
    selected_code = options.loc[options["label"] == selected_label, "codi_barri"].iloc[0]
    row = gdf.loc[gdf["codi_barri"] == selected_code].drop(columns=["geometry", "geometria_wgs84"], errors="ignore")

    if row.empty:
        st.info("No s'han trobat dades per al barri seleccionat.")
        return

    record = row.iloc[0]
    cluster_value = record.get("cluster", "No disponible")

    col1, col2 = st.columns(2)
    col1.metric("Barri", record.get("nom_barri", selected_label))
    col2.metric("Cluster", cluster_value)

    numeric_cols = get_numeric_columns(gdf)
    detail = (
        pd.DataFrame(
            {
                "variable": numeric_cols,
                "valor": [record[col] for col in numeric_cols],
            }
        )
        .dropna(subset=["valor"])
        .sort_values("variable")
    )
    st.dataframe(detail, use_container_width=True, hide_index=True)



def show_cluster_bar_chart(df: pd.DataFrame) -> None:
    st.subheader("Comparacio de mitjanes per cluster")

    if "cluster" not in df.columns:
        st.warning("No es pot fer el grafic: falta la columna cluster.")
        return

    numeric_cols = get_numeric_columns(df)
    if not numeric_cols:
        st.info("No hi ha variables numeriques disponibles per comparar.")
        return

    selected_variable = st.selectbox(
        "Variable per comparar",
        numeric_cols
    )
    chart_data = (
        df.groupby("cluster", dropna=False)[selected_variable]
        .mean()
        .reset_index()
        .sort_values("cluster")
    )
    chart_data["cluster_label"] = "Cluster " + chart_data["cluster"].astype(str)

    fig = px.bar(
        chart_data,
        x="cluster_label",
        y=selected_variable,
        color="cluster_label",
        text_auto=".3f",
        labels={
            "cluster_label": "Cluster",
            selected_variable: selected_variable,
        },
        title=f"Mitjana de {selected_variable} per cluster",
    )
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, use_container_width=True)
