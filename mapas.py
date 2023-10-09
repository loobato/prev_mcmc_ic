#%% Iniciando o mapa com as delimitações
import json
import folium
import inspect
import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import matplotlib.pyplot as plt
from PIL import Image
from unidecode import unidecode
from shower import Shower

#%%
prev_c1 = pd.read_excel(r"C:\Users\henri\OneDrive\Desktop\Cousas da Facu\Pesquisa\Excelzar\prev_c1_final.xlsx")

# %%

class Mapas:

    def __init__(self, dados=None, *args) -> None:
        if 'Data' in dados.columns:
            dados = dados.drop('Data', axis=1)
        self.dados = dados

        self.sc = json.load(open('dados_mapas\santa_catarina.json', 'r'))
        self.correcao_microrregs()
        self.ranks = Shower(self.dados, 'rankings')
        if len(args) > 0:
            self.save = args[0]
        pass

    def get_calling_method_name(self):
        # Obtém a pilha de chamadas
        stack = inspect.stack()
        # O nome do método que chamou o método atual estará no índice 2 da pilha
        calling_method_name = stack[2].function
        return calling_method_name

    def correcao_microrregs(self):
        if 'Unnamed: 0' in self.dados.columns:
            self.dados = self.dados.drop('Unnamed: 0', axis=1)
        
        self.dados.Microrregiao = self.dados.Microrregiao.replace({'Caçador':'Joaçaba',
                                                                    'Jaraguá do Sul':'Joinville', 
                                                                    'Lages':'Campos de Lages',
                                                                    'Taió':'Rio do Sul',
                                                                    'S.Bento do Sul': 'São Bento do Sul',
                                                                    'São Miguel do Oeste':"São Miguel d'Oeste"})

        self.dados.Microrregiao = self.dados.Microrregiao.apply(unidecode)
        self.dados.Microrregiao = self.dados.Microrregiao.apply(str.upper)

    def mapa_comum(self):
        m = folium.Map(location=[-27.1803, -50.8667], zoom_start=6)

        borderstyle = {
            'color':'black',
            'weight':1,
            'fillOpacity': 0
        }

        for mc in self.sc['features']:
            folium.GeoJson(mc, 
                        style_function=lambda x:borderstyle,
                        tooltip=folium.GeoJsonTooltip(
                            fields=['MICRO'],
                            aliases=['Nome: '],
                            localize=True
                        )).add_to(m)

        return m
    
    def eventos(self):
        gp = self.dados.groupby(['Evento', 'Microrregiao']).count()['Item']
        
        mais_visu = self.ranks.evento.index[0]

        gp_ev = gp[mais_visu].reset_index()
        gp_ev = gp_ev.set_index(['Microrregiao'])
        keys = [x['properties']['MICRO'] for x in self.sc['features']]

        for mc in keys:
            if mc not in gp_ev.index:
                gp_ev.loc[mc] = 0
        gp_ev = gp_ev.reset_index()
        gp_ev.columns = ['Microrregiao', 'Qnt. Solic.']

        fig = px.choropleth(gp_ev,
                            geojson=self.sc, 
                            locations='Microrregiao', 
                            color='Qnt. Solic.',
                            featureidkey='properties.MICRO',
                            title='Chuvas',
                            height=250,
                            color_continuous_scale='Blues'
                            )
        fig.update_geos(fitbounds='geojson', visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                          title="Teste")
        return fig
    
    def microrregiao(self):
        dds = self.ranks.microrregiao
        keys = [x['properties']['MICRO'] for x in self.sc['features']]
        for mc in keys:
            if mc not in dds.index:
                dds.loc[mc] = 0

        df = dds.reset_index()

        fig = px.choropleth(df,
                            geojson=self.sc, 
                            locations='Microrregiao', 
                            color='Qnt. Solic.',
                            featureidkey='properties.MICRO',
                            title='Microrregiao',
                            height=250,
                            color_continuous_scale='Oranges'
                            )
        fig.update_geos(fitbounds='geojson', visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                          title="Teste")
        return fig
        
    def itens(self):
        gp = self.dados.groupby(['Item', 'Microrregiao']).sum()['Quantidade']
        mais_visu = self.ranks.itens.index[0]
        dds = gp[mais_visu]
        keys = [x['properties']['MICRO'] for x in self.sc['features']]

        for mc in keys:
            if mc not in dds.index:
                dds.loc[mc] = 0
        dds = dds.reset_index()
        dds.columns = ['Microrregiao', 'Qnt. Solic.']

        fig = px.choropleth(dds,
                            geojson=self.sc, 
                            locations='Microrregiao', 
                            color='Qnt. Solic.',
                            featureidkey='properties.MICRO',
                            title='Itens',
                            height=250,
                            color_continuous_scale='Greens'
                            )
        fig.update_geos(fitbounds='geojson', visible=False)
        fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},
                          title="Teste")
        return fig
# %%
