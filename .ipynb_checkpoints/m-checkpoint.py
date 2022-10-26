from dataclasses import dataclass
from bs4 import BeautifulSoup
import requests, openpyxl

excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Top 5 players"
sheet.append(['Rank', 'Name', 'Club', 'Rating'])

try:
    players = requests.get('https://one-versus-one.com/en/rankings')
    players.raise_for_status()

    soup = BeautifulSoup(players.text, 'lxml')

    data = soup.find('div', class_='pre-ad').find_all('a')
    
    for player in data:
        play = player.find('div', class_='rankings-table-row')
        rank = play.find('div', class_='rankings-table-cell number').text.split('#')[1].strip()
        name = play.find('div', class_='rankings-table-cell info').find('div', class_='player-name rankings-table__player-name').text
        club = play.find('div', class_='top-players-table__club').span.text
        rating = play.find('div', class_='rankings-table-cell value rankings-table__value').text.strip()

        sheet.append([rank, name, club, rating])

except Exception as e:
    print(e)

excel.save('Player Rankings.xlsx')
