from pathlib import Path
import streamlit as st
import json
import pandas as pd


from utils.ingesta_dades import load_data, load_dim_barris, load_labels_config
from utils.transformacions import prepare_geodata, get_numeric_columns, get_label_data
from utils.visualitzacio import plot_cluster_map, show_heatmap, show_cluster_profile, show_neighborhood_detail, show_cluster_bar_chart, deltes_bar

def main():
    
    BASE_DIR = Path(__file__).resolve().parent.parent
    CONFIG_PATH = BASE_DIR / "src" / "utils" / "config"
    

    st.set_page_config(
        page_title = "Gentrificació a Barcelona",
        layout="wide"
    )

    st.title("Conglomerats i dinàmiques de gentrificació a Barcelona")
    st.subheader("Aplicació interactiva per explorar els resultats del clustering per barri.")
    st.caption("Autor: Josep Rau")

    
    datasets = load_data(BASE_DIR)
    dim_barris = load_dim_barris(BASE_DIR)
    cluster_config = load_labels_config(CONFIG_PATH)

    dataset_tabs = st.tabs(list(datasets.keys()))
    for tab, periode_seleccionat in zip(dataset_tabs, datasets.keys()):
        with tab:
            df_raw_sel = datasets[periode_seleccionat].copy()
            
            df_sel = get_label_data(df_raw_sel, cluster_config, periode_seleccionat)
            

            gdf = prepare_geodata(df_sel, dim_barris)
            num_cols = get_numeric_columns(df_sel)

            row1_1, row_1_2 = st.columns(2, vertical_alignment="top", border=True)
            row_2_1, row_2_2 = st.columns(2, vertical_alignment="top", border=True)

        #    left_col, right_col = st.columns([1.1, 0.9], gap="large")

            with row1_1:
                plot_cluster_map(gdf, periode_seleccionat)
            with row_2_1:
                show_cluster_profile(df_sel, num_cols)
            with row_1_2:
                show_neighborhood_detail(gdf, key_prefix=periode_seleccionat)
            with row_2_2:
                show_cluster_bar_chart(df_sel, key_prefix=periode_seleccionat)
            if periode_seleccionat != "Deltes":
                show_heatmap(gdf, key_prefix=periode_seleccionat)
            else:
                row_3_1, row_3_2 = st.columns(2, vertical_alignment="top", border=True)
                with row_3_1:
                    show_heatmap(gdf, key_prefix=periode_seleccionat)
                with row_3_2:
                    deltes_bar(gdf)

        

if __name__ == "__main__":
    main()
