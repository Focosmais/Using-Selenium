#!/bin/env python
# -*- coding: utf-8 -*-
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import UnexpectedAlertPresentException
import time
import shutil
import os
import errno
import csv

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "certidoes/estadual"}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)
database = [] #os dados são salvos aqui
result = []
databasekeys = {'ID':'empty', 'nome':'empty', 'estadual':'empty', 'municipal':'empty', 'receita':'empty'}

def estadual(item, index, folder):
    window_checkpoint_1 = driver.window_handles[0]
    def getPlusInputCnpj():
        driver.get("https://sistemas.sefaz.ba.gov.br/sistemas/sigat/Default.Aspx?Modulo=CREDITO&Tela=DocEmissaoCertidaoInternet&limparSessao=1&sts_link_externo=2")

        cnpj_input = driver.find_element_by_xpath('//*[@id="_ctl0__ctl1_num_cnpj"]')
        cnpj_input = cnpj_input.send_keys(item)

    getPlusInputCnpj()

    try:
        driver.find_element_by_xpath('//*[@id="_ctl0__ctl1_btn_Imprimir"]').click()
    except:
        getPlusInputCnpj()
    try:
        window_checkpoint_2 =driver.window_handles[1]
        driver.switch_to_window(window_checkpoint_2)
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="_ctl0__ctl0_crv_relatorio"]/tbody/tr[1]/td/table/tbody/tr/td/table/tbody/tr/td[1]/a[2]/img').click()
        driver.find_element_by_name("button").click()
        time.sleep(5)
        #driver.execute_("window.print()")
        #driver.save_screenshot(nome +' estadual.png')
        #prints(nome)


        try:
            os.mkdir(folder)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
        shutil.move(os.path.join("/home/ti/Downloads/","Untitled.pdf"), (os.path.join(folder, nomes[index] + "estadual.pdf" )))
        #time.sleep(10)
        driver.close()
        driver.switch_to_window(window_checkpoint_1)
        database.append({'ID':str(index), 'nome': nomes[index], 'estadual': 'OK', 'municipal': 'EMPTY', 'receita': 'EMPTY'})
        print('estadual concluido')
    except (NoSuchElementException, IndexError) as error:
        try:
            print ('erro estadual')
            database[index]['estadual']='ERRO'
            pass
        except IndexError:
            database.append({'ID':str(index), 'nome': nomes[index], 'estadual': 'ERRO', 'municipal': 'EMPTY', 'receita': 'EMPTY'})
    except NoSuchWindowException:
        database.append({'ID':str(index), 'nome': nomes[index], 'estadual': 'OK', 'municipal': 'EMPTY', 'receita': 'EMPTY'})
        shutil.move(os.path.join("/home/ti/Downloads/","Untitled.pdf"), (os.path.join(folder, nomes[index] + "estadual.pdf" )))
cnpjs = []
nomes = []

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

def main():
    index = 0
    results=read()
    for item in results:

        for item in result:
            nomes.append(item['nome'])
            cnpjs.append(item['cnpj'])


    for item in cnpjs:
        folder = os.path.join("/home/ti/", nomes[index])
        print("#########################################################################")
        print(nomes[index])
        print('#########################################################################')
        print(index)
        driver.switch_to_window(driver.window_handles[0])
        try:
            estadual(item, index, folder)
        except FileNotFoundError:
            os.mkdir(folder)
            shutil.move(os.path.join("/home/ti/Downloads/","Default.aspx"), (os.path.join(folder, nomes[index] + "estadual.pdf" )))
        except UnexpectedAlertPresentException:
            driver.switch_to_alert().accept()
            driver.switch_to_window(driver.window_handles[0])
        except:
            pass

        index +=1


    print ('writting results')
    writedis(database, databasekeys)
main()