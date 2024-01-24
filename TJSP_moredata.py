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


dicionario = {'Processo': [], 'Classe/Assunto': [],'Relator':[],'Comarca': [],  'Ementa': []}
#dicionario = {'Processo': [], 'Classe/Assunto': [], 'Relator':[], 'Comarca': [], 'Orgao Julgador': [], 'DT do Julgamento': [], 'Ementa': []}
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
classe = []
relator = []
comarca = []

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

        # Encontra a tabela de acordãos
        acord =  pagina.find_all( 'tr',class_='fundocinza1')
        
        # Adiciona os dados extraidos aos vetores
    for i in acord:
        # Adiciona cada ementa ao vetor
        id.append(i.find('a').getText().strip())
        _ementa = i.find('div',attrs={'align': 'justify'})

        if _ementa is not None:
            ementa.append(_ementa.text.strip('\n\t\t\t\t\t\t\t\t\t\t\t \t').strip('\n').strip('\n\t\t\t\t\t\t\t\t\t\t\t\t\n\t\t\t\t\t\t\t\t\t\t\t\t').rstrip())                                                                           
        else:
            ementa.append('Sem ementa')
        # Adiciona cada classe ao vetor
        atributos = i.find_all('td')
        count = 0
        for i in atributos:
           
           #print(f'linha {count}, texto {c[0]}') debug para encontrar as keys
            # ---- Classe/Assunto ----
            c = i.getText().split()
            if c[0] == 'Classe/Assunto:':
                _classe = ' '.join(c[1:])
                classe.append(_classe)
            #print(_classe)
            # ---- Relator ----
            if c[0] == 'Relator(a):':
                _relator = ' '.join(c[1:])
                relator.append(_relator)
            # ---- Comarca ----  
            if c[0] == 'Comarca:':
                _comarca = ' '.join(c[1:])
                comarca.append(_comarca)
          
      
# Criando Dicionário
#print(len(id),len(classe),len(ementa))
pares_combinados = zip(id,classe,relator,comarca,ementa)

for tupla in pares_combinados:
    dicionario['Processo'].append(tupla[0])
    dicionario['Classe/Assunto'].append(tupla[1])
    dicionario['Relator'].append(tupla[2])
    dicionario['Comarca'].append(tupla[3])
   #dicionario['Orgao Julgador'].append(tupla[4])
   #dicionario['DT do Julgamento'].append(tupla[5])
    dicionario['Ementa'].append(tupla[4])

# Importa os dados da tabela para um DataFrame
df = pd.DataFrame(dicionario)

#print(encontra_indice(dicionario,'DANOS MORAIS')) # Print do indice da ementa 
#print(df.to_string(max_colwidth=1000)) # Print de todo o dataframe
#Cria tabela excel
df.to_excel('database3.xlsx', index_label='ID')


