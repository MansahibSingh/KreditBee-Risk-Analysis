
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

## Key Insights
 * **Scalability:** By using **HTTP Request** nodes instead of basic email nodes, these workflows can be integrated into any modern ERP or CRM system.
 * **Accuracy:** Using the **LLaMA 3.3 70B** model ensures that the risk analysis remains contextually aware of financial nuances like DTI (Debt-to-Income) impact.
 * **Efficiency:** Automated 100% of the manual report-writing process for the risk department.

**Project developed by:** Mansahib Singh\
**Final Submission Date:** June 22, 2026
