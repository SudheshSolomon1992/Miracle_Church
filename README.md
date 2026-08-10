# Church Feedback Streamlit App

This project is a simple Streamlit-based feedback form for a church or ministry team. It is designed to be anonymous and stores each submission in a Google Sheet without collecting personal information from the user.

## What it does

- Displays a clean anonymous feedback form in the browser
- Collects only survey responses defined in the config file
- Saves every form submission into a Google Sheet automatically

## Project structure

- `app.py` – Streamlit application UI and Google Sheets submission logic
- `form_config.json` – Defines the survey title, description, and dynamic fields
- `requirements.txt` – Python dependencies
- `.env.example` – Example environment variables
- `.gitignore` – Ignore secrets and local files

## Prerequisites

Before you run the app, make sure you have:

1. Python 3.10+ installed
2. A Google Cloud project
3. A Google Sheet that you want to write into
4. A Google service account JSON key with access to the sheet

## Step-by-step setup

### 1. Create a folder for the project

Create a new folder next to your current repository, for example:

```bash
c:\Users\sudhe\Documents\Miracle Church\church-feedback-streamlit
```

### 2. Create and activate a virtual environment

From inside the project folder:

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Create a Google Sheet

1. Open Google Sheets.
2. Create a new spreadsheet.
3. Name the first worksheet `Feedback`.
4. Add these headers in row 1:

```text
Timestamp | Name | Email | Category | Rating | Message | Consent
```

### 5. Create a Google Cloud service account

1. Go to the Google Cloud Console.
2. Create a new project or use an existing one.
3. Enable the Google Sheets API.
4. Create a service account.
5. Create a JSON key for that service account.
6. Download the JSON file and save it inside your project folder as `credentials.json`.

### 6. Share the Google Sheet with the service account

1. Open the spreadsheet.
2. Click Share.
3. Add the service account email from the JSON file.
4. Give it Editor access.

### 7. Configure environment variables

Copy `.env.example` to `.env` and fill in your values:

```bash
copy .env.example .env
```

Edit `.env` and replace the sample values with your sheet details.

Example:

```env
GOOGLE_SERVICE_ACCOUNT_FILE=credentials.json
GOOGLE_SERVICE_ACCOUNT_JSON=
GOOGLE_SHEET_URL=https://docs.google.com/spreadsheets/d/your-sheet-id/edit
GOOGLE_WORKSHEET_NAME=Feedback
FORM_CONFIG_FILE=form_config.json
```

### 8. Configure the form questions

The form fields are driven by `form_config.json`.

Example file:

```json
{
  "title": "Young Adults Fellowship Monthly Feedback",
  "description": "Tell us how the monthly young adults fellowship is going and what topics you would like to see next.",
  "fields": [
    {
      "name": "full_name",
      "label": "Full name",
      "type": "text",
      "required": true
    },
    {
      "name": "attendance_status",
      "label": "Did you attend the last fellowship?",
      "type": "radio",
      "options": ["Yes", "No"],
      "required": true
    },
    {
      "name": "favorite_topic",
      "label": "What topic did you enjoy most?",
      "type": "dropdown",
      "options": ["Bible Study", "Prayer", "Testimony Sharing", "Leadership Session", "Games and Fellowship", "Other"],
      "required": true
    },
    {
      "name": "improvement_suggestion",
      "label": "What would you like to improve for the next fellowship?",
      "type": "text",
      "required": true
    }
  ]
}
```

Supported field types:

- `text`
- `dropdown`
- `radio`
- `checkbox` for multi-select questions, stored as a comma-separated value in one cell

### 9. Run the app

Start the Streamlit app with:

```bash
streamlit run app.py
```

Your browser will open the app automatically. Complete the form and submit it to store the entry in your Google Sheet.

## Notes

- Do not commit your `credentials.json` file or `.env` file to Git.
- For Streamlit Community Cloud, keep the service account JSON in secret storage rather than in the repository.
- If your sheet is not found, confirm that the service account email has Editor permissions.
- If the app fails to authenticate, make sure the Google Sheets API is enabled in your Google Cloud project.

## Secure deployment for Streamlit Community Cloud

To keep the Google credentials private while deploying a public app:

1. Push the app code to GitHub.
2. In Streamlit Community Cloud, open the app settings.
3. Add a secret named `google` with a key named `service_account_json`.
4. Use the full JSON object from your downloaded Google service account key.
5. Do not store the JSON key in the repo.

Example secret structure:

```toml
[google]
service_account_json = "{\"type\": \"service_account\", ... }"
```

This keeps the service account credentials private while still allowing your public Streamlit app to write to Google Sheets.

## Common troubleshooting

### Error: `FileNotFoundError` for credentials

This means the path in `GOOGLE_SERVICE_ACCOUNT_FILE` is incorrect or the JSON file is missing.

### Error: `Spreadsheet not found`

Check that the `GOOGLE_SHEET_URL` points to the correct spreadsheet.

### Error: permission denied

Make sure the service account email is shared on the sheet with Editor access.
