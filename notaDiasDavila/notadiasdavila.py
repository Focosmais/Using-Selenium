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

driver = webdriver.Chrome()

#################
empresas = []
cnpjs = []
values = []
descriptions = []
################# 


def login(cpf, senha):
    driver.get("https://diasdavila.saatri.com.br/")
    time.sleep(10)
    #loginbutton
    driver.find_element_by_id("lnk_Login").click()
    time.sleep(5)

    userfield = driver.find_element_by_id("Cpf")
    #userfield.click()
    #userfield.clear()
    userfield = userfield.send_keys(cpf)

    passfield = driver.find_element_by_id("Senha")
    #passfield.click()
    #passfield.clear()
    passfield = passfield.send_keys(senha + Keys.ENTER)


###############################################
result = []

def read(path):
    with open(path, 'r') as inputfile:
        try:
            getinput = csv.DictReader(inputfile)
            for row in getinput:
                result.append(row)
        except KeyError:
            getinput = csv.DictReader(inputfile, delimiter = ';')
            for row in getinput:
                result.append(row)
        except:
            raise
    return result
###############################################




def navigate(cnpj, value, description, cnae, aliq):
    driver.get(
        'https://diasdavila.saatri.com.br/DocumentoFiscalAutenticado/Emitir')
    cnpjField = driver.find_element_by_id('txt_CpfCnpj')
    cnpjField.clear()
    cnpjField = cnpjField.send_keys(cnpj)
    driver.find_element_by_xpath('/html/body').click()
    time.sleep(10)

    try:
        driver.find_element_by_xpath('//*[@id="DataTables_Table_0"]/tbody/tr[1]/td[1]/div').click()
        driver.find_element_by_xpath('//*[@id="cbb_EstadoTomador_chosen"]/a').click()
        driver.find_element_by_xpath('//*[@id="cbb_EstadoTomador_chosen"]/div/ul/li[5]').click()
        time.sleep(2)
        driver.find_element_by_xpath('//*[@id="cbb_MunicipioTomador_chosen"]/a/span').click()
        driver.find_element_by_xpath('//*[@id="cbb_MunicipioTomador_chosen"]/div/ul/li[120]').click()
        cnaeStep1 = driver.find_element_by_xpath('//*[@id="select2-chosen-1"]').click()
        time.sleep(2)
        cnaeStep2 = driver.find_element_by_xpath('//*[@id="s2id_autogen1_search"]')
        cnaeStep2 = cnaeStep2.send_keys(cnae)
        time.sleep(2)
        cnaeStep3 = driver.find_element_by_xpath('//*[@id="select2-results-1"]').click()
        discriminacao = driver.find_element_by_id('txt_DiscriminacaoServico')
        discriminacao = discriminacao.send_keys(description)
        valor = driver.find_element_by_id('DocumentoFiscalItem_ValorServico')
        valor = valor.send_keys(value)
        # aliquota        = driver.find_element_by_xpath('//*[@id="cbb_AliquotaSimplesNacional"]/option[4]').click()
        aliqField = driver.find_element_by_xpath('//*[@id="DocumentoFiscalItem_AliquotaIss"]')
        aliqField = aliqField.send_keys(aliq)
        #emitir = driver.find_element_by_id('btn_Emitir').click()
    except:

        # bota  oSearch     = driver.find_element_by_xpath('//*[@id="btn_LocalizarContribuinte"]/span[1]').click()
        time.sleep(2)
        cnaeStep1 = driver.find_element_by_xpath('//*[@id="select2-chosen-1"]').click()
        time.sleep(3)
        cnaeStep2 = driver.find_element_by_xpath('//*[@id="s2id_autogen1_search"]')
        cnaeStep2 = cnaeStep2.send_keys(cnae)
        time.sleep(10)
        cnaeStep3 = driver.find_element_by_xpath('//*[@id="select2-results-1"]').click()
        discriminacao = driver.find_element_by_id('txt_DiscriminacaoServico')
        discriminacao = discriminacao.send_keys(description)
        valor = driver.find_element_by_id('DocumentoFiscalItem_ValorServico')
        valor = valor.send_keys(value)
        # aliquota        = driver.find_element_by_xpath('//*[@id="cbb_AliquotaSimplesNacional"]/option[4]').click()
        aliqField = driver.find_element_by_xpath('//*[@id="DocumentoFiscalItem_AliquotaIss"]')
        aliqField = aliqField.send_keys(aliq)
        #emitir = driver.find_element_by_id('btn_Emitir').click()


def interface():
    def getFields(field):
        field_text = field.get()

        return (field_text)

    window = tk.Tk()
    window.title("ACESSO")

    loginFieldLabel = Label(
        window, text="CNPJ da empresa").grid(row=0, column=1)
    loginField = Entry(window)
    loginField.grid(row=1, column=1)

    passFieldLabel = Label(window, text="Senha").grid(row=2, column=1)
    passField = Entry(window)
    passField.grid(row=3, column=1)

    cnaeFieldLabel = Label(window, text="CNAE").grid(row=4, column=1)
    cnaeField = Entry(window)
    cnaeField.grid(row=5, column=1)

    aliqFieldLabel = Label(window, text='Aliquota').grid(row=6, column=1)
    aliqField = Entry(window)
    aliqField.grid(row=7, column=1)

    def start():
        window2 = tk.Tk()
        window2.title('EMITINDO')
        progress = ttk.Progressbar(window2, length=300, mode='determinate')
        progress.grid(row=1)
        sizeData = IntVar()
        index = 0
        def updateProgress():
            try:
                progress.step(100/len(cnpjs))
                infoLabel.configure(text = empresas[index])
                infoLabel2.configure(text = values[index])
                window2.update_idletasks()
            except ZeroDivisionError:
                raise
                pass
        filePath= filedialog.askopenfilename()
        data= read(filePath)

        for item in data:
            empresas.append(item['empresa'])
            cnpjs.append(item['cnpj'])
            values.append(item['valor'])
            descriptions.append(item['discriminacao'])

        sizeData= len(cnpjs)
        print(sizeData)
        login(getFields(loginField), getFields(passField))

        for cnpj, val, desc, name in zip(cnpjs, values, descriptions, empresas):
            infoLabel= Label(window2, text = empresas[0])
            infoLabel.grid(row=2)
            infoLabel2= Label(window2, text = values[0])
            infoLabel2.grid(row=3)
            updateProgress()
            window2.update()
            window2.update_idletasks()

            navigate(cnpj, val, desc, getFields(cnaeField), getFields(aliqField))

            index += 1

    sendButton= Button(window, text = "ENVIAR", command = start).grid(row=8, column=1)

interface()
try:
    root.mainloop()
except KeyboardInterrupt:
    raise
