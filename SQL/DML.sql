-- Insert sample data into Member table
INSERT INTO Member (first_name, last_name, height, weight) VALUES
('John', 'Doe', 175.5, 82.3),
('Jane', 'Smith', 162.3, 58.7),
('Alice', 'Johnson', 170.0, 64.0);

-- Insert sample data into Trainer table
INSERT INTO Trainer (first_name, last_name) VALUES
('Tom', 'Hardy'),
('Emma', 'Watson');

-- Insert sample data into TrainerAvailability table
INSERT INTO TrainerAvailability (trainer_id, date, start_time, end_time) VALUES
(1, '2024-04-10', '08:00:00', '12:00:00'),
(2, '2024-04-11', '09:00:00', '13:00:00');

-- Insert sample data into Billing table
INSERT INTO Billing (category, amount, date, member_id, status) VALUES
('Membership Fee', 120.00, '2024-04-01', 1, 'Paid'),
('Personal Training', 50.00, '2024-04-05', 2, 'Pending');

-- Insert sample data into FitnessGoals table
INSERT INTO FitnessGoals (member_id, goals) VALUES
(1, 'Increase strength and endurance'),
(2, 'Lose weight and gain flexibility');

-- Insert sample data into ExerciseRoutines table
INSERT INTO ExerciseRoutines (member_id, routines) VALUES
(1, 'Weight lifting, Cardio'),
(2, 'Yoga, Pilates');

-- Insert sample data into PTSession table
INSERT INTO PTSession (session_date, start_time, end_time, trainer_id, member_id) VALUES
('2024-04-10', '10:00:00', '11:00:00', 1, 1),
('2024-04-11', '11:00:00', '12:00:00', 2, 2);

-- Insert sample data into FitnessClass table
INSERT INTO FitnessClass (class_name, class_date, start_time, end_time, num_participants, max_participants, trainer_id) VALUES
('Yoga Basics', '2024-04-10', '08:00:00', '09:30:00', 5, 20, 1),
('Pilates Intro', '2024-04-11', '10:00:00', '11:30:00', 3, 15, 2);

-- Insert sample data into EnrolledMembers table
INSERT INTO EnrolledMembers (class_id, member_id) VALUES
(1, 1),
(1, 2),
(2, 2);

-- Insert sample data into Bookings table
INSERT INTO Bookings (room_name, class_id) VALUES
('Room A', 1),
('Room B', 2);

-- Insert sample data into AdminStaff table
INSERT INTO AdminStaff (first_name, last_name) VALUES
('Bob', 'Builder'),
('Sue', 'Chef');

-- Insert sample data into FitnessEquipment table
INSERT INTO FitnessEquipment (equipment_name, last_maintenance) VALUES
('Treadmill', '2024-03-01'),
('Elliptical', '2024-01-15');
