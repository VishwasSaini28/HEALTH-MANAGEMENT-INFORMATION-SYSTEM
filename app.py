from pathlib import Path
import streamlit as st
import sqlite3
import uuid
from datetime import datetime, date
import pandas as pd
import plotly.express as px

# ============================================================
# HIMS - PROFESSIONAL STREAMLIT APPLICATION
# Doctor Portal + Patient Registration Chatbot
# Validation uses if / elif / else only. No regular expressions.
# ============================================================

st.set_page_config(
    page_title="HIMS | Doctor Portal",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded",
)

BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "hims.db"

# ============================================================
# PROFESSIONAL UI
# ============================================================

st.markdown("""
<style>
/* ---------- Global ---------- */
/* ---------- Global ---------- */
.stApp {
    background: #FDF6F0;   /* pastel cream background */
    color: #333333;        /* dark gray text */
}
.block-container {
    max-width: 1450px;
    padding: 1.6rem 2.3rem 3rem;
}
#MainMenu, footer {visibility:hidden;}

h1, h2, h3, h4 {
    color: #333333 !important;
    letter-spacing: -0.35px;
}
p, label, .stCaption {
    color: #555555;
}



/* ---------- Buttons ---------- */
.stButton > button {
    border-radius:10px;
    min-height:42px;
    font-weight:700;
    border:1px solid #f8cdd0;
    background:#ffffff;
    color:#444;
    transition:.15s ease;
}
.stButton > button:hover {
    border-color:#FF0000;
    color:#FF0000;
}
.stButton > button[kind="primary"] {
    background: linear-gradient(135deg,#FF0000,#FF6666) !important;
    color:#ffffff !important;
    border:0 !important;
    box-shadow:0 8px 18px rgba(255,0,0,.20);
}

/* ---------- Sidebar ---------- */
section[data-testid="stSidebar"] {
    background: #E6F0FA; /* pastel blue */
    border-right: 1px solid #B3D1F2;
}
.sidebar-logo {
    background: linear-gradient(135deg,#FF0000,#FF6666); /* red gradient */
    box-shadow: 0 8px 20px rgba(255,0,0,.22);
}
.sidebar-title, .sidebar-sub, .sidebar-section {
    color: #000000 !important; /* black text */
}

/* ---------- KPI Headings ---------- */
.kpi-label {
    font-weight: 900 !important;        /* bold text */
    color: #004C99 !important;          /* deep pastel blue for contrast */
    text-transform: uppercase;
    letter-spacing: 0.8px;
}

/* ---------- KPI Values ---------- */
.kpi-value {
    font-weight: 850 !important;
    color: #000000 !important;          /* black for clarity */
}

/* ---------- KPI Notes ---------- */
.kpi-note {
    color: #333333 !important;          /* darker gray for readability */
}

/* ---------- Section Titles ---------- */
.section-title {
    font-weight: 900 !important;
    color: #004C99 !important;          /* same deep blue for consistency */
}

/* ---------- Section Subtitles ---------- */
.section-subtitle {
    color: #000000 !important;          /* black text */
    font-weight: 600 !important;
}


/* ---------- Hero ---------- */
.hero {
    background: linear-gradient(135deg,#E6F0FA 0%,#B3D1F2 55%,#A7C7E7 100%);
    border-radius: 20px;
    padding: 28px 31px;
    color: #000000; /* black text */
    box-shadow: 0 14px 32px rgba(100,150,200,.16);
    margin-bottom: 20px;
}
.hero h1, .hero p, .hero-kicker {
    color: #000000 !important;
}


/* ---------- Inputs / Controls ---------- */
.stTextInput input,
.stTextArea textarea,
.stDateInput input,
.stTimeInput input,
[data-baseweb="input"] input,
[data-baseweb="textarea"] textarea,
[data-baseweb="select"] input,
[data-baseweb="select"] [role="combobox"] {
    color: #000000 !important;                /* black text */
    -webkit-text-fill-color: #000000 !important;
    background-color: #E6F0FA !important;     /* pastel blue background */
    caret-color: #FF0000 !important;          /* red caret */
    border-radius: 9px !important;
}

.stTextInput > div,
.stTextArea > div,
.stDateInput > div,
.stTimeInput > div,
[data-baseweb="input"] > div,
[data-baseweb="textarea"] > div,
[data-baseweb="select"] > div {
    background-color: #E6F0FA !important;
    border-color: #B3D1F2 !important;         /* pastel blue border */
}

.stTextInput input::placeholder,
.stTextArea textarea::placeholder,
[data-baseweb="input"] input::placeholder,
[data-baseweb="textarea"] textarea::placeholder {
    color: #000000 !important;                /* black placeholder */
    -webkit-text-fill-color: #000000 !important;
    opacity: 1 !important;
}

.stTextInput input:focus,
.stTextArea textarea:focus,
.stDateInput input:focus,
.stTimeInput input:focus,
[data-baseweb="input"] input:focus,
[data-baseweb="textarea"] textarea:focus {
    color: #000000 !important;
    -webkit-text-fill-color: #000000 !important;
    border-color: #FF0000 !important;         /* red border on focus */
    box-shadow: 0 0 0 3px rgba(255,0,0,.15) !important; /* red glow */
    outline: none !important;
}

/* Selectbox, radio and checkbox labels/options */
[data-baseweb="select"] *,
[data-baseweb="popover"] *,
[role="option"],
[role="listbox"] *,
.stRadio label,
.stRadio label p,
.stCheckbox label,
.stCheckbox label p {
    color: #000000 !important;                /* black labels */
}

/* Make arrows/icons red */
.stSelectbox div[data-baseweb="select"] svg,
.stDateInput svg,
.stTimeInput svg {
    fill: #FF0000 !important;
}

/* Buttons */
.stButton > button,
.stDownloadButton > button,
button[kind] {
    color: #000000 !important;                /* black text */
    -webkit-text-fill-color: #000000 !important;
    background-color: #E6F0FA !important;     /* pastel blue background */
}

.stButton > button[kind="primary"],
button[kind="primary"] {
    background: linear-gradient(135deg,#FF0000,#FF6666) !important;
    color: #ffffff !important;
    -webkit-text-fill-color: #ffffff !important;
}

.stButton > button:hover {
    color: #FF0000 !important;
    -webkit-text-fill-color: #FF0000 !important;
    border-color: #FF0000 !important;
}

/* Browser autofill */
.stTextInput input:-webkit-autofill,
.stTextInput input:-webkit-autofill:hover,
.stTextInput input:-webkit-autofill:focus,
.stTextInput input:-webkit-autofill:active {
    -webkit-text-fill-color: #000000 !important;
    -webkit-box-shadow: 0 0 0 1000px #E6F0FA inset !important;
    box-shadow: 0 0 0 1000px #E6F0FA inset !important;
}

/* ---------- Tables ---------- */
[data-testid="stDataFrame"] {
    border:1px solid #B3D1F2;
    border-radius:12px;
    overflow:hidden;
    background-color: #E6F0FA;
}


/* ---------- Hide empty top gap ---------- */
div[data-testid="stVerticalBlock"] > div:has(> div.stMarkdown) {
    max-width:100%;
}
</style>
""", unsafe_allow_html=True)



