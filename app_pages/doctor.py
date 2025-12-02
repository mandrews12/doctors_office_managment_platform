import streamlit as st
import pandas as pd
from routes.styles import load_styles
from datetime import datetime, timedelta
from crud.doctor import get_doctor_schedule
from crud.doctor import add_past_visit_details
from crud.doctor import get_patients_of_doctor
from crud.doctor import schedule_appointment

def render():
    load_styles()
    
    st.title("Doctor — Schedule & Appointments")
    st.divider()
    
    # --- Fetch doctor_schedule view ---
    schedule_raw = get_doctor_schedule()
    # normalize to pandas DataFrame if possible
    scheduleDF = pd.DataFrame(schedule_raw)
    
    if scheduleDF is None or len(scheduleDF) == 0:
        st.info("No Upcoming Appointments")
        return
    
    # --- Doctor dropdown ---
    doctors = scheduleDF["doctor_last_name"].unique()
    selected_doctor = st.selectbox("Choose Doctor Name", doctors)
    filteredDF = scheduleDF[scheduleDF["doctor_last_name"] == selected_doctor]
    
    # --- Schedule table ---
    st.subheader(f"{selected_doctor}'s Schedule")
    table_data = []
    for row in filteredDF.itertuples(index=False):
        # handle appointment_date possibly being string or datetime
        try:
            appt_dt = row.appointment_date
            date_str = appt_dt.strftime("%Y-%m-%d %H:%M") if hasattr(appt_dt, "strftime") else str(appt_dt)
        except Exception:
            date_str = ""

        # patient names
        try:
            patient_first = getattr(row, "patient_first_name", "")
            patient_last = getattr(row, "patient_last_name", "")
        except Exception:
            patient_first = ""
            patient_last = ""

        table_data.append({
            "Appointment Date": date_str,
            "Patient": f"{patient_first} {patient_last}".strip(),
            "Reason": getattr(row, "reason_for_visit", ""),
            "Status": getattr(row, "status", "")
        })
    st.table(table_data)
    
    # --- Next availability ---
    future_appts = filteredDF[filteredDF["appointment_date"] > datetime.now()]
    if not future_appts.empty:
        next_appt = future_appts["appointment_date"].min()
        st.markdown(f"**Next Available Appointment:** {next_appt.strftime('%Y-%m-%d %H:%M')}")
    else:
        st.markdown("**Next Available Appointment:** No Upcoming Appointments")
    
    st.divider()
    
    # get patients for selected doctor; normalize to DataFrame
    patients_raw = get_patients_of_doctor(
        doctor_fname=filteredDF.iloc[0]["doctor_first_name"],
        doctor_lname=selected_doctor
    )
    if patients_raw is None:
        patients = pd.DataFrame()
    elif isinstance(patients_raw, list):
        patients = pd.DataFrame(patients_raw)
    else:
        try:
            patients = pd.DataFrame(patients_raw)
        except Exception:
            patients = pd.DataFrame()
    
    # --- Appointment Form ---
    st.subheader("Schedule a New Appointment")
    with st.form("appointment_form"):
        patient_opts = []
        if not patients.empty:
            try:
                patient_opts = [f"{row['fname']} {row['lname']}" for index, row in patients.iterrows()]
            except Exception:
                # fallback if patients is list-like
                try:
                    patient_opts = [f"{p.get('fname','')} {p.get('lname','')}".strip() for p in patients]
                except Exception:
                    patient_opts = []

        patient_name = st.selectbox("Select Patient", options=patient_opts)
        appointment_date = st.date_input("Select Date", min_value=datetime.today())
        appointment_time = st.time_input("Select Time")
        reason = st.text_area("Reason for Visit")
        submitted = st.form_submit_button("Schedule Appointment")
        
        if submitted:
            result = schedule_appointment(patient_name.split(" ")[0], patient_name.split(" ")[1], appointment_date, appointment_time, reason)
            if isinstance(result, tuple):
                ok, msg = result
            else:
                ok = bool(result)
                msg = None

            if ok:
                st.success(msg or "Appointment scheduled successfully!")
            else:
                st.error(msg or "Failed to schedule appointment. Please verify patient exists and try again.")
    
    st.divider()
    
    st.subheader("Manage Appointment Notes")
    with st.form("past_visit_form"):
        patient_name = st.selectbox("Select Patient", options=patient_opts)
        visit_date = st.date_input("Visit Date", max_value=datetime.today())
        visit_reason = st.text_area("Visit Reason")
        visit_notes = st.text_area("Visit Notes")
        submitted = st.form_submit_button("Add Patient Visit Details")
        
        if submitted:
            st.success(f"Visit details added for {patient_name} on {visit_date}")
            # Extract first and last names for patient
            patient_fname, patient_lname = patient_name.split(" ", 1)
            # Call the function to add past visit details to the database
            add_past_visit_details(visit_reason, visit_notes, patient_fname, patient_lname, selected_doctor, visit_date)