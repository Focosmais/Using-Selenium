from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
import time
import csv
import calendar
import json
import os
import glob

dberro = []
#nome = "NFSe_RPS_"

#chrome_options = Options()
# chrome_options.add_argument("--headless")
#prefs = {"setDownloadBehavior" : {"behavior":"allow", "downloadPath":"~/Downloads"}}
#chrome_options.add_experimental_option("prefs", prefs)
#chromeOptions = webdriver.ChromeOptions(chrome_options=chrome_options)
driver = webdriver.Chrome(executable_path='./chromedriver')

db2 = []
database_keys = {'empresa': 'none',
                 'cnpj': 'none',
                 'faturamento': 'none'}


def login(id, passw):
    # Download com chrome headless
    driver.command_executor._commands["send_command"] = (
        "POST",
        '/session/$sessionId/chromium/send_command'
    )
    params = {
        'cmd': 'Page.setDownloadBehavior',
        'params': {
            'behavior': 'allow',
            'downloadPath': 'xmls'
        }
    }
    driver.execute("send_command", params)

    driver.get('https://nfse.salvador.ba.gov.br')
    user_field = driver.find_element_by_xpath('//*[@id="txtLogin"]')
    user_field.clear()
    user_field = user_field.send_keys(id)

    pass_field = driver.find_element_by_id('txtSenha')
    pass_field.clear()
    pass_field = pass_field.send_keys(passw)
    driver.find_element_by_xpath('//*[@id="cmdLogin"]').click()


def xmldownload(month, nome):
    try:
        driver.switch_to_window(driver.window_handles[0])
        driver.get(
            'https://nfse.salvador.ba.gov.br/site/contribuinte/nota/ExportaArquivo.aspx')
        driver.find_element_by_xpath(
            '//*[@id="ddlTipoArquivo"]/option[3]').click()
        data_inicial_field = driver.find_element_by_xpath(
            '//*[@id="tbInicio"]')
        data_inicial_field.clear()
        data_final_field = driver.find_element_by_xpath('//*[@id="tbFim"]')

        if month > 9:
            data_inicial_field = data_inicial_field.send_keys(
                '01/'+str(month)+'/2018')
        else:
            data_inicial_field = data_inicial_field.send_keys(
                '01/0'+str(month)+'/2018')
        data_final_field.clear()
        if month > 9:
            data_final_field = data_final_field.send_keys(
                str(calendar.monthrange(2018, month)[1])+'/'+str(month)+'/2018')

        else:
            data_final_field = data_final_field.send_keys(
                str(calendar.monthrange(2018, month)[1])+'/0'+str(month)+'/2018')
        time.sleep(5)
        driver.execute_script(
            'javascript:WebForm_DoPostBackWithOptions(new WebForm_PostBackOptions("ctl00$MainContent$btGerar", "", true, "", "", false, false))')
        # driver.find_element_by_xpath('//*[@id="btGerar"]').click()
        time.sleep(2)
        file = glob.glob('xmls/NFSe*')
        print(file)
        try:
            os.rename(file[0], 'xmls/'+nome+str(month)+'/2018.xml')
        except IndexError:
            if driver.find_element_by_xpath('//*[@id="rfvContribuinte"]').is_displayed():
                driver.find_element_by_xpath(
                    '//*[@id="ddlPrestador"]/option[2]').click()
            driver.find_element_by_xpath('//*[@id="btGerar"]').click()
            driver.find_element_by_xpath('//*[@id="btGerar"]').click()
            time.sleep(2)
            file = glob.glob('xmls/NFSe*')
            try:
                os.rename(file[0], 'xmls/'+nome+str(month)+'2018.xml')
            except FileNotFoundError:
                nome2 = nome.translate({ord(c): None for c in '/'})
                os.rename(file[0], 'xmls/'+nome2+str(month)+'2018.xml')
            except IndexError:
                time.sleep(10)
                os.rename(file[0], 'xmls/'+nome+str(month)+'2018.xml')

    except UnexpectedAlertPresentException:
        alert = driver.switch_to.alert
        alert.accept()


def getfat(month):
    driver.switch_to_window(driver.window_handles[0])
    driver.get(
        'https://nfse.salvador.ba.gov.br/site/contribuinte/nota/consulta.aspx')
    emissao_radio = driver.find_element_by_xpath('//*[@id="rbNFe"]').click()

    data_inicial_field = driver.find_element_by_name(
        'ctl00$MainContent$tbInicio')
    data_inicial_field.clear()
    if month > 9:
        data_inicial_field = data_inicial_field.send_keys(
            '01/'+str(month)+'/2018')
    else:
        data_inicial_field = data_inicial_field.send_keys(
            '01/0'+str(month)+'/2018')
    data_final_field = driver.find_element_by_xpath('//*[@id="tbFim"]')
    data_final_field.clear()

    if month > 9:
        data_final_field = data_final_field.send_keys(
            str(calendar.monthrange(2018, month)[1])+'/'+str(month)+'/2018')

    else:
        data_final_field = data_final_field.send_keys(
            str(calendar.monthrange(2018, month)[1])+'/0'+str(month)+'/2018')

    time.sleep(5)
    error = driver.find_element_by_xpath('//*[@id="rfvDataFim"]')
    if error.is_displayed:
        driver.find_element_by_xpath('//*[@id="btEmitidas"]').click()
        driver.find_element_by_xpath('//*[@id="btEmitidas"]').click()
    else:
        driver.find_element_by_xpath('//*[@id="btEmitidas"]').click()

    try:
        driver.switch_to_window(driver.window_handles[1])
    except IndexError:
        try:
            driver.find_element_by_xpath('//*[@id="btEmitidas"]').click()
            driver.find_element_by_xpath('//*[@id="ddlContribuinte"]/option[2]').click()
            driver.switch_to_window(driver.window_handles[1])
        except:
            driver.find_element_by_xpath('//*[@id="btEmitidas"]').click()
            driver.find_element_by_xpath('//*[@id="ddlContribuinte"]/option[2]').click()
            driver.switch_to_window(driver.window_handles[1])

    valor = driver.find_element_by_xpath('//*[@id="tblResumo"]/tbody/tr[3]/td[2]').text

    time.sleep(3)

    try:
        driver.switch_to_window(driver.window_handles[1])
        close = driver.close()
        driver.switch_to_window(driver.window_handles[1])
        close = driver.close()
    except:
        raise
    print(valor)

    return(valor)


def read():
    result = []
    with open('inputall.csv', 'r') as inputfile:
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
    database = []
    index = 0
    global_result = read()
    # print(global_result)
    '''
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
                            '''
    # print(database)
    number = 9
    for item in global_result:
        if item['cidade'] == "SSA":
            print(item['empresa'])
            try:
                print(item['empresa'])
                driver.switch_to_window(driver.window_handles[0])
                login(item['cnpj'], item['senha'])
                try:
                    database.append(
                        {'empresa': item['empresa'], 'cnpj': item['cnpj'], 'faturamento': getfat(number)})
                    writedis(database, database_keys)

                    #xmldownload(number, item['empresa'])
                except NoSuchElementException:
                    print("login error")
                    login(item['cnpj'], item['senha'])

                driver.switch_to_window(driver.window_handles[0])

                # database.append(database_keys)
                # database[index]['empresa']=item['empresa']

                # print(database[index])
            except UnexpectedAlertPresentException:
                alert = driver.switch_to.alert
                alert.accept()
                #database[index]['meses'][str(number)] = getfat(number, item['empresa'])
                writedis(database, database_keys)

            except:
                raise

        writedis2(database, database_keys)

consulta()