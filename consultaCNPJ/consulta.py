from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
import urllib
import time
import csv
import os
import pdfkit
import json

url = "https://www.receita.fazenda.gov.br/pessoajuridica/cnpj/cnpjreva/Cnpjreva_Solicitacao2.asp"


driver = webdriver.Chrome()
driver.set_page_load_timeout(30)
index = 0
results = []
result = []
userDBC = input('deathbycaptcha username: ')
pwdDBC = input('deathbycaptcha password: ')
client = deathbycaptcha.SocketClient(userDBC, pwdDBC)
database = []
dbKeys = {"nome":'empy',
         "inscricao":'empy',
         "abertura":'empy',
         "nome_empresarial":'empy',
         "nome_fantasia":'empy',
         "atividade_principal":'empy',
         "atividade_secundaria":'empy',
         "natureza_juridica":'empy',
         "logradouro":'empy',
         "num":'empy',
         "complemento":'empy',
         "cep":'empy',
         "bairro":'empy',
         "municipio":'empy',
         "uf":'empy',
         "email":'empy',
         "telefone":'empy',
         "efr":'empy',
         "situacao_cadastral":'empy',
         "situacao_cadastral_data":'empy'}

def read():
    with open('input.csv', 'r') as inputfile:
        getinput = csv.DictReader(inputfile)
        for row in getinput:
            result.append(row)
    #print (result)
    return result
'''def writedis(values):
    with open('outputfile.csv', 'a') as outputfile:
        write = csv.DictWriter(outputfile, dbKeys)
        write.writeheader()
        for item in values:
            write.writerow(item)'''

cnpjs = read()

database = []
#def solvecaptcha():
#    captchaitems
#    driver.switch_to.framedriver.find_element_by_xpath('//*[@id="theForm"]/font/font/table/tbody/tr[2]/td/div/div/div/iframe')))
#    driver.find_element_by_xpath('//*[@id="recaptcha-anchor"]/div[5]').click()
#        try:


