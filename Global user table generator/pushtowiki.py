from os import listdir
import requests
import pandas as pd
import math
import csv
import mysql.connector
from iso639 import Lang


def header_data(wikiname):
    return "{{| class=\"wikitable sortable\"\n|+ {} user rank data\n|-\n! Rank !! Username !! Registration date !! Number of edits\n|-\n".format(
        wikiname)


def header_data_percentile(wikiname):
    return "{{| class=\"wikitable sortable\"\n|+ {} percentile data\n|-\n! Percentile !! Number of edits\n".format(
        wikiname)


def convert_to_string(fileloc, rankinc, wiki_name=None):
    limit = 80000000
    if rankinc:  # global
        df = pd.read_csv(fileloc, nrows=limit, on_bad_lines='skip', sep='|', quoting=csv.QUOTE_NONE)
    else:  # local
        df = pd.read_csv(fileloc, nrows=limit, on_bad_lines='skip', sep='\t', quoting=csv.QUOTE_NONE)
    df.rename(columns={"user_name": "Username", "user_registration": "Registration_date", "user_editcount": "Edits"},
              inplace=True)
    df = df[df['Edits'] >= 1]  # weed out users with no edits
    df.loc[df['Registration_date'].astype(str) == 'nan', 'Registration_date'] = '0'  # remove nan
    df['Registration_date'] = df['Registration_date'].astype(int)
    df['Registration_date'] = df['Registration_date'].astype(str)
    df.loc[df['Registration_date'] == '0', 'Registration_date'] = ''

    if not rankinc:
        df['Rank'] = df['Edits'].rank(method='max', ascending=False).astype(int)
    df['output'] = "|" + df['Rank'].astype(str) + "||" + df['Username'].astype(str) + "||" + df[
        "Registration_date"].astype(str) + "||" + df["Edits"].astype(str)

    # https://stackoverflow.com/a/77999077/19370273
    # only consider complete rows
    df['str_length'] = df['output'].str.encode('utf-8').len()  # create column with length of strings
    df['str_length_cum'] = df['str_length'].cumsum()  # create column with cumulative length of strings
    df = df[df['str_length_cum'] < 2096900]  # filter with threshold
    del (df['str_length'])
    del (df['str_length_cum'])

    # convert to string

    toprint = pd.DataFrame({'text': ['\n|-\n'.join(df['output'].str.strip('"').tolist())]})['text'].item()

    # don't forget encoding limit!

    # toprint = toprint.encode('utf-8')[:2096900].decode('utf-8')
    toprint = toprint + '\n|}\n' + (add_categories(wiki_name) if wiki_name is not None else '')

    # print(f"first 1000 chars of global: {toprint[:1000].encode('unicode_escape')}")
    # print(f"last 1000 chars of global: {toprint[:-1000].encode('unicode_escape')}")

    return toprint, df


def add_categories(wiki_name):
    # input is something like 'enwiki', 'mlwikisource'
    # find the language
    cnx = mysql.connector.connect(option_files='/root/replica.my.cnf', host='meta.analytics.db.svc.wikimedia.cloud',
                                  database='meta_p')

    # handle exceptions
    exception_wikiname = dict(simplewiki='Simple English Wikipedia', simplewikibooks='Simple English Wikibooks',
                              simplewikiquote='Simple English Wikiquote', simplewiktionary='Simple English Wiktionary',
                              donatewiki='Fundraising')

    # get the global table
    cursor = cnx.cursor()
    query = ("SELECT dbname, lang, family, name from wiki")
    cursor.execute(query)
    res = pd.DataFrame(cursor.fetchall(), columns=[desc[0] for desc in cursor.description])
    # print(res)
    wiki_family = res[res['dbname'] == wiki_name]['family'].item()
    if wiki_family == 'special' or wiki_name in exception_wikiname:
        # not a content wiki
        if wiki_name in exception_wikiname:
            full_name = exception_wikiname[wiki_name]
        else:
            # get full name from database
            full_name = res[res['dbname'] == wiki_name]['name'].item()
        category_name = f"{full_name}"

    else:
        wiki_lang = res[res['dbname'] == wiki_name]['lang'].item()
        try:
            full_lang_name = Lang(wiki_lang).name
        except:
            return ''  # for invalid langs
        category_name = f"{full_lang_name} {wiki_family.capitalize()}"

    # now check whether this category exists in meta-wiki

    r = requests.get(f"https://meta.wikimedia.org/wiki/Category:{category_name}")
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
        toprint = toprint + '|-\n|' + remove_trailing_zeros(str(percentile[i])) + '||' + remove_trailing_zeros(
            str(edits[i])) + '\n|-\n'
    toprint = toprint + '|}\n\n'
    return header_data_percentile(wikiname) + toprint


def get_percentile_data(dframe, wikiname):
    # What this does: takes in a dataframe and outputs percentile data
    # edit_count is the last column
    ptr = 0.000000000
    old_bound = -1
    percentile = []
    edits = []
    dframe.rename(columns={"user_name": "Username", "user_registration": "Registration_date", "user_editcount": "Edits"},
              inplace=True)
    while ptr <= 1.0000001:
        # bound = math.floor(dframe.iloc[:, len(dframe.columns) - 1].quantile(min(ptr, 1)))
        bound = math.floor(dframe['Edits'].quantile(min(ptr, 1)))
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
        tp, dframe = convert_to_string(filename, False, page_name)
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
