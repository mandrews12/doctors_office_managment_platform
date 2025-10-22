
-- query to get insurance details for a specific patient (nested)
select * from insurance where insurance_id = (
    select insur_id from patient where patient_id = 1
);

-- get number of patients assigned to each doctor (join)
select d.fname, d.lname, count(*) as num_patients from doctor d join patient p on d.doctor_id = p.doc_id group by d.fname, d.lname;

-- update patient phone number

-- remove patient record if no long with office

-- get supplies where amount is less than 10

-- query to get all for 1 patient from the patient_info

-- get all the patients names treated by House 


