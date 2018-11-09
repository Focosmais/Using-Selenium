from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException
import time
import csv
import calendar
import json
import os
import glob


chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "xmls e guias"}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

def login(cnpj, passw):
    #cnpj
    driver.get('https://nfse.salvador.ba.gov.br')
    user_field = driver.find_element_by_xpath('//*[@id="txtLogin"]') 
    user_field.clear()
    user_field = user_field.send_keys(id)
    #password
    pass_field = driver.find_element_by_id('txtSenha')
    pass_field.clear()
    pass_field = pass_field.send_keys(passw)
    driver.find_element_by_xpath('//*[@id="cmdLogin"]').click()

db = []

def fat(name, month):
    driver.switch_to_window(driver.window_handles[0])
    driver.get('https://nfse.salvador.ba.gov.br/site/contribuinte/nota/ExportaArquivo.aspx')
    driver.find_element_by_xpath('//*[@id="ddlTipoArquivo"]/option[3]').click()
    data_inicial_field = driver.find_element_by_xpath('//*[@id="tbInicio"]')
    data_inicial_field.clear()
    data_final_field = driver.find_element_by_xpath('//*[@id="tbFim"]')
    

    if month > 9:
        data_inicial_field = data_inicial_field.send_keys('01/'+str(month)+'/2018')
    else:
        data_inicial_field = data_inicial_field.send_keys('01/0'+str(month)+'/2018')
    data_final_field.clear()

    if month > 9:
        data_final_field = data_final_field.send_keys(str(calendar.monthrange(2018,month)[1])+'/'+str(month)+'/2018')
    else:
        data_final_field = data_final_field.send_keys(str(calendar.monthrange(2018,month)[1])+'/0'+str(month)+'/2018')
    time.sleep(5)
    driver.execute_script("javascript:ConsultarNotas('notasapuradas.aspx');")

    driver.switch_to.window(driver.window_handles[0])
    
    faturamento = driver.find_element_by_xpath('//*[@id="tblResumo"]/tbody/tr[3]/td[2]').text()
    print(faturamento)

    #download XML
    driver.find_element_by_xpath('//*[@id="ddlTipoArquivo"]/option[3]').click()
    driver.execute_script("expAguarde(this); __doPostBack('ctl00$MainContent$true$btGerar','')")

    time.sleep(2)
    file = glob.glob('xmls/NFSe*')
    print(file)
    os.rename(file[0], 'xmls/'+nome+'.xml')

    return faturamento
def ISS(month):
    driver.get('https://nfse.salvador.ba.gov.br/site/contribuinte/guia/guias.aspx')

    iss_month_dropdown = driver.find_element_by_xpath('//*[@id="ddlMes"]/option['+str(int(month)+1)+']').click()
    driver.find_element_by_xpath('//*[@id="btConsulta"]').click()

    try:
        driver.find_element_by_xpath('//*[@id="dgGuias"]/tbody/tr[2]/td[6]/a').click()
        driver.find_element_by_xpath('//*[@id="btVisualizarGuia"]').click()
        try:
            driver.find_element_by_xpath('//*[@id="btVisualizarGuia"]').click()
        except NoSuchElementException:
            print('só uma guia')
    except NoSuchElementException:
        print('Não existem guias')

    # todo baixar guias


def read():
    result = []
    with open('inputfile.csv', 'r') as inputfile:
        getinput = csv.DictReader(inputfile)
        for row in getinput:
            result.append(row)

        # print(result)
    return result

def writeresult():
    dbKeys = {"fat":'',"empresa":''}
    with open('outputfile.csv', 'w') as outputfile:
        write = csv.DictWriter(outputfile, dbKeys)
        write.writeheader()
        for item in values:
            write.writerow(item)
    with open('outputjson.json', 'w') as jsonout:
        jsonout.write(json.dumps(values))
