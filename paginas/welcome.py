import streamlit as st

st.title('Bem-vindo ao Data Insight!')
st.markdown('''
Com o Data Insight você pode obter insights poderosos para seu dataset.
        
* Você carrega seu dataset em CSV;
* Você confirma ou ajusta alguns detalhes sobre as colunas do dataset; e
* O Data Insight faz o resto!
            ''')

st.markdown('\n\nPara começar, vamos importar um arquivo.')
st.page_link(page='paginas/load_dataset.py', label='Importar Arquivo', icon=None)

