#%%
import numpy as np
import pandas as pd
import eventos_mcmc as ev
import gastos_mcmc as gt
import dados_mcmc as ds
from scorador import Scorador
from shower import Shower
from dados_mcmc import dados_drive
from mydefs import excelzar
from graficos import Grafico

#np.random.seed(49)

class Previsao():

    def __init__(self, fatores=None, 
                 dados=None) -> None:
        
        self.fatores = fatores
        
        if not dados:
            self.dados = dados_drive
        else:
            self.dados = dados

        self.dados_unicos = ds.eventos_unicos(self.dados)

        self.pre_run()
        pass

    def pre_run(self):

        self.mat_trans = ev.watchousky(self.dados_unicos)
            
        if not self.fatores:
            self.mu_ev, self.std_ev, self.map_ev = ev.med_desv_eventos(self.dados)
            self.vet_inicial = ev.vetor_inicial(self.dados_unicos)
        else:
            self.serie_fatorada_total = ev.apl_fator(self.dados, self.fatores)
            self.serie_fatorada_unica = ev.apl_fator(self.dados_unicos, self.fatores)
            self.mu_ev, self.std_ev, self.map_ev = ev.med_desv_eventos(self.serie_fatorada_total)
            self.vet_inicial = ev.vetor_inicial(self.serie_fatorada_unica)

        
        self.dados_gastos = self.dados.dropna(axis=0, subset=['Item'])

        self.msm_microreg = ev.norms_microreg(self.dados_unicos)
        self.msm_item = gt.prob_item_evento(self.dados_gastos)
        self.pri = gt.prev_itens
        self.msm_solic = gt.prob_pedidos(self.dados)

        self.indexado, self.msm_qnts = gt.index_qnt(self.dados_gastos)
        
    def run(self):
        self.prev_eventos = ev.met_hast_sampler(self.mat_trans, 
                                                self.vet_inicial, 
                                                (self.mu_ev, 
                                                 self.std_ev, 
                                                 self.map_ev))                  
        self.prev_microrregiao = ev.aloc_microreg(self.msm_microreg,
                                                   self.prev_eventos)       
        self.prev_solicitacao = gt.solicitacoes(self.msm_solic, 
                                                self.pri, 
                                                self.msm_item, 
                                                self.prev_microrregiao)    
        self.prev_quantidades = gt.est_quantidades(self.prev_solicitacao, 
                                                   self.indexado)
        self.previsao = gt.totais(self.prev_quantidades)
        
        self.grafico = Grafico(real=[self.dados, 
                                     self.dados_unicos, 
                                     self.dados_gastos, 
                                     self.indexado],
                                previsao=[self.prev_eventos,
                                          self.prev_microrregiao,
                                          self.prev_solicitacao,
                                          self.prev_quantidades,
                                          self.previsao])
        
        self.scores = Scorador(previsao=[self.prev_eventos,
                                          self.prev_microrregiao,
                                          self.prev_solicitacao,
                                          self.prev_quantidades,
                                          self.previsao],
                                msms=[(self.mu_ev,self.std_ev,self.map_ev),
                                      {y:(x[0], x[1], x[3]) for y, x in self.msm_microreg.items()},
                                      self.msm_item,
                                      self.msm_solic,
                                      self.msm_qnts])
        
        self.rankings = Shower(self.previsao, 'rankings')

        return self.previsao
    
    def resultados(self, save=False, nome=None):
        
        fat = pd.DataFrame(self.fatores, index=[0])
        vi = self.vet_inicial.to_frame().transpose()
        solic = self.previsao.Evento.value_counts().to_frame().transpose()
        qntev = self.prev_eventos.Evento.value_counts().to_frame().transpose()
        self.tabela =  pd.concat([fat, vi, qntev, solic])
        self.tabela.index = ['Fatores', 'Freq. i', 'Qnt.', 'Solic.']
        self.tabela = self.tabela.fillna(0)
        
        self.top = pd.DataFrame(columns=['Eventos', 'Microrregioes', 'Itens'])
        self.top['Eventos'] = self.rankings.evento.index[:5]
        self.top['Itens'] = self.rankings.itens.index[:5]
        self.top['Microrregioes'] = self.rankings.microrregiao.index[:5]
        self.top.index.name = 'Ranking'
        self.top.index = list(range(1, 6))
        self.totais = pd.Series({"Eventos":qntev.transpose().sum()[0],
                                "Solicitacoes":len(self.previsao),
                                "Valor total":self.previsao["Valor Total"].sum(),
                                "Valor esperado":self.previsao["Valor Esperado"].sum()})
        
        self.gst_ev = self.previsao[['Evento', 'Valor Total']].groupby(['Evento']).sum().sort_values(by='Valor Total', ascending=False)
        self.gst_mc = self.previsao[['Microrregiao', 'Valor Total']].groupby(['Microrregiao']).sum().sort_values(by='Valor Total', ascending=False).head()
        
        print(self.tabela.transpose(), end='\n\n')
        print(self.scores.total().obj.transpose(), end='\n\n')
        print(self.totais, end='\n\n')
        print(self.top)

        if save:
            excelzar({"previsao":self.previsao,
                      "overview":self.tabela,
                      "totais":self.totais,
                      "erros":self.scores.total().obj.transpose(),
                      "ranking":self.top}, nome)
            
    def save(self, nome):
        excelzar({"previsao":self.previsao,
                  "overview":self.tabela,
                  "totais":self.totais,
                  "erros":self.scores.total().obj.transpose(),
                  "ranking":self.top}, nome)
# %%
