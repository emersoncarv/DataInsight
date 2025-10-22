import pandas as pd
from typing import overload

class DatasetAnalysis:
    def __init__(self, dados: pd.DataFrame):
        self.dados = dados
        self.colunas = None

    def getLinhasColunas(self):
        return self.dados.shape
    
    def getLinhasColunasTexto(self):
        return f'Linhas: {self.dados.shape[0]}, Colunas: {self.dados.shape[1]}'

    def getAmostra(self, n=5):
        return self.dados.head(n)

    def getColunasDTypes(self):
        return self.dados.dtypes

    def getValoresNulosTextoPercentual(self, coluna=None):
        if coluna is None:
            qtdInformacoes = self.dados.shape[0] * self.dados.shape[1]
            camposNulos = self.dados.isnull().sum()
        else:
            qtdInformacoes = self.dados[coluna].shape[0] 
            camposNulos = self.dados[coluna].isnull().sum()
        qtdNulos = camposNulos.sum()
        return f'Percentual de nulos: {(qtdNulos / qtdInformacoes * 100):0.2f}%'
    
    def getListaDeColunas(self):
        return self.dados.columns
    
    def getListaDeColunasTexto(self):
        colunas_str = ', '.join(self.dados.columns)
        return f'Colunas: {colunas_str.replace('\n', ',')}'
    
    def getTabelaDeColunas(self):
        tipos = []
        classif = []
        for t in self.dados.dtypes:
            if t == 'object':
                tipos.append('Texto')
                classif.append('Qualitativa Nominal')
            elif t == 'int64':
                tipos.append('Inteiro')
                classif.append('Quantitativa Discreta')
            elif t == 'float64':
                tipos.append('Decimal')
                classif.append('Quantitativa Contínua')
            elif t == 'datetime64[ns]':
                tipos.append('Data/Hora')
                classif.append('Data')
            else:
                tipos.append(None)
                classif.append(None)
        # return pd.DataFrame({'Cols': self.data.columns, 'Types': self.data.dtypes})
        #return pd.DataFrame(data={'NomeColuna': self.dados.columns, 'TipoColuna': tipos, 'ClassifColuna': classif}, index=self.dados.columns)
        if self.colunas is None:
            self.colunas = pd.DataFrame(data={'NomeColuna': self.dados.columns, 'TipoColuna': tipos, 'ClassifColuna': classif}, index=self.dados.columns)
        return self.colunas
    
    def setTabelaDeColunas(self, tabelaDeColunas: pd.DataFrame):
        self.colunas = tabelaDeColunas