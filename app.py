import streamlit as st
import pandas as pd
import requests
import re

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Loan Risk AI Tool", layout="wide")
st.title("🤖 Loan Risk AI Analyzer")

# ---------------------------
# Inputs
# ---------------------------
uploaded_file = st.file_uploader("Upload Loan Dataset (Excel) *", type=["xlsx"])
question = st.text_input("Ask your question *")
email = st.text_input("Enter your email *")

# ---------------------------
# Email Validation
# ---------------------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# ---------------------------
# Validation
# ---------------------------
is_valid = (
    uploaded_file is not None and
    question.strip() != "" and
    email.strip() != "" and
    is_valid_email(email)
)

# ---------------------------
# Button
# ---------------------------
if st.button("Analyze & Send Email", disabled=not is_valid):

    try:
        # Read file
        df = pd.read_excel(uploaded_file)

        # Fix JSON issue (Timestamp etc.)
        df = df.astype(str)

        payload = {
            "data": df.to_dict(orient="records"),
            "question": question,
            "email": email
        }

        # 🔐 Get webhook from secrets
        webhook_url = st.secrets["N8N_WEBHOOK_URL"]

        with st.spinner("🚀 Sending data for processing..."):
            response = requests.post(webhook_url, json=payload)

        if response.status_code == 200:
            st.success("✅ Request sent! You will receive an email shortly.")
        else:
            st.error(f"❌ Failed to connect (Status: {response.status_code})")

    except Exception as e:
        st.error(f"❌ Error: {e}")
