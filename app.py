import streamlit as st
import openai
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("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")

st.title("\U0001F4E7 AI-Powered Email Generator")

recipient = st.text_input("Recipient Email")
subject = st.text_input("Email Subject")
tone = st.selectbox("Select Tone", ["Formal", "Informal"])

def generate_email():
    prompt = f"Generate a {tone} email about {subject} addressed to {recipient}"
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are an email assistant."},
                  {"role": "user", "content": prompt}]
    )
    return response["choices"][0]["message"]["content"]

if st.button("Generate Email"):
    if not recipient or not subject:
        st.warning("Please enter recipient email and subject.")
    else:
        email_content = generate_email()
        st.text_area("Generated Email", email_content, height=200)
        
        if st.button("Send Email"):
            sender_email = os.getenv("EMAIL_USER")
            email_password = os.getenv("EMAIL_PASS")
            
            msg = MIMEMultipart()
            msg['From'] = sender_email
            msg['To'] = recipient
            msg['Subject'] = subject
            msg.attach(MIMEText(email_content, 'plain'))
            
            try:
                with smtplib.SMTP('smtp.gmail.com', 587) as server:
                    server.starttls()
                    server.login(sender_email, email_password)
                    server.sendmail(sender_email, recipient, msg.as_string())
                st.success("✅ Email sent successfully!")
            except Exception as e:
                st.error(f"❌ Failed to send email: {e}")
