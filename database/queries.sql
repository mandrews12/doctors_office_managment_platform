
-- Get distribution of patients across doctors
SELECT d.fname, d.lname, count(*) as num_patients 
FROM doctor d 
JOIN patient p ON d.doctor_id = p.doc_id 
GROUP BY d.fname, d.lname;

-- Find all patients treated by Dr. House
SELECT DISTINCT p.fname, p.lname
FROM patient p
JOIN doctor d ON p.doc_id = d.doctor_id
WHERE d.lname = 'House';

-- View upcoming appointments for Dr. House
SELECT * 
FROM doctor_schedule 
WHERE doctor_last_name = 'House';

-- Get detailed information for a specific patient
SELECT * 
FROM patient_info 
WHERE patient_last_name = 'Lopez' AND patient_first_name = 'Ethan';

-- Get insurance details for a patient
SELECT * 
FROM insurance 
WHERE insurance_id = (
    SELECT insur_id 
    FROM patient 
    WHERE patient_id = 1
);

-- Identify supplies that need reordering
SELECT * 
FROM supplies 
WHERE quantity < 10;

-- Add more supplies after order recieved
update supplies
set quantity = quantity + 10
where supply_id = 4;

-- Verify no patients have allergies to their medications
SELECT patient_id, fname, lname, allergies, medications
FROM patient
WHERE allergies = medications;

-- Update patient contact information
UPDATE patient 
SET phone_number = "543-9876" 
WHERE patient_id = 10;

-- Delete a patient record
DELETE FROM patient 
WHERE patient_id = 10;

-- more examples of joins
select * from past_visits pv
join patient p on pv.patient_id = p.patient_id
where p.lname = 'Lopez';

select * from past_visits pv
join doctor d on pv.doctor_id = d.doctor_id
where d.lname = 'House';