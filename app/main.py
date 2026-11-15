import streamlit as st

from src.municipios import cargar_municipios, obtener_lista_municipios, obtener_geometria_municipio

# 1. Cargar datos (cacheado)
gdf = cargar_municipios()

if gdf is not None:
    # 2. Obtener lista de nombres para el selector
    lista_nombres = obtener_lista_municipios(gdf)
    
    # 3. Widget de Streamlit con búsqueda (selectbox permite escribir para filtrar)
    municipio_seleccionado = st.selectbox(
        "Selecciona un municipio:",
        options=lista_nombres,
        index=None, # Para que empiece vacío
        placeholder="Escribe para buscar..."
    )
    
    # 4. Si el usuario ha seleccionado algo, obtener su geometría
    if municipio_seleccionado:
        geometria = obtener_geometria_municipio(gdf, municipio_seleccionado)
        if geometria is not None:
            st.write(f"Has seleccionado: {municipio_seleccionado}")
            # Aquí iría el código para pintar el mapa con Folium
            # (lo veremos en el siguiente paso)

