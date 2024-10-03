import streamlit as st
import time
from comentarios.comentario import  exibir_comentarios, format_csv_comentario
from hugging_face.analise_sentimento import modelo_ia, grafico_barra, nuvem_palavras
import plotly.express as p


def main():
    st.title("Análise de Sentimentos com IA")

    #input_url = st.text_input("", key='input_text')
    input_url = 'https://www.amazon.com.br/Detergentes-Powerball-Embalagem-Econ%C3%B4mica-Finish/product-reviews/B07Y3B33KG/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews'
    num_paginas = 1

    if input_url:
       dados_url = format_csv_comentario(input_url, num_paginas)
       dados_modelo_ia = modelo_ia(dados_url)
       
       #renderizando gráfico
       st.plotly_chart(grafico_barra(dados_modelo_ia)) 
       st.pyplot(nuvem_palavras(modelo_ia(dados_modelo_ia), 'Comentario','POS'))

    else:
        st.warning("Por favor, insira uma URL do produto Amazon.")

if __name__ == '__main__':
    main()
