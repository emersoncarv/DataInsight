import streamlit as st
import time
import pandas as pd
from classes.Dataset import AnaliseDataset

if st.session_state['dados'] is None:
    mensagem = "Não há um dataset carregado. Redirecionando para a página de importação de arquivos em instantes."
    progresso = st.progress(0, text=mensagem)
    for percentual in range(100):
        time.sleep(0.015)
        progresso.progress(percentual+1, text=mensagem)
    st.switch_page('paginas/load_dataset.py')

st.title('Configuração de Colunas')
st.write('Refine a definição de cada uma das colunas do dataset e clique em Confirmar.')

# obtém os dados armazenados
dados = st.session_state['dados']
if st.session_state['colunas'] is not None:
    # print('\ncolumn_config Iniciando')
    # print(st.session_state['colunas'])
    pass 
dfColunas = st.session_state['colunas']

dfColunas_Edit = st.data_editor(
    dfColunas,
    column_config={
        "NomeColuna": st.column_config.TextColumn(
            "Nome da Coluna",
            required=True,
            disabled=True
        ),
        "TipoColuna": st.column_config.SelectboxColumn(
            "Tipo de Dados",
            width="medium",
            options=[
                "Texto",
                "Inteiro",
                "Decimal",
                "Data",
                "Data/Hora"
            ],
            required=True,
        ),
        "ClassifColuna": st.column_config.SelectboxColumn(
            "Classificação",
            width="medium",
            options=[
                "Qualitativa Nominal",
                # "Qualitativa Ordinal",
                "Quantitativa Discreta",
                "Quantitativa Contínua",
                "Data",
                "Data/Hora"
            ],
            required=True,
            disabled=True,
        )
        
    },
    hide_index=True
)

# se confirmado, atualiza a configuração de colunas
if st.button('Confirmar'):
    st.session_state['colunas'] = dfColunas_Edit

    dados_ajuste = pd.DataFrame( st.session_state['dados'] )
    for idx, row in dfColunas_Edit.iterrows():
        tipo = None
        if row['TipoColuna'] == 'Inteiro':
            tipo = 'int64'
        elif row['TipoColuna'] == 'Decimal':
            tipo = 'float64'
        elif row['TipoColuna'] == 'Texto':
            tipo = 'object'
        elif row['TipoColuna'] == 'Data':
            tipo = 'datetime64[ns]'
        elif row['TipoColuna'] == 'Data/Hora':
            tipo = 'datetime64[ns]'

        if tipo is not None:
            dados_ajuste[idx] = dados_ajuste[idx].astype(tipo)

    # print(dados_ajuste.info())

    # aplica a alteração nos dados
    st.session_state['dados'] = dados_ajuste
    st.rerun()


st.info(f'Linhas: {st.session_state['dados'].shape[0]}, Colunas: {st.session_state['dados'].shape[1]}')
st.subheader('Preview com a configuração')
dados_preview = st.session_state['dados'].head(10)
# print(dados_preview)
st.dataframe(dados_preview)
