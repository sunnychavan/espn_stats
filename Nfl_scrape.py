import requests
from bs4 import BeautifulSoup as bs
import numpy as np
import pandas as pd


def pull_espn_data(year, offense = True):
    link = "https://www.espn.com/nfl/stats/team/_/view/"
    yr = str(year)
    if offense == True:
        type = "offense"
    else:
        type = "defense"
    link = link + type + "/" + "season/" + yr + "/seasontype/2"
    req = requests.get(link)
    soup = bs(req.text, "lxml")
    ts = soup.body.find("div", class_ = "Table__ScrollerWrapper relative overflow-hidden").find("div", class_ = "Table__Scroller")#find("table").find('thead').find('tr', class_ = "Table__sub-header Table__TR Table__even").th
    ts1 = ts.find('tr', class_ = "Table__sub-header Table__TR Table__even")

    '''Headers for dataframe'''
    headers = []
    team_head = soup.body.find('thead', class_ = 'Table__header-group Table__THEAD').find('tr', class_ = 'Table__sub-header Table__TR Table__even').span.div.text
    headers.append(team_head)
    for x in ts1.find_all('th', class_ = "Table__TH"):
        headers.append(x.span.a.text)

    '''Saving Team names in a list'''
    team_names = []
    for tr in soup.body.find('tbody', class_ = 'Table__TBODY').find_all('tr', class_ = "Table__TR Table__TR--sm Table__even"):
        #team_names.append(tr.td.div.children)Z
        list_of_children = list(tr.td.div.children)
        if(list_of_children[-1].name != "a"):
            team_names.append(list_of_children[-1])
        else:
            team_names.append(list_of_children[-1].text)

    '''Data for dataframe'''
    matrix = []
    ts2 = ts.find('tbody', class_ = 'Table__TBODY')
    for q in ts2.find_all('tr', class_ = "Table__TR Table__TR--sm Table__even"):
        if len(team_names) != 0:
            matrix.append(team_names.pop(0))
        for p in q.find_all("td", class_ = 'Table__TD'):
            matrix.append(p.div.text)

    matrix_new = np.reshape(matrix, (32, -1))
    df = pd.DataFrame(columns = headers, data = matrix_new)
    print(df)


year = input("Enter year: ")
type = str(input("Enter Offense of Defense: "))

if type.lower() == "offense":
    is_offense = True
else:
    is_offense = False

pull_espn_data(year, is_offense)






#for x in table_h.find_all("th"):
    #x.find("span", class_ = "underline").find("a", class_ = "AnchorLink clr-gray-01").text
