import geopandas as gpd
import pandas as pd

import plotly.express as px
import streamlit as st

from utils.transformacions import get_numeric_columns, get_label_data


SHARED_NEIGHBORHOOD_KEY = "selected_codi_barri"


def sync_neighborhood_selection(widget_key: str) -> None:
    st.session_state[SHARED_NEIGHBORHOOD_KEY] = st.session_state[widget_key]


def plot_cluster_map(gdf: gpd.GeoDataFrame, selected_period: str) -> None:
    st.subheader(f"Clusters dels barris de Barcelona ({selected_period})")
    map_data = gdf.dropna(subset=["cluster"]).copy()
        
    map_data["cap_nom_barri"] = map_data["nom_barri"].str.capitalize()
    map_data["cluster_label"] = "Cluster " + map_data["cluster"].astype(str)
    map_data["tooltip_cluster"] = map_data["cluster"].astype(str)

    center = map_data.geometry.unary_union.centroid
    fig = px.choropleth_mapbox(
        map_data,
        geojson=map_data.__geo_interface__,
        locations="codi_barri",
        featureidkey="properties.codi_barri",
        color="nom",
        color_discrete_map=map_data.to_dict()["color"],
        hover_name="cap_nom_barri",
        hover_data={
            "codi_barri": True,
            "tooltip_cluster": False,
            "cluster_label": False,
            "cluster": True,
            #"poblacio_total": True if "poblacio_total" in map_data.columns else False,
            #"import_euros": True

        },
        mapbox_style="carto-positron",
        center={"lat": center.y, "lon": center.x},
        zoom=11,
        opacity=1
    )
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        legend_title_text="Cluster",
        height=620,
    )
    fig.update_traces(marker_line_width=0.8, marker_line_color="white")
    st.plotly_chart(fig, width='stretch')

def show_cluster_profile(df: pd.DataFrame, numeric_cols: list) -> pd.DataFrame | None:
    st.subheader("Perfil mitja dels clusters")

    if not numeric_cols:
        st.info("No s'han trobat variables numeriques per resumir.")
        return None

    profile = (
        df.groupby("cluster", dropna=False)[numeric_cols]
        .mean()
        .round(3)
        .T
        .reset_index()
    )
    st.dataframe(profile, width='stretch', height="content", hide_index=True)
    return profile


def show_neighborhood_detail(gdf: gpd.GeoDataFrame, key_prefix: str) -> None:
    st.subheader("Detall del barri")

    options = (
        gdf[["codi_barri", "nom_barri"]]
        .dropna(subset=["nom_barri"])
        .drop_duplicates(subset=["codi_barri"])
        .sort_values("nom_barri")
        .assign(label=lambda data: data["nom_barri"] + " (" + data["codi_barri"].astype(str) + ")")
    )

    available_codes = options["codi_barri"].tolist()
    if not available_codes:
        st.info("No hi ha barris disponibles per seleccionar.")
        return

    shared_code = st.session_state.get(SHARED_NEIGHBORHOOD_KEY, available_codes[0])
    if shared_code not in available_codes:
        shared_code = available_codes[0]
        st.session_state[SHARED_NEIGHBORHOOD_KEY] = shared_code

    widget_key = f"{key_prefix}_barri"
    st.session_state[widget_key] = shared_code

    labels_by_code = dict(zip(options["codi_barri"], options["label"]))
    selected_code = st.selectbox(
        "Escull un barri",
        available_codes,
        format_func=lambda code: labels_by_code.get(code, str(code)),
        key=widget_key,
        on_change=sync_neighborhood_selection,
        args=(widget_key,),
    )
    row = gdf.loc[gdf["codi_barri"] == selected_code].drop(columns=["geometry", "geometria_wgs84"], errors="ignore")

    if row.empty:
        st.info("No s'han trobat dades per al barri seleccionat.")
        return

    record = row.iloc[0]
    cluster_value = record.get("nom", "No disponible")
    selected_label = labels_by_code.get(selected_code, str(selected_code))

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
    st.dataframe(detail, width='stretch', height="content", hide_index=True)



def show_cluster_bar_chart(df: pd.DataFrame, key_prefix: str) -> None:
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
        numeric_cols,
        key=f"{key_prefix}_cluster_variable",
    )
    chart_data = (
        df.groupby(["nom", "color"], dropna=False)[selected_variable]
        .mean()
        .reset_index()
        .sort_values("nom")
    )
    

    fig = px.bar(
        chart_data,
        x="nom",
        y=selected_variable,
        color="nom",
        color_discrete_map=chart_data.to_dict()["color"],
        text_auto=".2f",
        labels={
            "cluster_label": "Cluster",
            selected_variable: selected_variable,
        },
        title=f"Mitjana de {selected_variable} per cluster",
    )
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, width='stretch')


def show_heatmap(gdf: gpd.GeoDataFrame, key_prefix: str) -> None:
    st.subheader("Heatmap")

    
    numeric_cols = get_numeric_columns(gdf)
    if not numeric_cols:
        st.info("No hi ha variables numeriques disponibles per comparar.")
        return
    
    selected_variable = st.selectbox(
        "Variable per al heatmap",
        numeric_cols,
        index=0,
        key=f"{key_prefix}_heatmap_variable",
    )

    map_data = gdf.dropna(subset=[selected_variable]).copy()
    if map_data.empty:
        st.warning("No hi ha dades disponibles per a la variable seleccionada.")
        return

    map_data["cap_nom_barri"] = map_data["nom_barri"].str.capitalize()
    center = map_data.geometry.unary_union.centroid
    fig = px.choropleth_mapbox(
        map_data,
        geojson=map_data.__geo_interface__,
        locations="codi_barri",
        featureidkey="properties.codi_barri",
        color=selected_variable,
        color_continuous_scale="greens",
        hover_name="cap_nom_barri",
        hover_data={
            "codi_barri": True,
            selected_variable: True,
        },
        mapbox_style="carto-positron",
        center={"lat": center.y, "lon": center.x},
        zoom=11,
        opacity=0.75,
        title=f"Heatmap de {selected_variable} a Barcelona",
    )
    fig.update_layout(
        margin={"r": 0, "t": 50, "l": 0, "b": 0},
        coloraxis_colorbar={"title": selected_variable},
        height=620,
    )
    fig.update_traces(marker_line_width=0.8, marker_line_color="white")
    st.plotly_chart(fig, width='stretch')

def deltes_bar(gdf):
    st.subheader("Variació per variable")
    numeric_cols = get_numeric_columns(gdf)

    chart_data = (
        gdf[numeric_cols].mean().reset_index(name="Valor").sort_values("Valor")
    )
    
    fig = px.bar(
        chart_data,
        x="Valor",
        y="index",
        text_auto=".2f"
    )
    fig.update_layout(showlegend=False, xaxis_title=None, yaxis_title=None)
    st.plotly_chart(fig, width='stretch')
