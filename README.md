# sitewatch

A script that tells you when things update. To set this up, you need html2text `pip install html2text`.
Set up email notifications if desired according to the instructions below.
Then one can just run `sitewatch.py` on a schedule.

# emailer setup

A script to send mass customizable emails via Gmail API.

## project usage

**warning**: if sending from a different email from the previous run, make sure to delete `token.json` and replace `credentials.json`! To do this, follow the steps in "Credentials Setup".

To mail merge:
- Populate `email-recipients.csv` with one header row, with the strings that are required in `email-text.html`, and the other rows with information. Headers "from", "to", and "subject" are required. (Note that "cc" and "bcc" are not, and the headers are case sensitive.)
- Write in `email-text.html` with the HTML of the email. Put to-be-replaced things in brackets, e.g. `{num}`.
- The script is `emailer.py`.

### credentials setup (each time)
1. try running `emailer.py' directly; it might work!
2. go to https://console.cloud.google.com, find the relevant API/project/
3. click the "download json" button and move the json into this directory; call it `credentials.json'
4. run `emailer.py'; this should give a Google log in screen
5. ending screen should be `The authentication flow has completed. You may close this window.`

## project setup

### 
You need these Google things:
- google-api-python-client: `pip install --upgrade google-api-python-client`
- google-auth-oauthlib: `pip install google-auth-oauthlib`

### credentials setup (one-time per email)
1. Go to console.cloud.google.com, and log in with the desired email.
2. Make a new project, or use an arbitrary existing one. Set its location to "No Organization".

#### configure oauth consent screen
3. At the OAuth Consent Screen, set the user type to "External" (since you don't have an organization).
4. Fill in the app name as "emailer" (or whatever; it doesn't matter), and the support email as your email. No optional fields matter.
5. To select scopes, first go to the API library from the OAuth Consent Screen (in a separate tab) and enable the Gmail API. Then, return to the app-registration screen and add the Gmail modify scope: `https://www.googleapis.com/auth/gmail.modify`.
6. Set yourself as a test user.

#### get credentials
8. Go to Menu > APIs & Services > Credentials.
9. Click Create Credentials > OAuth client ID.
10. Set the application type as "Desktop App", fill in other fields, and finish.
11. Download the JSON file; move it into the emailer directory and rename it `credentials.json`.