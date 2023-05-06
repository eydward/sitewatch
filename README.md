# sitewatch

A script that scans through sites and checks for differences for you. Requires [html2text](https://pypi.org/project/html2text/), plus other dependencies if you want email updates.

After setup, you can just run `sitewatch.py`, perhaps with a scheduling tool.

Probably. nothing works on not-Windows. (TODO)

## project setup (without emails)

Two things.

1. You can change the list of sites in `sitelist.csv`. Each row is one site. There are three columns:
    1. The name you want the site to go by (e.g. "xkcd")
    2. The link to the site (e.g. "[xkcd.com](https://www.xkcd.com)")
    3. The mode you want to process the site by:
        - `html` mode will read the HTML of the page. (Note that for most modern websites  this will give you a bunch of false positives.)
        - `text` mode will read the words on the page, and also check the names of the images.
        - `link` mode does everything `text` does, but also checks all the hyperlinks are the same.

    sitewatch also saves the HTML pages of websites it's seen, so you can go to `~\Documents\sitewatch` and diff them if you want to see what changed.
    Occasionally, you also probably want to clean that folder out. (TODO - automatically do this)

2. If you don't want email notifications when sitewatch detects a change in a site, you should write `{"emails":"false"}` into `options.json`. If you do want email notifications, proceed to the next section.
(Note that with a bit of work you can e.g. use this to [update a Rainmeter skin](https://forum.rainmeter.net/viewtopic.php?t=18117) instead.)

## email setup instructions

If you want email notifications then write `{"emails":"true", "from":"(send from email)", "to":"(send to email)"}` into `options.json`. Your "send from" email must be accessible with the Gmail API, so any gmail should work.

Next, get:
- google-api-python-client: `pip install --upgrade google-api-python-client`
- google-auth-oauthlib: `pip install google-auth-oauthlib`

Credentials setup (with the "from" email):

1. Go to [console.cloud.google.com](console.cloud.google.com), and log in with the desired email.
2. Make a new project, or use an arbitrary existing one. Set its location to "No Organization".

Configure oauth consent screen:

3. At the OAuth Consent Screen, set the user type to "External" (since you don't have an organization).
4. Fill in the app name as "emailer" (or whatever; it doesn't matter), and the support email as your email. No optional fields matter.
5. To select scopes, first go to the API library from the OAuth Consent Screen (in a separate tab) and enable the Gmail API. Then, return to the app-registration screen and add the Gmail modify scope: `https://www.googleapis.com/auth/gmail.modify`.
6. Set yourself as a test user.

Get credentials:

8. Go to Menu > APIs & Services > Credentials.
9. Click Create Credentials > OAuth client ID.
10. Set the application type as "Desktop App", fill in other fields, and finish.
11. Download the JSON file; move it into the emailer directory and rename it `credentials.json`.