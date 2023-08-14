#%%
import numpy as np
import pandas as pd
import warnings
from previsao import Previsao

warnings.filterwarnings('ignore')

#%% Cenário 1 - Probabilidades constantes

c1 = Previsao()
prev_c1 = c1.run()
erro_c1 = c1.scores.total()
rank_c1 = c1.rankings
rank_c1.evento
#%% Cenario 2 - Probabilidades alteram conforme alteração
#               de um conjunto de dados pro outro

fator = {'Enxurrada': 1,
 'Inundação': 1,
 'Chuvas Intensas': 1,
 'Vendaval': 1,
 'Granizo': 1,
 'Estiagem': 1,
 'Ciclone': 1}

c2 = Previsao(fator)
prev_c2 = c2.run()
erro_c2 = c2.scores.total()
rank_c2 = c2.rankings
rank_c2.evento

#%% Cenario 3 - Probabilidades variam de acordo com
#               as previsoes do PBMC

c3

#%% Cenario 4 - Probabilidades variam de acordo com estudo
#               técnico da SEDEC sobre avanço industrial e agropec

