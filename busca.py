from bs4 import BeautifulSoup
from urllib.request import urlopen
import pandas as pd
from urllib.request import urlretrieve


#busca = input('Digite o nome da cerveja:')
#url = 'https://www.buscape.com.br/search?q={0}'.format(busca)
url = 'https://www.buscape.com.br/search?q=cerveja+heineken'
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36'}
response  = urlopen(url)
html = response.read()
soup = BeautifulSoup(html, 'html.parser')

cards = []


anuncios = soup.find('div',{'id':'pageSearchResultsBody'}).findAll('div', class_="card card--offer card--cpc")
for anuncio in anuncios:
	#print(str(anuncio) + "\n\n")
	card = {}

	for info in anuncio:
		anuncio.find('span',{'class':'mainValue'}).getText()
		card['value'] = anuncio.find('span',{'class':'mainValue'}).getText()
		

		card[info.get('class')[0].split('-')[-1]] = info.get_text()
		anuncio.find('div',{'class':'cardFooter'}).find('a').get('href')
		card['link'] ='https://www.buscape.com.br/' + anuncio.find('div',{'class':'cardFooter'}).find('a').get('href')

		


		#dataset = pd.DataFrame.from_dict(card, orient = 'index').T
		#dataset.to_csv('./resultado_final/trigueiro.csv',sep=';', encoding='utf-8-sig')
		

	cards.append(card)
	#image = anuncio.find('a', {'class':'cardImage'}).img
	#urlretrieve(image.get('src'),'./resultado_final/imagem/' + image.get('src').split('/')[-1])
  


dataset = pd.DataFrame(cards)
#dataset = pd.DataFrame.from_dict(cards, orient = 'index').T
dataset.to_csv('./info/dados/fil.csv',sep=';', encoding='utf-8-sig')  	
#print(dataset)