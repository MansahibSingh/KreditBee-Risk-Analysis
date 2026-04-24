import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import requests
import re

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Loan Risk AI Tool", layout="wide")
st.title("🤖 Loan Risk AI Analyzer")

# ---------------------------
# Input Fields (Required)
# ---------------------------
uploaded_file = st.file_uploader("Upload Loan Dataset (Excel) *", type=["xlsx"])

question = st.text_input("Ask your question about the dataset *")

email = st.text_input("Enter your email *")

# ---------------------------
# Email Validation
# ---------------------------
def is_valid_email(email):
    pattern = r"^[\w\.-]+@[\w\.-]+\.\w+$"
    return re.match(pattern, email)

# ---------------------------
# Email Function
# ---------------------------
def send_email(to_email, body):
    try:
        sender = st.secrets["EMAIL_USER"]
        password = st.secrets["EMAIL_PASS"]

        msg = MIMEText(body)
        msg["Subject"] = "Loan Risk Analysis"
        msg["From"] = sender
        msg["To"] = to_email

        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
            server.login(sender, password)
            server.send_message(msg)

    except Exception as e:
        st.error(f"❌ Email Error: {e}")

# ---------------------------
# AI Function (OpenRouter)
# ---------------------------
def generate_ai_response(df, question):

    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]

        total_loans = len(df)
        bad_loans = len(df[df["loan_condition"] == "Bad Loan"])
        bad_pct = (bad_loans / total_loans) * 100 if total_loans else 0

        avg_interest = df["interest_rate"].mean()

        high_dti = len(df[df["debt_to_income"] > 0.35])
        high_dti_pct = (high_dti / total_loans) * 100 if total_loans else 0

        grade_risk = df.groupby("grade")["risk_flag"].mean().round(3).to_dict()
        region_risk = df.groupby("region")["risk_flag"].mean().round(3).to_dict()

        summary = f"""
        Total Loans: {total_loans}
        Bad Loan %: {bad_pct:.2f}
        Avg Interest Rate: {avg_interest:.2f}
        High DTI (>0.35): {high_dti_pct:.2f}

        Risk by Grade: {grade_risk}
        Risk by Region: {region_risk}
        """

        prompt = f"""
        You are a senior financial risk analyst.

        Dataset Summary:
        {summary}

        User Question:
        {question}

        Tasks:
        1. Answer clearly
        2. Highlight risk patterns
        3. Identify concerning trends
        4. Suggest business actions

        Keep response concise and professional.
        """

        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json={
                "model": "openai/gpt-4o-mini",
                "messages": [
                    {"role": "user", "content": prompt}
                ]
            }
        )

        result = response.json()

        if "choices" not in result:
            return "❌ AI Error: Check API key or model."

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ AI Error: {e}"

# ---------------------------
# Validation Logic
# ---------------------------
is_valid = (
    uploaded_file is not None and
    question.strip() != "" and
    email.strip() != "" and
    is_valid_email(email)
)

# ---------------------------
# Button (Disabled until valid)
# ---------------------------
analyze_clicked = st.button(
    "Analyze & Send Email",
    disabled=not is_valid
)

# ---------------------------
# Inline Warnings (Better UX)
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
# Main Execution
# ---------------------------
if analyze_clicked:

    try:
        df = pd.read_excel(uploaded_file)

        required_cols = [
            "loan_condition",
            "interest_rate",
            "debt_to_income",
            "grade",
            "region",
            "risk_flag"
        ]

        missing_cols = [col for col in required_cols if col not in df.columns]

        if missing_cols:
            st.error(f"❌ Missing required columns: {missing_cols}")
        else:
            with st.spinner("🤖 Analyzing data with AI..."):
                result = generate_ai_response(df, question)

            send_email(email, result)

            st.success("✅ Analysis complete! Email sent successfully.")

            st.subheader("📊 AI Response Preview")
            st.write(result)

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
