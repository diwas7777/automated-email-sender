import pandas as pd

users_data = pd.read_csv("dummy_user.csv")


import email, smtplib, ssl

from email import encoders
from email.mime.base import MIMEBase
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

for items in range(len(users_data)):
    subject = "Certificate by Diwas [Email Sender]"
    body = f"Hi {users_data['Name'][items]}, Here is your certificate👍🏽"
    receiver_email = users_data['Email'][items]
    # ------------------------------------------------------------ #
    # ----------------- MODIFY HERE ------------------------------ #
    # ------------------------------------------------------------ #
    sender_email = "Your Email" # Put your email here
    password = 'Generated APP Password' # Generate from https://myaccount.google.com/apppasswords
    # ------------------------------------------------------------ #

    print(f"Sending email to {receiver_email}")

    # Create a multipart message and set headers
    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = receiver_email
    message["Subject"] = subject
    message["Bcc"] = receiver_email  # Recommended for mass emails
    

    # Add body to email
    message.attach(MIMEText(body, "plain"))

    filename = "Certificate/"+str(users_data['SN'][items])+".jpg"  # In same directory as script

    # Open file in binary mode
    with open(filename, "rb") as attachment:
        # Add file as application/octet-stream
        # Email client can usually download this automatically as attachment
        part = MIMEBase("application", "octet-stream")
        part.set_payload(attachment.read())

    # Encode file in ASCII characters to send by email    
    encoders.encode_base64(part)

    # Add header as key/value pair to attachment part
    part.add_header(
        "Content-Disposition",
        f"attachment; filename= {users_data['Name'][items]}.jpg",
    )

    # Add attachment to message and convert message to string
    message.attach(part)
    text = message.as_string()

    # Log in to server using secure context and send email
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(sender_email, password)
        server.sendmail(sender_email, receiver_email, text)