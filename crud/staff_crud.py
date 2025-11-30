# File for database operations related to the staff page
from routes.db import execute_query
from routes.db import execute_non_query


def get_all_staff():
    """READ: Retrieve all staff members."""
    query = """
    SELECT staff_id, role, department, salary, employment_date, clock_in, clock_out
    FROM staff
    ORDER BY role, employment_date;
    """
    staff = execute_query(query)
    return staff


def get_staff_by_id(staff_id):
    """READ: Retrieve a specific staff member by their ID."""
    query = """
    SELECT staff_id, role, department, salary, employment_date, clock_in, clock_out
    FROM staff
    WHERE staff_id = :staff_id;
    """
    params = {"staff_id": staff_id}
    staff_info = execute_query(query, params=params)
    return staff_info


def add_staff(role, employment_date, department=None, salary=None):
    """CREATE: Add a new staff member to the database."""
    query = """
    INSERT INTO staff (role, employment_date, department, salary)
    VALUES (:role, :employment_date, :department, :salary);
    """
    params = {
        "role": role,
        "employment_date": employment_date,
        "department": department,
        "salary": salary,
    }
    execute_non_query(query, params=params)


def update_staff_info(staff_id, role, department, salary):
    """UPDATE: Update an existing staff member's information."""
    query = """
    UPDATE staff
    SET role = :role,
        department = :department,
        salary = :salary
    WHERE staff_id = :staff_id;
    """
    params = {
        "staff_id": staff_id,
        "role": role,
        "department": department,
        "salary": salary,
    }
    execute_non_query(query, params=params)


def delete_staff(staff_id):
    """DELETE: Delete a staff member from the database."""
    query = """
    DELETE FROM staff
    WHERE staff_id = :staff_id;
    """
    params = {"staff_id": staff_id}
    execute_non_query(query, params=params)