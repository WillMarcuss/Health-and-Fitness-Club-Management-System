import dbController as db
import datetime


def check_id_exists(id_value, table, id_column):
    result = db.execute_query(
        f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {id_column} = %s);",
        (id_value,),
        fetch=True,
    )
    return result[0]["exists"]


def register_member(first_name, last_name, height, weight):
    member_id = db.execute_query(
        "INSERT INTO member (first_name, last_name, height, weight) VALUES (%s, %s, %s, %s) RETURNING member_id;",
        (first_name, last_name, float(height), float(weight)),
        fetch=True,
    )[0]["member_id"]
    print(
        f"Registered successfully. Your member ID is {member_id}. Please remember it for login."
    )


def update_member_profile(
    member_id, first_name=None, last_name=None, height=None, weight=None
):
    fields = []
    values = []
    if first_name:
        fields.append("first_name = %s")
        values.append(first_name)
    if last_name:
        fields.append("last_name = %s")
        values.append(last_name)
    if height:
        fields.append("height = %s")
        values.append(height)
    if weight:
        fields.append("weight = %s")
        values.append(weight)
    values.append(member_id)
    db.execute_query(
        "UPDATE Member SET " + ", ".join(fields) + " WHERE member_id = %s;",
        tuple(values),
        fetch=True,
    )


def display_member_dashboard(member_id):
    routines = db.execute_query(
        "SELECT * FROM ExerciseRoutines WHERE member_id = %s;",
        (member_id,),
        fetch=True,
    )[0]["routines"]
    goals = db.execute_query(
        "SELECT * FROM FitnessGoals WHERE member_id = %s;",
        (member_id,),
        fetch=True,
    )[0]["goals"]
    print(f"Exercise Routines: {routines}")
    print(f"Fitness Goals: {goals}")


def schedule_session(member_id, trainer_id, session_date, start_time, end_time):
    trainer = db.execute_query(
        "SELECT * FROM PTSession WHERE trainer_id = %s AND session_date = %s AND ((start_time <= %s AND end_time > %s) OR (start_time < %s AND end_time >= %s));",
        (trainer_id, session_date, start_time, start_time, end_time, end_time),
        fetch=True,
    )[0]
    if trainer:
        print("Trainer not available at the requested time.")
        return
    db.execute_query(
        "INSERT INTO PTSession (session_date, start_time, end_time, trainer_id, member_id) VALUES (%s, %s, %s, %s, %s);",
        (session_date, start_time, end_time, trainer_id, member_id),
        fetch=True,
    )
    print("Session scheduled successfully.")


def set_trainer_availability(trainer_id, date, sTime, eTime):
    if not checkDateTimeValidity(date, sTime, eTime):
        print("\nInvalid date or time formats.")
        return

    fetch_query = """
    SELECT start_time, end_time FROM TrainerAvailability
    WHERE trainer_id = %s AND date = %s
    """
    existing_slots = db.execute_query(fetch_query, (trainer_id, date), fetch=True)

    for slot in existing_slots:
        if not is_acceptable_overlap(
            sTime, eTime, slot["start_time"], slot["end_time"]
        ):
            print("\nUnacceptable overlap detected with existing trainer availability.")
            return

    insert_query = """
    INSERT INTO TrainerAvailability (trainer_id, date, start_time, end_time)
    VALUES (%s, %s, %s, %s)
    """
    db.execute_query(insert_query, (trainer_id, date, sTime, eTime))
    print("\nTrainer availability successfully added.")


def checkDateTimeValidity(date, sTime, eTime):
    try:
        datetime.datetime.strptime(date, "%Y-%m-%d")
        datetime.datetime.strptime(sTime, "%H:%M")
        datetime.datetime.strptime(eTime, "%H:%M")

        start_datetime = datetime.datetime.strptime(f"{date} {sTime}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.datetime.strptime(f"{date} {eTime}", "%Y-%m-%d %H:%M")

        return end_datetime > start_datetime
    except ValueError:
        return False


def is_acceptable_overlap(new_start, new_end, existing_start, existing_end):
    new_start = datetime.datetime.strptime(new_start, "%H:%M").time()
    new_end = datetime.datetime.strptime(new_end, "%H:%M").time()
    return new_end <= existing_start or new_start >= existing_end


def search_for_member(fName=None, lName=None):
    if (fName is None or fName.strip() == "") and (
        lName is None or lName.strip() == ""
    ):
        return None

    query = "SELECT * FROM Member WHERE "
    args = []

    if fName is not None and fName.strip() != "":
        query += "LOWER(first_name) = LOWER(%s)"
        args.append(fName.strip())

    if lName is not None and lName.strip() != "":
        if args:
            query += " AND "

        query += "LOWER(last_name) = LOWER(%s)"
        args.append(lName.strip())

    results = db.execute_query(query, args, fetch=True)
    return results


#Admin Functions
# 1. Manage Room Bookings
def manageRoomBookings():
    print("\n--- Manage Room Bookings ---\n")
    print("1. View Room Bookings")
    print("2. Update Room Booking")
    print("3. Exit\n")
    choice = input("Enter Choice: ")
    
    if choice == '1':
        print('\n====================================================')
        print('\nAll scheduled room bookings (starting from earliest date):\n')
        roomBookings = db.execute_query("SELECT b.booking_id, b.room_name, f.*, t.first_name, t.last_name FROM bookings b JOIN fitnessclass f ON b.class_id = f.class_id JOIN trainer t ON f.trainer_id = t.trainer_id ORDER BY f.class_date ASC", (), fetch=True)
        
        for roomBooking in roomBookings:

            print("Room: " + roomBooking['room_name'] + '\n')

            classDetails = roomBooking[2:]
            print(f"Class: {classDetails[1]}")
            print(f"Date: {classDetails[2]}")
            print(f"Start Time: {classDetails[3]}")
            print(f"End Time: {classDetails[4]}")
            
            trainerDetails = roomBooking[10:]
            print(f"Trainer: {trainerDetails[0]} {trainerDetails[1]}\n")
        
        print('====================================================')

    elif choice == '2':
        bookingID = input("\nEnter Booking ID: ")
        newRoomName = input("Enter new name for the room: ")

        booking = db.execute_query("SELECT * FROM bookings WHERE booking_id = %s;", (bookingID,), fetch=True)

        if booking:
            db.execute_query("UPDATE bookings SET room_name = %s WHERE booking_id = %s;", (newRoomName, bookingID), fetch=False)
            print("\nSuccessfully updated booking!")
        else:
            print('\nBooking ID does not exist.')

    elif choice == '3':
        return
    
    else:
        print("Invalid option.")

# 2. Monitor Equipment Maintenance
def monitorEquipmentMaintenance():
    print("\n--- Monitor Equipment Maintenance ---\n")
    print("1. View Equipment Maintenance")
    print("2. Update Equipment's Maintenance Date")
    print("3. Add Equipment + Maintenance Date")
    print("4. Exit\n")
    choice = input("Enter Choice: ")
    
    if choice == '1':
        print('\n====================================================')
        print('\nAll equipment maintenance records:\n')
        maintenanceRecords = db.execute_query("SELECT * FROM fitnessequipment;", (), fetch=True)
        
        for record in maintenanceRecords:
            print(f"Equipment ID: {record[0]}")
            print(f"Equipment Name: {record[1]}")
            print(f"Last Maintenance Date: {record[2]}\n")
        
        print('====================================================')

    elif choice == '2':
        equipmentID = input("\nEnter Equipment ID to update maintenance date: ")
        newDate = input("Enter new maintenance date (YYYY-MM-DD): ")

        equipment = db.execute_query("SELECT * FROM fitnessequipment WHERE equipment_id = %s;", (equipmentID,), fetch=True)

        if equipment:
            db.execute_query("UPDATE fitnessequipment SET last_maintenance = %s WHERE equipment_id = %s;", (newDate, equipmentID), fetch=False)
            print("\nSuccessfully updated equipment maintenance date!\n")
        else:
            print('\nEquipment ID does not exist.\n')

    elif choice == '3':
        equipmentName = input("\nEnter new Equipment Name: ")
        maintenanceDate = input("Enter Maintenance Date (YYYY-MM-DD): ")

        db.execute_query("INSERT INTO fitnessequipment (equipment_name, last_maintenance) VALUES (%s, %s);", (equipmentName, maintenanceDate), fetch=False)

        print("\nSuccessfully added new equipment and maintenance date!\n")

    elif choice == '4':
        print("Exiting maintenance monitor.")
        return
    
    else:
        print("Invalid option.")

# 3. Update Class Schedules
def updateClassSchedule():
    print("\n--- Update Class Schedule ---\n")
    print("1. View Class Schedules")
    print("2. Update Class Schedule")
    print("3. Add New Class to Schedule")
    print("4. Exit\n")
    choice = input("Enter Choice: ")

    if choice == '1':
        print('\n====================================================')
        print('\nAll scheduled fitness classes:\n')
        classSchedules = db.execute_query("SELECT * FROM fitnessclass;", (), fetch=True)

        for schedule in classSchedules:
            print(f"Class Name: {schedule[1]}")
            print(f"Class Date: {schedule[2]}")
            print(f"Start Time: {schedule[3]}")
            print(f"End Time: {schedule[4]}\n")

        print('====================================================')

    elif choice == '2':
        classID = input("\nEnter Class ID to update: ")
        newDate = input("Enter new class date (YYYY-MM-DD): ")
        newStartTime = input("Enter new start time (HH:MM): ")
        newEndTime = input("Enter new end time (HH:MM): ")

        fitnessClass = db.execute_query("SELECT * FROM fitnessclass WHERE class_id = %s;", (classID,), fetch=True)
        
        if fitnessClass:
            db.execute_query("UPDATE fitnessclass SET class_date = %s, start_time = %s, end_time = %s WHERE class_id = %s;", (newDate, newStartTime, newEndTime, classID))
            print("\nClass schedule updated successfully!")
        else:
            print("\nClass ID not found.")

    elif choice == '3':
        className = input("\nEnter new class name: ")
        classDate = input("Enter class date (YYYY-MM-DD): ")
        startTime = input("Enter start time (HH:MM): ")
        endTime = input("Enter end time (HH:MM): ")
        maxParticipants = input("Enter max participants (#): ")
        trainerID = input("Enter trainer ID: ")

        trainerAvailability = db.execute_query("SELECT * FROM trainer_availability WHERE trainer_id = %s AND date = %s AND start_time <= %s AND end_time >= %s;", (trainerID, classDate, startTime, endTime), fetch=True)

        ptSessionCollision = db.execute_query("SELECT * FROM ptsession WHERE trainer_id = %s AND session_date = %s AND ((start_time <= %s AND end_time > %s) OR (start_time < %s AND end_time >= %s) OR (start_time >= %s AND end_time <= %s));", (trainerID, classDate, startTime, startTime, endTime, endTime, startTime, endTime), fetch=True)

        classCollision = db.execute_query("SELECT * FROM fitnessclass WHERE trainer_id = %s AND class_date = %s AND ((start_time <= %s AND end_time > %s) OR (start_time < %s AND end_time >= %s) OR (start_time >= %s AND end_time <= %s));", (trainerID, classDate, startTime, startTime, endTime, endTime, startTime, endTime), fetch=True)

        if trainerAvailability and not ptSessionCollision and not classCollision:
            db.execute_query("INSERT INTO fitnessclass (class_name, class_date, start_time, end_time, num_participants, max_participants, trainer_id) VALUES (%s, %s, %s, %s, %s, %s, %s);", (className, classDate, startTime, endTime, 0, maxParticipants, trainerID), fetch=False)
            print("\nNew class schedule added successfully!")
        else:
            print("\nThe trainer is not available during the given date and time or there is a collision with an existing session/class.")

    elif choice == '4':
        return

    else:
        print("\nInvalid choice, please try again.")

# 4. Process Payments
