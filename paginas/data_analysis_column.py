import streamlit as st
import time
import pandas as pd
from classes.Dataset import AnaliseDataset
import locale 
locale.setlocale(locale.LC_ALL, locale='pt_BR')
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


st.title('Análise de Dados Univariada')
ds = AnaliseDataset(st.session_state['dados'], st.session_state['colunas'])
colunas = pd.DataFrame(st.session_state['colunas'])

colNome, _ = st.columns(2)
with colNome:
    nomeColuna = st.selectbox('Selecione a coluna a detalhar', options=ds.Colunas)
    coluna = colunas[colunas.NomeColuna == nomeColuna]

# informações iniciais
dados = pd.DataFrame(st.session_state['dados'][nomeColuna])
st.write(f'Tipo de dados: {coluna['TipoColuna'].iloc[0]} | Classificação: {coluna['ClassifColuna'].iloc[0]}')
st.write(f'{ds.PercentualValoresNulos()['texto']}')


# coluna qualitativa
if 'Qualitativa' in coluna['ClassifColuna'].iloc[0]:
    st.divider()
    
    col1, col2 = st.columns([0.4, 0.6])
    dfDistFreq = ds.DistribuicaoDeFrequencia(nomeColuna)
    concentracao_itens = ds.ConcentracaoDeItens(nomeColuna)
    # print(concentracao_itens)

    with col1:
        # st.subheader('Concentração de Itens')
        # st.write('Concentração de Itens')
        # st.write(ds.ConcentracaoDeItens(nomeColuna)['texto'])
        st.write(concentracao_itens['texto'])
        st.dataframe(dfDistFreq, use_container_width=True)

    with col2:
        # # st.subheader('Distribuição dos Itens')
        # fig = px.bar(dfDistFreq, x='Quantidade', y=nomeColuna, text_auto=True, orientation='h', title='Distribuição dos Itens')
        # fig.update_layout(yaxis={'categoryorder': 'total ascending'})
        # st.plotly_chart(fig)
        fig = go.Figure()
 
        # altera cor da barra para itens que fazem parte da concentração
        # itens_concentracao = ds.ConcentracaoDeItens(nomeColuna)['lista']
        marker_colors = ['darkgreen' if (len(concentracao_itens['lista']) > 0) and (str(item) in concentracao_itens['lista']) 
                         else 'blue' 
                         for item in dfDistFreq[nomeColuna]]
        
        fig.add_trace(go.Bar(
            x=dfDistFreq[nomeColuna],
            y=dfDistFreq['Quantidade'],
            name='Quantidade',
            #marker_color='blue',
            marker_color=marker_colors
        ))
        
        fig.add_trace(go.Scatter(
            x=dfDistFreq[nomeColuna],
            y=dfDistFreq['PercentualAcum']/100,
            mode='lines+markers',
            name='% Acumulado',
            yaxis='y2',
            marker_color='red',
        ))
        
        fig.update_layout(
            title='Distribuição dos Itens',
            xaxis=dict(type='category'),
            yaxis=dict(title='Quantidade'),
            yaxis2=dict(
                title='% Acumulado',
                overlaying='y',
                side='right',
                rangemode='tozero',
                tickvals=[0, 25, 50, 75, 100],
                tickformat='%',
            )
        )
        
        # fig.show()
        st.plotly_chart(fig)


# coluna quantitativa
if 'Quantitativa' in coluna['ClassifColuna'].iloc[0]:
    col1, col2, col3 = st.columns(3)

    with col1:
        # st.subheader('Histograma')
        fig = px.histogram(dados, title=f'Histograma de {nomeColuna}', labels=None)
        fig.update(layout_showlegend=False)
        st.plotly_chart(fig)

    with col2:
        st.dataframe(ds.EstatisticaDescritiva(nomeColuna), use_container_width=True)

    with col3:
        # st.subheader('Outliers')
        outliers = ds.Outliers(nomeColuna)
        st.write(f'Quantidade de outliers: {outliers['valor']}')
        # st.write(f'% outliers: {ds.EstatisticaDescritiva(nomeColuna)['lista']['PctOutliers']}')

        # Criar o boxplot com Plotly
        fig = px.box(dados, title=f'Boxplot')
        st.plotly_chart(fig)

# colunas Data e Data/Hora
if ('Data' in coluna['ClassifColuna'].iloc[0]) or ('Data/Hora' in coluna['ClassifColuna'].iloc[0]):
    col1, col2, col3 = st.columns(3)

    with col1:
        # st.subheader('Registros diários')
        dados_agrupados = dados.value_counts().reset_index()
        dados_agrupados.sort_values(by=[nomeColuna], inplace=True)

        fig = px.line(dados_agrupados, x=nomeColuna, y='count', title='Registros Diários')
        fig.update_traces(texttemplate="%{y}")
        st.plotly_chart(fig)

    with col2:
        # st.subheader('Registros por mês')
        dados_agrupados = dados
        dados_agrupados['__anomes'] = dados_agrupados[nomeColuna].dt.to_period('M')
        dados_agrupados['__anomes'] = dados_agrupados['__anomes'].dt.to_timestamp()
        dados_agrupados = dados['__anomes'].value_counts().reset_index()
        dados_agrupados.sort_values(by=['__anomes'], inplace=True)
        
        fig = px.bar(dados_agrupados, x='__anomes', y='count', labels='y', title='Registros por Mês')
        fig.update_traces(texttemplate="%{y}")
        st.plotly_chart(fig)

    with col3:
        # st.subheader('Registros por dia sem.')
        dados_agrupados = dados
        dados_agrupados['__diasem'] = dados_agrupados[nomeColuna].dt.day_name(locale='pt_BR')
        dados_agrupados = dados['__diasem'].value_counts().reset_index()
        dados_agrupados.sort_values(by=['count'], ascending=True, inplace=True)
        
        fig = px.bar(dados_agrupados, x='count', y='__diasem', labels='y', orientation='h', title='Registros por Dia da Semana')
        fig.update_traces(texttemplate="%{x}")
        st.plotly_chart(fig)
        
if 'Data/Hora' in coluna['ClassifColuna'].iloc[0]:
    col1, col2 = st.columns([0.7, 0.3])

    with col1:
        # st.subheader('Registros por hora do dia')
        dados_agrupados = dados
        dados_agrupados['__hora'] = dados_agrupados[nomeColuna].dt.hour
        dados_agrupados = dados['__hora'].value_counts().reset_index()
        dados_agrupados.sort_values(by=['count'], ascending=True, inplace=True)
        
        fig = px.bar(dados_agrupados, x='__hora', y='count', labels='y', title='Registros por Hora do Dia')
        fig.update_traces(texttemplate="%{y}")
        st.plotly_chart(fig)

