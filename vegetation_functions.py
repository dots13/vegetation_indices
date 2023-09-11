""" Module that contains functions to the Google Earth Engine vegetation project workflow  """

# IMPORTS
import ee

def mask_clouds(image):
    """
    Masks clouds and cloud shadows in Landsat surface reflectance image.
    Obtained from:
        https://developers.google.com/earth-engine/datasets/catalog/COPERNICUS_S2_SR

    :param image: ee.Image
    :return: ee.Image with masked clouds and cloud shadows
    """
    # Get the pixel QA band
    qa = image.select('QA60')
    # Bits 10 and 11 are clouds and cirrus, respectively
    cloud_bit_mask = 1 << 10
    cirrus_bit_mask = 1 << 11
    # Both flags should be set to zero, indicating clear conditions
    mask = qa.bitwiseAnd(cloud_bit_mask).eq(0).And(
            qa.bitwiseAnd(cirrus_bit_mask).eq(0))

    return image.updateMask(mask).divide(10000).copyProperties(image)

def get_ndvi(image):
    """
    Calculates a Normalized Difference Vegetation Index (NDVI) and adds
    it as a new band to a given image.

    :param image: ee.Image
    :return: ee.Image with added NDVI band
    """
    ndvi = image.normalizedDifference(['B8', 'B4']).rename("NDVI")
    image = image.addBands(ndvi)

    # Return image with NDVI band
    return image


def get_ndmi(image):
    """
    Calculates a Normalized Difference Moisture Index (NDVI) and adds
    it as a new band to a given image.

    :param image: ee.Image
    :return: ee.Image with added NDVI band
    """
    ndmi = image.normalizedDifference(['B8', 'B11']).rename("NDMI")
    image = image.addBands(ndmi)

    # Return image with NDMI band
    return image


def get_msavi(image):
    """
    Calculates a Modified Soil Adjusted Vegetation Index (MSAVI) and
    adds it as a new band to a given image.

    :param image: ee.Image
    :return: ee.Image with added NDVI band
    """
    msavi = image.expression(
        '0.5 * ( 2 * NIR + 1 - ((2 * NIR + 1)**(2) - 8 * (NIR - RED))**(0.5))',
        {
            'NIR': image.select('B8'),
            'RED': image.select('B4'),
        }).rename("MSAVI")
    image = image.addBands(msavi)
    return image


def get_bsi(image):
    """
    Calculates a Bare Soil Index (BSI) and adds it as a new band to
    a given image.

    :param image: ee.Image
    :return: ee.Image with added BSI band
    """
    bsi = image.expression(
        '((RED + SWIR) - (NIR + BLUE)) / ((RED + SWIR) + (NIR + BLUE))',
        {
            'RED': image.select('B4'),
            'SWIR': image.select('B11'),
            'NIR': image.select('B8'),
            'BLUE': image.select('B2'),
        }).rename("BSI")
    image = image.addBands(bsi)
    return image



