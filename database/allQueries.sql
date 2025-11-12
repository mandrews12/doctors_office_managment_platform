-- Create Database --
create database if not exists doctor_office;

-- Use Database --
use doctor_office; 

-- Patient Table --
create table if not exists patient (
    patient_id int primary key,
    fname varchar(100) not null,
    lname varchar(100) not null,
    pdob date not null,
    gender varchar(100) not null,
    email varchar(100),
    allergies varchar(1000),
    medications varchar(1000),
    phone_number varchar(100) not null,
    address varchar(100),
    doc_id int,
    insur_id int,
    FOREIGN KEY (doc_id) REFERENCES doctor(doctor_id) ON DELETE SET NULL,
    FOREIGN KEY (insur_id) REFERENCES insurance(insurance_id) ON DELETE SET NULL
);

-- Insurance Table --
create table if not exists insurance (
    insurance_id int primary key, 
    iprovider varchar(100), 
    ilimitations varchar(100), 
    inotes varchar(100), 
    email varchar(100), 
    phone_number varchar(100)
); 

-- Appointment Table --
create table if not exists appointment (
    appointment_id int primary key,
    appointment_date datetime not null,
    reason_for_visit varchar(1000),
    status varchar(100),
    visit_notes varchar(1000),
    patient_id int not null,
    doctor_id int not null,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id) ON DELETE CASCADE
);

-- Past Visits Table --
create table if not exists past_visits (
    visit_id int primary key, 
    visit_reason varchar(100), 
    visit_notes varchar(100),
    patient_id int not null,
    doctor_id int not null,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id) ON DELETE CASCADE,
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id) ON DELETE CASCADE
); 

-- Staff Table --
create table if not exists staff (
    staff_id int primary key, 
    department varchar(100), 
    role varchar(100), 
    salary int, 
    employment_date date, 
    clock_in timestamp, 
    clock_out timestamp
); 

-- Supplies Table --
create table if not exists supplies (
    supply_id int primary key, 
    quantity int,
    supplier_name varchar(100), 
    price int, 
    supply_name varchar(100), 
    type_of_product varchar(100), 
    expiration_date date, 
    in_stock varchar(100),
    staff_id int,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id) ON DELETE SET NULL
); 

-- Doctor Table --
create table if not exists doctor (
    doctor_id int primary key, 
    fname varchar(100), 
    lname varchar(100),
    role varchar(100), 
    salary int, 
    email varchar(100), 
    phone_number varchar(100), 
    address varchar(100)
); 

-- alters and constraints
alter table patient
add constraint ins_check check (insur_id IS NOT NULL);

alter table appointment
add constraint status_val check (status in ("Scheduled","Completed","Confirmed","Not Confirmed", "Cancelled"));

alter table patient
add constraint med_allergy_check check (medications != allergies);

-- views
create view patient_info as
    select p.fname as patient_first_name, p.lname as patient_last_name, p.pdob as date_of_birth, p.phone_number, a.appointment_date as next_appointment, d.lname as doctor, i.iprovider as insurance_provider, i.ilimitations as policy_limits
    from patient p 
    join appointment a on p.patient_id = a.patient_id
    join insurance i on p.insur_id = i.insurance_id
    join doctor d on p.doc_id = d.doctor_id
    order by patient_last_name, patient_first_name;

create view doctor_schedule as
    select d.fname as doctor_first_name, d.lname as doctor_last_name, a.appointment_date, p.fname as patient_first_name, p.lname as patient_last_name, a.reason_for_visit, a.status
    from doctor d
    join appointment a on d.doctor_id = a.doctor_id
    join patient p on a.patient_id = p.patient_id
    order by d.lname, d.fname, a.appointment_date;

-- indexes
create index idx_patient_name on patient (lname, fname);

create index idx_doctor_name on doctor (lname, fname);

create index idx_appointment_date on appointment (appointment_date);

/*
This part of the SQL file is part of the "Doctors Office Management Platform" project. 
It contains sample/demo data for populating the database, which was generated using AI tools. 
The data is intended for testing and development purposes only and does not represent real-world data.
*/