# DATABASE
# ============================================================
# DATABASE (SQLite version)
# ============================================================

import sqlite3
import streamlit as st
import pandas as pd
from datetime import datetime

DB_PATH = "hims.db"   # local file, will be created if not exists

def db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row  # return rows as dict-like objects
    return conn

# --- Initialize database ---
def init_db():
    conn = db()
    cur = conn.cursor()

    # Doctors table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS doctors (
            doctor_id TEXT PRIMARY KEY,
            doctor_name TEXT NOT NULL,
            department TEXT NOT NULL,
            specialty TEXT,
            room TEXT,
            password TEXT DEFAULT '1234'
        )
    """)

    # Patients table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            patient_id TEXT PRIMARY KEY,
            fullname TEXT,
            dob DATE,
            age INTEGER,
            gender TEXT,
            marital_status TEXT,
            mobile TEXT,
            email TEXT,
            aadhaar TEXT,
            address TEXT,
            area TEXT,
            city TEXT,
            state TEXT,
            pincode TEXT,
            blood_group TEXT,
            emergency_name TEXT,
            emergency_number TEXT,
            symptoms TEXT,
            symptom_duration TEXT,
            current_condition TEXT,
            allergies TEXT,
            previous_surgery TEXT,
            family_history TEXT,
            has_insurance TEXT,
            insurance_provider TEXT,
            policy_number TEXT,
            insurance_validity DATE,
            department TEXT,
            preferred_doctor TEXT,
            appointment_date DATE,
            appointment_time TIME,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    # Seed doctors
    doctors = [
        ("RAK001", "Dr. Rakesh", "Cardiology", "Cardiologist", "Room 101", "1234"),
        ("MAD001", "Dr. Madan", "Physiology", "Physician", "Room 102", "1234"),
        ("PRI001", "Dr. Priya", "Dermatology", "Dermatologist", "Room 103", "1234"),
        ("ANI001", "Dr. Anil", "Neurology", "Neurologist", "Room 104", "1234"),
    ]

    for doctor in doctors:
        cur.execute("""
            INSERT OR IGNORE INTO doctors
            (doctor_id, doctor_name, department, specialty, room, password)
            VALUES (?, ?, ?, ?, ?, ?)
        """, doctor)

    conn.commit()
    conn.close()

# --- Query helpers ---
def get_doctor(doctor_id):
    conn = db()
    row = conn.execute(
        "SELECT * FROM doctors WHERE UPPER(doctor_id)=UPPER(?)",
        (doctor_id,)
    ).fetchone()
    conn.close()
    return dict(row) if row else None

def get_doctors():
    conn = db()
    rows = conn.execute(
        "SELECT doctor_id, doctor_name, department FROM doctors ORDER BY doctor_name"
    ).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_patient_df(doctor_id=None, today_only=False, upcoming=False):
    conn = db()
    today = datetime.now().strftime("%Y-%m-%d")

    if doctor_id:
        if today_only:
            query = """
                SELECT * FROM patients
                WHERE UPPER(preferred_doctor)=UPPER(?)
                  AND appointment_date=?
                ORDER BY appointment_time
            """
            rows = conn.execute(query, (doctor_id, today)).fetchall()
        elif upcoming:
            query = """
                SELECT * FROM patients
                WHERE UPPER(preferred_doctor)=UPPER(?)
                  AND appointment_date>=?
                ORDER BY appointment_date, appointment_time
            """
            rows = conn.execute(query, (doctor_id, today)).fetchall()
        else:
            rows = conn.execute("""
                SELECT * FROM patients
                WHERE UPPER(preferred_doctor)=UPPER(?)
                ORDER BY appointment_date DESC, appointment_time DESC
            """, (doctor_id,)).fetchall()
    else:
        rows = conn.execute("""
            SELECT * FROM patients
            ORDER BY appointment_date DESC, appointment_time DESC
        """).fetchall()

    conn.close()
    return pd.DataFrame([dict(r) for r in rows])
# ============================================================
# IF / ELSE VALIDATION — NO REGEX
# ============================================================

def valid_date(value):
    if value == "":
        return False
    try:
        datetime.strptime(value, "%Y-%m-%d")
        return True
    except ValueError:
        return False


def valid_time(value):
    if value == "":
        return False
    try:
        datetime.strptime(value, "%H:%M")
        return True
    except ValueError:
        return False


def validate(field, value):
    value = str(value).strip()

    if field in ["fullname", "emergency_name", "city", "state"]:
        if value == "":
            return False, "This field cannot be empty."
        elif not value.replace(" ", "").isalpha():
            return False, "Use letters and spaces only."

    elif field == "dob":
        if not valid_date(value):
            return False, "Enter a valid date in YYYY-MM-DD format."

    elif field == "age":
        if not value.isdigit():
            return False, "Age must contain numbers only."
        elif int(value) < 1 or int(value) > 120:
            return False, "Age must be between 1 and 120."

    elif field == "gender":
        if value.lower() not in ["male", "female", "other", "m", "f", "o"]:
            return False, "Choose Male, Female or Other."

    elif field == "marital_status":
        if value.lower() not in [
            "single", "married", "divorced", "widowed", "separated"
        ]:
            return False, "Enter a valid marital status."

    elif field in ["mobile", "emergency_number"]:
        if len(value) != 10:
            return False, "Number must contain exactly 10 digits."
        elif not value.isdigit():
            return False, "Number must contain digits only."
        elif value[0] not in "6789":
            return False, "Enter a valid Indian mobile number."

    elif field == "email":
        if value.count("@") != 1:
            return False, "Enter a valid email address."
        parts = value.split("@")
        if parts[0] == "" or parts[1] == "":
            return False, "Enter a valid email address."
        elif "." not in parts[1]:
            return False, "Email domain must contain a dot."
        elif parts[1].startswith(".") or parts[1].endswith("."):
            return False, "Enter a valid email address."

    elif field == "aadhaar":
        if len(value) != 12:
            return False, "Aadhaar must contain exactly 12 digits."
        elif not value.isdigit():
            return False, "Aadhaar must contain digits only."

    elif field == "pincode":
        if len(value) != 6:
            return False, "Pincode must contain exactly 6 digits."
        elif not value.isdigit():
            return False, "Pincode must contain digits only."

    elif field == "blood_group":
        if value.upper() not in [
            "A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"
        ]:
            return False, "Enter a valid blood group."

    elif field == "has_insurance":
        if value.lower() not in ["yes", "no"]:
            return False, "Choose Yes or No."

    elif field == "insurance_validity":
        if not valid_date(value):
            return False, "Enter a valid date in YYYY-MM-DD format."

    elif field == "preferred_doctor":
        doctor = get_doctor(value.upper())
        if not doctor:
            return False, "Doctor ID not found."

    elif field == "appointment_date":
        if not valid_date(value):
            return False, "Enter a valid date in YYYY-MM-DD format."

    elif field == "appointment_time":
        if not valid_time(value):
            return False, "Use HH:MM format, for example 14:30."

    elif field in [
        "address", "area", "symptoms", "symptom_duration",
        "current_condition", "department"
    ]:
        if value == "":
            return False, "This field cannot be empty."

    return True, ""


def assign_department(symptoms):
    text = symptoms.lower()

    if "chest" in text or "heart" in text:
        return "Cardiology"
    elif "bone" in text or "fracture" in text:
        return "Orthopedics"
    elif "skin" in text or "rash" in text:
        return "Dermatology"
    elif "eye" in text or "vision" in text:
        return "Ophthalmology"
    elif "brain" in text or "headache" in text:
        return "Neurology"
    else:
        return "General Medicine"


# ============================================================
# PATIENT CHATBOT
# ============================================================

QUESTIONS = [
    ("fullname", "What is your full name?"),
    ("dob", "What is your date of birth?"),
    ("age", "What is your age?"),
    ("gender", "What is your gender?"),
    ("marital_status", "What is your marital status?"),
    ("mobile", "What is your 10-digit mobile number?"),
    ("email", "What is your email address?"),
    ("aadhaar", "What is your 12-digit Aadhaar number?"),
    ("address", "What is your house number / street?"),
    ("area", "What is your area / locality?"),
    ("city", "What city do you live in?"),
    ("state", "What state do you live in?"),
    ("pincode", "What is your 6-digit pincode?"),
    ("blood_group", "What is your blood group?"),
    ("emergency_name", "Who is your emergency contact?"),
    ("emergency_number", "What is the emergency contact number?"),
    ("symptoms", "Please describe your symptoms."),
    ("symptom_duration", "How long have you had these symptoms?"),
    ("current_condition", "Describe your current medical condition."),
    ("allergies", "Do you have any allergies? Type No if none."),
    ("previous_surgery", "Any previous surgery? Type No if none."),
    ("family_history", "Enter family medical history, or type No."),
    ("has_insurance", "Do you have health insurance?"),
    ("insurance_provider", "What is your insurance provider?"),
    ("policy_number", "What is your insurance policy number?"),
    ("insurance_validity", "What is the policy expiry date?"),
    ("department", "Which department do you prefer?"),
    ("preferred_doctor", "Which doctor would you like to consult?"),
    ("appointment_date", "What appointment date do you need?"),
    ("appointment_time", "What appointment time do you need?"),
]


def save_patient(data):
    patient_id = (
        "PAT"
        + datetime.now().strftime("%Y%m%d%H%M%S")
        + uuid.uuid4().hex[:4].upper()
    )

    auto_department = assign_department(data.get("symptoms", ""))
    department = data.get("department") or auto_department

    conn = db()
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO patients (
            patient_id, fullname, dob, age, gender, marital_status,
            mobile, email, aadhaar, address, area, city, state, pincode,
            blood_group, emergency_name, emergency_number, symptoms,
            symptom_duration, current_condition, allergies, previous_surgery,
            family_history, has_insurance, insurance_provider, policy_number,
            insurance_validity, department, preferred_doctor,
            appointment_date, appointment_time, created_at
        )
        VALUES (
            %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
    """, (
        patient_id,
        data.get("fullname"),
        data.get("dob"),
        int(data.get("age")),
        data.get("gender"),
        data.get("marital_status"),
        data.get("mobile"),
        data.get("email"),
        data.get("aadhaar"),
        data.get("address"),
        data.get("area"),
        data.get("city"),
        data.get("state"),
        data.get("pincode"),
        data.get("blood_group"),
        data.get("emergency_name"),
        data.get("emergency_number"),
        data.get("symptoms"),
        data.get("symptom_duration"),
        data.get("current_condition"),
        data.get("allergies"),
        data.get("previous_surgery"),
        data.get("family_history"),
        data.get("has_insurance"),
        data.get("insurance_provider"),
        data.get("policy_number"),
        data.get("insurance_validity"),
        department,
        data.get("preferred_doctor"),
        data.get("appointment_date"),
        data.get("appointment_time"),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ))

    conn.commit()
    cur.close()
    conn.close()

    return patient_id, auto_department, department
import streamlit as st
import pandas as pd
import uuid
from datetime import datetime, date

# --- Reset function ---
def reset_chat():
    for key in [
        "chat_step", "chat_data", "chat_done",
        "chat_patient_id", "chat_department"
    ]:
        st.session_state.pop(key, None)

# --- Chatbot page ---
def chatbot_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Patient Services</div>
        <h1>Patient Registration</h1>
        <p>Complete your HIMS registration through a guided, validated conversation.</p>
    </div>
    """, unsafe_allow_html=True)

    # Initialize session state
    if "chat_step" not in st.session_state:
        st.session_state.chat_step = 0
        st.session_state.chat_data = {}
        st.session_state.chat_done = False

    # If registration is complete
    if st.session_state.chat_done:
        st.success("Registration completed successfully.")

        st.markdown("""
        <div class="card">
            <div class="card-title">Registration Complete</div>
            <div class="card-subtitle">Your patient information has been saved in HIMS.</div>
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3 = st.columns(3)
        c1.metric("Patient ID", st.session_state.chat_patient_id)
        c2.metric("Department", st.session_state.chat_department)
        c3.metric("Status", "Registered")

        st.markdown("### Registration Summary")
        summary = st.session_state.chat_data.copy()
        hidden = ["aadhaar", "policy_number"]
        safe_summary = {
            k.replace("_", " ").title(): (
                "••••" + str(v)[-4:] if k in hidden and v else v
            )
            for k, v in summary.items()
        }
        st.dataframe(
            pd.DataFrame(list(safe_summary.items()), columns=["Field", "Value"]),
            use_container_width="stretch",
            hide_index=True,
        )

        if st.button("＋ Register Another Patient", type="primary"):
            reset_chat()
            st.rerun()
        return

    # Current step
    step = st.session_state.chat_step
    total = len(QUESTIONS)

    # ✅ Boundary check to prevent IndexError
    if step >= total:
        patient_id, auto_department, department = save_patient(st.session_state.chat_data)
        st.session_state.chat_patient_id = patient_id
        st.session_state.chat_department = department
        st.session_state.chat_done = True
        st.rerun()
        return

    # Ask current question
    field, question = QUESTIONS[step]
    left, main, right = st.columns([0.8, 2.6, 0.8])

    with main:
        st.markdown(
            f'<div class="chat-shell">'
            f'<div class="step-label">PATIENT INTAKE · STEP {step + 1} OF {total}</div>'
            f'<div style="margin-top:10px;">'
            f'<div class="bot-message">🤖 <b>HIMS Assistant</b><br>{question}</div>'
            f'</div></div>',
            unsafe_allow_html=True,
        )

        st.progress((step + 1) / total)

        # Input controls
        if field == "gender":
            answer = st.radio("Your answer", ["Male", "Female", "Other"],
                              horizontal=True, key=f"input_{field}")
        elif field == "marital_status":
            answer = st.selectbox("Your answer",
                                  ["Single", "Married", "Divorced", "Widowed", "Separated"],
                                  key=f"input_{field}")
        elif field == "has_insurance":
            answer = st.radio("Your answer", ["Yes", "No"],
                              horizontal=True, key=f"input_{field}")
        elif field == "blood_group":
            answer = st.selectbox("Your answer",
                                  ["A+", "A-", "B+", "B-", "AB+", "AB-", "O+", "O-"],
                                  key=f"input_{field}")
        elif field == "preferred_doctor":
            doctor_list = get_doctors()
            options = [f"{d['doctor_id']} — {d['doctor_name']} ({d['department']})"
                       for d in doctor_list]
            selected = st.selectbox("Choose doctor", options, key=f"input_{field}")
            answer = selected.split(" — ")[0]
        elif field == "department":
            answer = st.selectbox("Preferred department",
                                  ["General Medicine", "Cardiology", "Orthopedics",
                                   "Dermatology", "Ophthalmology", "Neurology", "Physiology"],
                                  key=f"input_{field}")
        elif field in ["dob", "insurance_validity", "appointment_date"]:
            selected_date = st.date_input("Your answer", value=date.today(), key=f"input_{field}")
            answer = selected_date.strftime("%Y-%m-%d")
        elif field == "appointment_time":
            selected_time = st.time_input("Your answer", value=datetime.now().time(), key=f"input_{field}")
            answer = selected_time.strftime("%H:%M")
        elif field in ["symptoms", "current_condition", "allergies",
                       "previous_surgery", "family_history", "address"]:
            answer = st.text_area("Your answer", key=f"input_{field}", height=100)
        else:
            answer = st.text_input("Your answer", key=f"input_{field}",
                                   placeholder="Type your answer here...")

        if field == "has_insurance" and str(answer).lower() == "no":
            st.caption("Insurance details will be skipped.")

        if st.button("Continue  →", type="primary", use_container_width="stretch"):
            ok, message = validate(field, answer)
            if not ok:
                st.error(message)
                return

            st.session_state.chat_data[field] = str(answer).strip()

            # Conditional insurance flow
            if field == "has_insurance" and str(answer).lower() == "no":
                st.session_state.chat_data["insurance_provider"] = ""
                st.session_state.chat_data["policy_number"] = ""
                st.session_state.chat_data["insurance_validity"] = ""
                st.session_state.chat_step += 4
            else:
                st.session_state.chat_step += 1

            st.rerun()


# ============================================================
# LOGIN
# ============================================================

def login_page():
    st.markdown("""
    <style>
    /* --- Doctor Portal Styling (Blue Theme) --- */
    .login-card {
        background: #E6F0FA;
        border-radius: 20px;
        box-shadow: 0 10px 25px rgba(0, 102, 204, 0.25);
        padding: 40px 50px;
        text-align: center;
        margin: 40px auto;
        width: 600px;
    }

    .login-title {
        font-size: 36px;
        font-weight: 800;
        color: #000000;
        margin-bottom: 10px;
    }

    .login-sub {
        font-size: 16px;
        color: #333;
        margin-bottom: 30px;
    }

    .stTextInput > div > div > input {
        background-color: #F8FBFF !important;
        border: 1px solid #B3D1F2 !important;
        border-radius: 10px !important;
        color: #000 !important;
    }

    .stTextInput label {
        font-weight: 600;
        color: #333;
    }

    .stButton > button {
        background: linear-gradient(90deg, #FF0000, #FF6666);
        color: white;
        font-weight: 600;
        border-radius: 10px;
        padding: 10px 0;
        box-shadow: 0 6px 15px rgba(255, 0, 0, 0.25);
        border: none;
    }

    .stButton > button:hover {
        background: linear-gradient(90deg, #FF6666, #FF0000);
    }
    </style>
    """, unsafe_allow_html=True)

    st.markdown("""
    <div class="login-card">
        <div style="background: #E6F0FA; border-radius: 20px; padding: 25px;">
            <div class="login-title">Doctor Portal</div>
            <div class="login-sub">
                Sign in to view your patient queue and clinical dashboard.
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1, 1.4, 1])
    with center:
        doctor_id = st.text_input("Doctor ID", placeholder="Example: RAK001", key="login_doctor")
        password = st.text_input("Password", type="password", placeholder="Enter password", key="login_password")

        if st.button("Sign In →", use_container_width="stretch"):
            doctor = get_doctor(doctor_id.strip().upper())
            if doctor and password == doctor["password"]:
                st.session_state.logged_in = True
                st.session_state.doctor_id = doctor["doctor_id"]
                st.session_state.page = "Dashboard"
                st.rerun()
            else:
                st.error("Invalid Doctor ID or password.")

# ============================================================
# DOCTOR DASHBOARD
# ============================================================


def kpi(label, value, icon, note):
    st.markdown(f"""
    <div class="kpi-card">
        <div class="kpi-top">
            <div class="kpi-label">{label}</div>
            <div class="kpi-icon">{icon}</div>
        </div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-note">{note}</div>
    </div>
    """, unsafe_allow_html=True)


def dashboard_page():
    doctor_id = st.session_state.doctor_id
    doctor = get_doctor(doctor_id)

    today = datetime.now().strftime("%Y-%m-%d")

    assigned = get_patient_df(doctor_id=doctor_id)
    today_df = get_patient_df(doctor_id=doctor_id, today_only=True)
    upcoming_df = get_patient_df(doctor_id=doctor_id, upcoming=True)

    st.markdown(f"""
    <div class="hero">
        <div class="hero-kicker">Doctor Workspace · {doctor['doctor_id']}</div>
        <h1>Good day, {doctor['doctor_name']} 👋</h1>
        <p>{doctor['specialty']} · {doctor['department']} · {doctor['room']} · {today}</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        kpi("Today's Queue", len(today_df), "👥", "Patients scheduled today")
    with c2:
        kpi("Total Assigned", len(assigned), "📋", "Patients assigned to you")
    with c3:
        if not assigned.empty and "age" in assigned:
            avg_age = assigned["age"].dropna().mean()
            value = f"{avg_age:.1f}" if pd.notna(avg_age) else "—"
        else:
            value = "—"
        kpi("Average Age", value, "◌", "Years across assigned patients")
    with c4:
        if not assigned.empty:
            insured = assigned["has_insurance"].fillna("").astype(str).str.lower().eq("yes").sum()
            rate = (insured / len(assigned)) * 100
            value = f"{rate:.0f}%"
        else:
            value = "0%"
        kpi("Insurance Rate", value, "✓", "Among assigned patients")

    st.markdown("""
    <div class="section-head">
        <div>
            <div class="section-title">Today's Patient Queue</div>
            <div class="section-subtitle">Patients currently scheduled to see you today</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if today_df.empty:
        st.markdown("""
        <div class="card">
            <div class="card-title">No patients scheduled today</div>
            <div class="card-subtitle">Your queue is currently clear.</div>
        </div>
        """, unsafe_allow_html=True)
    else:
        for _, patient in today_df.iterrows():
            with st.container():
                a, b, c, d = st.columns([1, 2.3, 2.3, 1.3])

                with a:
                    st.markdown(
                        f'<div class="queue-time">🕐 {patient["appointment_time"]}</div>',
                        unsafe_allow_html=True,
                    )
                with b:
                    st.markdown(
                        f'<div class="queue-name">{patient["fullname"]}</div>'
                        f'<div class="queue-meta">{patient["patient_id"]} · '
                        f'{patient["age"]} yrs · {patient["gender"]}</div>',
                        unsafe_allow_html=True,
                    )
                with c:
                    symptom = str(patient["symptoms"] or "Not provided")
                    st.markdown(
                        f'<span class="symptom-chip">{symptom[:70]}</span>',
                        unsafe_allow_html=True,
                    )
                with d:
                    st.caption(str(patient["department"] or doctor["department"]))

    st.markdown("""
    <div class="section-head">
        <div>
            <div class="section-title">Clinical Overview</div>
            <div class="section-subtitle">Demographics and patient distribution</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    chart1, chart2 = st.columns(2)

    with chart1:
        st.markdown(
            '<div class="card"><div class="card-title">Patients by Gender</div>'
            '<div class="card-subtitle">Your assigned patient population</div></div>',
            unsafe_allow_html=True,
        )
        if not assigned.empty:
            gender = (
                assigned["gender"].fillna("Unknown")
                .replace({"m": "Male", "f": "Female", "o": "Other"})
                .value_counts()
                .reset_index()
            )
            gender.columns = ["Gender", "Patients"]
            fig = px.bar(
                gender, x="Gender", y="Patients",
                text="Patients",
                template="plotly_white",
            )
            fig.update_layout(
    		height=300,
    		margin=dict(l=10, r=10, t=15, b=10),
    		showlegend=False,
    		paper_bgcolor="rgba(0,0,0,0)",
    		plot_bgcolor="rgba(0,0,0,0)",
    		font=dict(color="#000000", size=12),  # black text globally
    		xaxis=dict(
        	    color="#000000",                   # black axis labels
        	    tickfont=dict(color="#000000", size=11, family="sans-serif"),
		    title=dict(
			text="Gender",
        	    	font=dict(color="#000000", size=12, family="sans-serif")
    		    )
		),
   		 yaxis=dict(
        	     color="#000000",
        	     tickfont=dict(color="#000000", size=11, family="sans-serif"),
		     title=dict(
			text="Patients", 
        	        font=dict(color="#000000", size=12, family="sans-serif")
  		     )
	       	 )
	     )


            
            fig.update_traces(
                marker_color="#A7C7E7",
		textfont=dict(color="#000000", size=12),
                textposition="outside",
            )
            st.plotly_chart(fig, use_container_width="stretch")
        else:
            st.info("No assigned patient data yet.")

    st.markdown("""
    <div class="section-head">
        <div>
            <div class="section-title">Upcoming Appointments</div>
            <div class="section-subtitle">Next patients in your schedule</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    if upcoming_df.empty:
        st.info("No upcoming appointments.")
    else:
        display_cols = [
            "appointment_date", "appointment_time", "patient_id",
            "fullname", "age", "gender", "symptoms"
        ]
        display_cols = [c for c in display_cols if c in upcoming_df.columns]
        st.dataframe(
            upcoming_df[display_cols].head(25),
            use_container_width="stretch",
            hide_index=True,
        )


    # --- CSS for selectbox ---
    st.markdown(
        """
        <style>
        /* Main selectbox */
        div[data-baseweb="select"] > div {
            background-color: #ffffff !important;
            color: #000000 !important;
            border-radius: 6px;
            border: 1px solid #cccccc !important;
        }

        /* Selectbox text */
        div[data-baseweb="select"] span {
            color: #000000 !important;
        }

        div[data-baseweb="select"] input {
            color: #000000 !important;
        }

        /* Dropdown */
        div[data-baseweb="popover"] {
            background-color: #ffffff !important;
        }

        div[data-baseweb="popover"] > div {
            background-color: #ffffff !important;
        }

        /* Dropdown options */
        div[data-baseweb="option"] {
            background-color: #ffffff !important;
            color: #000000 !important;
        }

        div[data-baseweb="option"] * {
            color: #000000 !important;
        }

        /* Hover */
        div[data-baseweb="option"]:hover {
            background-color: #eeeeee !important;
            color: #000000 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # --- Patient dropdown ---
    if assigned.empty:
        st.info("No patients are assigned to this Doctor ID.")
        return

    selected = st.selectbox(
        "Select patient",
        assigned["patient_id"].tolist(),
        format_func=lambda x: (
            f"{x} · {assigned.loc[assigned['patient_id'] == x, 'fullname'].iloc[0]}"
        ),
        key="doctor_patient_dropdown",
    )
    # --- Patient details ---
    patient = assigned[assigned["patient_id"] == selected].iloc[0]

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Patient", str(patient["fullname"]))
    d2.metric("Age", str(patient["age"]))
    d3.metric("Gender", str(patient["gender"]))
    d4.metric("Blood Group", str(patient["blood_group"]))

    left, right = st.columns(2)
    with left:
        with st.container(border=True):
            st.markdown("**Contact & Appointment**")
            st.write(f"📱 **Mobile:** {patient['mobile']}")
            st.write(f"✉️ **Email:** {patient['email']}")
            st.write(f"📅 **Appointment:** {patient['appointment_date']} {patient['appointment_time']}")
            st.write(f"📍 **Location:** {patient['city']}, {patient['state']}")

    with right:
        with st.container(border=True):
            st.markdown("**Clinical Information**")
            st.write(f"🩺 **Symptoms:** {patient['symptoms']}")
            st.write(f"⏱️ **Duration:** {patient['symptom_duration']}")
            st.write(f"⚕️ **Current Condition:** {patient['current_condition']}")
            st.write(f"⚠️ **Allergies:** {patient['allergies']}")

    with st.expander("View Complete Patient Record"):
        details = pd.DataFrame({ "Field": patient.index, "Value": patient.values.astype(str)})
        st.dataframe(details, use_container_width="stretch")
# ============================================================
# HOME
# ============================================================

def home_page():
    st.markdown("""
    <div class="hero">
        <div class="hero-kicker">Hospital Information Management System</div>
        <h1>HIMS Clinical Portal</h1>
        <p>Patient registration and doctor-side patient management in one application.</p>
    </div>
    """, unsafe_allow_html=True)

    a, b = st.columns(2)

    with a:
        st.markdown("""
        <div class="card">
            <div class="card-title">🤖 Patient Registration</div>
            <div class="card-subtitle">
                A guided chatbot collects patient information and validates
                every response before saving it to HIMS.
            </div>
            <br>
            <b>Includes</b><br>
            • Personal information<br>
            • Contact information<br>
            • Symptoms and medical history<br>
            • Insurance details<br>
            • Doctor and appointment selection
        </div>
        """, unsafe_allow_html=True)

        if st.button("Open Patient Registration  →", type="primary",
                     use_container_width="stretch"):
            st.session_state.page = "Patient Registration"
            st.rerun()

    with b:
        st.markdown("""
        <div class="card">
            <div class="card-title">👨‍⚕️ Doctor Portal</div>
            <div class="card-subtitle">
                Doctors log in with their Doctor ID and see only the patients
                scheduled for their own clinic queue.
            </div>
            <br>
            <b>Dashboard includes</b><br>
            • Today's patient queue<br>
            • Upcoming appointments<br>
            • Patient demographics<br>
            • Clinical details<br>
            • Complete patient records
        </div>
        """, unsafe_allow_html=True)

        if st.button("Doctor Login  →", use_container_width="stretch"):
            st.session_state.page = "Doctor Login"
            st.rerun()

    st.markdown("""
    <div style="margin-top:24px;text-align:center;color:#98a1b2;font-size:11px;">
        HIMS · Streamlit · Patient Intake + Doctor Workspace
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# APP STATE + NAVIGATION
# ============================================================

init_db()

if "page" not in st.session_state:
    st.session_state.page = "Home"

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

import streamlit as st
from datetime import datetime

# --- Sidebar Styling ---
st.markdown("""
<style>
/* Sidebar container */
section[data-testid="stSidebar"] {
    background-color: #f9f9f9;
    padding: 10px;
}

/* Red bar with HIMS text */
.sidebar-logo {
    background-color: #d62828;
    color: white;
    font-size: 30px;
    font-weight: 800;
    text-align: center;
    padding: 12px 0;
    border-radius: 6px;
    margin-bottom: 5px;
}

/* Clinical Management Portal below red bar */
.sidebar-sub {
    font-size: 16px;
    font-weight: 500;
    color: #333;
    text-align: center;
    margin-bottom: 25px;
}

/* MAIN MENU bold */
.sidebar-section {
    font-weight: 700;
    font-size: 18px;
    color: #000;
    text-align: center;
    margin-bottom: 10px;
}
</style>
""", unsafe_allow_html=True)

import streamlit as st

# --- Session setup ---
if "page" not in st.session_state:
    st.session_state.page = "Home"
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

# --- Navigation guard ---
def guard_navigation(target_page):
    # If doctor is logged in and trying to leave Dashboard
    if st.session_state.get("logged_in") and st.session_state.page == "Dashboard" and target_page != "Dashboard":
        st.session_state.next_page = target_page
        st.session_state.page = "ConfirmLogout"
    else:
        st.session_state.page = target_page
        st.rerun()

# --- Sidebar ---
with st.sidebar:
    st.markdown("""
    <div class="sidebar-logo">HIMS</div>
    <div class="sidebar-sub">Clinical Management Portal</div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="sidebar-section">MAIN MENU</div>', unsafe_allow_html=True)

    if st.button("⌂  Home", use_container_width="stretch", key="btn_home"):
        guard_navigation("Home")

    if st.button("🤖  Patient Registration", use_container_width="stretch", key="btn_patient"):
        guard_navigation("Patient Registration")

    if st.session_state.get("logged_in"):
        if st.button("▣  Doctor Dashboard", use_container_width="stretch", key="btn_dashboard"):
            guard_navigation("Dashboard")

        st.markdown('<div class="sidebar-section">SIGNED IN</div>', unsafe_allow_html=True)

        doctor = get_doctor(st.session_state.doctor_id)
        st.markdown(f"""
        <div class="card" style="padding:13px;">
            <b style="font-size:13px;">{doctor['doctor_name']}</b><br>
            <span style="font-size:10px;color:#7d879a;">
                {doctor['doctor_id']} · {doctor['department']}
            </span>
        </div>
        """, unsafe_allow_html=True)

        if st.button("↪  Logout", use_container_width="stretch", key="btn_logout"):
            st.session_state.logged_in = False
            st.session_state.pop("doctor_id", None)
            st.session_state.page = "Home"
            st.rerun()
    else:
        if st.button("👨‍⚕️  Doctor Login", use_container_width="stretch", key="btn_login"):
            guard_navigation("Doctor Login")

# --- Page routing ---
page = st.session_state.page

if page == "Home":
    home_page()

elif page == "Patient Registration":
    chatbot_page()

elif page == "Doctor Login":
    login_page()

elif page == "Dashboard":
    if st.session_state.get("logged_in"):
        dashboard_page()
    else:
        st.session_state.page = "Doctor Login"
        st.rerun()

elif page == "ConfirmLogout":
    st.warning("You are currently signed in. Do you want to stay logged in or log out?")
    col1, col2 = st.columns(2)
    with col1:
        if st.button("Stay Logged In", key="btn_stay"):
            # Cancel navigation, stay on Dashboard
            st.session_state.page = "Dashboard"
            st.rerun()
    with col2:
        if st.button("Logout", key="btn_confirm_logout"):
            # Log out and continue to next page
            st.session_state.logged_in = False
            st.session_state.pop("doctor_id", None)
            st.session_state.page = st.session_state.get("next_page", "Home")
            st.success("You have been logged out.")
            st.rerun()
