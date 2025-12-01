-- MEMBER
CREATE TABLE IF NOT EXISTS member (
    member_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    date_of_birth DATE,
    gender VARCHAR(20),
    phone VARCHAR(20),
    created_at TIMESTAMP DEFAULT NOW()
);

-- TRAINER
CREATE TABLE IF NOT EXISTS trainer (
    trainer_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    specialization VARCHAR(100),
    phone VARCHAR(20)
);
-- ADMIN STAFF
CREATE TABLE IF NOT EXISTS adminstaff (
    admin_id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role VARCHAR(50)
);
-- ROOM
CREATE TABLE IF NOT EXISTS room (
    room_id SERIAL PRIMARY KEY,
    room_name VARCHAR(100) NOT NULL,
    location VARCHAR(100),
    capacity INT,
    admin_id INT REFERENCES adminstaff(admin_id)
); 
-- EQUIPMENT
CREATE TABLE IF NOT EXISTS equipment (
    equipment_id SERIAL PRIMARY KEY,
    room_id INT REFERENCES room(room_id),
    name VARCHAR(100) NOT NULL,
    status VARCHAR(20) CHECK (status IN ('working','broken','in_repair'))
);

-- FITNESS GOAL
CREATE TABLE IF NOT EXISTS fitnessgoal (
    goal_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    goal_type VARCHAR(50) NOT NULL,
    target_value NUMERIC,
    current_value NUMERIC,
    target_date DATE,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT NOW()
);
-- HEALTH METRICS
CREATE TABLE IF NOT EXISTS healthmetric (
    metric_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    weight NUMERIC,
    heart_rate INT,
    body_fat NUMERIC,
    recorded_at TIMESTAMP DEFAULT NOW()
);

-- TRAINER AVAILABILITY
CREATE TABLE IF NOT EXISTS traineravailability (
    availability_id SERIAL PRIMARY KEY,
    trainer_id INT REFERENCES trainer(trainer_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL
);

-- GROUP CLASS
CREATE TABLE IF NOT EXISTS groupclass (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(100) NOT NULL,
    trainer_id INT REFERENCES trainer(trainer_id),
    room_id INT REFERENCES room(room_id),
    admin_id INT REFERENCES adminstaff(admin_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    capacity INT
);
-- CLASS REGISTRATION
CREATE TABLE classregistration (
    registration_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    class_id INT REFERENCES groupclass(class_id),
    registered_at TIMESTAMP DEFAULT NOW()
);
-- PERSONAL TRAINING SESSION
CREATE TABLE IF NOT EXISTS personaltrainingSession (
    session_id SERIAL PRIMARY KEY,
    member_id INT REFERENCES Member(member_id),
    trainer_id INT REFERENCES trainer(trainer_id),
    room_id INT REFERENCES room(room_id),
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    status VARCHAR(20) CHECK (status IN ('scheduled','cancelled','completed'))
);
-- MAINTENANCE RECORD
CREATE TABLE IF NOT EXISTS maintenancerecord (
    maintenance_id SERIAL PRIMARY KEY,
    equipment_id INT REFERENCES equipment(equipment_id),
    admin_id INT REFERENCES adminstaff(admin_id),
    issue_description TEXT NOT NULL,
    reported_at TIMESTAMP DEFAULT NOW(),
    resolved_at TIMESTAMP,
    status VARCHAR(20) CHECK (status IN ('open','in_progress','resolved'))
);