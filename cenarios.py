#%%
import numpy as np
import pandas as pd
import warnings
from previsao import Previsao

warnings.filterwarnings('ignore')
np.random.seed(49)
#%% Cenário 1 - Probabilidades constantes

c1 = Previsao()
prev_c1 = c1.run()
erro_c1 = c1.scores.total()
rank_c1 = c1.rankings
rank_c1.evento
c1.prev_eventos.Evento.value_counts()

#%% Cenario 2 - Probabilidades alteram conforme alteração
#               de um conjunto de dados pro outro

fator_c2 = {'Enxurrada': 0.1818,
 'Inundação': 0,
 'Chuvas Intensas': 0.848485,
 'Vendaval': 0.631579,
 'Granizo': 1.135135,
 'Estiagem': 0,
 'Ciclone': 0}

c2 = Previsao(fator_c2)
prev_c2 = c2.run()
erro_c2 = c2.scores.total()
rank_c2 = c2.rankings
rank_c2.evento
c2.prev_eventos.Evento.value_counts()

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
c3.prev_eventos.Evento.value_counts()

#%% Cenario 4 - Probabilidades variam de acordo com estudo
#               técnico da SEDEC sobre avanço industrial e agropec

