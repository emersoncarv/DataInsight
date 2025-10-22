import streamlit as st
import pandas as pd
from classes.Dataset import AnaliseDataset

st.title('Importar Arquivo')

# Parte superior
col1, col2 = st.columns(2)
with col1:
    uploaded_file = st.file_uploader('Selecione seu arquivo CSV', type=['csv'], accept_multiple_files=False)
with col2:
    sep = st.selectbox('Selecione o separador de colunas', [',', ';', '\t', '|'])
    decimal = st.selectbox('Selecione o separador de decimais', ['.', ','])

    if uploaded_file is not None:
        data = pd.read_csv(uploaded_file, sep=sep, decimal=decimal)
        st.session_state['uploaded_file'] = uploaded_file
        st.session_state['sep'] = sep
        st.session_state['decimal'] = decimal
        st.session_state['dados'] = data

        if 'dados_preview' in st.session_state and st.session_state['colunas'] is not None:
            ds = AnaliseDataset(st.session_state['dados'], st.session_state['colunas'])
        else:
            ds = AnaliseDataset(st.session_state['dados'])
            st.session_state['colunas'] = ds.ConfigColunas

# parte inferior
if 'dados' in st.session_state and st.session_state['dados'] is not None:
    st.info(f'Linhas: {st.session_state['dados'].shape[0]}, Colunas: {st.session_state['dados'].shape[1]}')

    st.subheader('Preview')
    st.write(st.session_state['dados'])

