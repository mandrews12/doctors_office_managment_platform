# File for database operations related to the staff page
from routes.db import get_new_connection


def get_all_staff():
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            cursor.execute("""
            SELECT staff_id, role, department, salary, employment_date, clock_in, clock_out
            FROM staff
            ORDER BY role, employment_date;
            """)
            rows = cursor.fetchall()
            
            # turn rows into a dataframe-like list of dicts
            staff = [dict(row) for row in rows]
            return staff
        except Exception as e:
            print(f"Error fetching staff data: {e}")
            return []
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return []


def get_staff_by_id(staff_id):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            SELECT staff_id, role, department, salary, employment_date, clock_in, clock_out
            FROM staff
            WHERE staff_id = %s;
            """
            cursor.execute(query, (staff_id,))
            row = cursor.fetchone()
            if row:
                return dict(row)
            return None
        except Exception as e:
            print(f"Error fetching staff by id: {e}")
            return None
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return None


def add_staff(role, employment_date, department=None, salary=None):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            INSERT INTO staff (role, employment_date, department, salary)
            VALUES (%s, %s, %s, %s);
            """
            cursor.execute(query, (role, employment_date, department, salary))
            conn.commit()
            return True, "Staff member added successfully!"
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            raise e
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return False, "No database connection."


def update_staff_info(staff_id, role, department, salary):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor(dictionary=True)
            query = """
            UPDATE staff
            SET role = %s,
                department = %s,
                salary = %s
            WHERE staff_id = %s;
            """
            cursor.execute(query, (role, department, salary, staff_id))
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            raise e
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return False, "No database connection."


def delete_staff(staff_id):
    conn = get_new_connection()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            DELETE FROM staff
            WHERE staff_id = %s;
            """
            cursor.execute(query, (staff_id,))
            affected = cursor.rowcount
            conn.commit()
            if affected == 0:
                return False, f"No staff member found with id {staff_id}"
            return True, f"Deleted staff member id {staff_id}"
        except Exception as e:
            try:
                conn.rollback()
            except Exception:
                pass
            return False, str(e)
        finally:
            try:
                cursor.close()
            except Exception:
                pass
            conn.close()
    return False, "No database connection."