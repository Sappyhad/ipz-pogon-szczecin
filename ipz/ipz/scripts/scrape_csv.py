import requests
from bs4 import BeautifulSoup
import os
from django.conf import settings

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
        for i in range(1, weeks+1):
            zip_name = f'zip{i}.zip'
            zip_path = os.path.join(base_dir, 'ipz' , 'zips', zip_name)
            print(zip_path)
            download_request = session.get(f'https://portal.tracab.com/download/week/{i}/240/Default%202021', allow_redirects=True)
            open(zip_path, 'wb').write(download_request.content)

#scrapeTracab('p.jasinski@pogonszczecin.pl', 'Password')