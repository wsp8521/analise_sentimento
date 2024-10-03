import streamlit as st
import time
from comentarios.comentario import exibir_comentarios, format_csv_comentario
from hugging_face.analise_sentimento import modelo_ia, grafico_barra, nuvem_palavras
import plotly.express as p

def main():
    st.title("Análise de Sentimentos com IA")

    input_url = st.text_input("Insira a URL do produto Amazon:", key='input_text')
    num_paginas = 20

    if input_url:
        # Carrega os dados a partir da URL
        dados_url = format_csv_comentario(input_url, num_paginas)
        
        # Realiza a análise de sentimento
        dados_modelo_ia = modelo_ia(dados_url)
        
        # Renderiza gráfico de barras
        st.plotly_chart(grafico_barra(dados_modelo_ia)) 
        
        # Exibir nuvem de palavras para resenhas positivas
        caminho_imagem = nuvem_palavras(dados_modelo_ia, 'Comentario', 'POS')
        caminho_imagem_neg = nuvem_palavras(dados_modelo_ia, 'Comentario', 'NEG')
        
        # Exibir a imagem da nuvem de palavras para o sentimento positivo
        if caminho_imagem:
            st.image(caminho_imagem, caption='Nuvem de Palavras - Sentimento Positivo')
        else:
            st.warning("Nenhuma imagem gerada para sentimentos positivos.")
        
        # Exibir a imagem da nuvem de palavras para o sentimento negativo
        if caminho_imagem_neg:
            st.image(caminho_imagem_neg, caption='Nuvem de Palavras - Sentimento Negativo')
        else:
            st.warning("Nenhuma imagem gerada para sentimentos negativos.")

    else:
        st.warning("Por favor, insira uma URL do produto Amazon.")

if __name__ == '__main__':
    main()


#https://www.amazon.com.br/dp/B0B8C31YXR/ref=sspa_dk_detail_4?psc=1&pd_rd_i=B0B8C31YXR&pd_rd_w=DieHO&content-id=amzn1.sym.b0d855ab-21fd-49b1-ae3e-5a01e562f959&pf_rd_p=b0d855ab-21fd-49b1-ae3e-5a01e562f959&pf_rd_r=Z92E2M89ZZD37FZA88RB&pd_rd_wg=NnTkV&pd_rd_r=0bf5e521-e65b-4070-94ef-582f39aec0fb&s=computers&sp_csd=d2lkZ2V0TmFtZT1zcF9kZXRhaWwy