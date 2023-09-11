import ee
import streamlit as st
import geemap.foliumap as geemap

st.set_page_config(layout="wide")




def search_data():

    # st.header("Search Earth Engine Data Catalog")

    Map = geemap.Map()
    aoi = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM1_NAME', 'Utrecht')).geometry()
    Map.setOptions('SATELLITE')
    Map.centerObject(aoi, 10)
    Map.to_streamlit()

def app():
    st.title("Earth Engine Data Catalog")

    search_data()


app()

