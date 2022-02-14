#!/usr/bin/env python
# coding: utf-8

# In[1]:


#Comencemos por importar las librerías que utilizaremos:

import numpy as np                    # algebra lineal 
import pandas as pd                   # manipulación y análisis de datos
import matplotlib.pyplot as plt       # crear visualizaciones
get_ipython().run_line_magic('matplotlib', 'inline')
import plotly.offline as py           # amplia gama de opciones en gráficas
py.init_notebook_mode(connected=True)
import plotly.graph_objs as go        # opciones de interactividad en gráficas
import plotly.tools as tls            # opciones de Python para importar taquigrafía
import seaborn as sns                 # opciones para visualizar distribuciones aleatorias

import time                           # Librería necesaria para incluir el módulo de tiempo
import warnings                       # entrega toda clase de advertencias al usuario
warnings.filterwarnings('ignore')

global_temp_country = pd.read_csv('./archive/GlobalLandTemperaturesByCountry.csv')


# In[6]:


import plotly.express as px
df = px.data.global_temp_country().query("year == 2007").query("continent == 'Europe'")
df.loc[df['pop'] < 2.e6, 'country'] = 'Other countries' # Represent only large countries
fig = px.pie(df, values='pop', names='country', title='Population of European continent')
fig.show()


# In[2]:


# Eliminemos los países duplicados (en el análisis, no consideramos la presencia de colonias en estos países), 
# así como para los países donde no hay información sobre la temperatura

global_temp_country_clear = global_temp_country[~global_temp_country['Country'].isin(
    ['Denmark', 'Antarctica', 'France', 'Europe', 'Netherlands',
     'United Kingdom', 'Africa', 'South America'])]

global_temp_country_clear = global_temp_country_clear.replace(
   ['Denmark (Europe)', 'France (Europe)', 'Netherlands (Europe)', 'United Kingdom (Europe)'],
   ['Denmark', 'France', 'Netherlands', 'United Kingdom'])

# Calculamos los promediemos de la temperatura de cada país

countries = np.unique(global_temp_country_clear['Country'])
mean_temp = []
for country in countries:
    mean_temp.append(global_temp_country_clear[global_temp_country_clear['Country'] == 
                                               country]['AverageTemperature'].mean())


    
data = [ dict(
        type = 'choropleth',
        locations = countries,
        z = mean_temp,
        locationmode = 'country names',
        text = countries,
        marker = dict(
            line = dict(color = 'rgb(0,0,0)', width = 1)),
            colorbar = dict(autotick = True, tickprefix = '', 
            title = 'Temperatura \nMedia,\n°C')
            )
       ]

layout = dict(
    title = 'Temperatura superficial promedio por país',
    geo = dict(
        showframe = False,
        showocean = True,
        oceancolor = 'rgb(0,255,255)',
        projection = dict(
        type = 'orthographic',
            rotation = dict(
                    lon = 60,
                    lat = 10),
        ),
        lonaxis =  dict(
                showgrid = True,
                gridcolor = 'rgb(102, 102, 102)'
            ),
        lataxis = dict(
                showgrid = True,
                gridcolor = 'rgb(102, 102, 102)'
                )
            ),
        )

fig = dict(data=data, layout=layout)
py.iplot(fig, validate=False, filename='worldmap')


# In[3]:


mean_temp_bar, countries_bar = (list(x) for x in zip(*sorted(zip(mean_temp, countries), 
                                                             reverse = True)))
sns.set(font_scale=0.9) 
f, ax = plt.subplots(figsize=(4.5, 50))
colors_cw = sns.color_palette('coolwarm', len(countries))
sns.barplot(mean_temp_bar, countries_bar, palette = colors_cw[::-1])
Text = ax.set(xlabel='Average temperature', title='Temperatura promedio de la tierra en los países')


# In[4]:


global_temp = pd.read_csv("./archive/GlobalTemperatures.csv")

#Extract the year from a date
years = np.unique(global_temp['dt'].apply(lambda x: x[:4]))
mean_temp_world = []
mean_temp_world_uncertainty = []

for year in years:
    mean_temp_world.append(global_temp[global_temp['dt'].apply(
        lambda x: x[:4]) == year]['LandAverageTemperature'].mean())
    mean_temp_world_uncertainty.append(global_temp[global_temp['dt'].apply(
                lambda x: x[:4]) == year]['LandAverageTemperatureUncertainty'].mean())

