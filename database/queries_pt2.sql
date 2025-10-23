-- Update patient phone number
UPDATE patient 
SET phone_number = "543-9876" 
WHERE patient_id = 10;

-- Remove patient record
DELETE FROM patient 
WHERE patient_id = 10;

-- Get supplies where amount < 10
SELECT * 
FROM supplies 
WHERE quantity < 10;

-- Query to get one patient's data from patient_info view
SELECT * 
FROM patient_info 
WHERE patient_last_name = 'Chris' AND patient_first_name = 'Martinez';

-- Get all patients names treated by House
SELECT DISTINCT p.fname, p.lname
FROM patient p
JOIN doctor d ON p.doc_id = d.doctor_id
WHERE d.lname = 'House';

-- Check that patient's allergy does not equal medications
SELECT patient_id, fname, lname, allergies, medications
FROM patient
WHERE allergies = medications;