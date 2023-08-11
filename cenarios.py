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

#%% Cenario 2 - Probabilidades alteram conforme alteração
#               de um conjunto de dados pro outro

cenario2 = Previsao([0, 1, 2], [3, 4, 5], 15, 14)

#%% Cenario 3 - Probabilidades variam de acordo com
#               as previsoes do PBMC


#%% Cenario 4 - Probabilidades variam de acordo com estudo
#               técnico da SEDEC sobre avanço industrial e agropec

