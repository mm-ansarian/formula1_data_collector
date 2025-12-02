import requests
import datetime


print('\n\n\n')

print('=' * 25)
print('Formula 1 Data Collector') 
print('=' * 25)
print('Races')
print('-' * 25)

season = int(input(f'\nEnter a season from 1950 to {datetime.date.today().year}: '))

url = f'https://api.jolpi.ca/ergast/f1/{season}/races/'

response = requests.get(url)

print('\n\n')

result = (response.json())['MRData']['RaceTable']['Races']
for i in result:
    for key, value in i.items():
        if key == 'Circuit':
            circuit_name = value['circuitName']
            circuit_city = value['Location']['locality']
            circuit_country = value['Location']['country']
            print(f'{key}: {circuit_name}, {circuit_city}, {circuit_country}')
        elif key == 'FirstPractice' or key == 'SecondPractice' or key == 'ThirdPractice' or key == 'Qualifying':
            print(f'{key}: {value['date']}, {value['time']}')
        else:
            print(f'{key}: {value}')
    print('\n\n')

print('\n\n\n')
