import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import streamlit as st  # <--- THIS MUST BE AT THE TOP

# Now this works because 'st' is already loaded
EMAIL_SENDER = st.secrets["email_address"]
EMAIL_PASSWORD = st.secrets["email_password"]
EMAIL_RECEIVER = st.secrets["email_address"]

def send_email_alert(crypto_name, price):
    try:
        subject = f"🚨 ALERT: {crypto_name} Price Drop!"
        body = f"HEADS UP! \n\n{crypto_name} has dropped below your target price.\nCurrent Price: ${price}\n\nTime to buy?"

        # Create the email format
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = EMAIL_RECEIVER
        msg['Subject'] = subject
        msg.attach(MIMEText(body, 'plain'))

        # Connect to Gmail Server
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        server.send_message(msg)
        server.quit()
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False