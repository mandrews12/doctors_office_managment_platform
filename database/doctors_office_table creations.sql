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
    appointment_date datetime not null,
    reason_for_visit varchar(1000),
    status varchar(100),
    visit_notes varchar(1000),
    patient_id int not null,
    doctor_id int not null,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
);

-- Past Visits Table --
create table if not exists past_visits (
    visit_id int primary key, 
    visit_reason varchar(100), 
    visit_notes varchar(100),
    patient_id int not null,
    doctor_id int not null,
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

-- drop
drop table appointment;

drop view patient_info;

-- indexes
create index idx_patient_name on patient (lname, fname);

create index idx_doctor_name on doctor (lname, fname);

create index idx_appointment_date on appointment (appointment_date);