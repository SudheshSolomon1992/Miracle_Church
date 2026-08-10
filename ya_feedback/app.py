import json
import os
from datetime import datetime

import gspread
import streamlit as st
from dotenv import load_dotenv
from google.oauth2.service_account import Credentials

load_dotenv()

SERVICE_ACCOUNT_FILE = os.getenv("GOOGLE_SERVICE_ACCOUNT_FILE", "credentials.json")
SERVICE_ACCOUNT_JSON = os.getenv("GOOGLE_SERVICE_ACCOUNT_JSON")
SHEET_URL = os.getenv("GOOGLE_SHEET_URL")
WORKSHEET_NAME = os.getenv("GOOGLE_WORKSHEET_NAME", "Feedback")
CONFIG_FILE = os.getenv("FORM_CONFIG_FILE", "form_config.json")


def get_service_credentials():
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        return Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE)

    if SERVICE_ACCOUNT_JSON:
        service_account_info = json.loads(SERVICE_ACCOUNT_JSON)
        return Credentials.from_service_account_info(service_account_info)

    try:
        secret_data = st.secrets["google"]["service_account_json"]
        return Credentials.from_service_account_info(secret_data)
    except Exception:
        raise FileNotFoundError(
            "No Google service account credentials were found. "
            "Use either a local credentials.json file, a GOOGLE_SERVICE_ACCOUNT_JSON env var, "
            "or Streamlit Cloud secrets for the Google service account JSON."
        )


@st.cache_resource
def get_gsheet_client():
    if not SHEET_URL:
        raise ValueError("Please set GOOGLE_SHEET_URL in your environment or .env file.")

    scope = ["https://www.googleapis.com/auth/spreadsheets"]
    credentials = get_service_credentials().with_scopes(scope)
    client = gspread.authorize(credentials)
    spreadsheet = client.open_by_url(SHEET_URL)
    worksheet = spreadsheet.worksheet(WORKSHEET_NAME)
    return worksheet


@st.cache_data
def load_config():
    if not os.path.exists(CONFIG_FILE):
        raise FileNotFoundError(
            f"Form config file not found: {CONFIG_FILE}. Please create a JSON config file."
        )

    with open(CONFIG_FILE, "r", encoding="utf-8") as config_file:
        return json.load(config_file)


st.set_page_config(page_title="Miracle Church Feedback", page_icon="💬", layout="wide")

config = load_config()

