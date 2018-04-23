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
dberro = []
#nome = "NFSe_RPS_"
chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "xmls"}
chromeOptions.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

db2= []
database_keys = {'empresa' : 'none',
                'meses' : {'1' : 'none',
                            '2' : 'none',
                            '3' : 'none',
                            '4' : 'none',
                            '5' : 'none',
                            '6' : 'none',
                            '7' : 'none',
                            '8' : 'none',
                            '9' : 'none',
                            '10' : 'none',
                            '11' : 'none',
                            '12' : 'none'}}

def login(id, passw):
    driver.get('https://nfse.salvador.ba.gov.br')
    user_field = driver.find_element_by_xpath('//*[@id="txtLogin"]')
    user_field.clear()
    user_field = user_field.send_keys(id)

    pass_field = driver.find_element_by_id('txtSenha')
    pass_field.clear()
    pass_field = pass_field.send_keys(passw)
    driver.find_element_by_xpath('//*[@id="cmdLogin"]').click()

def xmldownload(month, nome):
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
    driver.execute_script('javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions("ctl00$MainContent$btGerar", "", true, "", "", false, false))')
    #driver.find_element_by_xpath('//*[@id="btGerar"]').click()
    time.sleep(2)
    file = glob.glob('xmls/NFSe*')
    print(file)
    os.rename(file[0], 'xmls/'+nome+str(month)+'/2018.xml')

def navigate(month, nome):
    print(nome + ' ' + str(month))
    try:
        driver.switch_to_window(driver.window_handles[0])
        driver.get('https://nfse.salvador.ba.gov.br/site/contribuinte/nota/consulta.aspx')
        emissao_radio = driver.find_element_by_xpath('//*[@id="rbNFe"]').click()

        data_inicial_field = driver.find_element_by_name('ctl00$MainContent$tbInicio')
        data_inicial_field.clear()
        if month > 9:
            data_inicial_field = data_inicial_field.send_keys('01/'+str(month)+'/2018')
        else:
            data_inicial_field = data_inicial_field.send_keys('01/0'+str(month)+'/2018')
        data_final_field = driver.find_element_by_xpath('//*[@id="tbFim"]')
        data_final_field.clear()

        if month > 9:
            data_final_field = data_final_field.send_keys(str(calendar.monthrange(2018,month)[1])+'/'+str(month)+'/2018')
           
        else:
            data_final_field = data_final_field.send_keys(str(calendar.monthrange(2018,month)[1])+'/0'+str(month)+'/2018')

        time.sleep(5)
        error = driver.find_element_by_xpath('//*[@id="rfvDataFim"]')
        if error.is_displayed:
            driver.find_element_by_xpath('//*[@id="btEmitidas"]').click()
            driver.find_element_by_xpath('//*[@id="btEmitidas"]').click()
        else:
            driver.find_element_by_xpath('//*[@id="btEmitidas"]').click()
        
        
        driver.switch_to_window(driver.window_handles[1])
        valor = driver.find_element_by_xpath('//*[@id="tblResumo"]/tbody/tr[3]/td[2]').text
        
        try:
            driver.close()
            xmldownload(month, nome)
            return (valor)
        except:
            raise
    except UnexpectedAlertPresentException:
        alert = driver.switch_to.alert
        alert.accept()
    #except NoSuchElementException:


def read():
    result = []
    with open('input.csv', 'r') as inputfile:
        getinput = csv.DictReader(inputfile)
        for row in getinput:
            result.append(row)

    return result

def writedis(values, dbKeys):
    with open('outputfile.csv', 'w') as outputfile:
        write = csv.DictWriter(outputfile, dbKeys)
        write.writeheader()
        for item in values:
            write.writerow(item)
    with open('outputjson.json', 'w') as jsonout:
        jsonout.write(json.dumps(values))

def writedis2(values, dbKeys):
    with open('outputfile2.csv', 'w') as outputfile:
        write = csv.DictWriter(outputfile, dbKeys)
        write.writeheader()
        for item in values:
            write.writerow(item)
    with open('outputjson.json', 'w') as jsonout:
        jsonout.write(json.dumps(values))
        
def consulta():
     
    index = 0
    global_result = read()
    #print(global_result)
    database = [{'empresa' : 'none',
                'meses' : {'1' : 'none',
                            '2' : 'none',
                            '3' : 'none',
                            '4' : 'none',
                            '5' : 'none',
                            '6' : 'none',
                            '7' : 'none',
                            '8' : 'none',
                            '9' : 'none',
                            '10' : 'none',
                            '11' : 'none',
                            '12' : 'none'}} for dummy in global_result]
    #print(database)
    for item in global_result:
        try:
            driver.switch_to_window(driver.window_handles[0])
            login(item['cnpj'], item['senha'])
            
            database.append(database_keys)
            database[index]['empresa']=item['empresa']
            
            for number in range(1,4):
                
                try:
                    database[index]['meses'][str(number)] = navigate(number, item['empresa'])
                    writedis(database, database_keys)
                    
                    #print(database[index])
                except UnexpectedAlertPresentException:
                    alert = driver.switch_to.alert
                    alert.accept()
                    database[index]['meses'][str(number)] = navigate(number, item['empresa'])
                    writedis(database, database_keys)
                except:
                    raise
            db2.append(database[index])
            index += 1
            print(index)
        
        except KeyboardInterrupt:
            writedis2(database, database_keys)

        except:
            dberro.append({'empresa':item['empresa']})
            index+=1


    writedis2(database, database_keys)


consulta()
