import os
import sys
import csv
from datetime import datetime
from pytz import timezone
import pytz
from pathlib import Path
import requests

path = r"C:\Users\edward\Documents\sitewatch"
sitelistcsv = r"C:\Users\edward\Documents\sitewatch\sitelist.csv"
sitelist = []

with open(sitelistcsv) as csvfile:
    reader = csv.reader(csvfile)
    for row in reader:  # each row is a list
        sitelist.append(row)

sys.stdout = open(path + "\\results.txt", "w")

ts = open(path + "\\timestamp.txt", "wt")
ts.write(datetime.utcnow().strftime("%Y/%m/%d %H:%M:%S"))

for row in sitelist:
    if len(row) < 2:
        continue  # for blank/incomplete/etc rows

    id = row[0].strip()
    url = row[1].strip()
    folderpath = path + "\\" + id
    if not os.path.exists(folderpath):
        os.makedirs(folderpath)

    try:
        r = requests.get(
            url,
            timeout=5,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
        )
    # except TimeoutError: # TODO: doesn't work
    #     print(id + "\t\t\tTIMED OUT")
    #     continue
    except:
        print(id + "\t\t\tFAILED")
        continue

    folderdir = os.listdir(folderpath)
    folderdir.sort(reverse=True)

    def addnewfile():
        newfilepath = (
            folderpath
            + "\\"
            + id
            + "-"
            + datetime.now()
            .astimezone(timezone("US/Pacific"))
            .strftime("%Y%m%d-%H%M%S")
            + ".html"
        )
        f = open(newfilepath, "wb")
        # print(newfilepath)
        f.write(r.content)
        f.close()

    if len(folderdir) == 0:  # nothing logged for this site yet! add new file
        print(id + "\t\t\tinitialized")
        addnewfile()
        continue

    # look at previous file
    oldfilepath = folderpath + "\\" + folderdir[0]
    if Path(oldfilepath).read_bytes() != r.content:  # file changed, add new file
        print(id + "\t\t\tchanged")
        addnewfile()
    else:  # don't do anything
        print(id + "\t\t\tunchanged")
        addnewfile()

# update rainmeter skin on script: https://forum.rainmeter.net/viewtopic.php?t=18117
