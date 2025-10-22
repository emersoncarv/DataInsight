import streamlit as st
import time
import pandas as pd
from classes.Dataset import AnaliseDataset
import plotly.express as px

if st.session_state['dados'] is None:
    mensagem = "Não há um dataset carregado. Redirecionando para a página de importação de arquivos em instantes."
    progresso = st.progress(0, text=mensagem)
    for percentual in range(100):
        time.sleep(0.015)
        progresso.progress(percentual+1, text=mensagem)
    st.switch_page('paginas/load_dataset.py')

st.title('Insights para o Dataset')
ds = AnaliseDataset(st.session_state['dados'], st.session_state['colunas'])
st.info(f'Linhas: {st.session_state['dados'].shape[0]}, Colunas: {st.session_state['dados'].shape[1]}')

# @st.cache_data
def load_insights():
    # ds = AnaliseDataset(st.session_state['dados'], st.session_state['colunas'])

    percNulos = []
    for coluna in ds.Colunas:
        _aux = ds.PercentualValoresNulos(coluna)
        percNulos.append([coluna, 'Percentual de Nulos', _aux['texto'], _aux['valor']])
    dfPercNulos = pd.DataFrame(data=percNulos, columns=['Nome da Coluna', 'Tipo de Informação', 'Informação', 'Valor'])
    # print(dfPercNulos)


    concItens = []
    for coluna in ds.ColunasQualitativas:
        _aux = ds.ConcentracaoDeItens(coluna)
        concItens.append([coluna, 'Concentração de Itens', _aux['texto'], _aux['valor']])
    dfConcItens = pd.DataFrame(data=concItens, columns=['Nome da Coluna', 'Tipo de Informação', 'Informação', 'Valor'])
    # print(dfConcItens)


    outliers = []
    for coluna in ds.ColunasQuantitativas:
        _aux = ds.Outliers(coluna)
        outliers.append([coluna, 'Outliers', _aux['texto'], _aux['valor']])
    dfOutliers = pd.DataFrame(data=outliers, columns=['Nome da Coluna', 'Tipo de Informação', 'Informação', 'Valor'])


    dfCorrelacoes_orig = ds.CorrelacoesRelevantes()
    if dfCorrelacoes_orig is not None:
        dfCorrelacoes = dfCorrelacoes_orig.copy()
        dfCorrelacoes['Nome da Coluna'] = dfCorrelacoes['coluna_a']
        dfCorrelacoes['Tipo de Informação'] = 'Correlação'
        dfCorrelacoes['Informação'] = '📈 Correlação com ' + dfCorrelacoes['coluna_b'] + ' (' + dfCorrelacoes['correlacao'].astype('str') + ')'
        dfCorrelacoes['Valor'] = dfCorrelacoes['correlacao']
        dfCorrelacoes = dfCorrelacoes[ ['Nome da Coluna', 'Tipo de Informação', 'Informação', 'Valor'] ]
    else:
        dfCorrelacoes = pd.DataFrame(data=None, columns=['Nome da Coluna', 'Tipo de Informação', 'Informação', 'Valor'])


    dfFinal = pd.concat([dfPercNulos, dfConcItens, dfOutliers, dfCorrelacoes], ignore_index=True)
    dfFinal.sort_values(by=['Nome da Coluna', 'Tipo de Informação'], inplace=True)
    return dfFinal

# carrega as informações
dados = load_insights()
lista_opcoes = dados['Tipo de Informação'][dados['Valor'] != 0].sort_values().unique()
lista_selecionados = st.multiselect('Selecione o tipo de informação a ser apresentado', options=lista_opcoes, default=lista_opcoes, placeholder='Selecione um tipo')

# filtra os dados de insights
dados_filtrados = dados[ dados['Tipo de Informação'].isin(lista_selecionados) ]
dados_filtrados = dados_filtrados[dados_filtrados['Valor'] != 0]

# apresenta insights
if dados_filtrados.shape[0] > 0:
    st.write(f'Quantidade de insights apresentados: {dados_filtrados.shape[0]}')
    col1, col2 = st.columns([0.25, 0.75])
    with col1:
        fig = px.pie(dados_filtrados, names='Tipo de Informação')
        st.plotly_chart(fig)
    with col2:
        st.dataframe(dados_filtrados.drop('Valor', axis=1), hide_index=True, width='stretch', selection_mode='multi-row')
    
else:
    st.info('Não há insights a apresentar.')