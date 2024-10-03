from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options  # Importar as opções do Chrome
from bs4 import BeautifulSoup
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

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
url_base = 'https://www.amazon.com.br/Multilaser-MO222-Mouse-Emborrachado-Preto/product-reviews/B074KR16JS/ref=cm_cr_getr_d_paging_btm_prev_1?ie=UTF8&reviewerType=all_reviews&pageNumber={}'

# Definir o número máximo de páginas a serem percorridas
num_paginas = 5  # Pode alterar conforme o necessário

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
    for comentario in comentarios:
        print(comentario)

# Exibir o número total de comentários extraídos
print(f"\nTotal de comentários extraídos: {len(todos_comentarios)}")

# Fechar o navegador
driver.quit()
