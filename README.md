You are a Risk Analysis AI. A user has asked: "Why is this loan classified as a Bad Loan?"
​Review the borrower's profile below and provide a short, human-readable explanation of the risk factors. Compare these factors to what a "Good Loan" typically looks like.
​Loan Profile:
Grade: {{$json.Grade}}
Interest Rate: {{$json.Interest_Rate}}
DTI: {{$json.Debt_to_Income_Ratio}}
Income: {{$json.Income_Category}}
Employment: {{$json.Employment_Length}}

​"Please format your entire response in HTML. Use <br><br> for paragraph breaks, <b> for bold text, and <ul><li> for bullet points. Do not use Markdown or asterisks."

Allan Cheerakunnil Alex
09:05
# Loan Risk Automation & GenAI Insights
This repository contains an end-to-end automation solution for financial risk analysis. It leverages **n8n** for workflow orchestration and **GenAI (LLaMA 3.3 70B)** to transform raw loan data into actionable business intelligence and human-readable transparency.

## Project Structure
 * **/workflows**: Contains Workflow1.json (Executive Reporting) and Workflow2.json (Loan Explanation).
 * **/screenshots**: Visual evidence of successful workflow execution and green-check verification.
## Tech Stack
 * **Automation:** n8n
 * **AI Model:** LLaMA 3.3 70B (via Groq/OpenAI Node)
 * **Data Handling:** JavaScript (n8n Code Node)
 * **API Integration:** REST API (HTTP Request Node / Webhooks)
 * **Testing:** httpbin.org (Post-request verification)
