use doctor_office; 

-- Patient Table --
create table patient (
    patient_id int primary key, 
    pname varchar(100), 
    pdob date, 
    next_visit datetime, 
    visit_notes varchar(1000), 
    gender varchar(100), 
    email varchar(100), 
    allergies varchar(100), 
    medications varchar(1000), 
    phone_number varchar(100),
    address varchar(100),
    doc_id int,
    insur_id,
    FOREIGN KEY (doc_id) REFERENCES doctor(doctor_id),
    FOREIGN KEY (insur_id) REFERENCES insurance(insurance_id)
); 

-- Insurance Table --
create table insurance (
    insurance_id int primary key, 
    iprovider varchar(100), 
    ilimitations varchar(100), 
    inotes varchar(100), 
    email varchar(100), 
    phone_number varchar(100)
); 

-- Appointment Table --
create table appointment (
    appointment_id int primary key, 
    reason_for_visit varchar(1000), 
    status varchar(100),
    patient_id int,
    doctor_id int,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
); 

-- Past Visits Table --
create table past_visits (
    visit_id int primary key, 
    visit_reason varchar(100), 
    visit_notes varchar(100),
    patient_id int,
    doctor_id int,
    FOREIGN KEY (patient_id) REFERENCES patient(patient_id),
    FOREIGN KEY (doctor_id) REFERENCES doctor(doctor_id)
); 

-- Staff Table --
create table staff (
    staff_id int primary key, 
    department varchar(100), 
    role varchar(100), 
    salary int, 
    employment_date date, 
    clock_in timestamp, 
    clock_out timestamp
); 

-- Supplies Table --
create table supplies (
    supply_id int primary key, 
    quantity int,
    supplier_name varchar(100), 
    price int, 
    supply_name varchar(100), 
    type_of_product varchar(100), 
    expiration_date date, 
    in_stock varchar(100),
    staff_id,
    FOREIGN KEY (staff_id) REFERENCES staff(staff_id)
); 

-- Doctor Table --
create table doctor (
    doctor_id int primary key, 
    dname varchar(100), 
    role varchar(100), 
    salary int, 
    email varchar(100), 
    phone_number varchar(100), 
    address varchar(100)
); 