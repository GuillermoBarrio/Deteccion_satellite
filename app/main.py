import streamlit as st
import folium
from streamlit_folium import st_folium
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

            # --- NUEVO: Construcción del mapa con Folium ---
            
            # 1. Obtener el centroide para centrar el mapa
            #    Usamos el sistema de coordenadas geográficas (EPSG:4326) que Folium espera
            geometria_wgs84 = geometria.to_crs(epsg=4326)
            centroide = geometria_wgs84.geometry.centroid.iloc[0]
            lat, lon = centroide.y, centroide.x

            # 2. Crear el mapa base
            m = folium.Map(location=[lat, lon], zoom_start=10, tiles="OpenStreetMap")

            # 3. Añadir la geometría del municipio como capa GeoJSON
            folium.GeoJson(
                geometria_wgs84,
                name=municipio_seleccionado,
                style_function=lambda x: {
                    "fillColor": "#ff7800",
                    "color": "#000000",
                    "weight": 1,
                    "fillOpacity": 0.3,
                },
                tooltip=folium.GeoJsonTooltip(fields=["NAMEUNIT"], aliases=["Municipio:"])
            ).add_to(m)

            # 4. Ajustar el zoom automáticamente a los límites del municipio
            bounds = geometria_wgs84.total_bounds  # [minx, miny, maxx, maxy]
            m.fit_bounds([[bounds[1], bounds[0]], [bounds[3], bounds[2]]])

            # 5. Mostrar el mapa en Streamlit
            st_folium(m, width=700, height=500)