import streamlit as st

from routes.styles import load_styles
from crud.patient import get_patient_names
from crud.patient import get_updatable_patient_info
from crud.patient import update_patient_info
from crud.patient import schedule_appointment
from crud.patient import get_medical_records
from crud.patient import add_patient

def render():
    
    load_styles()
    
    st.title("Patient Portal")
    
    st.subheader("Access your medical records, appointments, and keep your information up to date.")
    
    st.divider()
    
    # Select which patient to view
    st.subheader("Select Patient")
    
    patients_raw = get_patient_names()
    patients = []
    # normalize possible return types: list of dicts or DataFrame
    if patients_raw is None:
        patients = []
    elif isinstance(patients_raw, list):
        patients = [f"{p.get('fname','').strip()} {p.get('lname','').strip()}" for p in patients_raw if p.get('fname')]
    else:
        # assume DataFrame-like
        try:
            patients = [f"{row['fname']} {row['lname']}" for index, row in patients_raw.iterrows()]
        except Exception:
            patients = []
    

    # default patient selection is empty
    selected = st.selectbox("Choose Patient", options=["-- Select Patient --"] + patients)
    
    if selected == "-- Select Patient --":
        st.subheader("Add New Patient")
        with st.form("add_patient_form"):
            fname = st.text_input("First Name *")
            lname = st.text_input("Last Name *")
            email = st.text_input("Email")
            allergies = st.text_area("Allergies")
            medications = st.text_area("Current Medications")
            phone_number = st.text_input("Contact Number")
            address = st.text_area("Address")
            pdob = st.date_input("Date of Birth")
            gender = st.selectbox("Gender", options=["", "Male", "Female", "Other"])
            submitted = st.form_submit_button("OK")
            if submitted:
                ok, msg = add_patient(fname, lname, email, allergies, medications, phone_number, address, None, pdob, gender)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
    
    
    if selected and selected != "-- Select Patient --":
        # split into first and last name (split only on first space to allow multi-part last names)
        parts = selected.split(" ", 1)
        fname = parts[0]
        lname = parts[1] if len(parts) > 1 else ""
        patient_info_raw = get_updatable_patient_info(fname, lname)
    
    # update patient information form only visible if a patient is selected
    if selected and selected != "-- Select Patient --":
        st.subheader("Update Patient Information")
        # normalize patient_info to a dict
        patient_info = {}
        if patient_info_raw is None:
            patient_info = {}
        elif isinstance(patient_info_raw, list) and len(patient_info_raw) > 0:
            patient_info = patient_info_raw[0]
        else:
            try:
                # DataFrame-like
                patient_info = patient_info_raw.iloc[0].to_dict()
            except Exception:
                patient_info = {}

        with st.form("update_patient_info"):
            phone_number = st.text_input("Contact Number", value=patient_info.get("phone_number", ""))
            address = st.text_area("Address", value=patient_info.get("address", ""))
            email = st.text_input("Email", value=patient_info.get("email", ""))
            allergies = st.text_area("Allergies", value=patient_info.get("allergies", ""))
            medications = st.text_area("Current Medications", value=patient_info.get("medications", ""))

            submitted = st.form_submit_button("Update Information")
            if submitted:
                ok, msg = update_patient_info(fname, lname, email, allergies, medications, phone_number, address)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
                
        
    # schedule appointment section
    if selected and selected != "-- Select Patient --":
        st.subheader("Schedule Appointment")
        with st.form("schedule_appointment"):
            appointment_date = st.date_input("Appointment Date")
            appointment_time = st.time_input("Appointment Time")
            reason = st.text_area("Reason for Visit")

            scheduled = st.form_submit_button("Schedule Appointment")
            if scheduled:
                ok, msg = schedule_appointment(fname, lname, appointment_date, appointment_time, reason)
                if ok:
                    st.success(msg)
                else:
                    st.error(msg)
    
    # view medical records section (past visits)
    if selected and selected != "-- Select Patient --":
        records_raw = get_medical_records(fname, lname)
        st.subheader("Medical Records")
        # normalize records
        records = []
        if records_raw is None:
            records = []
        elif isinstance(records_raw, list):
            records = records_raw
        else:
            try:
                records = [row._asdict() for row in records_raw.itertuples(index=False)]
            except Exception:
                try:
                    records = [r for _, r in records_raw.iterrows()]
                except Exception:
                    records = []

        if not records:
            st.info("No medical records found for this patient.")
        else:
            for rec in records:
                # rec may be a dict or a Series-like
                try:
                    visit_date = rec.get("visit_date") if isinstance(rec, dict) else rec["visit_date"]
                    visit_reason = rec.get("visit_reason") if isinstance(rec, dict) else rec["visit_reason"]
                    visit_notes = rec.get("visit_notes") if isinstance(rec, dict) else rec["visit_notes"]
                except Exception:
                    # fallback for pandas Series
                    try:
                        visit_date = rec.visit_date
                        visit_reason = rec.visit_reason
                        visit_notes = rec.visit_notes
                    except Exception:
                        continue

                try:
                    date_str = visit_date.strftime("%Y-%m-%d") if hasattr(visit_date, "strftime") else str(visit_date)
                except Exception:
                    date_str = str(visit_date)

                st.markdown(f"**Visit Date:** {date_str}")
                st.markdown(f"**Visit Reason:** {visit_reason}")
                st.markdown(f"**Visit Notes:** {visit_notes}")
                st.markdown("---")
    

