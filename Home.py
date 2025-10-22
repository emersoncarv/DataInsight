import streamlit as st

# dados do dataset
if 'dados' not in st.session_state:
    # print('removendo dados')
    st.session_state['dados'] = None
    st.session_state['colunas'] = None

st.set_page_config(
    page_title='Data Insight',
    layout='wide'
)
    
pages = {
    "Data Insight": [
        st.Page('paginas/welcome.py', title='Boas-Vindas', default=True, icon='👋'),
        st.Page('paginas/load_dataset.py', title='Importar Arquivo', icon='📂'),
        st.Page('paginas/column_config.py', title='Config. Colunas', icon='📄'),
        st.Page('paginas/dataset_insights.py', title='Insights para o Dataset', icon='💡'),
        st.Page('paginas/data_analysis_column.py', title='Análise de Dados Univariada', icon='📈'),
        st.Page('paginas/data_analysis_multiple_columns.py', title='Análise de Dados Multivariada', icon='📈'),
    ]
}

pg = st.navigation(pages)
pg.run()    
