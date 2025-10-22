

-- Create Database --
create database if not exists doctor_office;

-- Use Database --
use doctor_office; 

-- Patient Table --
create table if not exists patient (
    patient_id int primary key,
    fname varchar(100),
    lname varchar(100),
    pdob date,
    gender varchar(100),
    email varchar(100),
    allergies varchar(1000),
    medications varchar(1000),
    phone_number varchar(100),
    address varchar(100),
    doc_id int,
    insur_id int,
    FOREIGN KEY (doc_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY (insur_id) REFERENCES insurance(insurance_id)
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
    appointment_date datetime,
    reason_for_visit varchar(1000),
    status varchar(100),
    visit_notes varchar(1000),
    patient_id int,
    doctor_id int,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
);

-- Past Visits Table --
create table if not exists past_visits (
    visit_id int primary key, 
    visit_reason varchar(100), 
    visit_notes varchar(100),
    patient_id int,
    doctor_id int,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
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
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
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

-- checks
alter table patient
add constraint ins_check check (insur_id IS NOT NULL);

alter table appointment
add constraint status_val check (status in ("Scheduled","Completed","Confirmed","Not Confirmed", "Cancelled"))

-- add check to make sure meds != allergies

-- view patient_info
create view patient_info as
    select p.fname as first_name, p.lname as last_name, p.pdob as date_of_birth, p.phone_number, a.appointment_date as next_appointment, d.lname as doctor, i.iprovider as insurance_provider, i.ilimitations as policy_limits
    from patient p 
    join appointment a on p.patient_id = a.patient_id
    join insurance i on p.insur_id = i.insurance_id
    join doctor d on p.doc_id = d.doctor_id
    order by last_name, first_name;


-- drop
drop table appointment;