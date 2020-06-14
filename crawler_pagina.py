from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from urllib.request import urlretrieve
from time import sleep
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
import socket

url = 'https://www.buscape.com.br/search?q=cerveja+heineken'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
response = urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

cards = []

anuncios = soup.find('div', {'id': 'pageSearchResultsBody'}).findAll('div', class_="card card--offer card--cpc")
for anuncio in anuncios:
    # print(str(anuncio) + "\n\n")
    card = {}

    for info in anuncio:
        anuncio.find('span', {'class': 'customValue'}).getText()
        card['value'] = anuncio.find('span', {'class': 'customValue'}).getText()

        card[info.get('class')[0].split('-')[-1]] = info.get_text()

    anuncio.find('div', {'class': 'cardFooter'}).find('a').get('href')
    card['link'] = 'https://www.buscape.com.br/' + anuncio.find('div', {'class': 'cardFooter'}).find('a').get('href')

    # dataset = pd.DataFrame.from_dict(card, orient = 'index').T
    # dataset.to_csv('./resultado_final/trigueiro.csv',sep=';', encoding='utf-8-sig')

    cards.append(card)

    image = anuncio.find('a', {'class': 'cardImage'}).img
    urlretrieve(image.get('src'), './info/imagem/' + image.get('src').split('/')[-1])

dataset = pd.DataFrame(cards)
# dataset = pd.DataFrame.from_dict(cards, orient = 'index').T
dataset.to_csv('./info/dados/filipe.csv', sep=';', encoding='utf-8-sig')


# ====================================================================================
# gravar + infos['value'] + infos['cardBody'] +infos['link']

def converte_json(cards):
    gravar = ""
    for infos in cards:
        gravar = gravar + infos['cardBody'] + 'Acesse o site ====>' + infos['link'] + '\n'
        #gravar = gravar + infos['cardBody'] + '\nPreco: ' + infos['value'] + '\nAcesse o site: ' + infos['link']
    return gravar


# message_text='Ola essa é uma mensagem automatizada de Whats App escrita pelo computador e enviada por Filipe Trigueiro. Obrigado pela atenção' # message
message_text = converte_json(cards)
# 'Ola essa é uma mensagem automatizada de Whats App escrita pelo computador  -----  Leo, não esquecer meu cabo vga amanhã.' # message
no_of_message = 1  # no. of time
moblie_no_list = [5521964596858]  # list of phone number


def element_presence(by, xpath, time):
    element_present = EC.presence_of_element_located((By.XPATH, xpath))
    WebDriverWait(driver, time).until(element_present)


def is_connected():
    try:
        # connect to the host -- tells us if the host is actually
        # reachable
        socket.create_connection(("www.google.com", 80))
        return True
    except:
        is_connected()


driver = webdriver.Chrome(executable_path=r'./chromedriver.exe')
driver.get("http://web.whatsapp.com")
sleep(10)  # wait time to scan the code in second


def send_whatsapp_msg(phone_no, text):
    driver.get("https://web.whatsapp.com/send?phone={}&source=&data=#".format(phone_no))
    try:
        driver.switch_to_alert().accept()
    except Exception as e:
        pass

    try:
        element_presence(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]', 30)
        txt_box = driver.find_element(By.XPATH, '//*[@id="main"]/footer/div[1]/div[2]/div/div[2]')
        global no_of_message
        for x in range(no_of_message):
            txt_box.send_keys(text)
            txt_box.send_keys("\n")

    except Exception as e:
        print("invailid phone no :" + str(phone_no))


for moblie_no in moblie_no_list:
    try:
        send_whatsapp_msg(moblie_no, message_text)

    except Exception as e:
        sleep(10)
        is_connected()

