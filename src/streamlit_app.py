from pathlib import Path
import geopandas as gpd
import streamlit as st
from shapely import wkt


from utils.ingesta_dades import load_data, load_dim_barris
from utils.transformacions import prepare_geodata, get_numeric_columns
from utils.visualitzacio import plot_cluster_map, show_cluster_profile, show_neighborhood_detail, show_cluster_bar_chart

def main():

    BASE_DIR = Path(__file__).resolve().parent.parent

    st.set_page_config(
        page_title = "Gentrificació a Barcelona",
        layout="wide"
    )

    st.title("Conglomerats i dinàmiques de gentrificació a Barcelona")
    st.caption("Aplicació interactiva per explorar els resultats del clustering per barri.")

    
    datasets = load_data(BASE_DIR)
    dim_barris = load_dim_barris(BASE_DIR)

    with st.sidebar:
        st.header("Filtres")
        periode_seleccionat = st.radio(
            "Conjunt de dades",
            options= [d for d in datasets.keys()],
            index= 0
        )

    df_sel = datasets[periode_seleccionat].copy()
    gdf = prepare_geodata(df_sel, dim_barris)
    num_cols = get_numeric_columns(df_sel)

    left_col, right_col = st.columns([1.1, 0.9], gap="large")

    with left_col:
        plot_cluster_map(gdf, periode_seleccionat)
        show_cluster_profile(df_sel, num_cols)

    with right_col:
        show_neighborhood_detail(gdf)
        show_cluster_bar_chart(df_sel)


if __name__ == "__main__":
    main()