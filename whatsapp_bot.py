from selenium import webdriver
import time
from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from urllib.request import urlretrieve

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


def converte_json(cards):
    gravar = ""
    for infos in cards:
        gravar = gravar + infos['cardBody'] + 'Acesse o site ====>' + infos['link'] + '\n'
        # gravar = gravar + infos['cardBody'] + '\nPreco: ' + infos['value'] + '\nAcesse o site: ' + infos['link']
    return gravar


class WhatsappBot:
    def __init__(self):
        # Parte 1 - A mensagem que você quer enviar
        self.mensagem = converte_json(cards)
        # "Boa noite pessoal, veja o video que acabou de sair https://www.youtube.com"
        # Parte 2 - Nome dos grupos ou pessoas a quem você deseja enviar a mensagem
        self.grupos_ou_pessoas = ["Coisas"]
        options = webdriver.ChromeOptions()
        options.add_argument('lang=pt-br')
        self.driver = webdriver.Chrome(
            executable_path=r'./chromedriver.exe', chrome_options=options)

    def EnviarMensagens(self):
        self.driver.get('https://web.whatsapp.com/')
        time.sleep(30)
        for grupo_ou_pessoa in self.grupos_ou_pessoas:
            campo_grupo = self.driver.find_element_by_xpath(
                f"//span[@title='{grupo_ou_pessoa}']")
            time.sleep(3)
            campo_grupo.click()
            chat_box = self.driver.find_element_by_class_name('_3uMse')
            time.sleep(3)
            chat_box.click()
            chat_box.send_keys(self.mensagem)
            botao_enviar = self.driver.find_element_by_xpath(
                "//span[@data-icon='send']")
            time.sleep(3)
            botao_enviar.click()
            time.sleep(5)


bot = WhatsappBot()
bot.EnviarMensagens()

# <span dir="auto" title="Coisas" class="_3ko75 _5h6Y_ _3Whw5">Coisas</span>
# <div tabindex="-1" class="_3uMse">
# <span data-icon="send" class="">
# _3uMse
# Eduardo é foda 🇧🇷
