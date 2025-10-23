
-- query to get insurance details for a specific patient (nested)
select * from insurance where insurance_id = (
    select insur_id from patient where patient_id = 1
);

-- get number of patients assigned to each doctor (join)
select d.fname, d.lname, count(*) as num_patients from doctor d join patient p on d.doctor_id = p.doc_id group by d.fname, d.lname;

-- update patient phone number
update patient set phone_number = '555-9999' where patient_id = 3;

-- remove patient record if no long with office
delete from patient where patient_id = 10;

-- get supplies where amount is less than 10
select supply_name from supplies where quantity < 10;

-- query to get all for 1 patient from the patient_info
select * from patient_info where patient_last_name = 'Doe' and patient_first_name = 'John';

-- get all the patients names treated by House 
select p.fname, p.lname from patient p join doctor d on p.doc_id = d.doctor_id where d.lname = 'House';

-- query to get upcoming appointments for a specific doctor from view
select * from  doctor_schedule where doctor_last_name = 'Cuddy';
