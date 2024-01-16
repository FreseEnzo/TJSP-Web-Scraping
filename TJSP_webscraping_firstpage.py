'''
Coded by Enzo Frese

16/01/2024

Web Scraping TJSP on the first page
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import pandas as pd

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

# Espera o carregamento
WebDriverWait(browser.page_source, 10)

# Extraímos o conteúdo da página
pagina = BeautifulSoup(browser.page_source, "html.parser")

# Encontra a tabela de acordos
acord =  pagina.find_all( 'tr',class_='fundocinza1')

id = []
ementa = []

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

print(encontra_indice(dicionario,'DANOS MORAIS')) # Print do indice da ementa 
print(df.to_string(max_colwidth=1000)) # Print de todo o dataframe

