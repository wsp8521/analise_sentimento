from pysentimiento import create_analyzer
import pandas as pd
import plotly.express as px
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Criando o modelo de análise de sentimento
modelo_analise_sentimento = create_analyzer(task='sentiment', lang='pt')

# Carregando os dados
dados = pd.read_csv('https://raw.githubusercontent.com/alura-cursos/hugging_face/main/Dados/resenhas.csv')

# Realizando a previsão de sentimento
resultado_previsao = modelo_analise_sentimento.predict(dados['Resenha'])
sentimento = [resultado.output for resultado in resultado_previsao]

# Adicionando a coluna de sentimento ao DataFrame
dados['Sentimento'] = sentimento

# Contagem de resenhas por sentimento
df_sentimento = dados.groupby('Sentimento').size().reset_index(name='Contagem')
fig = px.bar(df_sentimento, x='Sentimento', y='Contagem', title='Contagem de Resenhas por Sentimento')
fig.show()  # Descomente se quiser visualizar o gráfico

# Carregar stopwords em português
nltk.download('stopwords')
portuguese_stopwords = set(stopwords.words('portuguese'))

def nuvem_palavras(texto, coluna_texto, sentimento):
    # Filtrando as resenhas com base no sentimento especificado
    texto_sentimento = texto.query(f"Sentimento == '{sentimento}'")[coluna_texto]

    # Unindo todas as resenhas em uma única string
    texto_unido = " ".join(texto_sentimento)

    # Dividindo o texto em palavras e filtrando com stopwords
    palavras = texto_unido.split()
    palavras_filtradas = [palavra for palavra in palavras if palavra not in portuguese_stopwords]
    texto_filtrado = " ".join(palavras_filtradas)

    # Criando e exibindo a nuvem de palavras
    nuvem_palavras = WordCloud(width=800, height=500, max_words=50, background_color='white').generate(texto_filtrado)
    plt.figure(figsize=(10, 7))
    plt.imshow(nuvem_palavras, interpolation='bilinear')
    plt.axis('off')
    plt.show()

# Chamar a função para exibir a nuvem de palavras para as resenhas positivas
#nuvem_palavras(dados, 'Resenha', 'NEG')
