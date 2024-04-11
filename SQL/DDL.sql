CREATE TABLE Member (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    height NUMERIC(5, 2) CHECK (height > 0),
    weight NUMERIC(5, 2) CHECK (weight > 0)
);

CREATE TABLE Trainer (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

CREATE TABLE TrainerAvailability (
    availability_id SERIAL PRIMARY KEY,
    trainer_id INT NOT NULL,
    date DATE NOT NULL,
    start_time TIME NOT NULL,
    end_time TIME NOT NULL,
    CONSTRAINT fk_trainer_availability
        FOREIGN KEY (trainer_id)
        REFERENCES Trainer(trainer_id)
        ON DELETE CASCADE,
    CONSTRAINT check_time
        CHECK (end_time > start_time)
);

CREATE TABLE Billing (
    billing_id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    amount NUMERIC(10, 2) NOT NULL CHECK (amount >= 0),
    date DATE NOT NULL,
    member_id INT NOT NULL,
    status VARCHAR(255) NOT NULL CHECK (status IN ('Pending', 'Paid', 'Cancelled')),
    CONSTRAINT fk_member_billing
        FOREIGN KEY (member_id)
        REFERENCES Member(member_id)
);

CREATE TABLE FitnessGoals (
    member_id INT PRIMARY KEY,
    goals TEXT,
    CONSTRAINT fk_member_goals
        FOREIGN KEY (member_id)
        REFERENCES Member(member_id)
);

CREATE TABLE ExerciseRoutines (
    member_id INT PRIMARY KEY,
    routines TEXT,
    CONSTRAINT fk_member_routines
        FOREIGN KEY (member_id)
        REFERENCES Member(member_id)
);

CREATE TABLE PTSession (
    session_id SERIAL PRIMARY KEY,
    session_date DATE,
    start_time TIME,
    end_time TIME CHECK (end_time > start_time),
    trainer_id INT,
    member_id INT,
    CONSTRAINT fk_trainer_session
        FOREIGN KEY (trainer_id)
        REFERENCES Trainer(trainer_id),
    CONSTRAINT fk_member_session
        FOREIGN KEY (member_id)
        REFERENCES Member(member_id)
);

CREATE TABLE FitnessClass (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(255),
    class_date DATE,
    start_time TIME,
    end_time TIME CHECK (end_time > start_time),
    num_participants INT DEFAULT 0 CHECK (num_participants >= 0),
    max_participants INT CHECK (max_participants >= 0),
    trainer_id INT,
    CONSTRAINT fk_trainer_class
        FOREIGN KEY (trainer_id)
        REFERENCES Trainer(trainer_id),
    CONSTRAINT check_participants
        CHECK (num_participants <= max_participants)
);

CREATE TABLE EnrolledMembers (
    class_id INT,
    member_id INT,
    PRIMARY KEY (class_id, member_id),
    CONSTRAINT fk_class_enrolled
        FOREIGN KEY (class_id)
        REFERENCES FitnessClass(class_id),
    CONSTRAINT fk_member_enrolled
        FOREIGN KEY (member_id)
        REFERENCES Member(member_id)
);

CREATE TABLE Bookings (
    booking_id SERIAL PRIMARY KEY,
    room_name VARCHAR(255),
    class_id INT,
    CONSTRAINT fk_class_bookings
        FOREIGN KEY (class_id)
        REFERENCES FitnessClass(class_id)
);

CREATE TABLE AdminStaff (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

CREATE TABLE FitnessEquipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(255),
    last_maintenance DATE
);
