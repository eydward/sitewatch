import os
import csv
import time


def watch(site):
    return 2


# iterate through all sites & run "watch" on all of them
with open(r"sitelist.csv") as sitelistcsv:
    sitelist = csv.reader(sitelistcsv)
    for site in sitelist:
        # site should be a list:
        # site[0] = name; site[1] = link; site[2] = read mode (text/html)
        watch(site)

# update timestamp
open(r"timestamp.txt", "wt").write(time.ctime())

# all the tracking files go here
path = os.path.expanduser(r"\Documents\sitewatch")


def watch(row):
    if len(row) <= 2:
        print("failed: incomplete row")

    # remove accidental whitespaces if they exist
    name = row[0].strip()
    link = row[1].strip()
    mode = row[2].strip()

    return
