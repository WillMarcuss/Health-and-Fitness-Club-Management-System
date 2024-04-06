-- Creating the Member table
CREATE TABLE Member (
    member_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    height NUMERIC(5, 2),
    weight NUMERIC(5, 2)
);

-- Creating the Trainer table
CREATE TABLE Trainer (
    trainer_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

-- Creating the Billing table
CREATE TABLE Billing (
    billing_id SERIAL PRIMARY KEY,
    category VARCHAR(255),
    amount NUMERIC(10, 2),
    date DATE,
    member_id INT,
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

-- Creating the Fitness Goals table
CREATE TABLE FitnessGoals (
    member_id INT PRIMARY KEY,
    goals TEXT,
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

-- Creating the Exercise Routines table
CREATE TABLE ExerciseRoutines (
    member_id INT PRIMARY KEY,
    routines TEXT,
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

-- Creating the PT Session table
CREATE TABLE PTSession (
    session_id SERIAL PRIMARY KEY,
    session_date DATE,
    start_time TIME,
    end_time TIME,
    trainer_id INT,
    member_id INT,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id),
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

-- Creating the Fitness Class table
CREATE TABLE FitnessClass (
    class_id SERIAL PRIMARY KEY,
    class_name VARCHAR(255),
    class_date DATE,
    start_time TIME,
    end_time TIME,
    num_participants INT,
    max_participants INT,
    trainer_id INT,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
);

-- Creating the EnrolledMembers junction table for a many-to-many relationship
CREATE TABLE EnrolledMembers (
    class_id INT,
    member_id INT,
    PRIMARY KEY (class_id, member_id),
    FOREIGN KEY (class_id) REFERENCES FitnessClass(class_id),
    FOREIGN KEY (member_id) REFERENCES Member(member_id)
);

-- Creating the Bookings table
CREATE TABLE Bookings (
    booking_id SERIAL PRIMARY KEY,
    room_name VARCHAR(255),
    class_id INT,
    FOREIGN KEY (class_id) REFERENCES FitnessClass(class_id)
);

-- Creating the Admin Staff table
CREATE TABLE AdminStaff (
    employee_id SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255)
);

-- Creating the Fitness Equipment table
CREATE TABLE FitnessEquipment (
    equipment_id SERIAL PRIMARY KEY,
    equipment_name VARCHAR(255),
    last_maintenance DATE
);
