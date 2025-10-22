
-- query to fetch all patients

-- query to fetch all doctors

-- query to fetch all appointments

-- query to fetch appointments for a specific patient

-- query to fetch appointments for a specific doctor

-- query to fetch patients assigned to a specific doctor

-- query to fetch past visits for a specific patient

-- quert to fetch staff details

-- query to fetch supplies details

-- query to fetch supplies provided by a specific staff member

-- query to fetch doctors with a specific role

-- query to fetch patients with a specific ailment

-- query to fetch appointments with a specific status

-- query to get insurance details for a specific patient
select * from insurance where insurance_id = (
    select insur_id from patient where patient_id = 1
);

-- get number of patients assigned to each doctor
select d.fname, d.lname, count(*) as num_patients from doctor d join patient p on d.doctor_id = p.doc_id group by d.fname, d.lname;
