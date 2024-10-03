from comentarios.comentario import  exibir_comentarios, format_csv_comentario
from hugging_face.analise_sentimento import modelo_ia, grafico_barra, nuvem_palavras



url_base = 'https://www.amazon.com.br/Detergentes-Powerball-Embalagem-Econ%C3%B4mica-Finish/product-reviews/B07Y3B33KG/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={}'
num_paginas = 1

dados_url = format_csv_comentario(url_base, num_paginas)
dados_modelo_ia = modelo_ia(dados_url)



# print("DADOS CSV")
# print(dados_csv)
# print("ANALISE DE SENTIMENTOS")
print(dados_modelo_ia)
#grafico_barra(dados_modelo_ia)

nuvem_palavras(dados_modelo_ia, 'Comentario','NEU')

# extrator.scrape_reviews()  # Coleta os comentários
# csv_resultado = extrator.to_csv()  # Gera o CSV
# print(csv_resultado)  # Exibe o CSV no console
# extrator.close_driver()