trace0 = go.Scatter(
    x = years, 
    y = np.array(mean_temp_world) + np.array(mean_temp_world_uncertainty),
    fill= None,
    mode='lines',
    name='Uncertainty top',
    line=dict(
        color='rgb(0, 255, 255)',
    )
)
trace1 = go.Scatter(
    x = years, 
    y = np.array(mean_temp_world) - np.array(mean_temp_world_uncertainty),
    fill='tonexty',
    mode='lines',
    name='Uncertainty bot',
    line=dict(
        color='rgb(0, 255, 255)',
    )
)

trace2 = go.Scatter(
    x = years, 
    y = mean_temp_world,
    name='Average Temperature',
    line=dict(
        color='rgb(199, 121, 093)',
    )
)
data = [trace0, trace1, trace2]

layout = go.Layout(
    xaxis=dict(title='Año'),
    yaxis=dict(title='Temperatura media, °C'),
    title='Temperatura promedio de la tierra en el mundo <i>(en azul el valor de la Incertidumbre)</i>',
    showlegend = False)

fig = go.Figure(data=data, layout=layout)
py.iplot(fig)


# In[4]:


continent = ['Russia', 'United States', 'Niger', 'Greenland', 'Togo', 'Colombia']
mean_temp_year_country = [ [0] * len(years[70:]) for i in range(len(continent))]
j = 0
for country in continent:
    all_temp_country = global_temp_country_clear[global_temp_country_clear['Country'] == country]
    i = 0
    for year in years[70:]:
        mean_temp_year_country[j][i] = all_temp_country[all_temp_country['dt'].apply(
                lambda x: x[:4]) == year]['AverageTemperature'].mean()
        i +=1
    j += 1

traces = []
colors = ['rgb(0, 255, 255)', 'rgb(255, 0, 255)', 'rgb(0, 0, 0)',
          'rgb(255, 0, 0)', 'rgb(0, 255, 0)', 'rgb(0, 0, 255)']
for i in range(len(continent)):
    traces.append(go.Scatter(
        x=years[70:],
        y=mean_temp_year_country[i],
        mode='lines',
        name=continent[i],
        line=dict(color=colors[i]),
    ))

layout = go.Layout(
    xaxis=dict(title='Año'),
    yaxis=dict(title='Temperatura promedio, °C'),
    title='Temperatura promedio de la tierra en los continentes',)

fig = go.Figure(data=traces, layout=layout)
py.iplot(fig)


# In[190]:


# Extraiga el año de una fecha
years = np.unique(global_temp_country_clear['dt'].apply(lambda x: x[:4]))

# Creemos una matriz y agreguemos los valores de las temperaturas promedio en los países cada 20 años
mean_temp_year_country = [ [0] * len(countries) for i in range(len(years[::20]))]

j = 0
for country in countries:
    all_temp_country = global_temp_country_clear[global_temp_country_clear['Country'] == country]
    i = 0
    for year in years[::10]:
        mean_temp_year_country[i][j] = all_temp_country[all_temp_country['dt'].apply(
                lambda x: x[:4]) == year]['AverageTemperature'].mean()
        i +=1
    j += 1


# In[189]:


# Creemos un Streaming en Plotly (puede que no funcione bien en Colab, dado que la función Stream no corre en offline)
#  stream_tokens = tls.get_credentials_file () ['stream_ids']
#  token = stream_tokens [-1]
#  stream_id = dict (token = token, maxpoints = 60)

data = [ dict(
        type = 'choropleth',
        locations = countries,
        z = mean_temp,
        locationmode = 'country names',
        text = countries,
        marker = dict(
            line = dict(color = 'rgb(0,0,0)', width = 1)),
            colorbar = dict(autotick = True, tickprefix = '',
            title = 'Promedio\nTemperatura,\n°C'),
        #The following line is also needed to create Stream
        #stream = stream_id
            )
       ]

layout = dict(
    title = 'Temperatura promedio de la tierra en los países 20 años',
    geo = dict(
        showframe = False,
        showocean = True,
        oceancolor = 'rgb(0,255,255)',
        type = 'equirectangular'
    ),
)

fig = dict(data=data, layout=layout)
py.iplot(fig, validate=False, filename='world_temp_map')


# In[191]:


#Comencemos por importar las librerías que utilizaremos:
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

#Ahora importamos los datos de temperatura y dióxido de carbono global:
data_country = pd.read_csv("./archive/GlobalLandTemperaturesByCountry.csv")
data_colombia = data_country[data_country["Country"] == "Colombia"].copy()
data_colombia["dt"] = pd.to_datetime(data_colombia["dt"])

data_global = pd.read_csv("./archive/GlobalTemperatures.csv")
data_global["dt"] = pd.to_datetime(data_global["dt"])
ndsi = pd.read_csv("./archive/ee-chart5_.csv")


# In[192]:


