#%%
import numpy as no
import pandas as pd

class Shower:

    def __init__(self, to_show, tipo: str|int) -> None:
        self.obj = to_show
        self.tipo = tipo
        self.tipos()
        pass
    
    def tipos(self):
        if self.tipo == 'erros':
            self.evento = self.obj.Evento.values[0]
            self.microrregiao = self.obj.Microrregiao.values[0]
            self.itens = self.obj.Itens.values[0]
            self.solicitacoes = self.obj.Solicitacoes.values[0]
            self.quantidades = self.obj.Quantidades.values[0]
            self.media = self.obj['Média total'].values[0]
            
        elif self.tipo == 'rankings':
            n = 'Qnt. Solic.'
            self.evento = self.obj.Evento.value_counts().to_frame(n)
            self.microrregiao = self.obj.Microrregiao.value_counts().to_frame(n)
            self.itens = self.obj.Item.value_counts().to_frame(n)
            self.mc_por_ev = self.obj.groupby(['Microrregiao', 'Evento']).count()['Probabilidade'].to_frame(n)

            
            pass

