import streamlit as st
import pandas as pd
from routes.styles import load_styles
from crud.staff_crud import *
from datetime import datetime


def render():
    load_styles()
    
    st.title("Staff — Management")
    st.divider()
    
    # --- Fetch all staff data (READ) ---
    staff_query = """
        SELECT staff_id, role, department, employment_date, salary, clock_in, clock_out
        FROM staff
        ORDER BY role, employment_date
    """
    
    staffDF = pd.read_sql(staff_query, st.session_state["conn"])
    
    # --- Display Staff Table ---
    st.subheader("Staff Directory")
    if staffDF.empty:
        st.info("No Staff Members Found")
    else:
        table_data = []
        for row in staffDF.itertuples():
            employment_str = row.employment_date.strftime("%Y-%m-%d") if pd.notna(row.employment_date) else "—"
            salary_str = f"${row.salary:,.2f}" if pd.notna(row.salary) else "—"
            
            table_data.append({
                "ID": row.staff_id,
                "Role": row.role,
                "Department": row.department if pd.notna(row.department) else "—",
                "Employment Date": employment_str,
                "Salary": salary_str,
            })
        st.table(table_data)
    
    st.divider()
    
    # --- CRUD Operations Tabs ---
    tab1, tab2, tab3 = st.tabs(["Add Staff", "Update Staff", "Delete Staff"])
    
    # --- Add Staff ---
    with tab1:
        st.subheader("Add New Staff Member")
        with st.form("add_staff_form"):
            new_role = st.text_input("Role *", placeholder="e.g., Receptionist, Nurse")
            new_department = st.text_input("Department", placeholder="e.g., Front Desk, Clinical")
            new_employment_date = st.date_input("Employment Date *", value=datetime.today())
            new_salary = st.number_input("Salary", min_value=0.0, step=1000.0, format="%.2f")
            
            add_submitted = st.form_submit_button("Add Staff Member")
            
            if add_submitted:
                if not new_role:
                    st.error("Role is required.")
                else:
                    try:
                        add_staff(
                            role=new_role,
                            employment_date=new_employment_date,
                            department=new_department if new_department else None,
                            salary=new_salary if new_salary > 0 else None,
                        )
                        st.success(f"Successfully added new staff member: {new_role}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error adding staff member: {e}")
    
    # --- Update Staff ---
    with tab2:
        st.subheader("Update Staff Information")
        
        if not staffDF.empty:
            staff_options = {f"ID {row.staff_id} - {row.role}": row.staff_id 
                           for row in staffDF.itertuples()}
            selected_staff_label = st.selectbox("Select Staff Member", list(staff_options.keys()))
            selected_staff_id = staff_options[selected_staff_label]
            
            current_info = staffDF[staffDF["staff_id"] == selected_staff_id].iloc[0]
            
            with st.form("update_staff_form"):
                update_role = st.text_input("Role", value=current_info["role"] if pd.notna(current_info["role"]) else "")
                update_department = st.text_input("Department", value=current_info["department"] if pd.notna(current_info["department"]) else "")
                update_salary = st.number_input("Salary", value=float(current_info["salary"]) if pd.notna(current_info["salary"]) else 0.0, min_value=0.0, step=1000.0, format="%.2f")
                
                update_submitted = st.form_submit_button("Update Staff Member")
                
                if update_submitted:
                    try:
                        update_staff_info(
                            staff_id=selected_staff_id,
                            role=update_role,
                            department=update_department if update_department else None,
                            salary=update_salary if update_salary > 0 else None,
                        )
                        st.success(f"Successfully updated staff member ID {selected_staff_id}")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error updating staff member: {e}")
        else:
            st.info("No staff members available to update.")
    
    # --- Delete Staff ---
    with tab3:
        st.subheader("Delete Staff Member")
        st.warning("WARNING: This action cannot be undone.")
        
        if not staffDF.empty:
            staff_delete_options = {f"ID {row.staff_id} - {row.role}": row.staff_id 
                                   for row in staffDF.itertuples()}
            selected_delete_label = st.selectbox("Select Staff Member to Delete", list(staff_delete_options.keys()), key="delete_select")
            selected_delete_id = staff_delete_options[selected_delete_label]
            
            confirm_delete = st.checkbox(f"I confirm I want to delete staff member ID {selected_delete_id}")
            
            if st.button("Delete Staff Member", type="primary", disabled=not confirm_delete):
                try:
                    delete_staff(selected_delete_id)
                    st.success(f"Successfully deleted staff member ID {selected_delete_id}")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error deleting staff member: {e}")
        else:
            st.info("No staff members available to delete.")
