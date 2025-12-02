import datetime
import requests


print('\n\n\n')
print('Formula 1 Data Collector')
print('Collecting data...')

season = datetime.date.today().year
url = f"https://api.jolpi.ca/ergast/f1/{season}/driverStandings.json"

response = requests.get(url)
data = response.json()
standings = data['MRData']['StandingsTable']['StandingsLists'][0]['DriverStandings']

round_num = data['MRData']['StandingsTable']['StandingsLists'][0]['round']
podiums_data = {}

for round_i in range(1, int(round_num) + 1):
    try:
        results_url = f"https://api.jolpi.ca/ergast/f1/{season}/{round_i}/results.json"
        results_response = requests.get(results_url)
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

print(f"\n🏆 FORMULA 1 {season} DRIVER STANDINGS")
print(f"🎯 Season: {season}")
print("📊 Round: " + round_num)
print("=" * 88)
print(f"{'Pos':<5} {'Driver(Nationality)':<28} {'Team':<20} {'Points':<8} {'Wins':<6} {'Podiums':<8}")
print("-" * 88)

for driver in standings:
    pos = driver['position']
    driver_id = driver['Driver']['driverId']
    
    if len(driver['Driver']['givenName'].split(' ')) == 2:
        name = f"{list(driver['Driver']['givenName'].split(' '))[0][0]}.{list(driver['Driver']['givenName'].split(' '))[1][0]}. {driver['Driver']['familyName']}"
    else:
        name = f"{list(driver['Driver']['givenName'].split(' '))[0][0]}. {driver['Driver']['familyName']}"
    
    nationality = driver['Driver']['nationality']
    nat_code = NATIONALITY.get(nationality, nationality[:3].upper())
    
    team = driver['Constructors'][0]['name']
    points = driver['points']
    wins = driver['wins']
    
    podiums = podiums_data.get(driver_id, 0)
    
    driver_with_nat = f"{name}({nat_code})"
    
    print(f"{pos:<2}    {driver_with_nat:<28} {team:<20} {points:>8} {wins:>6} {podiums:>8}")

print("=" * 88)
print('\n\n\n')
