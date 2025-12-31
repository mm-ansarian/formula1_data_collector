from sys import exit
import datetime
import requests


def races_data_function():
    def format_key(key):
        return key[0] + ''.join((' ' + ch.lower()) if ch.isupper() else ch for ch in key[1:])
    try:
        print('\n\n\n')
        print('\033[1m' + 'Formula 1 Data Collector' + '\033[0m')
        print('Races data')

        season = input(f'\nEnter the season(from 1950 to {datetime.date.today().year}): ') or datetime.date.today().year

        try:
            season = int(float(season))
        except Exception:
            print('\n\n' + '\033[1m' + '\033[91m' + '!! Invalid input !!' + '\033[0m' + '\033[0m' + '\n\n\n')
            exit()

        if season < 1950 or season > datetime.date.today().year:
            print('\n\n' + '\033[1m' + '\033[91m' + '!! Input is out of the accepted range !!' + '\033[0m' + '\033[0m' + '\n\n\n')
            exit()

        print('\nCollecting data...')
        url = f'https://api.jolpi.ca/ergast/f1/{season}/races/'
        response = requests.get(url)

        print('\033[1m' + '\n\nRaces\n\n' + '\033[0m')

        races = response.json()['MRData']['RaceTable']['Races']
        PRACTICE_KEYS = {
            'FirstPractice', 'SecondPractice', 'ThirdPractice', 'Qualifying',
            'Sprint', 'SprintShootout', 'SprintQualifying'
        }

        for race in races:
            race_url = race.get('url')
            for key, value in race.items():
                if key == 'url':
                    race_url = value

                elif key == 'Circuit':
                    circuit_name = value.get('circuitName')
                    loc = value.get('Location', {})
                    circuit_city = loc.get('locality')
                    circuit_country = loc.get('country')
                    print(f'{"\033[1m" + key}: {"\033[0m" + circuit_name}, {circuit_city}, {circuit_country}')

                elif key == 'raceName':
                    print(f'{"\033[1m" + "Race name:"} {"\033[0m" + value}')

                elif key in PRACTICE_KEYS:
                    d = value.get('date').split('-')
                    d.reverse()
                    print(f'{"\033[1m" + format_key(key)}: {"\033[0m" + "/".join(d)}, {value.get("time")[:-4]}')

                elif key == 'date':
                    d = value.split('-')
                    d.reverse()
                    print(f'{"\033[1m" + "Date:"} {"\033[0m" + "/".join(d)}')

                elif key == 'time':
                    print(f'{"\033[1m" + "Time:"} {"\033[0m" + value[:-4]}')

                else:
                    print(f'{"\033[1m" + key.capitalize()}: {"\033[0m" + value}')

            if race_url:
                print(f'{"\033[1m" + "URL:"} {"\033[0m" + race_url}')

            print('\n')

        print('\n')
    except:
        print('\n\n' + '\033[1m' + '\033[91m' + "!! Something went wrong; that's all we know !!" + '\033[0m' + '\033[0m' + '\n\n\n')


if __name__ == '__main__':
    races_data_function()
