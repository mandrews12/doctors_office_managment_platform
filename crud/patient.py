#File for database operations related to the home page
from routes.db import post, get
from datetime import datetime as _datetime

def get_patient_names():
    query = """
    SELECT fname, lname FROM patient ORDER BY lname, fname;
    """
    return get(query)

def get_updatable_patient_info(patient_fname, patient_lname):
    query = """
    SELECT fname, lname, email, allergies, medications, phone_number, address
    FROM patient
    WHERE fname = %s AND lname = %s;
    """
    results = get(query, (patient_fname, patient_lname))
    return results

def update_patient_info(patient_fname, patient_lname, email, allergies, medications, phone_number, address):
    query = """
    UPDATE patient
    SET email = %s,
        allergies = %s,
        medications = %s,
        phone_number = %s,
        address = %s
    WHERE fname = %s AND lname = %s;
    """
    ok = post(query, (email, allergies, medications, phone_number, address, patient_fname, patient_lname))
    
    if ok:
        return True, "Patient information updated successfully!"
    else:
        return False, "Failed to update patient information."
            
   
    
def get_medical_records(patient_fname, patient_lname):
    query = """
    select visit_date, visit_reason, visit_notes from past_visits pv
    join patient p on pv.patient_id = p.patient_id
    where p.lname = %s AND p.fname = %s
    order by visit_id desc;
    """
    results = get(query, (patient_lname, patient_fname))
    return results
            

def schedule_appointment(patient_fname, patient_lname, appointment_date, appointment_time, reason):
    # Lookup patient id and doctor id
    results = get("SELECT patient_id, doc_id FROM patient WHERE fname = %s AND lname = %s",(patient_fname, patient_lname))
    p_id = results[0].get("patient_id") if results else None
    d_id = results[0].get("doc_id") if results else None

    appointment_datetime = _datetime.combine(appointment_date, appointment_time)

    query = """
    INSERT INTO appointment (patient_id, appointment_date, reason_for_visit, status, visit_notes, doctor_id)
    VALUES (%s, %s, %s, 'Scheduled', NULL, %s);
    """
    ok = post(query, (p_id, appointment_datetime, reason, d_id))
    if ok:
        return True, "Appointment scheduled successfully!"
    else:
        return False, "Failed to schedule appointment. Please verify patient exists and try again."
