from os import listdir
import requests
import pandas as pd
import math
import csv
import mysql.connector
from iso639 import Lang


def header_data(wikiname):
    return "{{| class=\"wikitable sortable\"\n|+ {} user rank data\n|-\n! Rank !! Username !! Registration date !! Number of edits\n".format(
        wikiname)


def header_data_percentile(wikiname):
    return "{{| class=\"wikitable sortable\"\n|+ {} percentile data\n|-\n! Percentile !! Number of edits\n".format(
        wikiname)


def convert_to_string(fileloc, rankinc, wiki_name=None):
    # wiki_name not required for global_contribs
    # input: a file
    # folder_loc = '/statdata/rawdata'
    # files = listdir(folder_loc) # get list of files
    # for f in files:
    #     filename = folder_loc + '/' + f
    #     fname = open(filename, "r+")
    limit = 80000000
    if rankinc:
        df = pd.read_csv(fileloc, nrows=limit, on_bad_lines='skip', sep='|', quoting=csv.QUOTE_NONE)
    else:
        df = pd.read_csv(fileloc, nrows=limit, on_bad_lines='skip', sep='\t', quoting=csv.QUOTE_NONE)
    # take the first N rows
    toprint = ''
    ptr = 0
    ecount = 0
    rank = 0
    for i in df.values:
        if ptr >= limit or (ptr >= 39500 and len(toprint.encode('utf-8')) > 2096360):
            break
        row = i.tolist()
        number_of_edits = row[len(row) - 1]
        if number_of_edits != ecount:
            # update rank
            rank = (ptr + 1)
            ecount = number_of_edits
        if number_of_edits == 0:
            break  # no point proceeding from here
        toprint = toprint + '|-\n|'
        # if we have only three rows
        if not rankinc:
            # then add rank for us
            toprint = toprint + str(rank) + '||'
        for j in range(0, len(row), 1):
            #         if (str(row[j]).isdecimal() and j == len(row) - 2):
            #            row[j] = int(row[j])
            if str(row[j]) != 'nan' and isinstance(row[j], float):
                toprint = toprint + str(int(row[j]))
            elif str(row[j]) != 'nan':
                toprint = toprint + str(row[j])
            if j < len(row) - 1:
                toprint = toprint + '||'

        toprint = toprint + '\n|-\n'
        ptr = ptr + 1

    toprint = toprint + '|}\n' + add_categories(wiki_name) if wiki_name is not None else ''
    if rankinc:
        print(f"first 1000 chars of global: {toprint[:1000]}")

    return toprint, df


def add_categories(wiki_name):
    # input is something like 'enwiki', 'mlwikisource'
    # find the language
    cnx = mysql.connector.connect(option_files='/root/replica.my.cnf', host='meta.analytics.db.svc.wikimedia.cloud', database='meta_p')
    # get the global table
    cursor = cnx.cursor()
    query = ("SELECT dbname, lang, family from wiki")
    cursor.execute(query)
    res = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    wiki_family = res[res['dbname'] == wiki_name]['family']
    if wiki_family == 'special':
        # not a content wiki
        return ''
    wiki_lang = res[res['dbname'] == wiki_name]['lang']
    full_lang_name = Lang(wiki_lang).name

    category_name = f"{full_lang_name} {wiki_family.capitalize()}"

    # now check whether this category exists in meta-wiki

    r = requests.head(f"https://meta.wikimedia.org/wiki/Category:{category_name}")
    if r.ok:
        return f"[[Category:{category_name}]]"
    else:
        return ''


def remove_trailing_zeros(string):
    # 5.4400 should be 5.44
    # https://bobbyhadz.com/blog/python-remove-trailing-zeros-from-decimal
    return string.rstrip('0').rstrip('.') if '.' in string else string


def convert_to_string_percentile(percentile, edits, wikiname):
    toprint = ''
    for i in range(0, len(percentile), 1):
        toprint = toprint + '|-\n|' + remove_trailing_zeros(str(percentile[i])) + '||' + remove_trailing_zeros(str(edits[i])) + '\n|-\n'
    toprint = toprint + '|}\n\n'
    return header_data_percentile(wikiname) + toprint


def get_percentile_data(dframe, wikiname):
    # What this does: takes in a dataframe and outputs percentile data
    # edit_count is the last column
    ptr = 0.000000000
    old_bound = -1
    percentile = []
    edits = []
    while ptr <= 1.0000001:
        bound = math.floor(dframe.iloc[:, len(dframe.columns) - 1].quantile(min(ptr, 1)))
        if bound != old_bound:
            old_bound = bound
            percentile.append(round(100 * min(ptr, 1), 5))
            edits.append(bound)
        if ptr < 0.65:
            ptr = ptr + 0.1  # 10%
        elif ptr < 0.97:
            ptr = ptr + 0.01  # 1%
        elif ptr < 0.99:
            ptr = ptr + 0.001  # 0.1%
        else:
            ptr = ptr + 0.0001  # 0.01%
    return convert_to_string_percentile(percentile, edits, wikiname)


def local_wiki_processing(folderloc):
    # process all local wiki data
    files = listdir(folderloc)
    percentile_toprint = ''
    for f in files:
        filename = folderloc + "/" + str(f)
        # print it the same way
        page_name = str(f)[:-4]
        print("Currently processing: {}".format(page_name))
        tp, dframe = convert_to_string(filename, False, str(f))
        toprint = header_data(page_name) + tp
        # and push it to an appropriate place on the wiki
        push_to_wiki('Rank data/' + page_name, toprint)
       # print(toprint)
        percentile_toprint = percentile_toprint + '=={}==\n\n'.format(page_name)
        percentile_toprint = percentile_toprint + get_percentile_data(dframe, page_name)
    return percentile_toprint


def push_to_wiki(page_name, string_to_print):
    S = requests.Session()

    f = open("../../botdetails.txt", "r")
    filecont = f.read().splitlines()
    f.close()
    if len(filecont) != 4:
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

    # Step 4: POST request to edit a page
    PARAMS_3 = {
        "action": "edit",
        "title": 'Global statistics/' + page_name,
        "token": CSRF_TOKEN,
        "format": "json",
        "text": string_to_print,
        "bot": 'true'
    }

    R = S.post(URL, data=PARAMS_3)
    DATA = R.json()

    print(DATA)


def main():
    fileloc = '/statdata/processed_csv/globalcontribs.csv'
    # H://testdata.txt
    stp, df = convert_to_string(fileloc, True)
    string_to_print = header_data('Global') + stp
    push_to_wiki("Rank data/Global", string_to_print)
    percentile_toprint = '=={}==\n\n'.format("Global") + get_percentile_data(df, "Global") + local_wiki_processing(
        '/statdata/rawcsv')
    push_to_wiki("Percentiles", percentile_toprint)
    # print(string_to_print)


main()
