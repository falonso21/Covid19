#!/usr/bin/env python
# coding: utf-8

# ### Autores:
# #### Francisco Alonso Fernández. Data Scientist en Future Space.
# #### Fernando Hernandez de Vega. Técnico Gis en Cirosip.

# In[1]:


from IPython.display import HTML

HTML('''
<script>code_show=true; 

function code_toggle() {
    if (code_show){
    $('div.input').hide();
    } else {
    $('div.input').show();
    }
    code_show = !code_show
} 

$( document ).ready(code_toggle);
</script>
<form action="javascript:code_toggle()"><input type="submit" value="Haz click para ver el código."></form>
''')


# In[2]:


from bs4 import BeautifulSoup
import requests
import re
import urllib.request

import pandas as pd

import json

import folium


# In[3]:


url = "https://www.juntadeandalucia.es/institutodeestadisticaycartografia/intranet/admin/rest/v1.0/consulta/39409"


# In[4]:


## Obtenemos los datos de hoy mediante una petición a la api

payload = {}
headers= {}

response = requests.request("GET", url, headers=headers, data = payload)
my_data = response.json()


# In[5]:


## Pasamos los datos del json a un DataFrame

fecha = []
territorio = []
confirmados_pdia = []
hospitalizados = []
uci = []
fallecidos = []

for index in range(len(my_data['data'])):
    fecha += [my_data['data'][index][0]['des']]
    territorio += [my_data['data'][index][1]['des']]
    confirmados_pdia += [my_data['data'][index][3]['format']]
    hospitalizados += [my_data['data'][index][5]['format']]
    uci += [my_data['data'][index][6]['format']]
    fallecidos += [my_data['data'][index][7]['format']]
    
Andalucia_df = pd.DataFrame({'Fecha':fecha,'Territorio':territorio, 'Nuevos casos':confirmados_pdia,              'Hospitalizados':hospitalizados,'UCI':uci, 'Fallecidos':fallecidos})


# In[6]:


## Pasamos la columna Fecha a tipo fecha

Andalucia_df['Fecha'] = pd.to_datetime(Andalucia_df['Fecha'], format='%d/%m/%Y')


# In[7]:


## Nos quedamos con los datos de la fehca más reciente en el momento de ejecución
Andalucia_LastDate = Andalucia_df[Andalucia_df.Fecha == Andalucia_df.Fecha[0]]
Andalucia_LastDate = Andalucia_LastDate[Andalucia_LastDate.Territorio != 'Andalucía']


# In[8]:


## Leemos el geojson, que contiene la información necesaria para pintar las coropletas

with open('Andalucia_GeoJSON.geojson',encoding="utf-8") as f:
    geo = json.load(f, encoding="utf-8")

## Se corrige un pequeño fallo con la tilde de Almería

geo['features'][0]['properties']['texto']='Almería'


# In[9]:


## Convertimos la columna de nuevos casos a enteros para que no haya problemas

Andalucia_LastDate["Nuevos casos"] = pd.to_numeric(Andalucia_LastDate["Nuevos casos"])


# In[10]:


## Mediante folium realizamos el mapa

m = folium.Map(location=[37, -4.8], zoom_start=6.5)

folium.Choropleth(
    geo_data=geo,
    name='choropleth',
    data=Andalucia_LastDate,
    columns=['Territorio','Nuevos casos'],
    key_on='feature.properties.texto',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    ## Nota: Fernando sabe de sobra que Hernández lleva tilde, pero el decode de Folium da problemas
    legend_name ='Created by: Francisco Alonso y Fernando Hernandez.').add_to(m)

folium.LayerControl().add_to(m)

## Cádiz
icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
icon = folium.CustomIcon(
icon_image,
icon_size=(30, 30),
icon_anchor=(15, 15),
popup_anchor=(0.1, -0.1))
folium.Marker([36.5, -6.1], popup='<h3> C&aacutediz: </h3>'+'<p>'+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Cádiz']['Fecha'].tolist()[0])[:-9]+'</p>'              +'<p> Nuevos casos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Cádiz']['Nuevos casos'].tolist()[0])+'</p>'              +'<p> Hospitalizados: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Cádiz']['Hospitalizados'].tolist()[0])+'</p>'              +'<p> UCI: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Cádiz']['UCI'].tolist()[0])+'</p>'              +'<p> Fallecidos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Cádiz']['Fallecidos'].tolist()[0])+'</p>',
              icon=icon).add_to(m)

## Sevilla
icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
icon = folium.CustomIcon(
icon_image,
icon_size=(30, 30),
icon_anchor=(15, 15),
popup_anchor=(0.1, -0.1))
folium.Marker([37.3, -5.9], popup='<h3> Sevilla: </h3>'+'<p>'+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Sevilla']['Fecha'].tolist()[0])[:-9]+'</p>'              +'<p> Nuevos casos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Sevilla']['Nuevos casos'].tolist()[0])+'</p>'              +'<p> Hospitalizados: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Sevilla']['Hospitalizados'].tolist()[0])+'</p>'              +'<p> UCI: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Sevilla']['UCI'].tolist()[0])+'</p>'              +'<p> Fallecidos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Sevilla']['Fallecidos'].tolist()[0])+'</p>',
              icon=icon).add_to(m)

