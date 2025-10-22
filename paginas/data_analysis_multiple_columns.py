import streamlit as st
import time
import pandas as pd
from classes.Dataset import AnaliseDataset
# import locale 
# locale.setlocale(locale.LC_ALL, locale='pt_BR')
import plotly.express as px
import plotly.graph_objects as go

# import warnings
# warnings.filterwarnings("ignore")

if st.session_state['dados'] is None:
    mensagem = "Não há um dataset carregado. Redirecionando para a página de importação de arquivos em instantes."
    progresso = st.progress(0, text=mensagem)
    for percentual in range(100):
        time.sleep(0.015)
        progresso.progress(percentual+1, text=mensagem)
    st.switch_page('paginas/load_dataset.py')


st.title('Análise de Dados Multivariada')
blnContinuar = True

ds = AnaliseDataset(st.session_state['dados'], st.session_state['colunas'])
dados = ds.Dados
colunas = ds.ConfigColunas

colEsq, colDir = st.columns(2)
with colEsq:
    nomeColunaEsq = st.selectbox('Selecione uma coluna', options=ds.Colunas, key='nomeColunaEsq', index=None)
    if nomeColunaEsq is not None:
        colunaEsq = colunas.loc[nomeColunaEsq]
        st.write(colunaEsq['ClassifColuna'])
with colDir:
    nomeColunaDir = st.selectbox('Selecione uma coluna', options=ds.Colunas, key='nomeColunaDir', index=None)
    if nomeColunaDir is not None:
        colunaDir = colunas.loc[nomeColunaDir]
        st.write(colunaDir['ClassifColuna'])

# alertas 
if nomeColunaEsq is None or nomeColunaDir is None:
    st.warning('Selecione os nomes das colunas para realizar a análise.')
    blnContinuar = False

if (nomeColunaEsq is not None) and (nomeColunaDir is not None) and (nomeColunaEsq == nomeColunaDir) :
    st.error('Por favor, selecione colunas distintas.')
    blnContinuar = False


# informações de análise
if blnContinuar:
    st.divider()
    colunaEsq = colunas.loc[nomeColunaEsq]
    colunaDir = colunas.loc[nomeColunaDir]

    # qualitativa vs qualitativa
    if ('Qualitativa' in colunaEsq['ClassifColuna']) and ('Qualitativa' in colunaDir['ClassifColuna']):
        matriz = ds.MatrizDeConfusao(nomeColunaEsq, nomeColunaDir)
        st.dataframe(matriz.style.highlight_max(axis=0, color='orange').highlight_min(axis=0, color='lightblue'), width='stretch')
        # fig = px.density_heatmap(matriz, title='Matriz de Confusão')
        # fig = px.density_mapbox(matriz)
        # st.plotly_chart(fig)

    
    # qualitativa vs quantitativa
    if (('Qualitativa' in colunaEsq['ClassifColuna']) and ('Quantitativa' in colunaDir['ClassifColuna'])): # or (('Quantitativa' in colunaEsq['ClassifColuna']) and ('Qualitativa' in colunaDir['ClassifColuna'])):
        operacao1 = st.selectbox('Informe a operação a aplicar na coluna Qualitativa', options=['Soma', 'Média', 'Contagem'])

        dados_analise = ds.TotalPorCategoria(nomeColunaEsq, nomeColunaDir, operacao1)
        # print(dados_analise)

        fig = px.bar(dados_analise.sort_values(by=nomeColunaDir), x=nomeColunaDir, y=nomeColunaEsq, labels=nomeColunaDir, orientation='h', 
                     title=f'{nomeColunaEsq} vs {nomeColunaDir}')
        fig.update_traces(texttemplate="%{x}")
        st.plotly_chart(fig)

    
    # quantitativa vs quantitativa
    if ('Quantitativa' in colunaEsq['ClassifColuna']) and ('Quantitativa' in colunaDir['ClassifColuna']):
        correlacao = ds.ValorDeCorrelacao(nomeColunaEsq, nomeColunaDir)
        if correlacao >= 0.7 or correlacao <= -0.7:
            box = st.info 
            blnMostrarCorr = True
        elif correlacao >= 0.4 or correlacao <= -0.4:
            box = st.warning
            blnMostrarCorr = True
        else:
            box = st.error
            blnMostrarCorr = False
        box(f'Correlação: {correlacao}')

        dados_amostra = dados.sample(10000, random_state=42, replace=True)
        fig = go.Figure()
        fig.add_trace(go.Scatter(
        # fig.add_trace(go.Scattergl(
            x=dados_amostra[nomeColunaEsq],
            y=dados_amostra[nomeColunaDir],
            mode='markers',
            name='Itens',
            zorder=1,
        ))
        fig.update_layout(
            title=dict(
                text=f'{nomeColunaEsq} vs {nomeColunaDir}'
            ),
            xaxis=dict(
                title=dict(
                    text=nomeColunaEsq
                )
            ),
            yaxis=dict(
                title=dict(
                    text=nomeColunaDir
                )
            )
        )

        if blnMostrarCorr:
            fig.add_trace(go.Scatter(
                x=[dados[nomeColunaEsq].min(), dados[nomeColunaEsq].max()] if correlacao > 0 else [dados[nomeColunaEsq].min(), dados[nomeColunaEsq].max()] ,
                y=[dados[nomeColunaDir].min(), dados[nomeColunaDir].max()] if correlacao > 0 else [dados[nomeColunaDir].max(), dados[nomeColunaDir].min()],
                mode='lines',
                name='Correlação',
                yaxis='y',
                marker_color='red',
                opacity=0.15,
                zorder=0,
            ))
        
        fig.update_layout(dict(showlegend=False))
        st.plotly_chart(fig)


    # data ou data/hora vs quantitativa
    if (('Data' in colunaEsq['ClassifColuna']) or ('Data/Hora' in colunaEsq['ClassifColuna'])) and ('Quantitativa' in colunaDir['ClassifColuna']):
        fig = px.line(data_frame=dados, x=nomeColunaEsq, y=nomeColunaDir, title=f'{nomeColunaDir} por {nomeColunaEsq}')
        st.plotly_chart(fig)
