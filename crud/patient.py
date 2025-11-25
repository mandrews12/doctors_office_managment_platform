#File for database operations related to the home page
from routes.db import execute_query
from routes.db import execute_non_query

def get_patient_names():
    query = """
    SELECT fname, lname 
    FROM patient;
    """
    
    patients = execute_query(query)
    return patients

def get_updatable_patient_info(patient_fname, patient_lname):
    query = """
    SELECT email, allergies, medications, phone_number, address
    FROM patient
    WHERE fname = :fname AND lname = :lname;
    """
    params = {
        "fname": patient_fname, 
        "lname": patient_lname
    }
    
    patient_info = execute_query(query, params=params)
    return patient_info

def update_patient_info(patient_fname, patient_lname, email, allergies, medications, phone_number, address):
    query = """
    UPDATE patient
    SET email = :email,
        allergies = :allergies,
        medications = :medications,
        phone_number = :phone_number,
        address = :address
    WHERE fname = :fname AND lname = :lname;
    """
    params = {
        "email": email,
        "allergies": allergies,
        "medications": medications,
        "phone_number": phone_number,
        "address": address,
        "fname": patient_fname,
        "lname": patient_lname,
    }
    execute_non_query(query, params=params)
    
def schedule_appointment(patient_fname, patient_lname, appointment_date, appointment_time, reason):
    query = """
    INSERT INTO appointment (patient_id, appointment_date, appointment_time, reason)
    VALUES (
        (SELECT id FROM patient WHERE fname = :fname AND lname = :lname),
        :appointment_date,
        :appointment_time,
        :reason
    );
    """
    params = {
        "fname": patient_fname,
        "lname": patient_lname,
        "appointment_date": appointment_date,
        "appointment_time": appointment_time,
        "reason": reason,
    }
    execute_non_query(query, params=params)
    
def get_medical_records(patient_fname, patient_lname):
    query = """
    select visit_reason, visit_notes from past_visits pv
    join patient p on pv.patient_id = p.patient_id
    where p.lname = :lname AND p.fname = :fname
    order by visit_id desc;
    """
    params = {
        "fname": patient_fname, 
        "lname": patient_lname
    }
    records = execute_query(query, params=params)
    return records