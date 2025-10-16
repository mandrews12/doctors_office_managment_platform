
-- Appointment Table --

-- Doctor Table --

-- Insurance Table

-- Past Visits Table --

-- Patient Table --

-- Staff Table --

-- Supplies Table --

-- Foreign Keys --

ALTER TABLE patient
ADD FOREIGN KEY (doc_id) REFERENCES doctor(doctor_id);

ALTER TABLE patient
ADD FOREIGN KEY (insur_id) REFERENCES insurance(insurance_id);

ALTER TABLE appointment
ADD FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id);

ALTER TABLE appointment
ADD FOREIGN KEY (patient_id) REFERENCES patient(patient_id);

ALTER TABLE past_visits
ADD FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id);

ALTER TABLE past_visits
ADD FOREIGN KEY (patient_id) REFERENCES patient(patient_id);

ALTER TABLE supplies
ADD FOREIGN KEY (staff_id) REFERENCES staff(staff_id);