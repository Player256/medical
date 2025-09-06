---

# AI Medical Appointment Scheduling and Patient Management System

This project is a workflow built in **n8n** for handling patient medical appointment scheduling, email communications, and reminders. It also has a **Gradio frontend** that connect to the n8n backend via a webhook.

---

## Integrations Setup

To make the system work, you need to setup integrations with:

1. **Google Sheets**

   * Used as EMR (Electronic Medical Records) to lookup patients.
   * Also used as admin booking sheet where appointment records are exported.

2. **Google Calendar**

   * Used for doctor’s schedule and booking slots.

3. **Gmail**

   * Used to send confirmation and reminder emails to patients.

4. **Google Gemini (PaLM) API**

   * Powers the AI agents for Scheduling and Reminders.

5. **Webhook**

   * Public webhook node in n8n to receive chat input.
   * Gradio frontend connects to this webhook.

---

## Credentials Setup

### Google Sheets

1. In n8n go to **Credentials**.
2. Add new credential → choose **Google Sheets API**.
3. Select **OAuth2** as authentication type.
4. Go to [Google Cloud Console](https://console.cloud.google.com).
5. Create a project, enable **Google Sheets API**.
6. Create OAuth2 client ID credentials.

   * Application type: Web application.
   * Add redirect URI: `https://<your-n8n-instance>/rest/oauth2-credential/callback`.
7. Copy the Client ID and Client Secret to n8n.
8. Save credential and connect it to your Google account.

### Google Calendar

1. In n8n add new credential → choose **Google Calendar API**.
2. Use same OAuth2 credentials you setup in Google Cloud.
3. Enable **Google Calendar API** in your project.
4. Add same Client ID and Client Secret.
5. Authenticate with your Google account.

### Gmail

1. In n8n add new credential → choose **Gmail API**.
2. In Google Cloud project, enable **Gmail API**.
3. Use same OAuth2 Client ID/Secret.
4. Authenticate with your Gmail account.
5. Now workflow can send confirmation and reminder emails.

### Gemini API

1. Sign up for Google AI Studio.
2. Get an API key from [Google AI Studio](https://makersuite.google.com/app/apikey).
3. In n8n, add new credential → choose **Google Gemini** (or OpenAI node with Gemini config if using custom).
4. Paste the API key.

---

## Flow of Workflow

1. **Patient Chat Interface**

   * The entrypoint for patients. They provide name, DOB, preferred doctor, location.
   * If patient is new, system ask for email so it can send calendar link and intake forms.

2. **AI Scheduling Agent**

   * Validate details.
   * Checks patient EMR in Google Sheets to see if they are new or returning.
   * Fetches doctor availability from Google Calendar.
   * Books appointment if slot is available.
   * Collects insurance info.

3. **Email Communication Tool**

   * Sends confirmation emails through Gmail.
   * For new patients, also sends intake form + calendar link.
   * For returning patients, sends appointment confirmation.

4. **Format Appointment Data & Admin Booking Export**

   * Appointment data is structured and pushed into admin Google Sheet.

5. **Reminder System**

   * A schedule trigger runs daily.
   * Gets appointments from Google Sheets.
   * Reminder Agent (Gemini model) decides type of reminder: simple or advanced.
   * If advanced, checks if forms are completed and if appointment confirmed.
   * Sends reminder emails accordingly.

---

## Gradio Frontend

* File: `gradio.py`
* Uses `gr.Interface` for chat UI.
* For every user input, it POST request to the n8n webhook URL.
* Response from n8n is displayed back in the Gradio app.

To run:

```bash
pip install gradio requests
python gradio.py
```

---

## How it works end-to-end

1. User opens Gradio app and type appointment request.
2. Input is sent to n8n webhook.
3. AI Scheduling Agent handles the chat, validates details, checks Google Sheets and Google Calendar.
4. If patient is new → ask for email, then send confirmation + intake form.
5. Appointment booked and exported to admin sheet.
6. Reminders are automatically triggered daily using Reminder Agent and Gmail.

---
