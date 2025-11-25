import streamlit as st

from routes.styles import load_styles
from crud.patient import get_patient_names
from crud.patient import get_updatable_patient_info
from crud.patient import update_patient_info
from crud.patient import schedule_appointment
from crud.patient import get_medical_records

def render():
    
    load_styles()
    
    st.title("Patient Portal")
    
    st.subheader("Access your medical records, appointments, and keep your information up to date.")
    
    st.divider()
    
    # Select which patient to view
    st.subheader("Select Patient")
    
    patients = get_patient_names()
    patients = [f"{row['fname']} {row['lname']}" for index, row in patients.iterrows()]
    
    # default patient selection is empty
    patient_id = st.selectbox("Choose Patient", options=["-- Select Patient --"] + patients)
    
    if patient_id and patient_id != "-- Select Patient --":
        patient_info = get_updatable_patient_info(patient_id.split(" ")[0], patient_id.split(" ")[1])
    
    # update patient information form only visible if a patient is selected
    if patient_id and patient_id != "-- Select Patient --":
        
        st.subheader("Update Patient Information")
        
        with st.form("update_patient_info"):
            phone_number = st.text_input("Contact Number", value=patient_info["phone_number"].iloc[0])
            address = st.text_area("Address", value=patient_info["address"].iloc[0])
            email = st.text_input("Email", value=patient_info["email"].iloc[0])
            allergies = st.text_area("Allergies", value=patient_info["allergies"].iloc[0])
            medications = st.text_area("Current Medications", value=patient_info["medications"].iloc[0])
            
            submitted = st.form_submit_button("Update Information")
            if submitted:
                update_patient_info(patient_id.split(" ")[0], patient_id.split(" ")[1], email, allergies, medications, phone_number, address)
                st.success("Patient information updated successfully!")
                
        
    # schedule appointment section
    if patient_id and patient_id != "-- Select Patient --":
        st.subheader("Schedule Appointment")
        with st.form("schedule_appointment"):
            appointment_date = st.date_input("Appointment Date")
            appointment_time = st.time_input("Appointment Time")
            reason = st.text_area("Reason for Visit")
            
            scheduled = st.form_submit_button("Schedule Appointment")
            if scheduled:
                schedule_appointment(patient_id.split(" ")[0], patient_id.split(" ")[1], appointment_date, appointment_time, reason)
                st.success("Appointment scheduled successfully!")
    
    # view medical records section (past visits)
    if patient_id and patient_id != "-- Select Patient --":
        medical_records = get_medical_records(patient_id.split(" ")[0], patient_id.split(" ")[1])
        st.subheader("Medical Records")
        if medical_records.empty:
            st.info("No medical records found for this patient.")
        else:
            for index, record in medical_records.iterrows():
                st.markdown(f"**Visit Reason:** {record['visit_reason']}")
                st.markdown(f"**Visit Notes:** {record['visit_notes']}")
                st.markdown("---")
    