-- insert data into patient table
insert into patient (patient_id, fname, lname, pdob, gender, email, allergies, medications, phone_number, address, doc_id, insur_id) values
(1, 'John', 'Doe', '1985-02-14', 'Male', 'john.doe@email.com', 'Penicillin', 'Lisinopril', '555-1001', '12 Oak St', 1, 1),
(2, 'Jane', 'Smith', '1990-06-23', 'Female', 'jane.smith@email.com', 'None', 'Ibuprofen', '555-1002', '45 Maple Rd', 2, 2),
(3, 'Michael', 'Brown', '1978-11-02', 'Male', 'michael.brown@email.com', 'Peanuts', 'Metformin', '555-1003', '87 Birch Ave', 3, 3),
(4, 'Emily', 'Davis', '2001-08-19', 'Female', 'emily.davis@email.com', 'Sulfa drugs', 'Albuterol', '555-1004', '99 Cedar Dr', 4, 4),
(5, 'Sarah', 'Lee', '1995-12-09', 'Female', 'sarah.lee@email.com', 'Latex', 'Sertraline', '555-1005', '100 Pine St', 5, 5),
(6, 'David', 'Johnson', '1982-04-04', 'Male', 'david.j@email.com', 'None', 'Aspirin', '555-1006', '77 Elm St', 2, 1),
(7, 'Laura', 'Kim', '1999-10-12', 'Female', 'laura.kim@email.com', 'Nuts', 'Epinephrine', '555-1007', '56 Oak Rd', 4, 3),
(8, 'Chris', 'Martinez', '1975-03-17', 'Male', 'chris.m@email.com', 'None', 'Insulin', '555-1008', '23 Spruce St', 5, 5),
(9, 'Olivia', 'Clark', '2012-07-22', 'Female', 'olivia.clark@email.com', 'Strawberries', 'None', '555-1009', '9 Cherry Ln', 3, 2),
(10, 'Ethan', 'Lopez', '1988-09-05', 'Male', 'ethan.lopez@email.com', 'None', 'Omeprazole', '555-1010', '11 Walnut Ave', 5, 4);

-- insert data into appointment table
insert into appointment (appointment_id, appointment_date, reason_for_visit, status, visit_notes, patient_id, doctor_id) values
(1, '2026-10-20 09:30:00', 'Annual checkup', 'Scheduled', NULL, 1, 1),
(2, '2026-10-2 14:00:00', 'Follow-up for flu', 'Scheduled', NULL, 2, 2),
(3, '2026-10-23 11:00:00', 'Child vaccination', 'Scheduled', NULL, 9, 3),
(4, '2026-10-25 10:15:00', 'Skin rash evaluation', 'Scheduled', NULL, 4, 4),
(5, '2026-10-27 13:30:00', 'Migraine consultation', 'Scheduled', NULL, 10, 5),
(6, '2026-11-02 09:00:00', 'Blood pressure follow-up', 'Scheduled', NULL, 6, 2),
(7, '2026-11-05 15:00:00', 'Skin treatment review', 'Scheduled', NULL, 7, 4),
(8, '2026-11-07 10:30:00', 'MRI results discussion', 'Scheduled', NULL, 8, 5),
(9, '2026-11-09 09:15:00', 'Pediatric wellness exam', 'Scheduled', NULL, 9, 3),
(10, '2026-11-10 16:00:00', 'Neurological follow-up', 'Scheduled', NULL, 5, 5);

-- insert data into doctor table
insert into doctor (doctor_id, fname, lname, role, salary, email, phone_number, address) values
(1, 'James', 'Wilson', 'Cardiologist', 150000, 'jwilson@doctors.com', '555-1111', '123 Heart St'),
(2, 'Lisa', 'Cuddy', 'General Physician', 130000, 'lcuddy@doctors.com', '555-2222', '456 Wellness Ave'),
(3, 'Robert', 'Chase', 'Pediatrician', 125000, 'rchase@doctors.com', '555-3333', '789 Care Rd'),
(4, 'Allison', 'Cameron', 'Dermatologist', 140000, 'acameron@doctors.com', '555-4444', '321 Skin Blvd'),
(5, 'Gregory', 'House', 'Neurologist', 200000, 'ghouse@doctors.com', '555-5555', '999 Puzzle Dr');

