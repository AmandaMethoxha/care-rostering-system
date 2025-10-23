-- 1️⃣ Staff Details
CREATE TABLE IF NOT EXISTS staff_details (
    id SERIAL PRIMARY KEY,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    job_role VARCHAR(50),
    line_manager VARCHAR(100),
    contracted_hours DECIMAL,
    primary_team VARCHAR(50),
    preferred_travel_type VARCHAR(50),
    start_date DATE,
    leave_date DATE,
    email VARCHAR(100),
    work_number VARCHAR(50),
    postcode VARCHAR(10)
);

-- 2️⃣ Service User Details
CREATE TABLE IF NOT EXISTS service_user_details (
    id SERIAL PRIMARY KEY,
    unique_reference_code VARCHAR(20),
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    date_of_birth DATE,
    gender VARCHAR(10),
    rag_rating VARCHAR(10),
    nhs_number VARCHAR(15),
    start_date DATE,
    end_date DATE,
    primary_team VARCHAR(50),
    contact_number VARCHAR(50),
    contact_email VARCHAR(100),
    full_address VARCHAR(255),
    keysafe_code VARCHAR(10)
);

-- 3️⃣ Staff Regular Availability
CREATE TABLE IF NOT EXISTS staff_availability (
    id SERIAL PRIMARY KEY,
    staff_id INT REFERENCES staff_details(id) ON DELETE CASCADE,
    monday BOOLEAN DEFAULT FALSE,
    tuesday BOOLEAN DEFAULT FALSE,
    wednesday BOOLEAN DEFAULT FALSE,
    thursday BOOLEAN DEFAULT FALSE,
    friday BOOLEAN DEFAULT FALSE,
    saturday BOOLEAN DEFAULT FALSE,
    sunday BOOLEAN DEFAULT FALSE,
    start_time TIME,
    end_time TIME
);

-- Table: service_user_assignements
CREATE TABLE IF NOT EXISTS service_user_assignments (
    id SERIAL PRIMARY KEY,
    staff_id INT REFERENCES staff_details(id) ON DELETE CASCADE,
    service_user_id INT REFERENCES service_user_details(id) ON DELETE CASCADE,
    assignment_date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    notes TEXT
);

CREATE TABLE IF NOT EXISTS service_user_needs (
    id SERIAL PRIMARY KEY,
    service_user_id INT REFERENCES service_user_details(id) ON DELETE CASCADE,
    care_type VARCHAR(50),        -- e.g. Nurse, Doctor, Carer, Physiotherapist
    description TEXT,             -- e.g. “Morning medication assistance”
    frequency VARCHAR(50),        -- e.g. “Daily”, “Weekly”, “Mon/Wed/Fri”
    preferred_time TIME,          -- e.g. 09:00
    duration_minutes INT,         -- e.g. 30
    active BOOLEAN DEFAULT TRUE
);
