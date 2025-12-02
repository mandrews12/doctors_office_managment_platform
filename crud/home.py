#File for database operations related to the home page
from routes.db import post, get

def get_patient_count():
    results = get("SELECT COUNT(*) AS patient_count FROM patient;")
    if results:
        return results[0].get("patient_count", 0)
    return 0

def get_doctor_count():
    results = get("SELECT COUNT(*) AS doctor_count FROM doctor;")
    if results:
        return results[0].get("doctor_count", 0)            
    return 0

def get_staff_count():
    results = get("SELECT COUNT(*) AS staff_count FROM staff;")
    if results:
        return results[0].get("staff_count", 0)
    return 0

def get_specializations():
    results = get("SELECT DISTINCT role FROM doctor ORDER BY role;")
    specializations = [row.get("role") for row in results] if results else []
    return specializations

def get_appointments():
    query = """
    SELECT appointment_date, patient_last_name, doctor_last_name, status
    FROM doctor_schedule
    ORDER BY appointment_date ASC
    LIMIT 5;
    """
    results = get(query)
    return results