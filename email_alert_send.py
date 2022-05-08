import smtplib, ssl, os
from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv

load_dotenv()

subject = "Review Requested for Time Series"
body="""\
    <html>
        <head></head>
        <body>
            File could not be automatically processed: <br>
            Please delete rows with bad data and send back file as an attachment. <br>
            <b> Caution, do not modify filename! </b>
    </html>
    """

sender_email = os.getenv("EMAIL_USER")
receiver_email = [os.getenv("SENDER_LIST")]
print(receiver_email)
password = os.getenv("APP_PASS")

message = MIMEMultipart()
message["From"] = sender_email
message["To"] = ", ".join(receiver_email)
message["Subject"] = subject

message.attach(MIMEText(body, "html"))

filename = "2002048_mla_20210616_102506_DissolvedOxygen.csv"

with open(filename, "rb") as attachment:
    # Add file as application/octet-stream
    # Email client can usually download this automatically as attachment
    part = MIMEBase("application", "octet-stream")
    part.set_payload(attachment.read())

    # Add header as key/value pair to attachment part
part.add_header(
    "Content-Disposition",
    f"attachment; filename= {filename}",
)

# Add attachment to message and convert message to string
message.attach(part)
text = message.as_string()

# Log in to server using secure context and send email
context = ssl.create_default_context()
with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, text)
