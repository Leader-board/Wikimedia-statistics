import json, os
import pandas as pd
import pyreadstat
import pickle
import traceback

path_to_json = 'Z:/Wikipedia_json'
json_files = [pos_json for pos_json in os.listdir(path_to_json) if pos_json.endswith('.json')]
dfs = []
for j in json_files:
    print(j)
    with open(j,  encoding="utf8") as data_file:    
        data = json.load(data_file)
    df = pd.json_normalize(data, "messages")
    dfs.append(df)
    user_counts = dict(df['author.name'].value_counts())
    filename = j.replace(".json","")
    f = open("frequencies/" + filename + ".txt", "a",  encoding="utf8")
    for i in user_counts:
        f.write(str(i) + "╡" + str(user_counts[i]) + '\n')
    f.close()
    try:
        writer = pd.ExcelWriter("excel/" + filename + ".xlsx", engine='xlsxwriter', options={'strings_to_urls': False})
        df.to_excel(writer)
        writer.save()
        writer.close()
    except Exception as e:
        print("Excel size error")
        print(e)
        traceback.print_exc()
    dbfile = open("pickle/" + filename, 'ab')
    try:
        pickle.dump(df, dbfile)
    except Exception as e:
        print("Can't pickle " + filename)     
        print(e)
        traceback.print_exc()                
    dbfile.close()
# print(dfs)
res = pd.concat(dfs)
print(res.info)
user_counts = dict(res['author.name'].value_counts())
# https://www.w3schools.com/python/python_file_write.asp
f = open("user_frequency.txt", "a",  encoding="utf8")
for i in user_counts:
    f.write(str(i) + "╡" + str(user_counts[i]) + '\n')
f.close()
res.to_csv('wikipedia_discord.csv', '╡')
try:
    pyreadstat.write_sav(res, 'wikipedia_discord.sav')
except Exception as e:
    print("Can't save main to sav")
    print(e)
# res.to_excel('wikipedia_discord.xlsx')
# https://www.geeksforgeeks.org/understanding-python-pickling-example/
dbfile = open('wikipedia_discord_pickle', 'ab')
try:
    pickle.dump(res, dbfile)      
except Exception as e:
    print("Can't pickle main")  
    print(e)             
dbfile.close()