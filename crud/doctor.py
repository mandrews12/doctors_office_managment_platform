#File for database operations related to the doctor's page
from routes.db import get_new_connection
from mysql.connector import Error
from datetime import datetime as _datetime

def get_doctor_schedule():
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
            SELECT doctor_first_name, doctor_last_name, appointment_date,
                   patient_first_name, patient_last_name, reason_for_visit, status
            FROM doctor_schedule
            ORDER BY doctor_last_name, doctor_first_name, appointment_date;
            """)
            rows = cursor.fetchall()
            
            # turn rows into a dataframe-like list of dicts
            schedule = [dict(row) for row in rows]
            return schedule
        except Error as e:
            print(f"Error fetching doctor schedule: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close() 
    return []

def add_past_visit_details(visit_reason, visit_notes, patient_fname, patient_lname, doctor_lname, visit_date):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            # Lookup patient id and doctor id
            cursor.execute(
                "SELECT patient_id, doc_id FROM patient WHERE fname = %s AND lname = %s",
                (patient_fname, patient_lname),
            )
            row = cursor.fetchone()
            if not row:
                return False, "Patient not found"

            p_id = row.get("patient_id")
            d_id = row.get("doc_id")
            
            query = """
            INSERT INTO past_visits (visit_reason,visit_notes,patient_id,doctor_id,visit_date)
            VALUES (%s, %s, %s, %s, %s);
            """
            cursor.execute(query, (visit_reason, visit_notes, p_id, d_id, visit_date))
            conn.commit()
            return True, "Past visit details added successfully!"
        except Error as e:
            return False, f"Error inserting appointment: {e}"
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return False, "No database connection."
    
def get_patients_of_doctor(doctor_fname, doctor_lname):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT p.fname, p.lname
            FROM patient p
            JOIN doctor d ON p.doc_id = d.doctor_id
            WHERE d.fname = %s AND d.lname = %s;
            """
            cursor.execute(query, (doctor_fname, doctor_lname))
            rows = cursor.fetchall()
            patients = [dict(row) for row in rows]
            return patients
        except Exception as e:
            print(f"Error fetching patients of doctor: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return []

def schedule_appointment(patient_fname, patient_lname, appointment_date, appointment_time, reason):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)

            # Lookup patient id and doctor id
            cursor.execute(
                "SELECT patient_id, doc_id FROM patient WHERE fname = %s AND lname = %s",
                (patient_fname, patient_lname),
            )
            row = cursor.fetchone()
            if not row:
                return False, "Patient not found"

            p_id = row.get("patient_id")
            d_id = row.get("doc_id")

            appointment_datetime = _datetime.combine(appointment_date, appointment_time)

            query = """
            INSERT INTO appointment (patient_id, appointment_date, reason_for_visit, status, visit_notes, doctor_id)
            VALUES (%s, %s, %s, 'Scheduled', NULL, %s);
            """
            cursor.execute(query, (p_id, appointment_datetime, reason, d_id))
            conn.commit()
            return True, "Appointment scheduled"
        except Error as e:
            return False, f"Error inserting appointment: {e}"
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return False, "No database connection."