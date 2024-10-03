import nltk
from nltk.corpus import stopwords
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
from wordcloud import WordCloud
from pysentimiento import create_analyzer



def modelo_ia(data):
    
    # Criando o modelo de análise de sentimento
    modelo_analise_sentimento = create_analyzer(task='sentiment', lang='pt')

    # Carregando os dados
    dados = pd.read_csv(data)

    # Realizando a previsão de sentimento
    resultado_previsao = modelo_analise_sentimento.predict(dados['Comentario'])
    sentimento = [resultado.output for resultado in resultado_previsao]

    # Adicionando a coluna de sentimento ao DataFrame
    dados['Sentimento'] = sentimento
    return dados


def grafico_barra(data):
    # Contagem de resenhas por sentimento
    df_sentimento = data.groupby('Sentimento').size().reset_index(name='Contagem')
    fig = px.bar(df_sentimento, x='Sentimento', y='Contagem', title='Opinião sobre o produto')
    #return fig.show()  # Descomente se quiser visualizar o gráfico
    return fig

def nuvem_palavras(texto, coluna_texto, sentimento):
    # Carregar stopwords em português
    nltk.download('stopwords')
    portuguese_stopwords = set(stopwords.words('portuguese'))
    # Filtrando as resenhas com base no sentimento especificado
    texto_sentimento = texto.query(f"Sentimento == '{sentimento}'")[coluna_texto]
    
    if texto_sentimento.empty:
        print("Nenhum comentário encontrado para o sentimento especificado.")
        return
    
    # Unindo todas as resenhas em uma única string
    texto_unido = " ".join(texto_sentimento)

    # Dividindo o texto em palavras e filtrando com stopwords
    palavras = texto_unido.split()
    palavras_filtradas = [palavra for palavra in palavras if palavra not in portuguese_stopwords]
    texto_filtrado = " ".join(palavras_filtradas)

    # Criando e exibindo a nuvem de palavras
    nuvem_palavras = WordCloud(width=400, height=400, max_words=50, background_color='white').generate(texto_filtrado)
    plt.figure(figsize=(10, 7))
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis('off')
    return plt.show()

# # Chamar a função para exibir a nuvem de palavras para as resenhas positivas
# nuvem_palavras(dados, 'Resenha', 'NEG')
