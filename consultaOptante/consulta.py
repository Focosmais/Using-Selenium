from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import urllib
import time
import csv
import os
import deathbycaptcha
import base64
import json

url = 'http://www8.receita.fazenda.gov.br//SimplesNacional/Aplicacoes/ATBHE/ConsultaOptantes.app/ConsultarOpcao.aspx'

driver = webdriver.Chrome()
userDBC = input('deathbycaptcha username: ')
pwdDBC = input('deathbycaptcha password: ')
client = deathbycaptcha.SocketClient(userDBC, pwdDBC)
db = []
result=[]
dbKeys={'nome':'none',
        'cnpj':'none',
        'situacao':'none'}
def consulta(empresa, cnpj, index):
    driver.get(url)
    #driver.switch_to.frame('frame')
    #cnpj_field = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolderConteudo_636506548656840706"]')
    cnpj_field = driver.find_element_by_class_name('caixaTexto')
    time.sleep(3)
    captcha_image = driver.find_element_by_id('img-captcha2')
    img_captcha_base64 = driver.execute_async_script("""
        var ele = arguments[0], callback = arguments[1];
        ele.addEventListener('load', function fn(){
        ele.removeEventListener('load', fn, false);
        var cnv = document.createElement('canvas');
        cnv.width = this.width; cnv.height = this.height;
        cnv.getContext('2d').drawImage(this, 0, 0);
        callback(cnv.toDataURL('image/jpeg').substring(22));
        }, false);
        ele.dispatchEvent(new Event('load'));
        """, captcha_image)
    captcha_field = driver.find_element_by_xpath('//*[@id="ctl00_ContentPlaceHolderConteudo_txtTexto_captcha_serpro_gov_br"]')
    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))

    captcha_text = client.decode('captcha.jpg', 60)
    print(captcha_text)
    captcha_field = captcha_field.send_keys(captcha_text['text'])
    cnpj_field = cnpj_field.send_keys(cnpj)
    driver.find_element_by_name('ctl00$ContentPlaceHolderConteudo$btnConfirmar').click()
    #driver.switch_to_window(driver.window_handles[1])
    #db.append(dbKeys)
    situacao = driver.find_element_by_id('ctl00_ContentPlaceHolderConteudo_lblSituacaoSimples').text
    print(situacao)
    db.append({'nome':empresa, 'cnpj':cnpj, 'situacao':situacao})
    print(db[index]['nome'])
    #driver.switch_to_window(driver.window_handles[0])


def read():
    with open('input.csv', 'r') as inputfile:
        getinput = csv.DictReader(inputfile)
        for row in getinput:
            result.append(row)

    return result

def writedis(values):
    with open('result.json', 'w') as outputjson:
        outputjson.write(json.dumps(values))
    with open('outputfile.csv', 'w') as outputfile:
        write = csv.DictWriter(outputfile, dbKeys)
        write.writeheader()
        for item in values:
            write.writerow(item)
#consulta('10218844000167')
def start():
    values = read()
    print(values)
    index = 0

    for item in values:
        try:
            consulta(item['EMPRESA'], item['CNPJ'], index)
        except KeyboardInterrupt:
            writedis(db)
        except NoSuchElementException:
            time.sleep(5)
            try:
                consulta(item['EMPRESA'], item['CNPJ'], index)
            except NoSuchElementException:
                pass
            except:
                pass
        except:
            writedis(db)
            print('error, but your data could be saved')    
        print(db)
        print(index)
        index+=1
    writedis(db)

start()