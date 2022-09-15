import requests
import re
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
                for br in tds[1]('br'):  # replace all '<br>' with '\n' in command description
                    br.replace_with('\n')  # BeautifulSoup replace br with \n
                for br in tds[0]('br'):  # replace all '<br>' with '\n'
                    br.replace_with('/')  # BeautifulSoup replace br with \n in command
            except Exception as e:
                pass

            for i,td in enumerate(tds):
                #br_in_line = td.find_all('br')      # if <br/> in line(f.e. setoption behind the command as 2nd option), replace it with \n
                #if len(br_in_line) > 0:
                #    for br in br_in_line:
                #        br.replace_with('\n')
                if len(td.get_text().split()) == 1:             #  has only 1 word/cmd
                    title = table.find_previous_sibling('h3').get_text()
                    title = re.sub("[^0-9a-zA-Z]+", "", title)
                    cmd_list.setdefault(title, {})
                    #print(title, td.get_text())
                    cmd_list[title][td.get_text()] = tds[1].get_text()    # add cmd and descr to dict
    return cmd_list


#print(get_all_commands("https://tasmota.github.io/docs/Commands"))
#for key in cmd_list:
#    if cmd in cmd_list[key]:
#        print(key + ':\n' + cmd_list[key][cmd])