## Huelva
icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
icon = folium.CustomIcon(
icon_image,
icon_size=(30, 30),
icon_anchor=(15, 15),
popup_anchor=(0.1, -0.1))
folium.Marker([37.6, -6.8], popup='<h3> Huelva: </h3>'+'<p>'+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Huelva']['Fecha'].tolist()[0])[:-9]+'</p>'              +'<p> Nuevos casos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Huelva']['Nuevos casos'].tolist()[0])+'</p>'              +'<p> Hospitalizados: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Huelva']['Hospitalizados'].tolist()[0])+'</p>'              +'<p> UCI: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Huelva']['UCI'].tolist()[0])+'</p>'              +'<p> Fallecidos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Huelva']['Fallecidos'].tolist()[0])+'</p>',
              icon=icon).add_to(m)

## Córdoba
icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
icon = folium.CustomIcon(
icon_image,
icon_size=(30, 30),
icon_anchor=(15, 15),
popup_anchor=(0.1, -0.1))
folium.Marker([37.8, -4.7], popup='<h3> C&oacute;rdoba: </h3>'+'<p>'+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Córdoba']['Fecha'].tolist()[0])[:-9]+'</p>'              +'<p> Nuevos casos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Córdoba']['Nuevos casos'].tolist()[0])+'</p>'              +'<p> Hospitalizados: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Córdoba']['Hospitalizados'].tolist()[0])+'</p>'              +'<p> UCI: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Córdoba']['UCI'].tolist()[0])+'</p>'              +'<p> Fallecidos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Córdoba']['Fallecidos'].tolist()[0])+'</p>',
              icon=icon).add_to(m)

## Jaén
icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
icon = folium.CustomIcon(
icon_image,
icon_size=(30, 30),
icon_anchor=(15, 15),
popup_anchor=(0.1, -0.1))
folium.Marker([37.7, -3.7], popup='<h3> Ja&eacute;n: </h3>'+'<p>'+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Jaén']['Fecha'].tolist()[0])[:-9]+'</p>'              +'<p> Nuevos casos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Jaén']['Nuevos casos'].tolist()[0])+'</p>'              +'<p> Hospitalizados: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Jaén']['Hospitalizados'].tolist()[0])+'</p>'              +'<p> UCI: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Jaén']['UCI'].tolist()[0])+'</p>'              +'<p> Fallecidos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Jaén']['Fallecidos'].tolist()[0])+'</p>',
              icon=icon).add_to(m)

## Málaga
icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
icon = folium.CustomIcon(
icon_image,
icon_size=(30, 30),
icon_anchor=(15, 15),
popup_anchor=(0.1, -0.1))
folium.Marker([36.8, -4.5], popup='<h3> M&aacute;laga: </h3>'+'<p>'+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Málaga']['Fecha'].tolist()[0])[:-9]+'</p>'              +'<p> Nuevos casos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Málaga']['Nuevos casos'].tolist()[0])+'</p>'              +'<p> Hospitalizados: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Málaga']['Hospitalizados'].tolist()[0])+'</p>'              +'<p> UCI: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Málaga']['UCI'].tolist()[0])+'</p>'              +'<p> Fallecidos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Málaga']['Fallecidos'].tolist()[0])+'</p>',
              icon=icon).add_to(m)

## Granada
icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
icon = folium.CustomIcon(
icon_image,
icon_size=(30, 30),
icon_anchor=(15, 15),
popup_anchor=(0.1, -0.1))
folium.Marker([37.1, -3.5], popup='<h3> Granada: </h3>'+'<p>'+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Granada']['Fecha'].tolist()[0])[:-9]+'</p>'              +'<p> Nuevos casos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Granada']['Nuevos casos'].tolist()[0])+'</p>'              +'<p> Hospitalizados: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Granada']['Hospitalizados'].tolist()[0])+'</p>'              +'<p> UCI: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Granada']['UCI'].tolist()[0])+'</p>'              +'<p> Fallecidos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Granada']['Fallecidos'].tolist()[0])+'</p>',
              icon=icon).add_to(m)

## Almería
icon_image = "https://www.flaticon.es/premium-icon/icons/svg/3334/3334018.svg"
icon = folium.CustomIcon(
icon_image,
icon_size=(30, 30),
icon_anchor=(15, 15),
popup_anchor=(0.1, -0.1))
folium.Marker([37, -2.3], popup='<h3> Almer&iacute;a: </h3>'+'<p>'+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Almería']['Fecha'].tolist()[0])[:-9]+'</p>'              +'<p> Nuevos casos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Almería']['Nuevos casos'].tolist()[0])+'</p>'              +'<p> Hospitalizados: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Almería']['Hospitalizados'].tolist()[0])+'</p>'              +'<p> UCI: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Almería']['UCI'].tolist()[0])+'</p>'              +'<p> Fallecidos: '+str(Andalucia_LastDate[Andalucia_LastDate.Territorio == 'Almería']['Fallecidos'].tolist()[0])+'</p>',
              icon=icon).add_to(m)

m

