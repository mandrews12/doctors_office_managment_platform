#File for database operations related to the doctor's page
from datetime import datetime as _datetime
from routes.db import post, get

def get_doctor_schedule():
    query= """
    SELECT doctor_first_name, doctor_last_name, appointment_date, patient_first_name, patient_last_name, reason_for_visit, status
    FROM doctor_schedule
    ORDER BY doctor_last_name, doctor_first_name, appointment_date;
    """
    results = get(query)
    return results

def add_past_visit_details(visit_reason, visit_notes, patient_fname, patient_lname, doctor_lname, visit_date):
    results = get("SELECT patient_id, doc_id FROM patient WHERE fname = %s AND lname = %s", (patient_fname, patient_lname))
    if results:
        row = results[0]
        if not row:
            return False, "Patient not found"
        p_id = row.get("patient_id")
        d_id = row.get("doc_id")
            
    query = """
    INSERT INTO past_visits (visit_reason,visit_notes,patient_id,doctor_id,visit_date)
    VALUES (%s, %s, %s, %s, %s);
    """
    results = post(query, (visit_reason, visit_notes, p_id, d_id, visit_date))
    if results:
        return True, "Past visit details added successfully!"
    return False, "Error inserting appointment."
    
def get_patients_of_doctor(doctor_fname, doctor_lname):
    query = """
    SELECT p.fname, p.lname
    FROM patient p
    JOIN doctor d ON p.doc_id = d.doctor_id
    WHERE d.fname = %s AND d.lname = %s;
    """
    results = get(query, (doctor_fname, doctor_lname))
    return results

def schedule_appointment(patient_fname, patient_lname, appointment_date, appointment_time, reason):
    results = get(
    "SELECT patient_id, doc_id FROM patient WHERE fname = %s AND lname = %s",
    (patient_fname, patient_lname),)
    
    if results:
        row = results[0]
        if not row:
            return False, "Patient not found"
        p_id = row.get("patient_id")
        d_id = row.get("doc_id")

        appointment_datetime = _datetime.combine(appointment_date, appointment_time)

    query = """
    INSERT INTO appointment (patient_id, appointment_date, reason_for_visit, status, visit_notes, doctor_id)
    VALUES (%s, %s, %s, 'Scheduled', NULL, %s);
    """
    results = post(query, (p_id, appointment_datetime, reason, d_id))
    if results:
        return True, "Appointment scheduled"
    return False, "Error inserting appointment."