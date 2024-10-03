from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options  # Importar as opções do Chrome
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import io


# Função para extrair comentários de uma página
def extrair_comentarios(driver):
    # Pausa para garantir o carregamento da página
    time.sleep(3)
    
    # Coletar o HTML da página carregada
    soup = BeautifulSoup(driver.page_source, 'html.parser')

    # Substituir pela classe correta dos comentários
    comentarios = soup.find_all('span', {'data-hook': 'review-body'})
    
    # Retornar os comentários extraídos
    return [comentario.text.strip() for comentario in comentarios]

def esperar_comentarios_carregar(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-hook="review-body"]'))
    )

# Configurar as opções do Chrome para rodar em modo headless
chrome_options = Options()
chrome_options.add_argument("--headless")  # Executar sem interface gráfica
chrome_options.add_argument("--no-sandbox")  # Evitar erros de permissão em alguns sistemas
chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar erros em sistemas com pouca memória compartilhada

# Configurar o driver do navegador em modo headless
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

# Definir a URL base para os comentários, com um placeholder para o número da página
url_base = 'https://www.amazon.com.br/Detergentes-Powerball-Embalagem-Econ%C3%B4mica-Finish/product-reviews/B07Y3B33KG/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews&pageNumber={}'

# Definir o número máximo de páginas a serem percorridas
num_paginas = 15  # Pode alterar conforme o necessário

# Lista para armazenar todos os comentários
todos_comentarios = []

for pagina in range(1, num_paginas + 1):
    
    # Navegar para a página de comentários correspondente
    driver.get(url_base.format(pagina))
    
    # Extrair os comentários dessa página
    comentarios = extrair_comentarios(driver)
    
    # Adicionar os comentários dessa página à lista total
    todos_comentarios.extend(comentarios)
    
    # Exibir os comentários extraídos
    #for comentario in comentarios:
    #print(comentario)

# Exibir o número total de comentários extraídos
print(f"\nTotal de comentários extraídos: {len(todos_comentarios)}")


# Transformar os comentários em formato CSV
output = io.StringIO()
writer = csv.writer(output)
writer.writerow(['Comentario'])  # Cabeçalho
for comentario in todos_comentarios:
    writer.writerow([comentario])  # Gravar cada comentário

# Exibir a saída CSV no console
csv_output = output.getvalue()
print('TRANSFORMANDO AQUIVO CSV')
print(csv_output)



# Fechar o navegador
driver.quit()
