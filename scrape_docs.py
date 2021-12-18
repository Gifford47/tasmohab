import requests
import re, urllib
from bs4 import BeautifulSoup

def get_all_commands(url):
    page = requests.get(url)       # requests adds a '\' backslash at the end of the url->exception. why?
    if page.status_code != 200:
        return {}                                       # return empty dict
    soup = BeautifulSoup(page.content, 'html.parser')
    tables = soup.findAll("table")                   # BeautifulSoup find all 'table'
    cmd_list = {}

    for table in tables:
        lines = table.find_all('tr')                 # BeautifulSoup find 'tr'
        for line in lines:
            tds = line.find_all('td')              # BeautifulSoup find 'td' (zelle)
            try:
                for br in tds[1]('br'):  # replace all '<br>' with '\n'
                    br.replace_with('\n')  # BeautifulSoup replace br with \n
            except Exception as e:
                pass

            for i,td in enumerate(tds):
                if len(td.get_text().split()) == 1:             #  has only 1 word/cmd
                    title = table.find_previous_sibling('h3').get_text()
                    title = re.sub("[^0-9a-zA-Z]+", "", title)
                    cmd_list.setdefault(title, {})
                    cmd_list[title][td.get_text()] = tds[1].get_text()    # add cmd and descr to dict
    return cmd_list


#print(search_result)
#for key in cmd_list:
#    if cmd in cmd_list[key]:
#        print(key + ':\n' + cmd_list[key][cmd])