st.markdown(
    """
    <style>
        :root {
            --mc-blue-900: #0d3b6d;
            --mc-blue-700: #165aa6;
            --mc-blue-500: #2a72d5;
            --mc-blue-100: #dfeeff;
            --mc-red-700: #b91c1c;
            --mc-red-500: #d92d2d;
            --mc-red-100: #ffe5e5;
            --mc-red-150: #ffd1d1;
            --mc-text: #0d3b6d;
            --mc-accent: #b91c1c;
            --mc-border: #c9d9f6;
            --mc-surface: #edf5ff;
            --mc-surface-strong: #dcecff;
        }

        html, body {
            background: linear-gradient(180deg, var(--mc-blue-100) 0%, #eaf3ff 100%) !important;
            background-color: var(--mc-blue-100) !important;
            color: var(--mc-text) !important;
            color-scheme: light !important;
        }

        .stApp {
            background: linear-gradient(180deg, var(--mc-blue-100) 0%, #eaf3ff 100%) !important;
            background-color: var(--mc-blue-100) !important;
            color: var(--mc-text) !important;
            color-scheme: light !important;
        }

        [data-testid="stAppViewContainer"], [data-testid="stMain"], section.main, div.main,
        [data-testid="stVerticalBlockBorderWrapper"], [data-testid="stVerticalBlock"] {
            background: linear-gradient(180deg, var(--mc-blue-100) 0%, #eaf3ff 100%) !important;
            background-color: var(--mc-blue-100) !important;
            color: var(--mc-text) !important;
        }

        [data-testid="stForm"] {
            background: linear-gradient(180deg, #edf6ff 0%, #eef8ff 100%) !important;
            background-color: #edf6ff !important;
            border: 1px solid var(--mc-border) !important;
            border-radius: 22px !important;
            padding: 1rem 1rem 0.5rem 1rem !important;
            box-shadow: 0 10px 18px rgba(13, 59, 109, 0.08) !important;
        }

        .main .block-container {
            background: transparent !important;
            background-color: transparent !important;
            max-width: 1200px;
            padding-top: 2rem;
            padding-bottom: 3rem;
        }

        .brand-shell {
            display: flex;
            align-items: center;
            gap: 1rem;
            background: linear-gradient(135deg, var(--mc-blue-900), var(--mc-blue-700));
            border-radius: 22px;
            padding: 1.25rem 1.5rem;
            color: var(--mc-red-150);
            box-shadow: 0 12px 28px rgba(13, 59, 109, 0.12);
            border: 1px solid var(--mc-red-150);
            margin-bottom: 1.5rem;
        }

        .brand-badge {
            width: 58px;
            height: 58px;
            border-radius: 18px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-weight: 900;
            font-size: 1.15rem;
            background: linear-gradient(135deg, var(--mc-red-500), var(--mc-red-700));
            color: var(--mc-blue-100);
            box-shadow: inset 0 1px 0 #f9c6c6;
        }

        .eyebrow {
            font-size: 0.72rem;
            font-weight: 800;
            letter-spacing: 0.16rem;
            text-transform: uppercase;
            color: var(--mc-red-150);
            margin-bottom: 0.15rem;
        }

        h1 {
            margin: 0;
            font-size: clamp(2rem, 3vw, 2.7rem);
            line-height: 1.15;
            color: var(--mc-red-150) !important;
        }

        .subtext {
            color: #deebff;
            font-size: 1rem;
            margin-top: 0.45rem;
        }

        .form-card {
            background: linear-gradient(180deg, var(--mc-surface) 0%, #edf6ff 100%);
            border: 1px solid var(--mc-border);
            border-radius: 22px;
            padding: 1.5rem 1.5rem 0.5rem 1.5rem;
            box-shadow: 0 10px 18px rgba(13, 59, 109, 0.08);
        }

        .stForm {
            background: transparent;
        }

        .stTextInput > div > div > input,
        .stTextArea > div > div > textarea,
        .stSelectbox > div > div > select,
        .stMultiSelect > div > div > div,
        .stRadio > div {
            border-radius: 12px !important;
            border: 2px solid var(--mc-red-500) !important;
            background: var(--mc-blue-100) !important;
            color: var(--mc-text) !important;
            box-shadow: none !important;
        }

        .stTextArea > div > div > textarea {
            border: 2px solid var(--mc-red-500) !important;
        }

        .stTextInput label, .stSelectbox label, .stMultiSelect label, .stRadio > label,
        .stTextArea label {
            color: var(--mc-blue-900) !important;
            font-weight: 800 !important;
            font-size: 0.98rem !important;
            margin-bottom: 0.45rem;
        }

        .stTextInput input::placeholder,
        .stTextArea textarea::placeholder {
            color: var(--mc-blue-700) !important;
        }

        .stRadio > div {
            background: var(--mc-blue-100);
            border-radius: 12px;
            padding: 0.4rem 0.5rem;
            border: 1px solid var(--mc-red-150);
        }

        .stButton > button {
            background: linear-gradient(135deg, var(--mc-red-700), var(--mc-red-500));
            color: var(--mc-blue-100);
            border: none;
            border-radius: 12px;
            font-weight: 800;
            font-size: 1rem;
            padding: 0.8rem 1.4rem;
            box-shadow: 0 10px 18px rgba(185, 28, 28, 0.18);
            transition: transform 0.15s ease;
        }

        .stButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 12px 20px rgba(185, 28, 28, 0.22);
        }

        div[data-testid="stHorizontalBlock"] {
            gap: 0.75rem;
        }

        .stAlert {
            border-radius: 14px;
            border: 1px solid var(--mc-border);
        }

        .stInfo {
            background: var(--mc-blue-100) !important;
            color: var(--mc-blue-900) !important;
        }

        .stSuccess {
            background: #e8f7ef !important;
            color: #0d4d3a !important;
            border: 1px solid #7ec9a4 !important;
        }

        .stError {
            background: var(--mc-red-100) !important;
            color: var(--mc-red-700) !important;
            border: 1px solid var(--mc-red-500) !important;
        }

        .stWarning {
            background: #fff0d9 !important;
            color: #8a4a00 !important;
            border: 1px solid #d98200 !important;
        }

        [data-testid="stSidebar"] {
            display: none !important;
        }

        @media (max-width: 768px) {
            .main .block-container {
                padding-left: 0.75rem !important;
                padding-right: 0.75rem !important;
            }

            .brand-shell {
                padding: 1rem 1rem !important;
                align-items: flex-start !important;
            }

            h1 {
                font-size: 1.8rem !important;
                line-height: 1.2 !important;
            }

            .subtext {
                font-size: 0.92rem !important;
            }

            .stButton > button {
                width: 100% !important;
                font-size: 0.96rem !important;
            }

            .stRadio > div {
                display: block !important;
                padding: 0.25rem 0.35rem !important;
            }

            .stRadio > div > label {
                width: 100% !important;
                display: flex !important;
                align-items: center !important;
            }

            .stTextInput > div > div > input,
            .stTextArea > div > div > textarea,
            .stSelectbox > div > div > select,
            .stMultiSelect > div > div > div {
                font-size: 1rem !important;
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

config = load_config()

title = config.get("title", "Church Feedback Form")
description = config.get("description", "Please complete the form below.")

st.markdown(
    f"""
    <div class="brand-shell" style="padding-left: 1.25rem;">
      <div>
        <h1>Young Adults Fellowship Feedback</h1>
        <div class="subtext">{description}</div>
      </div>
    </div>
    """,
    unsafe_allow_html=True,
)

fields = config.get("fields", [])

responses = {}

with st.container():
    st.markdown('<div class="form-card">', unsafe_allow_html=True)
    with st.form("feedback_form", clear_on_submit=True):
        for field in fields:
            field_name = field["name"]
            field_label = field["label"]
            field_type = field["type"]
            required = field.get("required", False)

            if field_type == "text":
                responses[field_name] = st.text_area(
                    field_label,
                    key=field_name,
                    height=110,
                    help="Optional details are welcome." if not required else None,
                )
            elif field_type == "dropdown":
                responses[field_name] = st.selectbox(
                    field_label,
                    field.get("options", []),
                    key=field_name,
                )
            elif field_type == "radio":
                responses[field_name] = st.radio(
                    field_label,
                    field.get("options", []),
                    key=field_name,
                    horizontal=True,
                )
            elif field_type == "checkbox":
                responses[field_name] = st.multiselect(
                    field_label,
                    field.get("options", []),
                    key=field_name,
                )

        submitted = st.form_submit_button("Submit feedback")
    st.markdown('</div>', unsafe_allow_html=True)

if submitted:
    missing_required = []
    for field in fields:
        field_name = field["name"]
        field_value = responses.get(field_name, "")

        if field.get("required", False):
            if field["type"] == "checkbox" and not field_value:
                missing_required.append(field["label"])
            elif not str(field_value).strip():
                missing_required.append(field["label"])

    if missing_required:
        st.error("Please complete the following required fields: " + ", ".join(missing_required))
    else:
        try:
            worksheet = get_gsheet_client()
            row = [datetime.now().strftime("%Y-%m-%d %H:%M:%S")]
            for field in fields:
                value = responses.get(field["name"], "")
                if isinstance(value, list):
                    value = ", ".join(value)
                row.append(str(value).strip())

            worksheet.append_row(row, value_input_option="USER_ENTERED")
            st.success("Thank you! Your response has been submitted successfully.")
            st.balloons()
        except Exception as exc:
            st.error(f"There was a problem sending your feedback to Google Sheets: {exc}")

st.markdown("---")
st.info("This form stores submissions in a Google Sheet using a Google service account and the Google Sheets API.")
