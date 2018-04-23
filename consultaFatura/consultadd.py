from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import calendar
import json
import glob
import os

chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "xmls/dd"}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

def login(id, passw):
    driver.get('https://diasdavila.saatri.com.br/Autenticacao/Index')
    loginbutton     = driver.find_element_by_id("lnk_Login").click()
    userField = driver.find_element_by_xpath('//*[@id="Cpf"]')
    userField = userField.send_keys(id)

    passField = driver.find_element_by_xpath('//*[@id="Senha"]')
    passField = passField.send_keys(passw + Keys.ENTER)

def navigate(month, nome):
    driver.get('https://diasdavila.saatri.com.br/DocumentoFiscalAutenticado/BaixarXmlConsultaPorFaixa')
    data_inicial_field = driver.find_element_by_xpath('//*[@id="periodoInicial"]')
    data_final_field = driver.find_element_by_xpath('//*[@id="periodoFinal"]')

    data_inicial_field.clear()
    if month > 9:
        data_inicial_field = data_inicial_field.send_keys('01/'+str(month)+'/2018')
    else:
        data_inicial_field = data_inicial_field.send_keys('01/0'+str(month)+'/2018')
    
    data_final_field.clear()
    if month > 9:
        data_final_field = data_final_field.send_keys(str(calendar.monthrange(2018,month)[1])+'/'+str(month)+'/2018')
    else:
        data_final_field = data_final_field.send_keys(str(calendar.monthrange(2018,month)[1])+'/0'+str(month)+'/2018')

    send = driver.find_element_by_xpath('//*[@id="lnk_BaixarXmlConsultaPorFaixa"]').click()
    time.sleep(2)
    dialog = driver.find_element_by_xpath('/html/body/div[5]')
    if dialog.is_displayed():
        pass
    else:
        file = glob.glob('xmls/dd/NFSE*')
        os.rename(file[0], 'xmls/dd/'+nome+str(month)+'/2018.xml')

def read():
    result = []
    with open('input.csv', 'r') as inputfile:
        getinput = csv.DictReader(inputfile)
        for row in getinput:
            result.append(row)

    return result

def main():
    data = read()

    for item in data:
        print(item['empresa'])
        login(item['cga'], item['senha'])
        time.sleep(2)
        for number in range(1,4):
            try:
                navigate(number, item['empresa'])
            except NoSuchElementException:
                print('fail '+item['empresa'])
                break
            except:
                raise

main()