#%%
import numpy as np
import pandas as pd
import warnings
from previsao import Previsao

warnings.filterwarnings('ignore')

#%% Cenário 1 - Probabilidades constantes

cenario1 = Previsao()
previsao_cenario1 = cenario1.run()
erros_cenario1 = cenario1.scores.total()
rank_previsao = cenario1.rankings

#%% Cenario 2 - Probabilidades alteram conforme alteração
#               de um conjunto de dados pro outro

fator = {'Enxurrada': 01.5,
 'Inundação': 2.9,
 'Chuvas Intensas': 1.8,
 'Vendaval': 2,
 'Granizo': 3,
 'Estiagem': 1.5,
 'Ciclone': 0.1}

cenario2 = Previsao(fator)
cenario2.mu_ev, cenario2.std_ev

#%% Cenario 3 - Probabilidades variam de acordo com
#               as previsoes do PBMC


#%% Cenario 4 - Probabilidades variam de acordo com estudo
#               técnico da SEDEC sobre avanço industrial e agropec