-- insert data into past_visits table
insert into past_visits (visit_id, visit_reason, visit_notes, patient_id, doctor_id) values
(1, 'Checkup', 'Healthy overall, advised exercise', 1, 1),
(2, 'Cold symptoms', 'Prescribed rest and fluids', 2, 2),
(3, 'Ear infection', 'Antibiotics prescribed', 3, 3),
(4, 'Allergy test', 'Positive for pollen', 4, 4),
(5, 'Back pain', 'Referred to physical therapy', 5, 5),
(6, 'Annual physical', 'Blood work normal', 6, 2),
(7, 'Skin rash', 'Cream prescribed', 7, 4),
(8, 'MRI scan', 'Detected mild nerve inflammation', 8, 5),
(9, 'Flu shot', 'Tolerated well', 9, 3),
(10, 'Headache', 'Prescribed migraine medication', 10, 5);

-- insert data into supplies table
insert into supplies (supply_id, quantity, supplier_name, price, supply_name, type_of_product, expiration_date, in_stock, staff_id) values
(1, 100, 'MediSupply Co.', 200, 'Bandages', 'Medical', '2026-01-01', 'Yes', 1),
(2, 50, 'HealthPlus', 500, 'Syringes', 'Medical', '2027-03-10', 'Yes', 3),
(3, 20, 'CleanCare', 150, 'Disinfectant', 'Cleaning', '2026-07-15', 'Yes', 4),
(4, 10, 'TechMed', 800, 'Blood Pressure Monitor', 'Equipment', '2030-01-01', 'Yes', 2),
(5, 75, 'Wellness Inc.', 300, 'Gloves', 'Medical', '2026-12-31', 'Yes', 5);

-- insert data into staff table
insert into staff (staff_id, department, role, salary, employment_date, clock_in, clock_out) values
(1, 'Nursing', 'RN', 60000, '2019-03-10', NOW(), NULL),
(2, 'Reception', 'Front Desk', 40000, '2020-06-12', NOW(), NULL),
(3, 'Lab', 'Technician', 55000, '2018-08-01', NOW(), NULL),
(4, 'Admin', 'Office Manager', 65000, '2017-02-19', NOW(), NULL),
(5, 'Nursing', 'LPN', 50000, '2021-04-22', NOW(), NULL);

-- insert data into insurance table
insert into insurance (insurance_id, iprovider, ilimitations, inotes, email, phone_number) values
(1, 'Blue Cross', 'Covers up to 80%', 'Requires referral for specialist', 'contact@bluecross.com', '555-1110'),
(2, 'United Health', 'Full coverage on annual checkups', 'No out-of-network coverage', 'support@uh.com', '555-2220'),
(3, 'Aetna', '70% coverage', 'Requires pre-approval for MRI', 'info@aetna.com', '555-3330'),
(4, 'Cigna', 'Covers dental + vision', 'Low deductible', 'help@cigna.com', '555-4440'),
(5, 'Kaiser', 'Full in-network', 'Requires PCP assignment', 'member@kaiser.com', '555-5550');

show tables;

/* Sample Queries for Doctors Office Management Platform */

/* group by*/
SELECT d.fname, d.lname, count(*) as num_patients 
FROM doctor d 
JOIN patient p ON d.doctor_id = p.doc_id 
GROUP BY d.fname, d.lname;

/* inner join*/
SELECT DISTINCT p.fname, p.lname
FROM patient p
JOIN doctor d ON p.doc_id = d.doctor_id
WHERE d.lname = 'House';

/* nested query*/
SELECT * 
FROM insurance 
WHERE insurance_id = (
    SELECT insur_id 
    FROM patient 
    WHERE patient_id = 1
);

SELECT * 
FROM supplies 
WHERE quantity < 10;

/*update*/
update supplies
set quantity = quantity + 10
where supply_id = 4;

/*update*/
UPDATE patient 
SET phone_number = "543-9876" 
WHERE patient_id = 10;

/*delete*/
DELETE FROM patient 
WHERE patient_id = 10;

/*inner join*/
select * from past_visits pv
join patient p on pv.patient_id = p.patient_id
where p.lname = 'Lopez'
order by visit_id desc;

/*outer join*/
select * from past_visits pv
left join doctor d on pv.doctor_id = d.doctor_id
where d.lname = 'House';

/*between*/
select * from appointment
where appointment_date between '2026-10-20' and '2026-10-27';   

/*aggregate*/
select avg(salary) as avg_doctor_salary
from doctor;

/*not in*/
select fname, lname from patient
where doc_id not in (select doctor_id from doctor where lname = 'House');   

/*exists*/
select p.fname, p.lname
from patient p
where exists (select 1 from appointment a where a.patient_id = p.patient_id and a.status = 'Scheduled');