'''
Coded by Enzo Frese

16/01/2024

Web Scraping TJSP on the first page
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd
import requests


#Pesquisar palavra
def encontra_indice(dicionario, palavra):
  indices = []
  for chave, valor in dicionario.items():
    if palavra in valor:
      indices.append(chave)
  return indices

# Inicializamos o navegador
browser = webdriver.Chrome()

# Abrimos o site do TJSP
browser.get("https://esaj.tjsp.jus.br/cjsg/resultadoCompleta.do")

# Buscamos a aba de pesquisa
pesquisa = browser.find_element(By.ID, "iddados.buscaInteiroTeor")

# Digitamos a consulta
pesquisa.send_keys("\"banco do brasil\" e \"golpe do motoboy\"")

# Clicamos no botão de pesquisa
pesquisa.submit()

id = []
ementa = []


# Loop e extração dentro das páginas
for pagina in range(1,5):
    #Acesso da primeira página
    if(pagina == 1):
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "paginaAtual")))
        element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "fundocinza1")))

        # Extraímos o conteúdo da página
        pagina = BeautifulSoup(browser.page_source, "html.parser")

        # Encontra a tabela de acordos
        acord =  pagina.find_all( 'tr',class_='fundocinza1')
    else:
        # Acessa as outras paginas
        element = WebDriverWait(browser, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "paginaAtual")))
        # Click na próxima página
        links = browser.find_element(By.NAME, f'A{pagina}')
        links.click()
        element = WebDriverWait(browser, 100).until(EC.presence_of_element_located((By.CLASS_NAME, "fundocinza1")))

        # Extraímos o conteúdo da página
        pagina = BeautifulSoup(browser.page_source, "html.parser")

        # Encontra a tabela de acordos
        acord =  pagina.find_all( 'tr',class_='fundocinza1')

        # Adiciona os dados extraidos aos vetores
    for i in acord:
        id.append(i.find('a').getText().strip())
        b = i.find('div',attrs={'align': 'justify'})

        if b is not None:
            ementa.append(b.text.strip('\n\t\t\t\t\t\t\t\t\t\t\t \t').strip('\n').strip('\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t').rstrip())                                                                           
        else:
            ementa.append('Sem ementa')

# Criando Dicionário
dicionario = dict(zip(id,ementa))

# Importa os dados da tabela para um DataFrame
df = pd.DataFrame.from_dict(dicionario, orient='index', columns=['Ementa'])
df['Ementa'] = df['Ementa']
print(len(id))
#print(encontra_indice(dicionario,'DANOS MORAIS')) # Print do indice da ementa 
print(df.to_string(max_colwidth=1000)) # Print de todo o dataframe
#Cria tabela excel
df.to_excel('output.xlsx', index_label='ID')


