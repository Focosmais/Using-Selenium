from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import NoSuchElementException

import deathbycaptcha
import base64

dbcUser = input("user: ")
dbcPass = input("pass: ")
client = deathbycaptcha.SocketClient(dbcUser, dbcPass)


chromeOptions = webdriver.ChromeOptions()
prefs = {"download.default_directory" : "pdfs","plugins.always_open_pdf_externally": True, "download.prompt_for_download": False,}
chromeOptions.add_experimental_option("prefs",prefs)
driver = webdriver.Chrome(chrome_options=chromeOptions)

def getDanfe(chave):
    driver.get('https://www.webdanfe.com.br/danfe/index.html')
    campo_chave = driver.find_element_by_xpath('//*[@id="chaveNfe"]')
    campo_chave = campo_chave.send_keys(chave)
    driver.find_element_by_xpath('//*[@id="one"]/table/tbody/tr[4]/td/center/input[1]').click()
    
    imgCaptcha = driver.find_element_by_xpath('//*[@id="ctl00_PlaceHolderPrincipal_LabelCaptcha"]/img')
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
        """, imgCaptcha)
    with open(r"captcha.jpg", 'wb') as f:
        f.write(base64.b64decode(img_captcha_base64))
    captchaText = client.decode('captcha.jpg',60)
    captchaField = driver.find_element_by_xpath('//*[@id="ctl00_PlaceHolderPrincipal_LabelCaptchaInput"]')
    captchaField = captchaField.send_keys(captchaText['text'])

    driver.find_element_by_xpath('//*[@id="ctl00_PlaceHolderPrincipal_ButtonGerarDanfe"]').click()
    try:
        driver.find_element_by_xpath('/html/body/span/h1/text()')
        driver.find_element_by_xpath('/html/body/span/h2/i')
    except:
        ('runnin')

danfelist = [line.rstrip('\n') for line in open('input.txt', 'r')]

for item in danfelist:
    try:
        getDanfe(item)
    except:
        print("erro "+item)
        getDanfe(item)