#veamos cuantas dimensiones y registros contiene
data_country.shape


# In[202]:


#son mas de medio millon de registros ordenados en 4 columnas. Veamos los primeros registros
data_country.head()


# In[196]:


ndsi.shape


# In[197]:


#son mas de medio millon de registros ordenados en 5 columnas. Veamos los primeros registros
ndsi.head()


# In[198]:


plt.figure()
plt.style.use("fivethirtyeight")
annual_ndsi = ndsi.groupby(ndsi["Year"]).mean()
annual_ndsi.loc[2000:2020]["NDSI"].plot(figsize = (10,5), grid=True, legend=True)
plt.title("Niveles anuales de glacial - NDSI")
plt.ylabel("NDSI")
plt.show()


# In[199]:


plt.figure()
plt.style.use("fivethirtyeight")
annual_ndsi = ndsi.groupby(ndsi["Year"]).mean()
annual_ndsi.loc[2000:2020]["mean"].plot(figsize = (10,5), grid=True, legend=True)
plt.title("Niveles anuales de glacial - NDSI")
plt.ylabel("NDSI_mean")
plt.show()


# In[200]:


annual_mean_global = data_global.groupby(data_global["dt"].dt.year).mean()
reference_temperature_global = annual_mean_global.loc[2000:2020].mean()["LandAndOceanAverageTemperature"]
annual_mean_global["Anomaly"] = annual_mean_global["LandAndOceanAverageTemperature"] - reference_temperature_global

annual_mean_colombia = data_colombia.groupby(data_colombia["dt"].dt.year).mean()
reference_temperature_colombia = annual_mean_colombia.loc[2000:2020].mean()["AverageTemperature"]
annual_mean_colombia["Anomaly"] = annual_mean_colombia["AverageTemperature"] - reference_temperature_colombia


# In[201]:


plt.figure()
plt.style.use("fivethirtyeight")
annual_mean_global.loc[2000:2020]["Anomaly"].plot(figsize = (10,5), grid=True, legend=True, color="red" )

plt.title("Anomalía anual de la temperatura media base (Global)")
plt.xlabel('Años')
plt.ylabel('Anomalía de Temperatura')
plt.show()


# In[203]:


plt.figure()
plt.style.use("fivethirtyeight")
annual_mean_colombia.loc[2000:2020]["Anomaly"].plot(figsize = (10,3), grid= True, legend=True, color="orange")
plt.title("Anomalía anual de la temperatura media base para Colombia")
plt.xlabel('Años')
plt.ylabel('Anomalía Termicá (Cº)')
plt.show()


# In[204]:


annual_ndsi_temp = pd.merge(annual_mean_global.loc[2000:2020], annual_ndsi.loc[2000:2020], left_index=True, right_index=True)
annual_ndsi_temp = annual_ndsi_temp[["LandAndOceanAverageTemperature", "Anomaly", "NDSI"]].copy()
annual_ndsi_temp.corr()


# In[207]:


annual_mean_temp = pd.merge(annual_mean_global.loc[2000:2020], annual_ndsi.loc[2000:2020], left_index=True, right_index=True)
annual_mean_temp = annual_ndsi_temp[["LandAndOceanAverageTemperature", "Anomaly", "NDSI"]].copy()
annual_ndsi_temp.corr()


# In[208]:


plt.figure(figsize=(10,10))
sns.scatterplot(x="Anomaly",y="NDSI", data=annual_ndsi_temp, legend='full', color="black")
plt.title("Correlación entre las Anomalías Térmicas y el valor del NDSI - Colombia")


# In[212]:


from osgeo import gdal as GD  
import matplotlib.pyplot as mplot  
import numpy as npy  
data_set = GD.Open(r'./archive/L4_Composite3.tif')  
print(data_set.RasterCount)  
# As, there are 3 bands, we will store in 3 different variables  
band_1 = data_set.GetRasterBand(1) # red channel  
band_2 = data_set.GetRasterBand(4) # green channel  
band_3 = data_set.GetRasterBand(5) # blue channel  
b1 = band_1.ReadAsArray()  
b4 = band_2.ReadAsArray()  
b5 = band_3.ReadAsArray()  
img_1 = npy.dstack((b5, b4, b1))  
f = mplot.figure()  
#plt.imshow(img_1, vmin=0, vmax=255)
plt.imshow((img_1 * 255).astype(np.uint8))
 
mplot.savefig('Tiff.png')  

mplot.show()  


# In[211]:


plt.imshow(b3)


# In[214]:


fp = r'./archive/NDSI.tif'
img = rasterio.open(fp) 
# mention band no. in read() method starting from 1 not 0
show(img.read(1))


# In[ ]:




