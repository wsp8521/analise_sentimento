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

class ExtrarirComentario:
    def __init__(self, url_base, num_paginas):
        self.url_base = url_base
        self.num_paginas = num_paginas
        self.todos_comentarios = []
        self.driver = self.setup_driver()

    def setup_driver(self):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # Executar sem interface gráfica
        chrome_options.add_argument("--no-sandbox")  # Evitar erros de permissão em alguns sistemas
        chrome_options.add_argument("--disable-dev-shm-usage")  # Evitar erros em sistemas com pouca memória compartilhada
        return webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

    def extrair_comentarios(self):
        try:
            WebDriverWait(self.driver, 20).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, 'span[data-hook="review-body"]'))
            )
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            comentarios = soup.find_all('span', {'data-hook': 'review-body'})
            return [comentario.text.strip() for comentario in comentarios]
        except Exception as e:
            print(f"Erro ao extrair comentários: {str(e)}")
            return []

    def scrape_reviews(self):
        for pagina in range(1, self.num_paginas + 1):
            self.driver.get(self.url_base.format(pagina))
            time.sleep(2)  # Aguarda um pouco para a página carregar completamente
            comentarios = self.extrair_comentarios()
            self.todos_comentarios.extend(comentarios)

    def exibir_comentarios(self):
        for pagina in range(1, self.num_paginas + 1):
            self.driver.get(self.url_base.format(pagina))
            time.sleep(2)  # Aguarda um pouco para a página carregar completamente
            comentarios = self.extrair_comentarios()
            for comentario in comentarios:
                return comentario
        
        
    def to_csv(self):
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow(['Comentario'])  # Cabeçalho
        for comentario in self.todos_comentarios:
            writer.writerow([comentario])  # Gravar cada comentário
        return output.getvalue()

    def close_driver(self):
        self.driver.quit()

