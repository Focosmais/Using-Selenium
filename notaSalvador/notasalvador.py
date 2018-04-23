from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import csv
import tkinter as tk
from tkinter import ttk
from tkinter import *
from tkinter import filedialog
root = tk.Tk()
root.withdraw()

#################
empresas = []
cnpjs = []
values = []
descriptions = []
#################

driver = webdriver.Chrome()

driver.get("https://nfse.salvador.ba.gov.br/")

def login(id, passw):
    user_field = driver.find_element_by_xpath('//*[@id="txtLogin"]')
    user_field.clear()
    user_field = user_field.send_keys(id)

    pass_field = driver.find_element_by_id('txtSenha')
    pass_field.clear()
    pass_field = pass_field.send_keys(passw)
    driver.find_element_by_xpath('//*[@id="cmdLogin"]').click()

def navigate(cnpj, value, description, cnae, aliq):
          
    driver.get('https://nfse.salvador.ba.gov.br/site/contribuinte/nota/nota.aspx')
    cnpj_field = driver.find_element_by_id('tbCPFCNPJTomador')
    cnpj_field = cnpj_field.send_keys(cnpj)
    botao = driver.find_element_by_id('btAvancar').click()
    print(cnae)
    fill(value, description, cnae, aliq)
    
    #g = open('auxi2.txt', 'r+')

def fill(value, description, cnae, aliq):
    time.sleep(5)
    #print(cnae)

    cnae1 = driver.find_element_by_xpath('//*[@id="ddlCNAE_chosen"]/a/span').click()
    cnae1 = driver.find_element_by_xpath('//*[@id="ddlCNAE_chosen"]/a/span').click()
    cnae_text = driver.find_element_by_xpath('/html/body/article/form/div[3]/table/tbody/tr/td/div[1]/table[1]/tbody/tr[2]/td[1]/div[1]/div/div/input')
    time.sleep(2)
    try:
        cnae_text.click()
    except:
        cnae1 = driver.find_element_by_xpath('//*[@id="ddlCNAE_chosen"]/a/span').click()
        cnae_text.click()
    time.sleep(2)
    cnae_text = cnae_text.send_keys(cnae)
    cnae_select = driver.find_element_by_xpath('/html/body/article/form/div[3]/table/tbody/tr/td/div[1]/table[1]/tbody/tr[2]/td[1]/div[1]/div/ul/li').click()
    time.sleep(2)
    #cnaeSelect = driver.find_element_by_xpath('/html/body/article/form/div[3]/table/tbody/tr/td/div[1]/table[1]/tbody/tr[2]/td[1]/div[1]/div/ul/li[2]').click()
    
    cnae2 = driver.find_element_by_xpath('//*[@id="ddlAtividade_chosen"]/a/span').click()
    cnae2Select = driver.find_element_by_xpath('//*[@id="ddlAtividade_chosen"]/div/ul/li').click()

    aliqf = driver.find_element_by_xpath('//*[@id="tbAliquota"]')
    aliqf = aliqf.send_keys(aliq)
    time.sleep(5)
    valor = driver.find_element_by_id("tbValor")
    valor = valor.send_keys(value)
    discriminacao = driver.find_element_by_id("tbDiscriminacao")
    discriminacao = discriminacao.send_keys(description)
    emitir3 = driver.find_element_by_id("btEmitir").click() ############################## BOTÃO DE EMITIR
    time.sleep(5)
    try:
        driver.switch_to.alert.accept()
    except:
        print ("fail")
        
###############################################
result = []
def read(path):
    with open(path, 'r') as inputfile:
        getinput = csv.DictReader(inputfile)
        for row in getinput:
            result.append(row)

    return result
###############################################


def fetch():
    def getFields(field):
        field_text = field.get()
        #login_field_text = login_field.get()
        #pass_field_text = pass_field.get()

        return (field_text)

#        with open('logininfo.txt', 'w') as info:
#            info.write(loginFieldText + '\n')
#            info.write(passFieldText)


    window = tk.Tk()
    window.title("ACESSO")

    login_field_label = Label(window, text = "CNPJ ou CPF").grid(row = 0, column = 1)
    login_field = Entry(window)
    login_field.grid(row = 1, column = 1)

    pass_field_label = Label(window, text = "Senha").grid(row = 2, column = 1)
    pass_field = Entry(window)
    pass_field.grid(row = 3, column = 1)

    cnae_field_label = Label(window, text = "CNAE").grid(row = 4, column = 1)
    cnae_field = Entry(window)
    cnae_field.grid(row = 5, column = 1)

    aliq_field_label = Label(window, text = "Aliq.").grid(row = 6, column = 1)
    aliq_field = Entry(window)
    aliq_field.grid(row = 7, column = 1)
    #login_field = input('LOGIN: ')
    #password_field = input('SENHA: ')
    #cnae = input("num CNAE: ")

    def starting():
        #window.destroy()
        window_2 = tk.Tk()
        window_2.title("EMITINDO...")
        progress = ttk.Progressbar(window_2, length = 300, mode = 'determinate')
        #progress.start()
        progress.grid(row = 1)
        #print(str(size_data)+" empresas")
        size_data = IntVar()
        index = 0
        def update_progress():
            
            try:
                #progress.update_idletasks()
                progress.step(100/len(cnpjs))
                info_label.configure(text = empresas[index])
                info_label2.configure(text = values[index])
                window_2.update_idletasks()
            except ZeroDivisionError:
                raise
                pass

        file_path = filedialog.askopenfilename()
        data = read(file_path)

        #print(data)

        for item in data:
            
            empresas.append(item['empresa'])
            cnpjs.append(item['cnpj'])
            values.append(item['valor'])
            descriptions.append(item['discriminacao'])

        
        size_data = len(cnpjs)
        print(size_data)
        login(getFields(login_field), getFields(pass_field))
        #var = StringVar()
        #var2 = StringVar()
        for cnpj, val, desc, name in zip(cnpjs, values, descriptions, empresas):
            info_label = Label(window_2, text = empresas[0])
            info_label.grid(row = 2)
            info_label2 = Label(window_2, text = values[0])
            info_label2.grid(row = 3)
            update_progress()
            window_2.update()
            window_2.update_idletasks()
            
            navigate(cnpj, val, desc, getFields(cnae_field), getFields(aliq_field))

            index += 1
    send_button = Button(window, text = "ENVIAR", command = starting).grid(row = 8, column = 1)


fetch()
try:
    root.mainloop()
except KeyboardInterrupt:
    raise