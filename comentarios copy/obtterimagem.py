from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import time
import requests
from PIL import Image
from io import BytesIO

# Função para extrair imagens do produto
def extrair_imagens(driver):
    time.sleep(3)  # Pausa para garantir o carregamento da página
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    
    # Encontrar todas as tags <img> relacionadas ao produto
    imagens = soup.find_all('img', {'class': 'a-dynamic-image'})  # Classe típica de imagens do produto
    
    # Extrair os URLs das imagens (atributo 'src')
    urls_imagens = [img['src'] for img in imagens]
    
    return urls_imagens

# Configurar o driver do navegador
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

# Definir a URL do produto na Amazon
url_produto = 'https://www.amazon.com.br/Multilaser-MO222-Mouse-Emborrachado-Preto/dp/B074KR16JS/'
driver.get(url_produto)

# Extraindo as imagens do produto
imagens_produto = extrair_imagens(driver)

# Exibir as imagens extraídas
for url in imagens_produto:
    print("Exibindo imagem do produto: ", url)
    # Fazer download da imagem
    response = requests.get(url)
    img = Image.open(BytesIO(response.content))
    img.show()

# Fechar o navegador
driver.quit()
