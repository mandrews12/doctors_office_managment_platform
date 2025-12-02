# File for database operations related to the staff page
from routes.db import get, post

def get_all_staff():
    results = get("""
    SELECT staff_id, role, department, salary, employment_date, clock_in, clock_out
    FROM staff
    ORDER BY role, employment_date;
    """)
    return results

def get_staff_by_id(staff_id):
    query = """
    SELECT staff_id, role, department, salary, employment_date, clock_in, clock_out
    FROM staff
    WHERE staff_id = %s;
    """
    results = get(query, (staff_id,))
    return results

def add_staff(role, employment_date, department=None, salary=None):
    query = """
    INSERT INTO staff (role, employment_date, department, salary)
    VALUES (%s, %s, %s, %s);
    """
    
    ok = post(query, (role, employment_date, department, salary))
    if ok:
        return True, "Staff member added successfully!"
    else:
        return False, "Failed to add staff member."

def update_staff_info(staff_id, role, department, salary):
    query = """
    UPDATE staff
    SET role = %s,
        department = %s,
        salary = %s
    WHERE staff_id = %s;
    """
    
    ok = post(query, (role, department, salary, staff_id))
    if ok:
        return True, "Staff member updated successfully!"
    else:
        return False, "Failed to update staff member."

def delete_staff(staff_id):
    query = """
    DELETE FROM staff
    WHERE staff_id = %s;
    """
 
    ok = post(query, (staff_id,))
    if ok:
        return True, "Staff member deleted successfully!"
    else:
        return False, "Failed to delete staff member."