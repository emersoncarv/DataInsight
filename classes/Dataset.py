import pandas as pd
import streamlit as st

class AnaliseDataset:
    """
    Classe AnaliseDataset

    Esta classe fornece métodos para análise e geração de insights a partir de um DataFrame do pandas.
    """
    def __init__(self, dados: pd.DataFrame, configColunas: pd.DataFrame=None):
        """
        Inicializa a classe AnaliseDataset com os dados e a configuração das colunas.

        Parâmetros:
            dados (pd.DataFrame): DataFrame contendo os dados a serem analisados.
            configColunas (pd.DataFrame, opcional): DataFrame contendo a configuração das colunas. Se não for fornecido, a configuração será preparada automaticamente.

        Atributos:
            _dados (pd.DataFrame): DataFrame contendo os dados a serem analisados.
            _configColunas (pd.DataFrame): DataFrame contendo a configuração das colunas, incluindo tipo e classificação.
        """
        self._dados = dados
        if configColunas is not None:
            self._configColunas = configColunas
        else:
            self._configColunas = self._prepararConfigColunas()
        self._configColunas = self._classificarColunas()

    def _prepararConfigColunas(self) -> pd.DataFrame:
        """
        Prepara a configuração das colunas com base nos tipos de dados do DataFrame.

        Este método analisa os tipos de dados das colunas do DataFrame e cria um novo DataFrame com a configuração das colunas, incluindo o nome da coluna, o tipo de coluna e a classificação da coluna.

        Retorna:
            pd.DataFrame: DataFrame contendo a configuração das colunas, com as seguintes colunas:
                NomeColuna: Nome da coluna original.
                TipoColuna: Tipo de dados da coluna (Texto, Inteiro, Decimal, Data/Hora).
                ClassifColuna: Classificação da coluna (inicialmente None).
        """
        dados = self._dados

        tipos = []
        for t in dados.dtypes:
            if t == 'object':
                tipos.append('Texto')
            elif t == 'int64':
                tipos.append('Inteiro')
            elif t == 'float64':
                tipos.append('Decimal')
            elif t == 'datetime64[ns]':
                tipos.append('Data/Hora')
            else:
                tipos.append(None)
            
        # prepara dataframe
        auxColunas = pd.DataFrame(
            data={
                'NomeColuna': dados.columns, 
                'TipoColuna': tipos,
                'ClassifColuna': None
            }, index=dados.columns)
        
        return auxColunas
    
    def _obterClassificacaoColuna(self, tipoDeDados: str) -> str:
        """
        Obtém a classificação da coluna com base no tipo de dados.

        Parâmetros:
            tipoDeDados (str): Tipo de dados da coluna (Texto, Inteiro, Decimal, Data).

        Retorna:
            str: Classificação da coluna com base no tipo de dados
                - None para tipos de dados não reconhecidos.
        """
        if tipoDeDados == 'Texto':
            return 'Qualitativa Nominal'
        elif tipoDeDados == 'Inteiro':
            return 'Quantitativa Discreta'
        elif tipoDeDados == 'Decimal':
            return 'Quantitativa Contínua'
        elif tipoDeDados == 'Data':
            return 'Data'
        elif tipoDeDados == 'Data/Hora':
            return 'Data/Hora'
        else:
            return None
        
    def _classificarColunas(self) -> pd.DataFrame:
        """
        Classifica as colunas do DataFrame com base nos tipos de dados.

        Este método aplica a função `_obterClassificacaoColuna` a cada tipo de coluna no DataFrame de configuração das colunas, 
        atualizando a coluna 'ClassifColuna' com a classificação apropriada.

        Retorna:
            pd.DataFrame: DataFrame atualizado contendo a configuração das colunas, incluindo a classificação das colunas.
        """
        colunas = self._configColunas
        colunas['ClassifColuna'] = colunas['TipoColuna'].apply(lambda x: self._obterClassificacaoColuna(x))
        return colunas 

    @property
    def Dados(self):
        return self._dados
    
    @property
    def ConfigColunas(self):
        return self._configColunas
    
    @property
    def MemoriaEmBytes(self) -> pd.DataFrame:
        return self.Dados.memory_usage().sum()
    
    @property
    def QuantidadeDeLinhas(self) -> int:
        return self.Dados.shape[0]
    
    @property
    def QuantidadeDeColunas(self) -> int:
        return self.Dados.shape[1]
    
    @property 
    def Colunas(self) -> list:
        df = self._configColunas
        return df.loc[:, 'NomeColuna'].to_list()

    @property
    def ColunasQualitativas(self) -> list:
        df = self._configColunas[self._configColunas['ClassifColuna'].str.contains('Qualitativa')]
        return df['NomeColuna'].to_list()
    
    @property
    def ColunasQuantitativas(self) -> list:
        df = self._configColunas[self._configColunas['ClassifColuna'].str.contains('Quantitativa')]
        return df['NomeColuna'].to_list()
    
    @property
    def ColunasData(self) -> list:
        df = self._configColunas[self._configColunas['ClassifColuna'] == 'Data']
        return df['NomeColuna'].to_list()
    
    @property
    def ColunasDataHora(self) -> list:
        df = self._configColunas[self._configColunas['ClassifColuna'] == 'Data/Hora']
        return df['NomeColuna'].to_list()

    @property
    def ListaDeColunas(self) -> str: 
        """
        Retorna uma string com os nomes das colunas do DataFrame.

        Esta propriedade percorre as colunas do DataFrame e cria uma string com os nomes das colunas, separados por vírgulas.

        Retorna:
            str: String contendo os nomes das colunas do DataFrame.

        Exemplo de uso:
            >>> import pandas as pd
            >>> dados = pd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4, 5, 6],
            ...     'C': [7, 8, 9]
            ... })
            >>> analise = AnaliseDataset(dados)
            >>> lista_colunas = analise.ListaDeColunas
            >>> print(lista_colunas)
            'A, B, C'
        """
        dados = self.Dados
        colunas_str = ', '.join(dados.columns)
        return f'{colunas_str.replace('\n', ',')}'
    
    @property
    def ListaDeColunasETipos(self) -> str:
        """
        Retorna uma string com os nomes das colunas e seus respectivos tipos de dados.

        Esta propriedade percorre o DataFrame de configuração das colunas e cria uma lista de strings, onde cada string contém o nome da coluna e seu tipo de dados entre parênteses. A lista é então convertida em uma única string, com os itens separados por vírgulas.

        Retorna:
            str: String contendo os nomes das colunas e seus tipos de dados, no formato 'NomeColuna1 (TipoColuna1), NomeColuna2 (TipoColuna2)'.

        Exemplo de uso:
            >>> import pandas as pd
            >>> dados = pd.DataFrame({
            ...     'A': [1, 2, 3],
            ...     'B': [4.0, 5.0, 6.0],
            ...     'C': ['x', 'y', 'z']
            ... })
            >>> analise = AnaliseDataset(dados)
            >>> lista_colunas_tipos = analise.ListaDeColunasETipos
            >>> print(lista_colunas_tipos)
            'A (Inteiro), B (Decimal), C (Texto)'
        """
        colunas = self.ConfigColunas
        colunas_aux = []
        for idx, linha in colunas.iterrows():
            colunas_aux.append(linha['NomeColuna'] + ' (' + linha['TipoColuna'] + ')')
        return ', '.join(colunas_aux)

    # # -----------------------------
    # # Métodos gerais

    def Amostra(self, linhas: int) -> pd.DataFrame:
        return self.Dados.head(linhas)

    def PercentualValoresNulos(self, coluna=None) -> dict:
        """
        Calcula o percentual de valores nulos no DataFrame ou em uma coluna específica.

        Parâmetros:
            coluna (str, opcional): Nome da coluna para calcular o percentual de valores nulos. Se não for fornecido, o cálculo será feito para todo o DataFrame.

        Retorna:
            dict: Dicionário contendo:
                'valor': Percentual de valores nulos.
                'texto': String formatada com o percentual de valores nulos.

        Exemplo de uso:
        >>> import pandas as pd
        >>> dados = pd.DataFrame({
        ...     'A': [1, 2, None, 4],
        ...     'B': [None, 2, 3, 4]
        ... })
        >>> analise = AnaliseDataset(dados)
        >>> percentual_nulos = analise.PercentualValoresNulos()
        >>> print(percentual_nulos)
        {
            'valor': 25.0,
            'texto': 'Percentual de nulos: 25.00%'
        }
        >>> percentual_nulos_coluna = analise.PercentualValoresNulos(coluna='A')
        >>> print(percentual_nulos_coluna)
        {
            'valor': 25.0,
            'texto': 'Percentual de nulos: 25.00%'
        }
        """
        dados = self.Dados
        if coluna is None:
            qtdInformacoes = self.QuantidadeDeLinhas * self.QuantidadeDeColunas
            camposNulos = dados.isnull().sum()
        else:
            qtdInformacoes = self.QuantidadeDeLinhas
            camposNulos = dados[coluna].isnull().sum()
        qtdNulos = camposNulos.sum()
        ret = {
            'valor': qtdNulos / qtdInformacoes * 100,
            'texto': f'👎 Percentual de nulos: {qtdNulos / qtdInformacoes * 100:.2f}%'
        }
        return ret

    # -----------------------------
    # Análises Individuais
    # Colunas Qualitativas
    
    def DistribuicaoDeFrequencia(self, coluna: str) -> pd.DataFrame:
        """
        Calcula a distribuição de frequência de uma coluna qualitativa.

        Parâmetros:
            coluna (str): Nome da coluna qualitativa para calcular a distribuição de frequência.

        Retorna:
            pd.DataFrame: DataFrame contendo a distribuição de frequência da coluna, com as seguintes colunas:
                'Quantidade': Contagem de cada valor.
                'Percentual': Percentual de cada valor em relação ao total.
                'PercentualAcum': Percentual acumulado de cada valor.

        Lança:
            Exception: Se a coluna fornecida não for identificada como qualitativa.
        """
        if coluna not in self.ColunasQualitativas:
            raise Exception(f'A coluna {coluna} não é identificada como Qualitativa.')

        dfDados = self.Dados[coluna]
        qtdItens = dfDados.shape[0]

        dfItens = dfDados.value_counts(sort=True).reset_index()
        dfItens.rename(columns={'count': 'Quantidade'}, inplace=True)
        dfItens['Percentual'] = dfItens['Quantidade'] / qtdItens * 100.0
        dfItens['PercentualAcum'] = dfItens['Percentual'].cumsum() 

        return dfItens
    
    # def ConcentracaoDeItens(self, coluna: str, percentual_minimo_acum=0.7, percentual_maximo_registros=0.3) -> dict:
    #     if coluna not in self.ColunasQualitativas:
    #         raise Exception(f'A coluna {coluna} não é identificada como Qualitativa.')
        
    #     dfDados = self.Dados[coluna]

    #     # Contar a frequência de cada valor em percentual
    #     dfFrequencia = dfDados.value_counts(normalize=True)

    #     # Identificar os valores que somados correspondem a pelo menos N% do DataFrame
    #     soma_frequencia = 0
    #     valores_selecionados = []

    #     for valor, freq in dfFrequencia.items():
    #         soma_frequencia += freq
    #         valores_selecionados.append("'" + str(valor) + "'")
    #         if soma_frequencia >= percentual_minimo_acum:
    #             break

    #     if len(valores_selecionados) > (dfFrequencia.shape[0] * percentual_maximo_registros):
    #         valores_selecionados = []

    #     # prepara retorno
    #     if len(valores_selecionados) == 0:
    #         return {
    #             'valor': 0,
    #             'texto': 'Não há concentração de itens nesta coluna.'
    #         }
    #     elif len(valores_selecionados) == 1:
    #         return {
    #             'valor': 1,
    #             'texto': f"O item {valores_selecionados[0]} é responsável por {soma_frequencia*100:.2f}% dos dados."
    #         }
    #     else:
    #         return {
    #             'valor': len(valores_selecionados),
    #             'texto': f"Os itens {', '.join(valores_selecionados)} são responsáveis por {soma_frequencia*100:.2f}% dos dados."
    #         }
        
    def ConcentracaoDeItens(self, coluna: str) -> dict:
        """
        Calcula a concentração de itens em uma coluna qualitativa.

        Parâmetros:
            coluna (str): Nome da coluna qualitativa para calcular a concentração de itens.

        Retorna:
            dict: Dicionário contendo:
                'valor': Número de itens responsáveis pela concentração.
                'texto': String formatada com a descrição da concentração dos itens.
                'lista': Lista com os itens que estão concentrados.

        Lança:
            Exception: Se a coluna fornecida não for identificada como qualitativa.

        Exemplo de uso:
        >>> import pandas as pd
        >>> dados = pd.DataFrame({'Categoria': ['A', 'A', 'B', 'B', 'B', 'C', 'C', 'C', 'C']})
        >>> analise = AnaliseDataset(dados)
        >>> concentracao = analise.ConcentracaoDeItens('Categoria')
        >>> print(concentracao)
        {
            'valor': 1,
            'texto': "O item 'C' é responsável por 44.44% dos dados."
            'lista: ['C']
        }
        """
        if coluna not in self.ColunasQualitativas:
            raise Exception(f'A coluna {coluna} não é identificada como Qualitativa.')

        dfDados = pd.DataFrame(self.Dados[coluna])

        # identifica se a coluna possui apenas um valor exclusivo
        if dfDados[coluna].nunique() == 1:
            return {
                'valor': 1,
                'texto': f"💯 O item {dfDados[coluna][0]} é responsável por 100% dos dados.",
                'lista': [dfDados[coluna][0]]
            }
        
        # identifica se a coluna só possui valores exclusivos
        if len(dfDados[coluna].unique()) == dfDados[coluna].shape[0]:
            return {
                'valor': 1,
                'texto': f"🔑 A coluna é composta apenas de valores exclusivos.",
                'lista': []
            }

        # Contar a frequência de cada valor em percentual
        dfFrequencia = dfDados.value_counts(normalize=True).reset_index()
        valores_selecionados = []
        soma_frequencia = 0

        if dfFrequencia.shape[0] == 2 and dfFrequencia['proportion'][0] >= 0.7:
            # quando há poucos itens, não é possível considerar a média para identificar outliers
            valores_selecionados.append(str(dfFrequencia[coluna][0]))
            soma_frequencia = dfFrequencia['proportion'][0]
        else:
            # identificar outliers a partir da frequência
            dsFreq = AnaliseDataset(dfFrequencia)
            outliers = dsFreq.Outliers(coluna='proportion')
            # print(outliers)

            # busca os itens com concentração
            dfDadosConcentracao = dfFrequencia[dfFrequencia['proportion'].isin(outliers['lista'])]
            for idx, row in dfDadosConcentracao.iterrows():
                soma_frequencia += row['proportion']
                valores_selecionados.append(str(row[coluna]))
        
        #valores_selecionados = [valor.replace('.0', '') if valor.endswith('.0''') else valor for valor in valores_selecionados]
        valores_selecionados = [valor.replace('.0', '') for valor in valores_selecionados]

        # prepara retorno
        if len(valores_selecionados) == 0:
            return {
                'valor': 0,
                'texto': '📊 Não há concentração de itens nesta coluna.',
                'lista': []
            }
        elif len(valores_selecionados) == 1:
            return {
                'valor': 1,
                'texto': f"📊 O item '{valores_selecionados[0]}' é responsável por {soma_frequencia*100:.2f}% dos dados.",
                'lista': valores_selecionados
            }
        else:
            return {
                'valor': len(valores_selecionados),
                'texto': f"📊 Os itens '{"', '".join(valores_selecionados)}' são responsáveis por {soma_frequencia*100:.2f}% dos dados.",
                'lista': valores_selecionados
            }


    # -----------------------------
    # Análises Individuais
    # Colunas Quantitativas

    def Outliers(self, coluna: str, qtd_desvios:float=1.5) -> dict:
        """
        Identifica os outliers em uma coluna quantitativa.

        Parâmetros:
            coluna (str): Nome da coluna quantitativa para identificar os outliers.
            qtd_desvios (float): Quantidade de desvios-padrão para identificar os outliers acima ou abaixo.

        Retorna:
            dict: Dicionário contendo:
                'valor': Número de outliers identificados.
                'texto': String formatada com a quantidade de outliers.
                'lista': Lista de valores que são considerados outliers.

        Exemplo de uso:
        >>> import pandas as pd
        >>> dados = pd.DataFrame({'Valores': [10, 12, 14, 15, 18, 20, 22, 100]})
        >>> analise = AnaliseDataset(dados)
        >>> outliers = analise.Outliers('Valores')
        >>> print(outliers)
        {
            'valor': 1,
            'texto': 'Outliers: 1',
            'lista': [100],
        }
        """

        # Calcular o primeiro quartil (Q1) e o terceiro quartil (Q3)
        Q1 = self.Dados[coluna].quantile(0.25)
        Q3 = self.Dados[coluna].quantile(0.75)
        
        # Calcular o intervalo interquartil (IQR)
        IQR = Q3 - Q1
        
        # Definir os limites inferiores e superiores para outliers
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        
        # identifica outliers
        outliers = self.Dados[ (self.Dados[coluna] < lower_bound) | (self.Dados[coluna] > upper_bound) ][coluna].sort_values().to_list()
        outliers_acima  = [v for v in outliers if v > lower_bound]
        outliers_abaixo = [v for v in outliers if v < upper_bound]

        return {
            'valor': len(outliers),
            'texto': f'〽️ Outliers: {len(outliers)}',
            # 'valor_referencia': valor_referencia,
            'lista': outliers,
            'valor_acima': len(outliers_acima),
            'lista_acima': outliers_acima,
            'valor_abaixo': len(outliers_abaixo),
            'lista_abaixo': outliers_abaixo,
        }

    def EstatisticaDescritiva(self, coluna: str, 
                              metricas: list=['Menor', 'Maior', 'Média', 'Mediana', 'Desvio-Padrão', 'Maior', '25%', '75%', 'DIQ', 'QtdOutliers', 'PctOutliers', 'Outliers']):
        """
        Calcula as estatísticas descritivas de uma coluna quantitativa.

        Parâmetros:
            coluna (str): Nome da coluna quantitativa para calcular as estatísticas descritivas.
            metricas (list, opcional): Lista de métricas a serem calculadas. As métricas padrão são ['Menor', 'Maior', 'Média', 'Mediana', 'Desvio-Padrão', 'Maior', '25%', '75%', 'DIQ', 'QtdOutliers', 'PctOutliers', 'Outliers'].

        Retorna:
            dict: Dicionário contendo as métricas calculadas.

        Lança:
            Exception: Se a coluna fornecida não for identificada como quantitativa.

        Exemplo de uso:
            >>> import pandas as pd
            >>> dados = pd.DataFrame({'Valores': [10, 12, 14, 15, 18, 20, 22, 100]})
            >>> analise = AnaliseDataset(dados)
            >>> estatisticas = analise.EstatisticaDescritiva('Valores')
            >>> print(estatisticas)
            {
                'lista': {
                    'Menor': 10,
                    'Média': 26.375,
                    'Mediana': 16.5,
                    'Desvio-Padrão': 28.288,
                    'Maior': 100,
                    '25%': 13.5,
                    '75%': 21.5,
                    'DIQ': 8.0,
                    'QtdOutliers': 1,
                    'PctOutliers': 12.5,
                    'Outliers': [100]
                }
            }
        """
        
        if coluna not in self.ColunasQuantitativas:
            raise Exception(f'A coluna {coluna} não é identificada como Quantitativa.')
        
        informacao = {}
        if 'Menor' in metricas:
            informacao['Menor'] = self.Dados[coluna].min()
        if 'Média' in metricas:
            informacao['Média'] = self.Dados[coluna].mean()
        if 'Mediana' in metricas:
            informacao['Mediana'] = self.Dados[coluna].median()
        if 'Desvio-Padrão' in metricas:
            informacao['Desvio-Padrão'] = self.Dados[coluna].std()
        if 'Maior' in metricas:
            informacao['Maior'] = self.Dados[coluna].max()
        if '25%' in metricas:
            # informacao['0%'] = self.Dados[coluna].quantile(0)
            informacao['25%'] = self.Dados[coluna].quantile(0.25)
        if '75%' in metricas:
            informacao['75%'] = self.Dados[coluna].quantile(0.75)
            # informacao['100%'] = self.Dados[coluna].quantile(1)
        if 'DIQ' in metricas:
            informacao['DIQ'] = self.Dados[coluna].quantile(0.75) - self.Dados[coluna].quantile(0.25)
        if 'QtdOutliers' in metricas or 'PctOutliers' in metricas or 'Outliers' in metricas:
            # # identifica outliers
            outliers = self.Outliers(coluna)

            # adiciona informações
            if 'QtdOutliers' in metricas:
                informacao['QtdOutliers'] = outliers['valor'] 
            if 'PctOutliers' in metricas:
                informacao['PctOutliers'] = outliers['valor'] / self.Dados[coluna].count() * 100.0
            if 'Outliers' in metricas:
                informacao['Outliers'] = outliers['lista'] 

        #return informacao
        return {
            'lista': informacao
        }
    

    # # -----------------------------
    # # Análises Múltiplas
    
    def MatrizDeConfusao(self, coluna1: str, coluna2: str) -> pd.DataFrame:
        for coluna in [coluna1, coluna2]:
            if coluna not in self.ColunasQualitativas:
                raise Exception(f'A coluna {coluna} não é identificada como Qualitativa.')

        dados = self.Dados[[coluna1, coluna2]]
        return pd.crosstab(dados[coluna1], dados[coluna2])
    

    def TotalPorCategoria(self, coluna1: str, coluna2: str, operacao='Soma') -> pd.DataFrame:
        if coluna1 not in self.ColunasQualitativas:
            raise Exception(f'A coluna {coluna1} não é identificada como Qualitativa.')
        if coluna2 not in self.ColunasQuantitativas:
            raise Exception(f'A coluna {coluna1} não é identificada como Quantitativa.')

        dados = self.Dados[[coluna1, coluna2]]
        
        if operacao == 'Soma':
            operacao_agg = 'sum'
        elif operacao == 'Média':
            operacao_agg = 'mean'
        else:
            operacao_agg = 'count'

        # print(operacao, operacao_agg)
        return dados.groupby(coluna1).agg({coluna2: operacao_agg}).reset_index()
    
    
    def ValorDeCorrelacao(self, coluna1: str, coluna2: str) -> float:
        return self.Dados[coluna1].corr(self.Dados[coluna2])
    
    def MatrizDeCorrelacao(self) -> pd.DataFrame:
        colunas = self.ColunasQuantitativas
        if len(colunas) < 2:
            return None
        return self.Dados[colunas].corr()
    
    def CorrelacoesRelevantes(self, valor_base_correlacao: int=0.7):
        # gera a matriz de correlação das colunas quantitativas
        matriz_correlacao_orig = self.MatrizDeCorrelacao()
        if matriz_correlacao_orig is None:
            return None

        # remove o índice das linhas transformando em coluna_a
        matriz_correlacao_1 = matriz_correlacao_orig.reset_index().rename({'index': 'coluna_a'}, axis=1)
        # unpivota as colunas, transformando-as em linhas, gerando as colunas coluna_b e correlacao
        matriz_correlacao_2 = pd.melt(matriz_correlacao_1, id_vars=['coluna_a'], var_name='coluna_b', value_name='correlacao')

        # filtra apenas correlações de interesse com base no valor
        matriz_correlacao_3 = matriz_correlacao_2[
            (
                (matriz_correlacao_2['correlacao'] <= -valor_base_correlacao) |             # correlação negativa
                (matriz_correlacao_2['correlacao'] >= valor_base_correlacao)                # correlação positiva
            ) & (matriz_correlacao_2['coluna_a'] != matriz_correlacao_2['coluna_b'])        # coluna com ela mesma
        ].sort_values(by='correlacao', ascending=False)                                     # ordena de forma decrescente

        return matriz_correlacao_3

