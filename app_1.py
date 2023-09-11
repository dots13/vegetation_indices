import numpy as np
import ee
ee.Initialize()
import streamlit as st
import geemap.foliumap as geemap

st.set_page_config(layout="wide")

aoi = ee.FeatureCollection('FAO/GAUL/2015/level1').filter(ee.Filter.eq('ADM1_NAME','Utrecht')).geometry()

rgbVis = {
  'min': 0.0,
  'max': 0.3,
  'bands': ['B4', 'B3', 'B2'],
}

color = ['FFFFFF', 'CE7E45', 'DF923D', 'F1B555', 'FCD163', '99B718',
               '74A901', '66A000', '529400', '3E8601', '207401', '056201',
               '004C00', '023B01', '012E01', '011D01', '011301']
pallete = {"min":0, "max":1, 'palette':color}

colorizedVis = {
  'min': 0.0,
  'max': 1.0,
  'palette': ['0000ff', '00ffff', 'ffff00', 'ff0000', 'ffffff'],
};

def getNDVI(image):   
    
    # Normalized difference vegetation index (NDVI)
    ndvi = image.normalizedDifference(['B8','B4']).rename("NDVI")
    image = image.addBands(ndvi)

    return image
    
def getNDMI(image):
    
    # Normalized Difference Moisture Index (NDMI)
    NDMI = image.normalizedDifference(['B8','B11']).rename("NDMI")
    image = image.addBands(NDMI)

    return image

layers = {
        "NDMI": 'NDMI',
        "NDVI": 'NDVI',
        "f1": 'hz',
    }
options = list(layers.keys())
    
agg_fun = {
        "min": 'val1',
        "max": 'val2',
        "mean": 'hz',
        }

options_agg = list(agg_fun.keys())


col1, col2 = st.columns([1, 1])

subcol1, subcol2 = col1.columns(2)

subcolA, subcolB = col1.columns(2)

left = subcolA.selectbox("Select a left layer", options, index=1)
right = subcolB.selectbox("Select a left layer", options_agg, index=1)

with subcol1.expander("Select year and month", True):
    selected_year = subcolA.slider(
                        "Year",
                        2020,
                        2023,
                        value=2021,
                        step=1,
                    )
    selected_month = subcolB.slider(
                        "Month",
                        min_value=1,
                        max_value=12,
                        value=1,
                        step=1,
                    )
                    
                    

def maskS2clouds(image):
    
    qa = image.select('QA60')
    cloudBitMask = 1 << 10
    cirrusBitMask = 1 << 11
    mask = qa.bitwiseAnd(cloudBitMask).eq(0).And(
             qa.bitwiseAnd(cirrusBitMask).eq(0))
    
    return image.updateMask(mask).divide(10000).copyProperties(image)


palette_dic = {
    'NDVI' : pallete,
    'NDMI' : colorizedVis
}

left_img = ee.ImageCollection('COPERNICUS/S2')\
                .filter(ee.Filter.calendarRange(selected_year, selected_year, 'year'))\
                .filter(ee.Filter.calendarRange(selected_month, selected_month,'month'))\
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                .map(maskS2clouds) \
                .filterBounds(aoi)\
                .map(getNDVI)\
                .map(getNDMI)\
                .median()
                
right_img = ee.ImageCollection('COPERNICUS/S2')\
                .filter(ee.Filter.calendarRange(selected_year, selected_year, 'year'))\
                .filter(ee.Filter.calendarRange(selected_month, selected_month,'month'))\
                .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 20)) \
                .map(maskS2clouds) \
                .filterBounds(aoi)\
                .map(getNDVI)\
                .map(getNDMI)\
                .max()


utrecht_map = geemap.Map()
utrecht_map.setOptions('SATELLITE')
utrecht_map.centerObject(aoi, 10)
left_layer = geemap.ee_tile_layer(left_img.clip(aoi), rgbVis, 'RGB')
right_layer = geemap.ee_tile_layer(right_img.clip(aoi).select(left), palette_dic[left], left)
utrecht_map.split_map(left_layer, right_layer)

with col1:
    utrecht_map.to_streamlit(height=450)

    