# input: CSV of results
# output: relevant graphs
import matplotlib.pyplot as plt
import csv
import numpy as np
import sys
import csv
# https://stackoverflow.com/questions/15063936/csv-error-field-larger-than-field-limit-131072
csv.field_size_limit(sys.maxsize)
# from https://www.geeksforgeeks.org/visualize-data-from-csv-file-in-python/ https://matplotlib.org/3.5.0/gallery/pyplots/pyplot_text.html#sphx-glr-gallery-pyplots-pyplot-text-py
editcounts = []
# wikimedia/Raw CSV data/viwiki.csv
with open('/vol/bitbucket/dm1321/globalcontribs.csv','r') as csvfile:
    row = csv.reader(csvfile, delimiter = '|')
    x = 1
    # row should contain 3 values
    for rr in row:
        if (x == 1):
            x = x + 1
            continue
        editcounts.append(int(rr[3]))
MIN = 1
MAX = max(rr)
n, bins, patches = plt.hist(editcounts, bins=np.logspace(0, 7, 2500)) # https://stackoverflow.com/questions/45942488/histogram-in-log-scale-with-python
plt.xlabel('Number of edits')
plt.gca().set_xscale('log')
plt.gca().set_xlim([0.5, 10000000])
plt.yscale('log', nonposy='clip')
plt.ylabel('Number of users')
plt.show()