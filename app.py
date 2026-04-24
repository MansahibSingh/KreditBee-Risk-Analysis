import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

st.set_page_config(page_title="Loan Risk AI Tool", layout="wide")
st.title("🤖 Loan Risk AI Analyzer")

# ---------------------------
# Upload File
# ---------------------------
uploaded_file = st.file_uploader("Upload Loan Dataset (Excel)", type=["xlsx"])

question = st.text_input("Ask your question about the dataset")

email = st.text_input("Enter your email")

# ---------------------------
# Email Function
# ---------------------------
def send_email(to_email, body):
    sender = os.getenv("EMAIL_USER")
    password = os.getenv("EMAIL_PASS")

    msg = MIMEText(body)
    msg["Subject"] = "Loan Risk Analysis"
    msg["From"] = sender
    msg["To"] = to_email

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
        server.login(sender, password)
        server.send_message(msg)

# ---------------------------
# AI Logic (temporary)
# ---------------------------
def generate_insight(df, question):
    
    total_loans = len(df)
    bad_loans = len(df[df["loan_condition"] == "Bad Loan"])
    bad_pct = (bad_loans / total_loans) * 100 if total_loans else 0

    avg_interest = df["interest_rate"].mean()

    high_dti_pct = (len(df[df["debt_to_income"] > 0.35]) / total_loans) * 100 if total_loans else 0

    return f"""
Question: {question}

Summary:
- Total Loans: {total_loans}
- Bad Loan %: {bad_pct:.2f}%
- Avg Interest Rate: {avg_interest:.2f}
- High DTI (>35%): {high_dti_pct:.2f}%

Insight:
Risk is primarily driven by high debt-to-income ratio and higher interest rates.
"""

# ---------------------------
# Main Button
# ---------------------------
if st.button("Analyze & Send Email"):

    if uploaded_file and question and email:

        df = pd.read_excel(uploaded_file)

        result = generate_insight(df, question)

        send_email(email, result)

        st.success("✅ Email sent successfully!")

    else:
        st.warning("Please upload file, enter question, and email.")
