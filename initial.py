import os
from google.oauth2 import service_account
import google.cloud.dialogflow as dialogflow
import difflib
from googleapiclient.discovery import build
from datetime import datetime
import random

# Dialogflow setup
SERVICE_ACCOUNT_FILE = os.path.join(os.getcwd(), "placementbot_j9jk.json")
credentials = service_account.Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)
DIALOGFLOW_PROJECT_ID = "placementbot-j9jk"
DIALOGFLOW_LANGUAGE_CODE = "en"

# Google Sheets setup
SHEETS_CREDENTIALS_FILE = os.path.join(os.getcwd(), "sheets_credentials.json")
google_sheets_creds = service_account.Credentials.from_service_account_file(SHEETS_CREDENTIALS_FILE)
SPREADSHEET_ID = "1he1JJ2EkmQXoqWkR3WGlBXP92roUjV6mS6YUr9IYFz0"

# Dialogflow response function
def dialogflow_response(user_input):
    session_client = dialogflow.SessionsClient(credentials=credentials)
    session = session_client.session_path(DIALOGFLOW_PROJECT_ID, "unique-session-id")
    text_input = dialogflow.TextInput(text=user_input, language_code=DIALOGFLOW_LANGUAGE_CODE)
    query_input = dialogflow.QueryInput(text=text_input)
    response = session_client.detect_intent(request={"session": session, "query_input": query_input})
    fulfillment_text = response.query_result.fulfillment_text
    parameters = dict(response.query_result.parameters)
    return fulfillment_text, parameters

# Get info from 'Drives' tab
def get_upcoming_drives():
    try:
        service = build("sheets", "v4", credentials=google_sheets_creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(
            spreadsheetId=SPREADSHEET_ID,
            range="Drives!A2:F"
        ).execute()

        values = result.get("values", [])
        today = datetime.now().date()

        future_drives = []
        for row in values:
            if len(row) >= 6:
                try:
                    drive_date = datetime.strptime(row[1], "%Y-%m-%d").date()
                    if drive_date >= today:
                        future_drives.append(row)
                except:
                    continue

        if not future_drives:
            return "❌ No upcoming drives found."

        random.shuffle(future_drives)
        selected_drives = future_drives[:3]

        formatted_drives = []
        for row in selected_drives:
            company, date, cgpa, role, location, notes = row
            formatted = (
                f"📌 **{company}**\n"
                f"📅 Date: {date}\n"
                f"🎓 Min CGPA: {cgpa}\n"
                f"💼 Role: {role}\n"
                f"📍 Location: {location}\n"
                f"📝 Notes: {notes}\n"
                f"{'-'*30}"
            )
            formatted_drives.append(formatted)

        return "\n\n".join(formatted_drives)

    except Exception as e:
        import traceback
        return f"❌ Sheets API Error:\n{traceback.format_exc()}"

# BVRITH-specific FAQ responses
def get_bvrith_faq(user_question):
    try:
        service = build("sheets", "v4", credentials=google_sheets_creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="BVRITH_FAQs!A2:B").execute()
        values = result.get("values", [])
        user_question_lower = user_question.strip().lower()

        questions = [row[0].strip() for row in values if len(row) >= 2]
        question_map = {row[0].strip(): row[1] for row in values if len(row) >= 2}

        closest_matches = difflib.get_close_matches(user_question.strip(), questions, n=1, cutoff=0.5)

        if closest_matches:
            best_match = closest_matches[0]
            return f"ℹ️ {question_map[best_match]}"
        else:
            return "❌ Sorry, I couldn't find an answer to that BVRITH-related question."

    except Exception as e:
        import traceback
        return f"❌ Error fetching BVRITH FAQ:\n{traceback.format_exc()}"

# Get company info from 'CompanyInfo' tab
def get_company_info(company_name, more=False):
    try:
        service = build("sheets", "v4", credentials=google_sheets_creds)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=SPREADSHEET_ID, range="CompanyInfo!A2:H").execute()
        values = result.get("values", [])

        for row in values:
            if len(row) >= 7 and company_name.lower() in row[0].lower():
                if more:
                    return (
                        f"🔗 Useful Links:<br>"
                        f"🔹 <a href='{row[4]}' target='_blank'>Glassdoor</a><br>"
                        f"🔹 <a href='{row[5]}' target='_blank'>Reddit</a><br>"
                        f"🔹 <a href='{row[6]}' target='_blank'>Quora</a><br>"
                        f"🔹 <a href='{row[7]}' target='_blank'>GeeksforGeeks</a>"
                    )
                else:
                    return (
                        f"📌 {row[0]}<br>"
                        f"💬 <b>About:</b> {row[1]}<br>"
                        f"⚙️ <b>Hiring Process:</b> {row[2]}<br>"
                        f"🌐 <b>Website:</b> <a href='{row[3]}' target='_blank'>{row[3]}</a><br>"
                    )
        return f"❌ Sorry, no details found for '{company_name}'."

    except Exception as e:
        import traceback
        return f"❌ Error fetching company info:\n{traceback.format_exc()}"

# Track last company asked
last_company = None

# Central logic
def thinking(question):
    global last_company
    question_lower = question.lower()

    # 1. Handle BVRITH / placement cell / FAQ queries
    if any(k in question_lower for k in [
        "bvrith", "placement", "placement cell", "resume", "eligibility", "interview",
        "officer", "companies visited", "product-based", "contact", "team"
    ]):
        return get_bvrith_faq(question)

    # 2. Handle upcoming drives FIRST
    if any(k in question_lower for k in ["drive", "upcoming", "recruiter", "hiring"]):
        return get_upcoming_drives()

    # 3. Handle follow-up for more info
    if any(k in question_lower for k in ["more info", "more", "tell me more"]) and last_company:
        return get_company_info(last_company, more=True)

    # 4. Handle company queries
    if "tell me about" in question_lower:
        reply, parameters = dialogflow_response(question)
        company_name = None
        try:
            company_name = parameters.get("company")
        except:
            pass
        if not company_name:
            company_name = question_lower.replace("tell me about", "").strip()
        if company_name:
            last_company = company_name
            return get_company_info(company_name, more=False)

    # 5. Thank you responses
    if any(k in question_lower for k in ["thank you", "thanks", "thankyou"]):
        return "You're welcome! 😊 Let me know if you need help with anything else."

    # 6. Fallback to Dialogflow
    reply, _ = dialogflow_response(question)
    return reply

# Optional debug logs
print("🧪 Requesting range: Drives!A2:F")
print("🧪 Using spreadsheet ID:", SPREADSHEET_ID)
print("🧪 Using client email:", credentials.service_account_email)
