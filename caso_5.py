#!/usr/bin/env python
# coding: utf-8

# In[49]:


# Installs geemap package
import subprocess

try:
    import geemap
except ImportError:
    print('Installing geemap ...')
    subprocess.check_call(["python", '-m', 'pip', 'install', 'geemap'])


# In[50]:


import ee
import geemap


# In[51]:


Map = geemap.Map(center=[40,-100], zoom=4)
Map


# In[52]:


# Add Earth Engine dataset
image = ee.ImageCollection('COPERNICUS/S2')   .filterDate('2017-01-01', '2017-01-02').median()   .divide(10000).visualize(**{'bands': ['B12', 'B8', 'B4'], 'min': 0.05, 'max': 0.5})
  
Map.setCenter(35.2, 31, 13)
Map.addLayer(image, {}, 'Sentinel-2 images January, 2018')


# In[57]:


Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map


# In[58]:


# Add Earth Engine dataset
# Load the Sentinel-1 ImageCollection.
sentinel1 = ee.ImageCollection('COPERNICUS/S1_GRD')     .filterBounds(ee.Geometry.Point(-122.37383, 37.6193))

# Filter by metadata properties.
vh = sentinel1   .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VV'))   .filter(ee.Filter.listContains('transmitterReceiverPolarisation', 'VH'))   .filter(ee.Filter.eq('instrumentMode', 'IW'))

# Filter to get images from different look angles.
vhAscending = vh.filter(ee.Filter.eq('orbitProperties_pass', 'ASCENDING'))
vhDescending = vh.filter(ee.Filter.eq('orbitProperties_pass', 'DESCENDING'))

# Create a composite from means at different polarizations and look angles.
composite = ee.Image.cat([
  vhAscending.select('VH').mean(),
  ee.ImageCollection(vhAscending.select('VV').merge(vhDescending.select('VV'))).mean(),
  vhDescending.select('VH').mean()
]).focal_median()

# Display as a composite of polarization and backscattering characteristics.
Map.setCenter(-122.37383, 37.6193, 10)
Map.addLayer(vh, {'min': [-25, -20, -25], 'max': [0, 10, 0]}, 'composite')


# In[55]:


Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map


# In[ ]:





# In[ ]:




