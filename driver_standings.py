from sys import exit
import datetime
import requests


def driver_standings_function():
    try: 
        print('\n\n\n')
        print('\033[1m' + 'Formula 1 Data Collector' + '\033[0m')
        print('Driver standings in the season')

        season = input(f'\nEnter the season(from 1950 to {datetime.date.today().year}): ') or datetime.date.today().year

        try:
            season = int(float(season))
        except:
            print('\n\n' + '\033[1m' + '\033[91m' + '!! Invalid input !!' + '\033[0m' + '\033[0m' + '\n\n\n')
            exit()
        else:
            if season < 1950 or season > datetime.date.today().year:
                print('\n\n' + '\033[1m' + '\033[91m' + '!! Input is out of the accepted range !!' + '\033[0m' + '\033[0m' + '\n\n\n')
                exit()

        print('\nCollecting data...')
        base = "https://api.jolpi.ca/ergast/f1"
        session = requests.Session()
        timeout = 10

        url = f"{base}/{season}/driverStandings.json"
        response = session.get(url, timeout=timeout)
        data = response.json()

        standings_lists = data.get('MRData', {}).get('StandingsTable', {}).get('StandingsLists', [])
        if not standings_lists:
            print('\n\n' + '\033[1m' + '\033[91m' + "!! Season hasn't begun yet !!" + '\033[0m' + '\n\n\n')
            exit()

        standings = standings_lists[0].get('DriverStandings', [])

        round_num = standings_lists[0].get('round', '0')
        podiums_data = {}

        try:
            bulk_url = f"{base}/{season}/results.json?limit=1000"
            bulk_resp = session.get(bulk_url, timeout=timeout)
            bulk_ok = bulk_resp.status_code == 200
            if bulk_ok:
                bulk_data = bulk_resp.json()
                races_all = bulk_data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
                if races_all:
                    for race in races_all:
                        for result in race.get('Results', []):
                            pos = result.get('position')
                            if pos in ('1', '2', '3'):
                                driver_id = result['Driver']['driverId']
                                podiums_data[driver_id] = podiums_data.get(driver_id, 0) + 1
                else:
                    raise ValueError("No races in bulk response")
            else:
                raise ValueError("Bulk request failed")
        except Exception:
            for round_i in range(1, int(round_num) + 1):
                try:
                    results_url = f"{base}/{season}/{round_i}/results.json"
                    results_response = session.get(results_url, timeout=timeout)
                    results_data = results_response.json()

                    if 'RaceTable' in results_data['MRData'] and 'Races' in results_data['MRData']['RaceTable']:
                        race = results_data['MRData']['RaceTable']['Races'][0]

                        for result in race['Results']:
                            driver_id = result['Driver']['driverId']
                            position = result['position']

                            if position in ['1', '2', '3']:
                                podiums_data[driver_id] = podiums_data.get(driver_id, 0) + 1
                except:
                    continue

        NATIONALITY = {
            'American':'USA','Australian':'AUS','British':'UK','Canadian':'CAN','Chinese':'CHN',
            'Danish':'DEN','Dutch':'NED','Finnish':'FIN','French':'FRA','German':'GER',
            'Italian':'ITA','Japanese':'JPN','Mexican':'MEX','Monegasque':'MON',
            'New Zealander':'NZL','Spanish':'ESP','Thai':'THA','Brazilian':'BRA','Austrian':'AUT',
            'Swiss':'SUI','Russian':'RUS','Belgian':'BEL','Swedish':'SWE','Polish':'POL',
            'Hungarian':'HUN','Indian':'IND','South African':'RSA','Argentine':'ARG',
            'Malaysian':'MAS','Portuguese':'POR','Czech':'CZE','Turkish':'TUR','Iranian':'IRI',
            'Saudi':'KSA','Emirati':'UAE','Qatari':'QAT','Bahraini':'BHR','Kuwaiti':'KWT',
            'Israeli':'ISR','Korean':'KOR','Singaporean':'SGP','Indonesian':'INA',
            'Philippine':'PHI','Norwegian':'NOR','Irish':'IRL','Ukrainian':'UKR','Greek':'GRE',
            'Romanian':'ROU','Bulgarian':'BUL','Nigerian':'NGA','Egyptian':'EGY','Kenyan':'KEN',
            'Moroccan':'MAR','Algerian':'ALG','Chilean':'CHI','Colombian':'COL','Venezuelan':'VEN',
            'Peruvian':'PER','Uruguayan':'URU','Liechtensteiner':'LIE','Monacan':'MON',
            'Andorran':'AND','Luxembourger':'LUX','Icelandic':'ISL','Croatian':'CRO','Serbian':'SRB',
            'Slovak':'SVK','Slovenian':'SLO','Estonian':'EST','Latvian':'LAT','Lithuanian':'LTU',
            'Maltese':'MLT','Cypriot':'CYP','Armenian':'ARM','Azerbaijani':'AZE','Georgian':'GEO',
            'Kazakh':'KAZ','Uzbek':'UZB','Pakistani':'PAK','Bangladeshi':'BAN','Sri Lankan':'SRI',
            'Nepalese':'NEP','Afghan':'AFG','Iraqi':'IRQ','Jordanian':'JOR','Lebanese':'LIB',
            'Syrian':'SYR','Yemeni':'YEM','Omani':'OMA','Tunisian':'TUN','Libyan':'LBY',
            'Sudanese':'SUD','Ethiopian':'ETH','Ghanaian':'GHA','Senegalese':'SEN','Cameroonian':'CMR',
            'Ivory Coast':'CIV','Angolan':'ANG','Mozambican':'MOZ','Zimbabwean':'ZIM','Zambian':'ZAM',
            'Botswanan':'BOT','Namibian':'NAM','Mauritian':'MRI','Cuban':'CUB','Jamaican':'JAM',
            'Haitian':'HAI','Dominican':'DOM','Puerto Rican':'PUR','Costa Rican':'CRC','Panamanian':'PAN',
            'Guatemalan':'GUA','Honduran':'HON','Salvadoran':'SLV','Nicaraguan':'NIC','Paraguayan':'PAR',
            'Bolivian':'BOL','Ecuadorian':'ECU','Guyanese':'GUY','Surinamese':'SUR','Fijian':'FIJ',
            'Papua New Guinean':'PNG','Tongan':'TON','Samoan':'SAM','Vanuatuan':'VAN'
        }

        print('\033[1m' + f'\n🏆 FORMULA 1 {season} DRIVER STANDINGS' + '\033[0m')
        try:
            schedule_url = f"{base}/{season}.json"
            schedule_resp = session.get(schedule_url, timeout=timeout)
            schedule_data = schedule_resp.json()
            races = schedule_data['MRData']['RaceTable']['Races']
            total_races = len(races)
            races_left = total_races - int(round_num)

            season_finished = races_left == 0

            MAX_POINTS_PER_RACE = 26

            champ_decided = False
            if not season_finished and len(standings) >= 2:
                p1 = int(float(standings[0]['points']))
                p2 = int(float(standings[1]['points']))
                max_possible_p2 = p2 + (races_left * MAX_POINTS_PER_RACE)

                if p1 > max_possible_p2:
                    champ_decided = True
        except:
            season_finished = False
            champ_decided = False

        if standings:
            champ = standings[0]
            given = champ['Driver']['givenName']
            family = champ['Driver']['familyName']
            if len(given.split(' ')) == 2:
                champ_name = f"{list(given.split(' '))[0][0]}.{list(given.split(' '))[1][0]}. {family}"
            else:
                champ_name = f"{list(given.split(' '))[0][0]}. {family}"
            champ_team = champ['Constructors'][0]['name'] if champ.get('Constructors') else ''

            if season_finished:
                print(f"{'\033[1m' + '🎯 Season:' + '\033[0m'} {season}(Finished)")
                print(f"{'\033[1m' + '🏁 Champion:' + '\033[0m'} {champ_name}({champ_team})")
            elif champ_decided:
                print(f"{'\033[1m' + '🎯 Season:' + '\033[0m'} {season}(Champion Decided)")
                print(f"{'\033[1m' + '🏁 Champion:' + '\033[0m'} {champ_name}({champ_team})")
            else:
                print(f"{'\033[1m' + '🎯 Season:' + '\033[0m'} {season}(Ongoing)")
                print("\033[1m" + "🏁 Champion not decided yet." + "\033[0m")

        print("\033[1m" +"📊 Rounds: " + "\033[0m" + round_num) if int(round_num) > 1 else "\033[1m" +"📊 Round: " + "\033[0m" + round_num
        print(('\033[1m' + '=' + '\033[0m') * 88)
        print(f"{'\033[1m'}{'Pos':<5} {'Driver(Nationality)':<28} {'Team':<25} {'Points':<10} {'Wins':<7} {'Podiums':<8} {'\033[0m'}")
        print(('\033[1m' + '-' + '\033[0m') * 88)

        for driver in standings:
            try:
                pos = driver['position']
            except:
                break
            driver_id = driver['Driver']['driverId']

            if len(driver['Driver']['givenName'].split(' ')) == 2:
                name = f"{list(driver['Driver']['givenName'].split(' '))[0][0]}.{list(driver['Driver']['givenName'].split(' '))[1][0]}. {driver['Driver']['familyName']}"
            else:
                name = f"{list(driver['Driver']['givenName'].split(' '))[0][0]}. {driver['Driver']['familyName']}"

            nationality = driver['Driver']['nationality']
            nat_code = NATIONALITY.get(nationality, nationality[:3].upper())

            team = driver['Constructors'][0]['name']
            points = int(float(driver['points']))
            wins = driver['wins']

            podiums = podiums_data.get(driver_id, 0)

            driver_with_nat = f"{name}({nat_code})"

            print(f"{pos:<2}    {driver_with_nat:<28} {team:<26} {points:<10} {wins:<2} {podiums:>8}")

        print(('\033[1m' + '=' + '\033[0m') * 88)
        print('\n\n\n')
    except:
        print('\n\n' + '\033[1m' + '\033[91m' + "!! Something went wrong; that's all we know !!" + '\033[0m' + '\033[0m' + '\n\n\n')


if __name__ == '__main__':
    driver_standings_function()
