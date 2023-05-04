import os

import requests
from bs4 import BeautifulSoup
import  json
import pandas as pd


url = "https://store.steampowered.com/search/?term=gta"

def getData(url):
    r = requests.get(url)
    return r.text

# processing data
def parse(data):
    result = []
    soup = BeautifulSoup(data, "html.parser")
    try:
        os.mkdir('json_result')
    except FileExistsError:
        pass

    contents = soup.find('div', attrs={'id': 'search_resultsRows'})
    games = contents.find_all('a')

    # print(contents)

    for game in games:
        link = game['href']

        # print(link)
        # parsing data
        title = game.find('span', attrs={'class': 'title'}).text.strip()
        price = game.find('div', attrs={'class': 'search_price'}).text.strip()
        released = game.find('div', attrs={'class': 'search_released'}).text.strip()
        if released == '':
            released = 'None'

        # sorting data
        data_dict = {
        'title': title,
        'price': price,
        'link': link,
        'released': released,
        }

        # append
        result.append(data_dict)
    return result

    # writing json
    with open('json_result.json', 'w') as outfile:
        json.dump(result, outfile)
    return result

    # read json
def loadData():
    with open('json_result.json') as json_file:
        data = json.load(json_file)

# Process cleaned data from parser
def output(datas: list):
    for i in datas:
        print(i)

def generateData(result, filename):
    df = pd.DataFrame(result)
    df.to_excel(f'{filename}.xlsx', index=False)



if __name__ == '__main__':
    data = getData(url)
    final_data = parse(data)
    namafile = input('masukkan nama file : ')
    generateData(final_data, namafile)
    output(final_data)