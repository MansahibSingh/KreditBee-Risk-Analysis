import streamlit as st
import pandas as pd
import smtplib
from email.mime.text import MIMEText
import requests

# ---------------------------
# Page Config
# ---------------------------
st.set_page_config(page_title="Loan Risk AI Tool", layout="wide")
st.title("🤖 Loan Risk AI Analyzer")

# ---------------------------
# Upload File
# ---------------------------
uploaded_file = st.file_uploader("Upload Loan Dataset (Excel)", type=["xlsx"])

question = st.text_input("Ask your question about the dataset")

email = st.text_input("Enter your email")

# ---------------------------
# Email Function (Using Streamlit Secrets)
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
        st.error(f"Email Error: {e}")

# ---------------------------
# AI Function (OpenRouter)
# ---------------------------
def generate_ai_response(df, question):

    try:
        api_key = st.secrets["OPENROUTER_API_KEY"]

        # Create smart summary (instead of sending full dataset)
        total_loans = len(df)
        bad_loans = len(df[df["loan_condition"] == "Bad Loan"])
        bad_pct = (bad_loans / total_loans) * 100 if total_loans else 0

        avg_interest = df["interest_rate"].mean()

        high_dti = len(df[df["debt_to_income"] > 0.35])
        high_dti_pct = (high_dti / total_loans) * 100 if total_loans else 0

        grade_risk = df.groupby("grade")["risk_flag"].mean().to_dict()
        region_risk = df.groupby("region")["risk_flag"].mean().to_dict()

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
        1. Answer the question clearly
        2. Highlight key risk patterns
        3. Mention any concerning trends
        4. Suggest business actions

        Keep it concise, professional, and easy to understand.
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
            return "❌ AI Error: Check API key or model configuration."

        return result["choices"][0]["message"]["content"]

    except Exception as e:
        return f"❌ Error generating AI response: {e}"

# ---------------------------
# Main Button
# ---------------------------
if st.button("Analyze & Send Email"):

    if uploaded_file and question and email:

        try:
            df = pd.read_excel(uploaded_file)

            # Basic validation (important)
            required_cols = ["loan_condition", "interest_rate", "debt_to_income", "grade", "region", "risk_flag"]
            missing_cols = [col for col in required_cols if col not in df.columns]

            if missing_cols:
                st.error(f"Missing required columns: {missing_cols}")
            else:
                with st.spinner("Analyzing data with AI..."):
                    result = generate_ai_response(df, question)

                send_email(email, result)

                st.success("✅ Analysis complete! Email sent successfully.")

                st.subheader("📊 AI Response Preview")
                st.write(result)

        except Exception as e:
            st.error(f"Error processing file: {e}")

    else:
        st.warning("Please upload file, enter question, and email.")
