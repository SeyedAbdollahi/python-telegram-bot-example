import requests
import re
from bs4 import BeautifulSoup
import jdatetime
import re
import sys
sys.path.insert(0, './Database')
import database

baseURL = 'http://www.tgju.org/'
rial = ' واحد پول به ریال می باشد.'
dollar = ' واحد پول به دلار آمریکا می باشد.'

# add data to events.log file
def add_event_log(action, url):
    log = 'Action: [%s], url: [%s]' % (action, url)
    database.insert_log(log)

# check change rate
def change_rate(result_regex):
    if result_regex == '':
        return ''
    elif result_regex == 'high':
        return ' ⬆'
    elif result_regex == 'low':
        return ' ⬇'

def add_rate_to_text(soup):
    rates = re.findall(r'</strong><span class=\"(.*)\">', str(soup))
    text = soup.text.splitlines()
    count = 0
    result = str()
    for line in text:
        if count is 4:
            result += line + change_rate(rates[0]) + '\n'
        elif count is 5:
            result += line + change_rate(rates[1]) + '\n'
        elif count is 9:
            result += line + change_rate(rates[2]) + '\n'
        elif count is 10:
            result += line + change_rate(rates[3])
        else:
            result += line + '\n'
        count += 1
    return result

def get18k():
    url = baseURL + 'chart/geram18'
    soup = get_soup_from_html_request(url)
    gold18k_soup = soup.find('ul', attrs={'class': 'data-line float-right float-half'})
    result = '🔹' + rial + '\n' + '___ قیمت طلا 18 عیار ___' + add_rate_to_text(gold18k_soup)
    return result

def get24k():
    url = baseURL + 'chart/geram24'
    soup = get_soup_from_html_request(url)
    gold24k_soup = soup.find('ul', attrs={'class': 'data-line float-right float-half'})
    result = '🔹' + rial + '\n' + '___ قیمت طلا 24 عیار ___' + add_rate_to_text(gold24k_soup)
    return result

def get_ons():
    url = baseURL + 'chart/ons'
    soup = get_soup_from_html_request(url)
    ons_soup = soup.find('ul', attrs={'class': 'data-line float-right float-half'})
    result = '🔹' + dollar + '\n' + '___ قیمت انس طلا ___' + add_rate_to_text(ons_soup)
    return result

def get_soup_from_html_request(url):
    add_event_log('getHTML', url)
    html_request = requests.get(url)
    return BeautifulSoup(html_request.text, 'html.parser')
