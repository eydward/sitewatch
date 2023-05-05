from __future__ import print_function
import os, csv, base64
from email.message import EmailMessage
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ["https://www.googleapis.com/auth/gmail.modify"]


def sendemail(inputdict):
    """
    sends an email.
    content of email comes from file email-text.html
    specific {strings} are replaced by values in inputdict
    """
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    try:
        service = build("gmail", "v1", credentials=creds)

        message = EmailMessage()

        with open("email-text.html") as emfile:
            content = emfile.read()
        # format with https://stackoverflow.com/questions/5952344/
        content = content.format(**inputdict)

        # required "special things"
        message["From"] = inputdict["from"]
        message["To"] = inputdict["to"]
        message["Subject"] = inputdict["subject"]

        # optional "special things"
        message["cc"] = inputdict.get("cc", "")  # does this work??
        message["bcc"] = inputdict.get("bcc", "")  # does this work??

        message.add_header("Content-Type", "text/html")
        message.set_payload(content)

        encoded_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

        create_message = {"raw": encoded_message}
        # pylint: disable=E1101
        send_message = (
            service.users().messages().send(userId="me", body=create_message).execute()
        )
        print(f'Message Id: {send_message["id"]} sent to {inputdict["to"]}')

    except HttpError as error:
        print(f"An error occurred: {error}")


def emailer():
    # read the csv into the 2D array emaillist
    emailcsv = r"email-recipients.csv"
    emaillist = []
    with open(emailcsv) as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:  # each row is a list
            emaillist.append(row)

    # the first row of emaillist are the headers; iterate through all others
    for i in range(1, len(emaillist)):
        if len(emaillist[0]) != len(emaillist[i]):  # bad row, ignore it
            print("row " + i + " malformed")
            continue

        # make a dict: header names (for formatting) --> values
        inputdict = dict()
        for j in range(0, len(emaillist[0])):
            inputdict[emaillist[0][j]] = emaillist[i][j]

        # pass dict in to send an email
        sendemail(inputdict)


if __name__ == "__main__":
    emailer()
