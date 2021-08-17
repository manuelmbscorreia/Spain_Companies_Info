from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver import Chrome
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
import pandas as pd
import time
import unidecode
import requests
from bs4 import BeautifulSoup
import urllib3
import re
import numpy as np


#Preparar lista de cidades a selecionar e para Input
print("Pretende onter nomes das empresas de que região de Espanha?)
print("Escolha uma ou mais opções, escritas em minusculas sem acentos, separadas por virgula e um espaço.")

lista_ubicacion = ["espanha", "andalucia", "aragon", "canarias", "castilla la mancha", "castilla y leon",
                   "cataluna", "ceuta", "comunidad de madrid", "comunidad foral de navarra", "comunitat valenciana",
                   "extremadura", "galicia", "islas baleares", "la rioja", "melilla", "pais vasco",
                   "principado de asturias", "region de murcia"]


escolha = input("toda espanha, andalucia, aragon, canarias, castilla la mancha, castilla y leon, cataluna, ceuta, "
                "comunidad de madrid, comunidad foral de navarra, comunitat valenciana, extremadura, galicia, "
                "islas baleares, la rioja, melilla, pais vasco, principado de asturias, region de murcia:  "


lista_escolha = escolha.split(",")




#Setup Website

browser = webdriver.Firefox()
browser.get("https://codigopostal.ciberforma.pt/")
time.sleep(7)


#Get Element - Filter by region
path = "/html/body/div[1]/div/div[1]/div/div/div/div/section/div/div/div/div/div[1]/div[1]/div/div"
element = browser.find_element_by_xpath(path)

#Click on Element
actions = ActionChains(browser)
actions.move_to_element(element)
actions.click(element)
actions.perform()

#Choose Region
for a in lista_cidades:

      #Get Element
      index_div = int(lista_escolha.index(a)) + 1
      path = f"/html/body/div[1]/div/div[1]/div/div/div/div/section/div/div/div/div/div[1]/div[2]/div/" \
             f"div/div/div/div/div[1]/div[3]/div/div[2]/div/div/div/div[2]/div[{index_div}]/div/div[2]/label"
      element = browser.find_element_by_xpath(path)

      #Click on Element

      browser.execute_script("arguments[0].scrollIntoView();", element)
      actions = ActionChains(browser)
      actions.move_to_element(element)
      actions.click(element)
      actions.perform()

#Procurar Resultados
path = "/html/body/div[1]/div/div[1]/div/div/div/div/article/div/div/a"
element = browser.find_element_by_xpath(path)
browser.execute_script("arguments[0].scrollIntoView();", element)
actions = ActionChains(browser)
actions.move_to_element(element)
actions.click(element)
actions.perform()

#Aumentar Número de Páginas

#Clicar caixa
path = "/html/body/div[1]/div/div[1]/div/div/div/div/div[3]/div[2]/div[2]/span[2]/div/div[1]/span/span/i"
element = browser.find_element_by_xpath(path)
browser.execute_script("arguments[0].scrollIntoView();", element)
actions = ActionChains(browser)
actions.move_to_element(element)
actions.click(element)
actions.perform()

#Clicar 100 por página
path = "/html/body/div[3]/div[1]/div[1]/ul/li[6]"
element = browser.find_element_by_xpath(path)
actions = ActionChains(browser)
actions.move_to_element(element)
actions.click(element)
actions.perform()


#Retirar Info primeira página e fazer Documento Pandas
tabela = pd.read_table(browser)
table_titulos = tabela[0]
tables_info = tabela[1]
nomes_colunas = table_titulos.columns
tables_info.columns = nomes_colunas

for i in range(0, 3):
      try:
            #Clicar seta próxima página
            path = "/html/body/div[1]/div/div[1]/div/div/div/div/div[3]/div[2]/div[2]/button[1]/i"
            element = browser.find_element_by_xpath(path)
            browser.execute_script("arguments[0].scrollIntoView();", element)
            actions = ActionChains(browser)
            actions.move_to_element(element)
            actions.click(element)
            actions.perform()

            #Retirar Informação
            tab = pd.read_table(browser)
            tab_titles = tabela[0]
            tab_info = tabela[1]
            column_names = tab_titles.columns
            tab_info.columns = column_names

            #Juntar Info
            tables_info = tables_info.append(tab_info, ignore_index=True)

      except:
            pass

#Guardar como csv
tables_info.to_csv(f"Spain_Company_Names_and_Info.csv", sep = ",", index = False, header = True)

browser.quit()


