import streamlit as st
import pandas as pd
from routes.styles import load_styles
from datetime import datetime, timedelta

def render():
    load_styles()
    
    st.title("Doctor — Schedule & Appointments")
    st.divider()
    
    # --- Fetch doctor_schedule view ---
    doctorsched = """
        SELECT doctor_first_name, doctor_last_name, appointment_date,
               patient_first_name, patient_last_name, reason_for_visit, status
        FROM doctor_schedule
        ORDER BY doctor_last_name, doctor_first_name, appointment_date
    """
    
    scheduleDF = pd.read_sql(query, st.session_state["conn"])
    
    if scheduleDF.empty:
        st.info("No Upcoming Appointments")
        return
    
    # --- Doctor dropdown ---
    doctors = scheduleDF["doctor_last_name"].unique()
    selected_doctor = st.selectbox("Choose Doctor Name", doctors)
    filteredDF = scheduleDF[scheduleDF["doctor_last_name"] == selected_doctor]
    
    # --- Schedule table ---
    st.subheader(f"{selected_doctor}'s Schedule")
    table_data = []
    for row in filteredDF.itertuples():
        table_data.append({
            "Appointment Date": row.appointment_date.strftime("%Y-%m-%d %H:%M"), 
            "Patient": f"{row.patient_first_name} {row.patient_last_name}", 
            "Reason": row.reason_for_visit,
            "Status": row.status
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
    
    # --- Appointment Form ---
    st.subheader("Schedule a New Appointment")
    with st.form("appointment_form"):
        patient_name = st.text_input("Patient Name")
        appointment_date = st.date_input("Select Date", min_value=datetime.today())
        appointment_time = st.time_input("Select Time")
        reason = st.text_area("Reason for Visit")
        submitted = st.form_submit_button("Schedule Appointment")
        
        if submitted:
            st.success(f"Appointment scheduled for {patient_name} on {appointment_date} at {appointment_time}")

