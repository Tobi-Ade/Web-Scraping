"""
importing necessary libraries 
"""
from bs4 import BeautifulSoup
import requests, openpyxl

"""
Creating excel file to save scraped data 
"""
excel = openpyxl.Workbook()
sheet = excel.active
sheet.title = "Top 5 players"
sheet.append(['Rank', 'Name', 'Club', 'Rating'])

"""
Scraping the data
"""
try:
    players = requests.get('https://one-versus-one.com/en/rankings')
    players.raise_for_status()

    soup = BeautifulSoup(players.text, 'lxml')

    data = soup.find('div', class_='pre-ad').find_all('a')
    
    for player in data:
        plays = player.find('div', class_='rankings-table-row')
        rank = plays.find('div', class_='rankings-table-cell number').text.split('#')[1].strip()
        name = plays.find('div', class_='rankings-table-cell info').find('div', class_='player-name rankings-table__player-name').text
        club = plays.find('div', class_='top-players-table__club').span.text
        rating = plays.find('div', class_='rankings-table-cell value rankings-table__value').text.strip()

        sheet.append([rank, name, club, rating])

except Exception as e:
    print(e)

"""
Saving the data to the excel file
"""
excel.save('Player Rankings.xlsx')
