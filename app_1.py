import ee
import streamlit as st
import geemap.foliumap as geemap

st.set_page_config(layout="wide")

m = geemap.Map()
dem = ee.Image('USGS/SRTMGL1_003')

vis_params = {
    'min': 0,
    'max': 4000,
    'palette': ['006633', 'E5FFCC', '662A00', 'D8D8D8', 'F5F5F5']}

m.addLayer(dem, vis_params, 'SRTM DEM', True, 1)
m.addLayerControl()

# call to render Folium map in Streamlit
folium_static(m)

