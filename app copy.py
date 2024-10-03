import streamlit as st
from comentarios.comentario import  exibir_comentarios, format_csv_comentario
from hugging_face.analise_sentimento import modelo_ia, grafico_barra, nuvem_palavras
import plotly.express as px


import time
import streamlit as st

def main():
    st.title("Análise de Sentimentos com IA")

    input_url = st.text_input("URL do produto Amazon", key='input_text')

    if input_url:
        progresso = st.progress(0)  # Iniciar barra de progresso em 0%
        
        url_base = f'{input_url}&pageNumber={{}}'
        
        progresso.progress(30)  # Atualizar progresso para 30% ao processar a URL
        
        dados_csv = format_csv_comentario(url_base)
        
        if dados_csv is not None:  # Certifique-se de que dados_csv não é None
            progresso.progress(70)  # Atualizar para 70% enquanto prepara gráficos e análise
            
            # Exibição dos resultados
            col1, col2 = st.columns(2)  # Dividindo em colunas
            
            with col1:
                st.success(f'PALAVRAS POSITIVAS')
                nuvem_palavras(modelo_ia(dados_csv), 'Comentario','POS')
               
            with col2:
                st.error(f'PALAVRAS NEGATIVAS')
                nuvem_palavras(modelo_ia(dados_csv), 'Comentario','NEG')
                
            progresso.progress(100)  # Progresso concluído
            st.success("Análise concluída com sucesso!")
            
        else:
            st.error("Erro ao recuperar os dados. Verifique a URL.")
    else:
        st.warning("Por favor, insira uma URL do produto Amazon.")

if __name__ == '__main__':
    main()
