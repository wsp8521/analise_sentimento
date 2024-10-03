import csv
import io
import time
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager

# Função para extrair comentários de uma página
def extrair_comentarios(driver):
    time.sleep(3)
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    comentarios = soup.find_all('span', {'data-hook': 'review-body'})
    return [comentario.text.strip() for comentario in comentarios]

def esperar_comentarios_carregar(driver):
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-hook="review-body"]'))
    )

def configChrome():
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def exibir_comentarios(url_base, num_pagina):
    driver = configChrome()
    todos_comentarios = []

    for pagina in range(1, num_pagina + 1):
        driver.get(url_base.format(pagina))
        comentarios = extrair_comentarios(driver)
        todos_comentarios.extend(comentarios)

    driver.quit()
    return todos_comentarios

def format_csv_comentario(url_base, num_pagina):
    todos_comentarios = exibir_comentarios(url_base=url_base, num_pagina=num_pagina)
    
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(['Comentario'])  # Cabeçalho
    for comentario in todos_comentarios:
        writer.writerow([comentario])


    #retornando dados no formato csv
    output.seek(0) # Voltar o ponteiro do StringIO para o início
    return output

