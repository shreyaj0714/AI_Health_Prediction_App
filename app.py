
import streamlit as st
import pandas as pd

from database import (
    init_db,
    add_patient,
    get_patients,
    update_patient_email,
    delete_patient
)

from validation import (
    validate_name,
    validate_email,
    validate_dob,
    validate_blood_values
)

from ai_service import generate_health_remarks


# -----------------------------------
# PAGE CONFIGURATION
# -----------------------------------

st.set_page_config(
    page_title="AI Health Prediction",
    page_icon="🏥",
    layout="wide"
)

# Initialize database
init_db()


# -----------------------------------
# APPLICATION HEADER
# -----------------------------------

st.title("🏥 AI Health Prediction System")

st.write(
    "Patient Management Dashboard with AI-powered "
    "Health Observations"
)

st.info(
    "This application provides informational health observations "
    "and is not a substitute for professional medical advice."
)


# -----------------------------------
# FETCH PATIENT RECORDS
# -----------------------------------

patients = get_patients()


# -----------------------------------
# DASHBOARD SUMMARY
# -----------------------------------

total_patients = len(patients)

col1, col2 = st.columns(2)

with col1:
    st.metric("Total Patient Records", total_patients)

with col2:
    st.metric(
        "Unique Patients",
        len(set(patient["email"].lower() for patient in patients))
    )


st.divider()


# -----------------------------------
# APPLICATION TABS
# -----------------------------------

tab1, tab2, tab3, tab4 = st.tabs([
    "➕ Add Patient",
    "📋 Patient Records",
    "✏️ Update Patient",
    "🗑️ Delete Patient"
])


# -----------------------------------
# TAB 1: ADD PATIENT
# -----------------------------------

with tab1:

    st.subheader("Register New Patient")

    with st.form("add_patient_form"):

        full_name = st.text_input("Full Name")

        dob = st.text_input(
            "Date of Birth (DD/MM/YYYY)",
            placeholder="28/01/1960"
        )

        email = st.text_input("Email Address")

        st.markdown("### Blood Test Results")

        col1, col2, col3 = st.columns(3)

        with col1:
            glucose = st.number_input(
                "Glucose",
                min_value=0.0,
                value=100.0,
                step=1.0
            )

        with col2:
            haemoglobin = st.number_input(
                "Haemoglobin",
                min_value=0.0,
                value=13.0,
                step=0.1
            )

        with col3:
            cholesterol = st.number_input(
                "Cholesterol",
                min_value=0.0,
                value=180.0,
                step=1.0
            )

        submitted = st.form_submit_button(
            "Generate AI Remarks & Save Patient",
            use_container_width=True
        )

        if submitted:

            errors = []

            # Validate patient name
            valid, message = validate_name(full_name)
            if not valid:
                errors.append(message)

            # Validate email
            valid, message = validate_email(email)
            if not valid:
                errors.append(message)

            # Validate date of birth
            valid, message = validate_dob(dob)
            if not valid:
                errors.append(message)

            # Validate blood test values
            valid, message = validate_blood_values(
                glucose,
                haemoglobin,
                cholesterol
            )
            if not valid:
                errors.append(message)

            # Display validation errors
            if errors:

                for error in errors:
                    st.error(error)

            else:

                # Request AI-generated remarks
                with st.spinner("Generating AI health observations..."):

                    success, remarks = generate_health_remarks(
                        glucose,
                        haemoglobin,
                        cholesterol
                    )

                if success:

                    # Save patient after successful AI response
                    add_patient(
                        full_name.strip(),
                        dob.strip(),
                        email.strip(),
                        glucose,
                        haemoglobin,
                        cholesterol,
                        remarks
                    )

                    st.success("Patient added successfully!")
                    st.subheader("AI-Generated Remarks")
                    st.write(remarks)
                    st.rerun()

                else:
                    st.error(remarks)
                    st.warning(
                        "Patient was not saved because AI remarks "
                        "could not be generated. Check the API "
                        "connection and try again."
                    )


# -----------------------------------
# TAB 2: VIEW PATIENT RECORDS
# -----------------------------------

with tab2:

    st.subheader("All Patient Records")

    patients = get_patients()

    if patients:

        records = [dict(patient) for patient in patients]

        dataframe = pd.DataFrame(records)

        dataframe = dataframe.rename(columns={
            "id": "Patient ID",
            "full_name": "Full Name",
            "dob": "Date of Birth",
            "email": "Email Address",
            "glucose": "Glucose",
            "haemoglobin": "Haemoglobin",
            "cholesterol": "Cholesterol",
            "remarks": "AI Remarks"
        })

        st.dataframe(
            dataframe,
            use_container_width=True,
            hide_index=True
        )

        st.caption(f"Showing {len(patients)} patient records.")

    else:

        st.info("No patient records available yet.")


# -----------------------------------
# TAB 3: UPDATE PATIENT EMAIL
# -----------------------------------

with tab3:

    st.subheader("Update Patient Information")

    patients = get_patients()

    if patients:

        patient_options = {
            f"ID {p['id']} - {p['full_name']} ({p['email']})": p
            for p in patients
        }

        selected_label = st.selectbox(
            "Select Patient",
            list(patient_options.keys())
        )

        selected_patient = patient_options[selected_label]

        new_email = st.text_input(
            "New Email Address",
            value=selected_patient["email"]
        )

        if st.button("Update Email Address"):

            valid, message = validate_email(new_email)

            if valid:

                update_patient_email(
                    selected_patient["id"],
                    new_email.strip()
                )

                st.success("Patient email updated successfully!")
                st.rerun()

            else:

                st.error(message)

    else:

        st.info("No patients available to update.")


# -----------------------------------
# TAB 4: DELETE PATIENT
# -----------------------------------

with tab4:

    st.subheader("Delete Patient Record")

    patients = get_patients()

    if patients:

        patient_options = {
            f"ID {p['id']} - {p['full_name']} ({p['email']})": p
            for p in patients
        }

        selected_label = st.selectbox(
            "Select Patient to Delete",
            list(patient_options.keys()),
            key="delete_patient"
        )

        selected_patient = patient_options[selected_label]

        st.warning(
            f"You are about to delete "
            f"{selected_patient['full_name']}."
        )

        confirm_delete = st.checkbox(
            "I confirm that I want to delete this record."
        )

        if st.button("Delete Patient"):

            if confirm_delete:

                delete_patient(selected_patient["id"])

                st.success("Patient deleted successfully!")
                st.rerun()

            else:

                st.error("Please confirm before deleting.")

    else:

        st.info("No patient records available to delete.")


# -----------------------------------
# APPLICATION FOOTER
# -----------------------------------

st.divider()

st.caption(
    "AI Health Prediction System | Python, Streamlit, "
    "SQLite and Google Gemini"
)