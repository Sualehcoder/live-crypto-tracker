import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
import streamlit as st
# CONFIGURATION (Replace with your details)
EMAIL_SENDER = st.secrets["email_address"]


# ... inside your function or at top ...
# EMAIL_PASSWORD = "hardcoded_password" <--- DELETE THIS
EMAIL_PASSWORD = st.secrets["email_password"] # <--- USE THIS
EMAIL_RECEIVER = "your_email@gmail.com"      # Send to yourself

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
        server.starttls() # Secure the connection
        server.login(EMAIL_SENDER, EMAIL_PASSWORD)
        
        # Send
        server.send_message(msg)
        server.quit()
        
        return True
    except Exception as e:
        print(f"Error sending email: {e}")
        return False