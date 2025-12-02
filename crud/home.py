#File for database operations related to the home page
from routes.db import get_new_connection

def get_patient_count():
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) AS patient_count FROM patient;")
            row = cursor.fetchone()
            if row:
                return row.get("patient_count", 0)
            return 0
        except Exception as e:
            print(f"Error fetching patient count: {e}")
            return 0
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return 0

def get_doctor_count():
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) AS doctor_count FROM doctor;")
            row = cursor.fetchone()
            if row:
                return row.get("doctor_count", 0)
            return 0
        except Exception as e:
            print(f"Error fetching doctor count: {e}")
            return 0
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return 0

def get_staff_count():
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT COUNT(*) AS staff_count FROM staff;")
            row = cursor.fetchone()
            if row:
                return row.get("staff_count", 0)
            return 0
        except Exception as e:
            print(f"Error fetching staff count: {e}")
            return 0
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return 0

def get_specializations():
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT DISTINCT role FROM doctor;")
            rows = cursor.fetchall()

            # return a simple list of role strings
            specs = []
            for row in rows:
                try:
                    val = row.get("role")
                except Exception:
                    # fallback if row is a tuple
                    try:
                        val = row[0]
                    except Exception:
                        val = None
                if val:
                    specs.append(val)
            return specs
        except Exception as e:
            print(f"Error fetching specializations: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return []

def get_appointments():
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
            SELECT appointment_date, patient_last_name, doctor_last_name, status
            FROM doctor_schedule
            ORDER BY appointment_date ASC
            LIMIT 5;
            """)
            rows = cursor.fetchall()
            
            # turn rows into a dataframe-like list of dicts
            appts = [dict(row) for row in rows]
            return appts
        except Exception as e:
            print(f"Error fetching appointments: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return []