#!/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
import os
import errno
import csv

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "certidoes/municipal"}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

database = [] #os dados são salvos aqui
result = []
databasekeys = {'ID':'empty', 'nome':'empty', 'municipal':'empty'}
os.mkdir("/home/ti/certidoesnegativas")

def captchaMunicipal(item, index, folder):
    
    driver.get("http://servicosweb.sefaz.salvador.ba.gov.br/website/sistema/certidao_negativa/servicos_certidao_negativa.asp")
    window_checkpoint_1 = driver.window_handles[0]
    mark=driver.find_element_by_xpath('//*[@id="frm_cad"]/input[3]').click()
    i=1
    letras = []
    while i<6:
        letras.append(driver.find_element_by_xpath('//*[@id="frm_cad"]/div[3]/table/tbody/tr/td[1]/div/img['+str(i)+']').get_attribute("alt"))
        i+=1
    print(">Captcha decodificado")
    print(letras)
    campo_captcha = driver.find_element_by_xpath('//*[@id="frm_cad"]/div[3]/table/tbody/tr/td[2]/input')
    campo_captcha=campo_captcha.send_keys(letras[0] + letras[1] + letras[2] + letras[3] + letras[4])
    cnpjmun(item, index, folder)

def cnpjmun(cnpji, index, folder):
    database.append({'ID':str(index), 'nome': nomes[index], 'municipal': 'EMPTY'})
    cnpj=driver.find_element_by_xpath('//*[@id="txtCNPJ"]')
    cnpj = cnpj.send_keys(cnpji) #apenas numeros
    driver.find_element_by_xpath('//*[@id="frm_cad"]/p/input[1]').click()
    time.sleep(5)
    try:
        window_checkpoint_2 = driver.window_handles[1]
        driver.switch_to_window(window_checkpoint_2)
        #driver.execute_("window.print()")
        #time.sleep(10)
        driver.execute_script("document.body.style.zoom='zoom 67%'")
        try:
            os.mkdir(folder)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        driver.save_screenshot(os.path.join(folder, nomes[index] +"muncipal.png"))
        #####ONLY ubuntu####
        os.system("convert "+os.path.join(folder, nomes[index]+"muncipal.png")+" "+os.path.join(folder,nomes[index]+"muncipal.pdf"))
        
        #shutil.move(nomes[index]+"municipal.png", os.path.join(folder + nomes[index] + "municipal.png"))
        #shutil.move(os.path.join("/home/ti/Downloads/","Untitled.pdf"), (os.path.join("/home/ti/codes/Certidoes/", nome + "muncipal.pdf")))
        driver.close()
        database[index]['municipal']='ok'
        print('municipal concluido')
        driver.switch_to_window(driver.window_handles[0])
    except IndexError:
        print('erro municipal')
        database[index]['municipal']='ERRO'
        pass

def read():
    with open('inputfile.csv', 'r') as inputfile:
        getinput = csv.DictReader(inputfile)
        for row in getinput:
            result.append(row)

        print(result)
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
        try:
            driver.switch_to_window(driver.window_handles[0])
            captchaMunicipal(item, index, folder)
        except ValueError:
            print('retrying...')
            driver.switch_to_window(driver.window_handles[0])
            captchaMunicipal(item, index, folder)
        except UnexpectedAlertPresentException:
            print("retrying...")
            driver.switch_to_alert().accept()
            driver.switch_to_window(driver.window_handles[0])
        index +=1

    print ('writting results')
    writedis(database, databasekeys)
try:
    main()
except KeyboardInterrupt:
    print("cancel")
    print ('writting results')
    writedis(database, databasekeys)
except:
    print("ERROR")
    raise
    print("writting results")
    writedis(database, databasekeys)