import os, csv
import time
import requests
from pathlib import Path
import html2text
import emailer


def request(name, link):
    r = -1  # this is the request object
    try:
        r = requests.get(
            link,
            timeout=5,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
            },
        )
        print(name + " queried")
    except requests.exceptions.Timeout:
        print(name + " timed out")
    except:
        print(name + " failed")

    try:
        assert r != -1
    except AssertionError:
        print(name + " failed")

    return r


def parse(r, mode):
    # r is a bytes object
    pagecontent = ""
    if mode == "html":
        pagecontent = r.decode()
    else:
        h = html2text.HTML2Text()
        h.skip_internal_links = True
        h.ignore_images = False  # ???
        if mode == "text":
            h.ignore_links = True
            pagecontent = h.handle(r.decode())
        elif mode == "link":
            h.ignore_links = False

        pagecontent = h.handle(r.decode())
    return " ".join(pagecontent.split())


def updateemail(name, link):
    inputdict = dict()
    inputdict["from"] = "edward3yu@gmail.com"
    inputdict["to"] = "edward.yu@outlook.com"
    inputdict["subject"] = "sitewatch update " + name

    open(r"email-text.html", "wt").write(
        "The page "
        + link
        + " has been updated."
        + " (This is an automated message from sitewatch.)"
    )  # update timestamp

    emailer.sendemail(inputdict)


def watch(row, path, results):
    if len(row) <= 2:
        print("failed: incomplete row")
        return

    # remove accidental whitespaces if they exist
    name = row[0].strip()
    link = row[1].strip()
    mode = row[2].strip()

    r = request(name, link)
    pagecontent = parse(r.content, mode)

    # folder storing sitewatch history for this site
    folder = path + "\\" + name

    if not os.path.exists(folder):
        os.makedirs(folder)

    # writes pagecontent into a file in the correct folder
    def log(statusupdate, statusstr):
        if statusupdate:
            newfilepath = folder + "\\" + name + "-" + str(time.time()) + ".html"
            f = open(newfilepath, "wb")
            f.write(r.content)
            f.close()
            updateemail(name, link)
        with open(results, "a") as resultscsv:
            resultscsv.write(name + "," + statusstr + "\n")
        return

    # TODO - SORT THROUGH BELOW CODE FROM BEFORE???
    # recall that r.content should actually be pagecontent

    folderdir = os.listdir(folder)
    folderdir.sort(reverse=True)

    if len(folderdir) == 0:  # nothing logged for this site yet! add new file
        log(True, "initialized")
    else:
        # look at previous file
        prevrecord = folder + "\\" + folderdir[0]
        print("comparing to " + folderdir[0])

        # if file changed, add new file
        if parse(Path(prevrecord).read_bytes(), mode) != pagecontent:
            log(True, "changed")
        else:  # don't do anything
            log(False, "unchanged")
    return


def sitewatch():
    # set the sitewatch file storage directory (TODO - EVERYTHING PROBABLY DIES ON LINUX?)
    path = os.path.expanduser(r"~\Documents\sitewatch")
    if not os.path.exists(path):
        os.makedirs(path)

    # open the results file & clear it
    results = "results.csv"
    open(results, "w+").close()

    open(r"timestamp.txt", "wt").write(time.ctime())  # update timestamp

    # iterate through all sites & run "watch" on all of them
    with open(r"sitelist.csv") as sitelistcsv:
        sitelist = csv.reader(sitelistcsv)
        for site in sitelist:
            # site should be a list: site[0] = name; site[1] = link; site[2] = read mode (text/html)
            watch(site, path, results)

    return


if __name__ == "__main__":
    sitewatch()

# TODO - update rainmeter skin on script: https://forum.rainmeter.net/viewtopic.php?t=18117
