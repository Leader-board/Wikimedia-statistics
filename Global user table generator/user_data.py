from os import listdir
import requests
import pandas as pd
import math
import csv
from scipy import stats
import json
from urllib.request import urlopen
import re


def parse_json(list_loc):
    """
    Goal: go to the location in list_loc and use a JSON parser to parse the contents of that page
    https://www.geeksforgeeks.org/how-to-read-a-json-response-from-a-link-in-python/
    """
    url = list_loc
    response = urlopen(url)
    data_json = json.loads(response.read())
    part2 = json.loads(data_json['parse']['wikitext'])['targets']  # as json can't otherwise go that deep
    number_of_pages = len(part2)  # number of users to send to
    for i in range(0, number_of_pages, 1):
        page_name = part2[i]['title']
        # get the username
        user_name = re.split('[:\/]', page_name)[
            1]  # https://stackoverflow.com/questions/4998629/split-string-with-multiple-delimiters-in-python
        # and run the analysis there
        push_to_wiki(page_name, analyse_user(user_name, '/statdata'))


# input to function: a user
def percentile_and_user_count(username, fileloc, rankinc):
    # fileloc - absolute location to file
    if rankinc:
        df = pd.read_csv(fileloc, on_bad_lines='skip', sep='|', quoting=csv.QUOTE_NONE)
    else:
        df = pd.read_csv(fileloc, on_bad_lines='skip', sep='\t', quoting=csv.QUOTE_NONE)
    # we now have dataframe
    # get user details via linear search
    df_user = df[df['Username'] == username]
    if len(df_user.index) == 0:
        return 0, len(df), 0
    rank = df_user['Rank'].item()
    usercount = df_user['Edits'].item()
    percentile = stats.percentileofscore(df, usercount, kind='strict')
    return usercount, rank, percentile


def header_data(username):
    return "{{| class=\"wikitable sortable\"\n|+ {} global rank data\n|-\n! Wiki name !! Number of edits !! Approximate rank !! Percentile\n".format(
        username)


def convert_to_string(wikiname, usercount, rank, percentile):
    toprint = '|-\n|' + wikiname + '||' + str(usercount) + '||' + str(rank) + '||' + str(percentile) + '\n|-\n'
    return toprint


def analyse_user(username, folderloc):
    oldloc = folderloc
    folderloc = oldloc + "/processed_csv"
    files = listdir(folderloc)
    percentile_toprint = header_data(username)
    for f in files:
        filename = folderloc + "/" + str(f)
        # print it the same way
        page_name = str(f)[:-4]
        print(filename)
        # for each file, what do we want? 
        # we want the user's percentile and edit count for each wiki
        if 'global' in page_name:
            usercount, rank, percentile = percentile_and_user_count(username, filename, True)
        else:
            usercount, rank, percentile = percentile_and_user_count(username, filename, False)
        # prepare for printing
        if usercount != 0:
            percentile_toprint += convert_to_string(page_name, usercount, rank, percentile)

    # virtually duplicated code to handle the other folder; can be refactored
    folderloc = oldloc + "/rawcsv"
    files = listdir(folderloc)
    for f in files:
        filename = folderloc + "/" + str(f)
        # print it the same way
        page_name = str(f)[:-4]
        print(filename)
        # for each file, what do we want? 
        # we want the user's percentile and edit count for each wiki
        percentile = 0
        if 'global' in page_name:
            usercount, rank, percentile = percentile_and_user_count(username, filename, True)
        else:
            usercount, rank, percentile = percentile_and_user_count(username, filename, False)
        # prepare for printing
        if percentile != 0:
            percentile_toprint += convert_to_string(page_name, usercount, rank, percentile)
    percentile_toprint += '|}\n\n'
    return percentile_toprint


def push_to_wiki(username, string_to_print):
    S = requests.Session()

    f = open("/statdata/botdetails.txt", "r")
    filecont = f.read().splitlines()
    f.close()
    print(filecont)
    if (len(filecont) != 4):
        print("The botdetails file is not in the expected format")
        return
    URL = filecont[0]
    # Step 1: GET request to fetch login token
    PARAMS_0 = {
        "action": "query",
        "meta": "tokens",
        "type": "login",
        "format": "json"
    }
    # URL = r'https://meta.wikimedia.org/w/api.php'
    R = S.get(url=URL, params=PARAMS_0)
    DATA = R.json()

    LOGIN_TOKEN = DATA['query']['tokens']['logintoken']

    # Step 2: POST request to log in. Use of main account for login is not
    # supported. Obtain credentials via Special:BotPasswords
    # (https://www.mediawiki.org/wiki/Special:BotPasswords) for lgname & lgpassword
    PARAMS_1 = {
        "action": "login",
        "lgname": filecont[1],
        "lgpassword": filecont[2],
        "lgtoken": LOGIN_TOKEN,
        "format": "json"
    }

    R = S.post(URL, data=PARAMS_1)

    # Step 3: GET request to fetch CSRF token
    PARAMS_2 = {
        "action": "query",
        "meta": "tokens",
        "format": "json"
    }

    R = S.get(url=URL, params=PARAMS_2)
    DATA = R.json()

    CSRF_TOKEN = DATA['query']['tokens']['csrftoken']
    PARAMS_3 = {
        "action": "edit",
        "title": username,
        "token": CSRF_TOKEN,
        "format": "json",
        "text": string_to_print,
        "bot": 'true'
    }
    R = S.post(URL, data=PARAMS_3)
    DATA = R.json()

    print(DATA)


def main():
    parse_json(
        r'https://meta.wikimedia.org/w/api.php?action=parse&formatversion=2&page=Global+statistics/Mailing+list&prop=wikitext&format=json')
    # push_to_wiki('Martin Urbanec', analyse_user('Martin Urbanec', '/statdata'))


main()
