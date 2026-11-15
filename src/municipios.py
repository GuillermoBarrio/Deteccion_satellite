import geopandas as gpd
import streamlit as st
from pathlib import Path

# Definimos la ruta al shapefile de forma relativa a la raíz del proyecto
# Asumimos que la app se ejecuta desde la raíz (donde está el Dockerfile)
SHAPEFILE_PATH = Path(__file__).parent.parent / "data" / "limites_simp100.shp"

@st.cache_data # Cacheamos la carga del shapefile para que no se repita en cada interacción
def cargar_municipios():
    """
    Carga el shapefile de municipios y devuelve un GeoDataFrame.
    Se cachea para evitar lecturas repetidas del disco.
    """
    try:
        gdf = gpd.read_file(SHAPEFILE_PATH)
        # Verificamos que la columna 'NAMEUNIT' existe
        if 'NAMEUNIT' not in gdf.columns:
            st.error("El shapefile no contiene la columna 'NAMEUNIT'.")
            return None
        return gdf
    except Exception as e:
        st.error(f"Error al cargar el shapefile: {e}")
        return None

def obtener_lista_municipios(gdf):
    """
    Devuelve una lista ordenada de nombres de municipios únicos.
    """
    if gdf is None:
        return []
    # .dropna() por si hubiera valores nulos, .unique() para no repetir
    return sorted(gdf['NAMEUNIT'].dropna().unique())

def obtener_geometria_municipio(gdf, nombre_municipio):
    """
    Filtra el GeoDataFrame por el nombre del municipio y devuelve
    la fila correspondiente (o un GeoDataFrame vacío si no lo encuentra).
    """
    if gdf is None or not nombre_municipio:
        return None
    
    # Filtramos por el nombre exacto
    municipio = gdf[gdf['NAMEUNIT'] == nombre_municipio]
    
    if municipio.empty:
        return None
    return municipio