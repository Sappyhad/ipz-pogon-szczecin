import requests
from bs4 import BeautifulSoup
import os, shutil
from django.conf import settings
import pandas as pd
import zipfile
from googlesearch import search
import time

def get_transfermarkt_url(player_name):
    try:
        first_name = player_name.split(" ")[0]
        second_name = player_name.split(" ")[1]
        request_url = f'https://www.transfermarkt.pl/schnellsuche/ergebnis/schnellsuche?query={first_name}+{second_name}'
    except:
        request_url = f'https://www.transfermarkt.pl/schnellsuche/ergebnis/schnellsuche?query={player_name}'
    #print(request_url)
    r = requests.get(request_url, headers = {'User-agent': 'your bot 0.1'})
    #print(r.text)
    try:
        soup = BeautifulSoup(r.text, 'html.parser')
        td = soup.find('td', {'class': 'hauptlink'})
        link = td.findChildren('a', recursive=False)[0]['href']
        ret_link = 'https://www.transfermarkt.pl'+link
    except:
        ret_link = 'nie udało się znaleźć linku'
    return ret_link

def scrapeTracab(username: str, password: str, base_dir):
    request_url = 'https://portal.tracab.com/login'
    with requests.Session() as session:
        get_url = session.get(request_url)
        HTML = BeautifulSoup(get_url.text, 'html.parser')
        csrfmiddlewaretoken = HTML.find_all('input')[0]['value']
        print(csrfmiddlewaretoken)
        payload = {
            'identity': username,
            'password': password,
            'csrf_test_name': csrfmiddlewaretoken
        }
        headers = {
            'Referer': request_url
        }
        login_request = session.post(request_url,payload, headers=headers)
        league_results = session.get('https://portal.tracab.com/user/results/Ekstraklasa/2021')
        HTML = BeautifulSoup(league_results.text, 'html.parser')
        weeks = HTML.find_all('a', {'class': 'mwTabs'})[0]['data-mw']
        print(weeks)
        for i in range(1, int(weeks)+1):
            zip_name = f'zip{i}.zip'
            zip_path = os.path.join(base_dir, 'ipz' , 'zips', zip_name)
            print(zip_path)
            download_request = session.get(f'https://portal.tracab.com/download/week/{i}/240/Default%202021', allow_redirects=True)
            open(zip_path, 'wb').write(download_request.content)

def concatenate_csvs(base_dir):
    zip_dir = os.path.join(base_dir,'ipz','zips')
    csv_path = os.path.join(base_dir, 'csvs', 'Tracab_Data_Concatenated.csv')
    zip_contents = os.path.join(base_dir, 'ipz', 'zip_contents')
    #tworzenie pustego pliku finalnego
    with open(csv_path, 'w'):
        pass
    #iteracje po tych zipach zajebanych
    for filename in os.listdir(zip_dir):
        filename_path = os.path.join(zip_dir, filename)
        #iterowanie po folderze z zipami
        with zipfile.ZipFile(filename_path) as zip_file:
            #otworzenie danego zipa
            for name in zip_file.namelist():
                #unzipowanie potrzebnych plików
                if name.split("_")[-2] == "Summary" or name.split("_")[-2] == "Splits":
                    zip_file.extract(name, path=zip_contents)
        #przetwarzanie zip_contents - wejdź w folder, zajmij się plikami w nim, w między czasie usuń te niepotrzebne
        for dir in os.listdir(zip_contents):
            dir_path = os.path.join(zip_contents, dir)
            for csv in os.listdir(dir_path):
                #print(csv)
                if csv.split("_")[-2] == "Summary":
                    zip_csv_path = os.path.join(dir_path,csv)
                    #print(zip_csv_path)
                    game_id = csv.split("_")[0]
                    df = pd.read_csv(zip_csv_path, skiprows=9)
                    delimiter = df.loc[df['ID']=='ID'].index[0]
                    df_t1 = df[:delimiter]
                    df_t2 = df[delimiter+1:]
                    df_t1 = df_t1.drop('ID', axis=1)
                    df_t2 = df_t2.drop('ID', axis=1)
                    document_name = csv.split("_")
                    document_name[-2] = "Splits"
                    splits_csv = "_".join(document_name)
                    splits_csv_path = os.path.join(dir_path,splits_csv)
                    with open(splits_csv_path, 'r', encoding='utf8') as file:
                        lines = file.readlines()
                        druzyny = lines[1].replace("\"", "")
                        druzyny = druzyny.replace("\n", "")
                        #print(druzyny)
                    team1 = druzyny.split(" vs ")[0]
                    team2 = druzyny.split(" vs ")[1]
                    df_t1['team'] = team1
                    df_t2['team'] = team2
                    #tu jeszcze trzeba dodać ten transfermarkt zajebany
                    # df_t1['transfermarkt'] = df_t1['Player'].apply(get_transfermarkt_url)
                    # df_t2['transfermarkt'] = df_t2['Player'].apply(get_transfermarkt_url)
                    df_t1.to_csv(csv_path, mode='a', header=False, index=False)
                    df_t2.to_csv(csv_path, mode='a', header=False, index=False)

        #usuwanie wszystkiego w zip_contents
        for f in os.scandir(zip_contents):
            path = os.path.join(zip_contents,f)
            shutil.rmtree(path)

#dodaj funkcję która do finalnego pliku dodaje linki do transfermarkt: wyszukuje unikalne wartości nazwy zawodnika i wtedy szuka mu linka do transfermarktu,
# następnie wkleja do każdego jego wystąpienia ten link - trzeba to zrobić bo wpływa za dużo requestów i wywala błąd http

def add_transfermarkt(base_dir):
    csv_path = os.path.join(base_dir, 'csvs', 'Tracab_Data_Concatenated.csv')
    df = pd.read_csv(csv_path, header=None)
    unique_players = df.iloc[:, 0].unique()
    # for i in unique_players:
    #     print(i)
    df[df.shape[1]] = ""
    for i in unique_players:
        transfermarkt_url = get_transfermarkt_url(i)
        df.loc[df.iloc[:, 0] == i, df.columns[-1]] = transfermarkt_url
        #time.sleep(1)
        print(i)
        #print(df)
    df.to_csv(csv_path, sep=';', decimal=',', encoding='utf-8', index=False, header=False)

#scrapeTracab('p.jasinski@pogonszczecin.pl', 'Password')
#print(get_transfermarkt_url("piotr wlazło"))