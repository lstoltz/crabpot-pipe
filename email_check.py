import os
from imbox import Imbox
import traceback
from datetime import datetime, timedelta
from dotenv import load_dotenv

load_dotenv()

username = "chrp.crabpot@gmail.com" # email credentials
password = os.getenv("APP_PASS")
download_folder = r'C:\Users\lstol\Documents\repositories\crabpot-pipe\email_attachements'
host = "imap.gmail.com"


if not os.path.isdir(download_folder):
    os.makedirs(download_folder, exist_ok=True)
    
mail = Imbox(host, username=username, password=password, ssl=True, ssl_context=None, starttls=False)
d = datetime.today() - timedelta(days=7)
messages = mail.messages(date__gt=d) # gets all received emails from past week

for (uid, message) in messages:
    mail.mark_seen(uid) # mark message as read

    for idx, attachment in enumerate(message.attachments): # loop over the emails
        try:
            att_fn = attachment.get('filename') # gets attached files
            download_path = f"{download_folder}/{att_fn}"
            print(download_path)
            with open(download_path, "wb") as fp:
                fp.write(attachment.get('content').read())
        except:
            print(traceback.print_exc())

mail.logout()