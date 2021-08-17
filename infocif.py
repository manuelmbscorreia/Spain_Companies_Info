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


#Setup Website

#profile = webdriver.FirefoxProfile('/usr/local/bin/')
browser = webdriver.Firefox()
browser.get("http://www.infocif.es/buscador/#/")
time.sleep(10)


#Get Element - Filter by region
path = "/html/body/div[1]/div/div[1]/div/div/div/div/section/div/div/div/div/div[1]/div[1]/div/div"
element = browser.find_element_by_xpath(path)

#Click on Element
actions = webdriver.ActionChains(browser)
actions.move_to_element(element)
actions.click(element)
actions.perform()

time.sleep(4)

#Get Element

path = "/html/body/div[1]/div/div[1]/div/div/div/div/section/div/div/div/div/div[1]/div[2]/div/div/div/div/div/div[1]/div[3]/div/div[2]/div/div/div/div[2]/div[12]/div/div[2]/div"

element = browser.find_element_by_xpath(path)

#Click on Element
actions = webdriver.ActionChains(browser)
actions.move_to_element(element)
actions.click(element)
actions.perform()

time.sleep(3)

#Procurar Resultados
path = "/html/body/div[1]/div/div[1]/div/div/div/div/article/div/div/a"
element = browser.find_element_by_xpath(path)

actions = webdriver.ActionChains(browser)
actions.move_to_element(element)

time.sleep(2)

actions.click(element)
actions.perform()

time.sleep(7)

#Aumentar Número de Páginas

#Clicar caixa
path = "/html/body/div[1]/div/div[1]/div/div/div/div/div[3]/div[2]/div[2]/span[2]/div/div[1]/span/span/i"
element = browser.find_element_by_xpath(path)
actions = webdriver.ActionChains(browser)

time.sleep(2)

element.location_once_scrolled_into_view
actions.move_to_element(element)
actions.click(element)
actions.perform()

time.sleep(3)

#Clicar 100 por página
path = "/html/body/div[3]/div[1]/div[1]/ul/li[6]"
element = browser.find_element_by_xpath(path)
actions = webdriver.ActionChains(browser)
actions.move_to_element(element)
actions.click(element)
actions.perform()

time.sleep(7)

#Retirar Info primeira página e fazer Documento Pandas

#Extract
soup = BeautifulSoup(browser.page_source, 'lxml')
tables = soup.find_all('table')
tabela = pd.read_html(str(tables))

#Work
table_titulos = tabela[0]
tables_info = tabela[1]
nomes_colunas = table_titulos.columns
tables_info.columns = nomes_colunas

time.sleep(3)

for i in range(0, 999999):
      try:
            #Clicar seta próxima página
            path = "/html/body/div[1]/div/div[1]/div/div/div/div/div[3]/div[2]/div[2]/button[1]/i"
            element = browser.find_element_by_xpath(path)
            #browser.execute_script("arguments[0].scrollIntoView();", element)
            element.location_once_scrolled_into_view
            time.sleep(2)
            actions = webdriver.ActionChains(browser)
            actions.move_to_element(element)
            actions.click(element)
            actions.perform()

            time.sleep(7)

            # Extract
            soup = BeautifulSoup(browser.page_source, 'lxml')
            tables = soup.find_all('table')
            tabela = pd.read_html(str(tables))

            # Work
            tab_titles = tabela[0]
            tab_info = tabela[1]
            column_names = tab_titles.columns
            tab_info.columns = column_names

            #Juntar Info
            tables_info = tables_info.append(tab_info, ignore_index=True)

            time.sleep(3)

      except:
            pass


time.sleep(3)

#Guardar como csv
tables_info.to_csv(f"Spain_Company_Names_and_Info.csv", sep = ",", index = False, header = True)

time.sleep(3)

browser.quit()


