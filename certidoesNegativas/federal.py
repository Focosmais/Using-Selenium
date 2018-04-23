#/bin/env/python3
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
#from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import WebDriverException
from selenium.common.exceptions import TimeoutException
import time
import os
import base64
import errno
import csv

urlclean = "https://www.google.com/"
url = "http://www.receita.fazenda.gov.br/Aplicacoes/ATSPO/Certidao/CNDConjuntaSegVia/ResultadoSegVia.asp?Origem=1&Tipo=1&NI="
os.mkdir("/home/ti/certidoesnegativas")

#configurações do chrome
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "certidoes/federal"}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

database = [] #os dados são salvos aqui
result = []
databasekeys = {'ID':'empty', 'nome':'empty', 'receita':'empty'}

def receita(cnpj, index, folder):
    driver.get(url+cnpj)

    database.append({'ID':str(index), 'nome': nomes[index], 'receita': 'EMPTY'})
    try:
        driver.find_element_by_xpath('/html/body/div[2]/table/tbody/tr/td[3]/a/img').click()
        time.sleep(2)
        driver.switch_to_window(driver.window_handles[1])
        driver.execute_script("document.body.style.zoom='zoom 67%'")
        try:
            os.mkdir(folder)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        driver.save_screenshot(os.path.join(folder, nomes[index] +"receitafederal.png"))
        os.system("convert "+os.path.join(folder, nomes[index]+"receitafederal.png")+" "+os.path.join(folder,nomes[index]+"receitafederal.pdf"))
        driver.close()
        driver.switch_to_window(driver.window_handles[0])
        print('receita concluida')
        database[index]['receita'] = "OK"
    except NoSuchElementException:
        database[index]['receita'] = "erro"
    
def read():
    with open('inputfile.csv', 'r') as inputfile:
        getinput = csv.DictReader(inputfile)
        for row in getinput:
            result.append(row)

        #print(result)
    return result

def writedis(values, valuekeys):
    with open('outputfile.csv', 'w') as outputfile:
        write = csv.DictWriter(outputfile, valuekeys.keys())
        write.writeheader()
        for item in values:
            write.writerow(item)
cnpjs = []
nomes = []

def main():
    index = 0
    results=read()
    for item in results:
        nomes.append(item['nome'])
        cnpjs.append(item['cnpj'])

    
    print(nomes)

    for item in cnpjs:
            folder = os.path.join("/home/ti/certidoesnegativas", nomes[index])
            print("#########################################################################")
            print(nomes[index])
            print('#########################################################################')
            print(index)
            if index == 99 or index == 199 or index == 299 or index == 399:
                print('waiting 30 minutes')
                time.sleep(3600)
            try:
                driver.switch_to_window(driver.window_handles[0])
                receita(item, index, folder)
                index += 1
            except TimeoutException:
                driver.get(urlclean)
                print("retrying...")
                try:
                    driver.switch_to_window(driver.window_handles[0])
                    receita(item, index, folder)
                    index += 1
                except:
                    pass

                
    print("writting results")
    writedis(database, databasekeys)    

try:
    main()
except KeyboardInterrupt:
    print("cancel")
    print("writting results")
    writedis(database, databasekeys)
except:
    print("ERROR")
    print("writting results")
    writedis(database, databasekeys)
    raise


