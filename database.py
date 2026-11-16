
import sqlite3

DB_NAME = "patients.db"


def get_connection():
    """Create a connection to the patient database."""
    connection = sqlite3.connect(DB_NAME)
    connection.row_factory = sqlite3.Row
    return connection


def init_db():
    """Create the patients table if it does not exist."""
    connection = get_connection()

    connection.execute("""
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            dob TEXT NOT NULL,
            email TEXT NOT NULL,
            glucose REAL NOT NULL,
            haemoglobin REAL NOT NULL,
            cholesterol REAL NOT NULL,
            remarks TEXT DEFAULT ''
        )
    """)

    connection.commit()
    connection.close()


def add_patient(full_name, dob, email, glucose,
                haemoglobin, cholesterol, remarks):
    """Add a new patient to the database."""
    connection = get_connection()

    connection.execute("""
        INSERT INTO patients
        (full_name, dob, email, glucose,
         haemoglobin, cholesterol, remarks)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (
        full_name, dob, email, glucose,
        haemoglobin, cholesterol, remarks
    ))

    connection.commit()
    connection.close()


def get_patients():
    """Return all patient records."""
    connection = get_connection()

    patients = connection.execute(
        "SELECT * FROM patients ORDER BY id"
    ).fetchall()

    connection.close()
    return patients


def update_patient_email(patient_id, new_email):
    """Update a patient's email address."""
    connection = get_connection()

    connection.execute(
        "UPDATE patients SET email = ? WHERE id = ?",
        (new_email, patient_id)
    )

    connection.commit()
    connection.close()


def delete_patient(patient_id):
    """Delete a patient using their ID."""
    connection = get_connection()

    connection.execute(
        "DELETE FROM patients WHERE id = ?",
        (patient_id,)
    )

    connection.commit()
    connection.close()
