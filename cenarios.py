#%%
import numpy as np
import pandas as pdG
import warnings
from previsao import Previsao
from mapas import Mapas

warnings.filterwarnings('ignore')
np.random.seed(49)
#%% Cenário 1 - Probabilidades constantes

c1 = Previsao()
prev_c1 = c1.run()
erro_c1 = c1.scores.total()
rank_c1 = c1.rankings
rank_c1.evento
c1.resultados(True, 'prev_c1_final')

#%% Cenario 2 - Probabilidades alteram conforme alteração
#               de um conjunto de dados pro outro

# fatores dados por:
#     (qnt_eventounico_dados2 - qnt_eventounico_dados1) / qnt_eventounico_dados1

fator_c2 = {'Enxurrada': -0.9473684210526315,
 'Inundação': -0.9523809523809523,
 'Chuvas Intensas':-0.2631578947368421,
 'Vendaval': -0.5384615384615384,
 'Granizo': 0.3125,
 'Estiagem': 0,
 'Ciclone': 0}

c2 = Previsao(fator_c2)
prev_c2 = c2.run()
erro_c2 = c2.scores.total()
rank_c2 = c2.rankings
rank_c2.evento
c2.resultados(True, 'prev_c2_final')

#%% Cenario 3 - Probabilidades variam de acordo com
#               as previsoes do PBMC

fator_c3 = {'Enxurrada': 0.161,
 'Inundação': 0.164,
 'Chuvas Intensas': 0.1,
 'Vendaval': 0,
 'Granizo': 0.357,
 'Estiagem': 0,
 'Ciclone': 0}

c3 = Previsao(fator_c3)
prev_c3 = c3.run()
rank_c3 = c3.rankings
rank_c3.evento
c3.resultados()

#%% PREVISÕES FEITAS
'''Essa parte aqui eu tive que fazer a mão, sem automatizar essas coisas na classe de 
Previsao porque não tinha tempo e também porque meu PC desligou e perdi as previsões feitas,
me restando apenas o xlsx que foi gerado.'''

path = r'C:\Users\henri\OneDrive\Desktop\Cousas da Facu\Pesquisa\Excelzar'
prev_c1 = pd.read_excel(path + '\prev_c1_final.xlsx')
prev_c2 = pd.read_excel(path + '\prev_c2_final.xlsx')
prev_c3 = pd.read_excel(path + '\prev_c3_final.xlsx')

#%% Valores dos rankings

cb_c1 = prev_c1[['Item', 'Valor Esperado']].groupby(['Item']).sum().sort_values("Valor Esperado", ascending=False)
cb_c2 = prev_c2[['Item', 'Valor Esperado']].groupby(['Item']).sum().sort_values("Valor Esperado", ascending=False)
cb_c3 = prev_c3[['Item', 'Valor Esperado']].groupby(['Item']).sum().sort_values("Valor Esperado", ascending=False)

perc_cb_c1 = cb_c1.loc['Cesta básica 7d']/cb_c1.sum()[0]
perc_cb_c2 = cb_c2.loc['Cesta básica 7d']/cb_c2.sum()[0]
perc_cb_c3 = cb_c3.loc['Cesta básica 7d']/cb_c3.sum()[0]

med_cb_esperado = (perc_cb_c1+ perc_cb_c2+ perc_cb_c3)/3

cb_mc_c1 = prev_c1.groupby(['Item', 'Microrregiao']).sum()['Quantidade'].sort_values(ascending=False).loc['Cesta básica 7d']
cb_mc_c2 = prev_c2.groupby(['Item', 'Microrregiao']).sum()['Quantidade'].sort_values(ascending=False).loc['Cesta básica 7d']
cb_mc_c3 = prev_c3.groupby(['Item', 'Microrregiao']).sum()['Quantidade'].sort_values(ascending=False).loc['Cesta básica 7d']

cb_mc_c3

#%% Criação de gráficos - C1

mapas_c1 = Mapas(prev_c1)
mapas_c1.eventos().show()
mapas_c1.microrregiao().show()
mapas_c1.itens().show()
#%% C2
mapas_c2 = Mapas(prev_c2)
mapas_c2.eventos().show()
mapas_c2.microrregiao().show()
mapas_c2.itens().show()
#%% C3
mapas_c3 = Mapas(prev_c3)
mapas_c3.eventos().show()
mapas_c3.microrregiao().show()
mapas_c3.itens().show()
# %% SERIE HISTORICA
from dados_mcmc import dados_drive

mapa_orig = Mapas(dados_drive)
mapa_orig.microrregiao()
mapa_orig.eventos()
mapa_orig.itens()