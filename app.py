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
# Input Fields
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
# Validation Check
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
analyze_clicked = st.button(
    "Analyze & Send Email",
    disabled=not is_valid
)

# ---------------------------
# User Guidance
# ---------------------------
if not uploaded_file:
    st.info("📂 Please upload an Excel file")

if not question:
    st.info("❓ Please enter a question")

if email and not is_valid_email(email):
    st.warning("⚠️ Enter a valid email address")

if not email:
    st.info("📧 Please enter your email")

# ---------------------------
# Main Logic
# ---------------------------
if analyze_clicked:

    try:
        # Read Excel
        df = pd.read_excel(uploaded_file)

        # Convert dataframe to JSON
        data_json = df.to_dict(orient="records")

        payload = {
            "data": data_json,
            "question": question,
            "email": email
        }

        # 🔴 IMPORTANT: Replace with your n8n webhook URL later
        webhook_url = "https://your-n8n-url/webhook/loan-analysis"

        with st.spinner("🚀 Sending data for analysis..."):
            response = requests.post(webhook_url, json=payload)

        if response.status_code == 200:
            st.success("✅ Request sent successfully! You will receive an email shortly.")
        else:
            st.error("❌ Failed to connect to automation workflow.")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
