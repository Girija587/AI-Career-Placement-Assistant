AI-Powered Career Placement Assistant 🎓🤖
An intelligent chatbot system designed to assist students with campus placements by providing real-time information about company drives, placement preparation tips, and college-specific FAQs. The system integrates Dialogflow for natural language understanding, Google Sheets as a backend database, and Flask as a webhook service to deliver dynamic and personalized responses.

🚀 Features
🔍 Company Information Lookup
Ask for details about any company and get its description, hiring process, and official website.

🌐 Additional Research Links
Access external resources (Glassdoor, Reddit, Quora) for in-depth insights.

📅 Upcoming Drives
Returns 3 random upcoming drive details based on the current date.

🎓 College-Specific FAQ
Answers questions related to BVRITH and Sri Vishnu Educational Society.

💬 Polite Interaction Handling
Responds appropriately to phrases like "thank you", "okay", etc.

🛠️ Tech Stack
Frontend: Dialogflow (Chat interface, Google Assistant Integration)

Backend: Flask (Webhook server)

Database: Google Sheets API

AI/ML: BERT-CNN hybrid model for context understanding and classification

Deployment: PythonAnywhere / Heroku (optional)

📁 Project Structure
bash
Copy
Edit
├── webhook/
│   ├── initial.py           # Main Flask app handling Dialogflow webhook
│   ├── credentials.json     # Google API service account credentials
│   └── requirements.txt     # Python dependencies
├── data/
│   └── CompanyInfoSheet     # Google Sheets with two tabs: Drives, CompanyInfo
├── models/
│   └── model.pkl            # Trained BERT-CNN model (optional)
└── README.md
🔧 Setup Instructions
Clone the repository

bash
Copy
Edit
git clone https://github.com/yourusername/placement-assistant.git
cd placement-assistant
Create a virtual environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
Install dependencies

bash
Copy
Edit
pip install -r requirements.txt
Add Google Sheets API credentials

Place your credentials.json file in the webhook/ folder.

Run the Flask webhook

bash
Copy
Edit
python initial.py
Connect to Dialogflow

Add the Flask webhook URL to your Dialogflow agent's Fulfillment section.

📊 Google Sheets Structure
Drives Tab
Company	Date	Role	Location	Deadline

CompanyInfo Tab
Company	About	Hiring Process	Website	Glassdoor	Reddit	Quora

📌 Future Enhancements
Add user authentication for personalized dashboards

Enable resume analysis and feedback

Integrate with email/SMS for drive notifications

Admin panel for updating Google Sheets data