def consulta(cnpj, index):
    database.append({"nome":'empy',
         "inscricao":'empy',
         "abertura":'empy',
         "nome_empresarial":'empy',
         "nome_fantasia":'empy',
         "atividade_principal":'empy',
         "atividade_secundaria":'empy',
         "natureza_juridica":'empy',
         "logradouro":'empy',
         "num":'empy',
         "complemento":'empy',
         "cep":'empy',
         "bairro":'empy',
         "municipio":'empy',
         "uf":'empy',
         "email":'empy',
         "telefone":'empy',
         "efr":'empy',
         "situacao_cadastral":'empy',
         "situacao_cadastral_data":'empy'})
    errcount = 0
    try:
        driver.get(url)
    except NoSuchElementException:
        driver.get(url)

    if "Emissão de Comprovante de Inscrição e de Situação Cadastral" == driver.title:
        mainWindow = driver.current_window_handle
        time.sleep(3)
        driver.find_element_by_xpath('//*[@id="captchaSonoro"]').click()
        captcha_image = driver.find_element_by_xpath('//*[@id="imgCaptcha"]')
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
        with open(r"captcha.jpg", 'wb') as f:
            f.write(base64.b64decode(img_captcha_base64))
        captcha_text = client.decode('captcha.jpg', 60)
        #captcha_field = captcha_field.sendkeys(captcha_text)
        cnpj_field = driver.find_element_by_xpath('//*[@id="cnpj"]')
        cnpj_field = cnpj_field.send_keys(cnpj)
        captcha_field = driver.find_element_by_xpath('//*[@id="txtTexto_captcha_serpro_gov_br"]')
        print(captcha_text)
        captcha_field = captcha_field.send_keys(captcha_text['text'])
        time.sleep(2)
        submit = driver.find_element_by_xpath('//*[@id="submit1"]').click()
        #try:
        #    for c in range(1,6)
        #        for l in range
        #        driver.find_element_by_xpath('//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[1]/div/div[1]')
        #        driver.find_element_by_xpath('//*[@id="rc-imageselect-target"]/table/tbody/tr[1]/td[2]/div/div[1]')
        #input('waiting for the user')
        print('done')
    elif "Tela de respostas" == driver.title:
        if errcount == 0:
            time.sleep(10)
            driver.get(url)
            errcount = 1
        else:
            pass
    time.sleep(2)
    #database.append(dbKeys)
    #extracted_data = [
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/font[2]').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[2]/tbody/tr/td[3]/font[1]').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[4]/tbody/tr/td/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[5]/tbody/tr/td/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[5]/tbody/tr/td/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[7]/tbody/tr/td/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[8]/tbody/tr/td[1]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[8]/tbody/tr/td[3]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[8]/tbody/tr/td[5]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[9]/tbody/tr/td[1]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[9]/tbody/tr/td[3]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[9]/tbody/tr/td[5]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[9]/tbody/tr/td[7]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[10]/tbody/tr/td[1]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[10]/tbody/tr/td[3]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[11]/tbody/tr/td/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[12]/tbody/tr/td[1]/font[2]/b').text,,
    #driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[12]/tbody/tr/td[3]/font[2]/b').text,
    #]
    html=driver.page_source
    database[index]['nome'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/font[2]/b').text
    database[index]['inscricao'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[2]/tbody/tr/td[1]/font[2]/b[1]').text
    database[index]['abertura'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[2]/tbody/tr/td[3]/font[2]/b').text
    database[index]['nome_empresarial'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[3]/tbody/tr/td/font[2]/b').text
    database[index]['nome_fantasia'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[4]/tbody/tr/td/font[2]/b').text
    database[index]['atividade_principal'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[5]/tbody/tr/td/font[2]/b').text
    database[index]['atividade_secundarias'] = []
    #soup = BeautifulSoup(html, 'lxml')
    #comments_to_search_for = {'<!-- Início Linha ATIVIDADE ECONOMICA SECUNDARIA-->', '<!-- Fim Linha ATIVIDADE ECONOMICA SECUNDARIA -->'}
    #i=1
    
    for i in range(14):
        try:
            #print(i)
            #print(driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[6]/tbody/tr/td/font['+str(i)+']/b').text)
            
            #print(driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[6]/tbody/tr/td/font['+i+']/b').text)
            database[index]['atividade_secundarias'].append(driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[6]/tbody/tr/td/font['+str(i)+']/b').text)
        except:
            pass
    database[index]['natureza_juridica'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[7]/tbody/tr/td/font[2]/b').text
    database[index]['logradouro'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[8]/tbody/tr/td[1]/font[2]/b').text
    database[index]['num'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[8]/tbody/tr/td[3]/font[2]/b').text
    database[index]['complemento'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[8]/tbody/tr/td[5]/font[2]/b').text
    database[index]['cep'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[9]/tbody/tr/td[1]/font[2]/b').text
    database[index]['bairro'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[9]/tbody/tr/td[3]/font[2]/b').text
    database[index]['muncipio'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[9]/tbody/tr/td[5]/font[2]/b').text
    database[index]['uf'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[9]/tbody/tr/td[7]/font[2]/b').text
    database[index]['email'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[10]/tbody/tr/td[1]/font[2]/b').text
    database[index]['telefone'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[10]/tbody/tr/td[3]/font[2]/b').text
    database[index]['efr'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[11]/tbody/tr/td/font[2]/b').text
    database[index]['situacao_cadastral'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[12]/tbody/tr/td[1]/font[2]/b').text
    database[index]['situacao_cadastral_data'] = driver.find_element_by_xpath('//*[@id="principal"]/table[2]/tbody/tr/td/table[12]/tbody/tr/td[3]/font[2]/b').text
    time.sleep(2)
    print(database)
    driver.get(url)



def main():
    index = 0
    errcount = 0

    try:
        for item in cnpjs:
            try:
                print (consulta(item['cnpj'], index))
                print (database[index]['nome'])
                print (database[index]['atividade_principal'])
                print (database[index]['atividade_secundarias'])
                #writedis(consulta(item['cnpj'], index))
                index +=1
            except:
                if errcount < 2:
                    print (consulta(item['cnpj'], index))
                    print (database[index]['nome'])
                    print (database[index]['atividade_principal'])
                    print (database[index]['atividade_secundarias'])
                    #writedis(consulta(item['cnpj'], index))
                    errcount+=1
                    index +=1
                else:
                    errcount = 0
                    pass
                    
    except:
       # writedis(consulta(item['cnpj'], index))
       with open('output.json', 'w') as output:
            output.write(json.dumps(database))
            pass
        
with open('output.json', 'w') as output:
            output.write(json.dumps(database))
main()
with open('output2.json', 'w') as output:
        output.write(json.dumps(database))