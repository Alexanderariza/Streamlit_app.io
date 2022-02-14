


# In[3]:


import ee
import geemap


# In[4]:


Map = geemap.Map(center=[40,-100], zoom=4)
Map


# In[5]:


# Add Earth Engine dataset
image = ee.ImageCollection('COPERNICUS/S2')   .filterDate('2017-01-01', '2017-01-02').median()   .divide(10000).visualize(**{'bands': ['B12', 'B8', 'B4'], 'min': 0.05, 'max': 0.5})
  
Map.setCenter(35.2, 31, 13)
Map.addLayer(image, {}, 'Sentinel-2 images January, 2018')


# In[6]:


Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map


# In[9]:


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


# In[8]:


Map.addLayerControl() # This line is not needed for ipyleaflet-based Map.
Map


# In[20]:


# Declaramos dos  momentos temporales para disponer de los datos necesarios
Tiempo1 = ee.ImageCollection ('COPERNICUS/S2')   .filterDate ('2019-07-06' ,'2019-07-11')   .filterMetadata ('CLOUDY_PIXEL_PERCENTAGE', 'Less_Than', 40)
Secano = Tiempo1.reduce(ee.Reducer.median())

Tiempo2 = ee.ImageCollection ('COPERNICUS/S2')   .filterDate ('2019-09-13' ,'2019-09-14')   .filterMetadata ('CLOUDY_PIXEL_PERCENTAGE', 'Less_Than', 40)
Inundacion = Tiempo2.reduce(ee.Reducer.median())

# Analizamos los valores de humedad a partir de las bandas 8 y 11
Humedad2 = Inundacion.normalizedDifference (['B8_median', 'B11_median'])
Humedad1 = Secano.normalizedDifference (['B8_median', 'B11_median'])

# Simbolizamos los valores de humedad en el momento de la inundacion
Map.addLayer(Humedad2, {'min': -1, 'max': 0.7, 'palette': ['#0000ff', 'F1B555', '99B718', '66A000', '3E8601',
    '056201', '023B01', '011D01', 'blue']},'Inundacion')

# Simbolizamos los valores de humedad previos a la inundacion y vinculamos vistas comparativas
MapasVinculados = ui.Map()
MapasVinculados.addLayer(Humedad1, {'min': -1, 'max': 0.6, 'palette': ['#0000ff', 'F1B555', '99B718', '66A000', '3E8601',
    '056201', '023B01', '011D01', 'blue']},'Pre-Inundacion')

SWIPE = ui.Map.Linker([ui.root.widgets().get(0), MapasVinculados])

# Integramos el efecto swipe creando una cortinilla horizontal o vertical
SWIPE2 = ui.SplitPanel({
  'firstPanel': SWIPE.get(0),
  'secondPanel': SWIPE.get(1),
  'orientation': 'horizontal', #'horizontal' o 'vertical'
  'wipe': True,
  
ui.root.widgets().reset([SWIPE2])

# Mostramos los mapas vinculados con efecto swipe, centrando den zona AOI y asignando zoom
Map.setCenter(35.2, 31, 13)


# In[ ]:




