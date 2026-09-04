# patient_generator_sqlite.py
# ============================================================
import sqlite3
from faker import Faker
import random
from datetime import datetime

DB_PATH = "hims.db"   # SQLite file

# --- Database connection ---
def db():
    conn = sqlite3.connect(DB_PATH)
    return conn

# --- Generate patients ---
def generate_patients(n=2000):
    fake = Faker()
    patients = []

    for i in range(n):
        dob = fake.date_of_birth(minimum_age=1, maximum_age=90)
        age = (datetime.now().date() - dob).days // 365

        appointment_date = fake.date_between(start_date="today", end_date="+30d")
        appointment_time = fake.time()

        patients.append((
            f"PAT{i+1:05d}",  # patient_id
            fake.name(),
            dob,
            age,
            random.choice(["Male", "Female", "Other"]),
            random.choice(["Single", "Married", "Divorced"]),
            fake.phone_number()[:15],
            fake.email(),
            str(fake.unique.random_number(digits=12)),  # Aadhaar
            fake.address(),
            fake.city(),   # area
            fake.city(),   # city
            fake.state(),
            fake.postcode(),
            random.choice(["A+", "A-", "B+", "B-", "O+", "O-", "AB+", "AB-"]),
            fake.name(),   # emergency_name
            fake.phone_number()[:15],  # emergency_number
            fake.sentence(nb_words=6), # symptoms
            f"{random.randint(1, 30)} days", # symptom_duration
            random.choice(["Stable", "Critical", "Recovering"]), # current_condition
            fake.word(),   # allergies
            fake.word(),   # previous_surgery
            fake.word(),   # family_history
            random.choice(["Yes", "No"]), # has_insurance
            fake.company(), # insurance_provider
            fake.bothify(text="POL####"), # policy_number
            fake.date_between(start_date="today", end_date="+365d"), # insurance_validity
            random.choice(["Cardiology", "Dermatology", "Neurology", "Physiology"]), # department
            random.choice(["RAK001", "PRI001", "ANI001", "MAD001"]), # preferred_doctor
            appointment_date,
            appointment_time
        ))
    return patients

# --- Insert into DB ---
def insert_patients(patients):
    conn = db()
    cur = conn.cursor()

    sql = """
        INSERT INTO patients (
            patient_id, fullname, dob, age, gender, marital_status, mobile, email,
            aadhaar, address, area, city, state, pincode, blood_group,
            emergency_name, emergency_number, symptoms, symptom_duration,
            current_condition, allergies, previous_surgery, family_history,
            has_insurance, insurance_provider, policy_number, insurance_validity,
            department, preferred_doctor, appointment_date, appointment_time
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?,
                ?, ?, ?, ?, ?, ?, ?, ?)
    """

    cur.executemany(sql, patients)
    conn.commit()
    conn.close()
    print(f"Inserted {len(patients)} patients successfully!")

if __name__ == "__main__":
    patients = generate_patients(2000)
    insert_patients(patients)
