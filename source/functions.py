import dbController as db
import datetime


def check_id_exists(id_value, table, id_column):
    result = db.execute_query(
        f"SELECT EXISTS(SELECT 1 FROM {table} WHERE {id_column} = %s);",
        (id_value,),
        fetch=True,
    )
    return result[0]["exists"]


def register_member(first_name, last_name, height, weight, goals, routines):
    member_id = db.execute_query(
        "INSERT INTO member (first_name, last_name, height, weight) VALUES (%s, %s, %s, %s) RETURNING member_id;",
        (first_name, last_name, float(height), float(weight)),
        fetch=True,
    )[0]["member_id"]

    db.execute_query(
        "INSERT INTO FitnessGoals (member_id,goals) VALUES (%s, %s)", (member_id, goals)
    )
    db.execute_query(
        "INSERT INTO ExerciseRoutines (member_id,routines) VALUES (%s, %s)",
        (member_id, routines),
    )

    db.execute_query(
    "INSERT INTO Billing (category, amount, date, member_id, status) VALUES (%s, %s, CURRENT_DATE, %s, %s)",
    ("Membership Fee", 120, member_id, "Pending")
)

    return member_id


def update_member_profile(
    member_id,
    first_name=None,
    last_name=None,
    height=None,
    weight=None,
    fitnessgoals=None,
    exerciseroutines=None,
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
    if fitnessgoals:
        db.execute_query(
            "UPDATE FitnessGoals SET goals = %s WHERE member_id = %s;",
            (fitnessgoals, member_id),
        )
    if exerciseroutines:
        db.execute_query(
            "UPDATE ExerciseRoutines SET routines = %s WHERE member_id = %s;",
            (exerciseroutines, member_id),
        )
    values.append(member_id)
    db.execute_query(
        "UPDATE Member SET " + ", ".join(fields) + " WHERE member_id = %s;",
        tuple(values),
    )


def fetchRoutines(member_id):
    return db.execute_query(
        "SELECT * FROM ExerciseRoutines WHERE member_id = %s;",
        (member_id,),
        fetch=True,
    )[0]["routines"]


def fetchGoals(member_id):
    return db.execute_query(
        "SELECT * FROM FitnessGoals WHERE member_id = %s;",
        (member_id,),
        fetch=True,
    )[0]["goals"]


def fetchMemberClasses(member_id):
    return db.execute_query(
        "SELECT fc.* FROM EnrolledMembers em JOIN fitnessclass fc ON em.class_id = fc.class_id WHERE em.member_id = %s",
        (member_id,),
        fetch=True,
    )


def fetchPTSessions(member_id):
    return db.execute_query(
        "SELECT pts.*, tr.first_name AS trainer_first_name, tr.last_name AS trainer_last_name FROM ptsession pts JOIN trainer tr ON pts.trainer_id = tr.trainer_id WHERE pts.member_id = %s",
        (member_id,),
        fetch=True,
    )


def checkPTSessionExists(member_id, session_id):
    return db.execute_query(
        "SELECT COUNT(*) FROM PTsession WHERE session_id = %s AND member_id = %s;",
        (session_id, member_id),
        fetch=True,
    )


def findTrainerForSession(session_id):
    return db.execute_query(
        "SELECT trainer_id FROM ptsession WHERE session_id = %s;",
        (session_id,),
        fetch=True,
    )


def reschedulePTSession(date, startTime, endTime, session_id):
    db.execute_query(
        "UPDATE PTsession SET session_date = %s, start_time = %s, end_time = %s WHERE session_id = %s;",
        (date, startTime, endTime, session_id),
    )


def deletePTSession(member_id, session_id):
    db.execute_query(
        "DELETE FROM PTsession WHERE session_id = %s AND member_id = %s;",
        (session_id, member_id),
    )


def fetchTrainers():
    return db.execute_query(
        """
    SELECT t.*, ta.date, ta.start_time, ta.end_time
    FROM trainer t
    LEFT JOIN traineravailability ta ON t.trainer_id = ta.trainer_id
    """,
        fetch=True,
    )


def fetchFitnessClasses():
    return db.execute_query("SELECT * FROM FitnessClass", fetch=True)


def fetchClassIDs():
    classes = db.execute_query("SELECT class_id FROM FitnessClass", fetch=True)
    classes = [str(sublist[0]) for sublist in classes]
    return classes


def schedule_session(member_id, trainer_id, session_date, start_time, end_time):
    if not (
        checkDateTimeValidity(session_date, start_time, end_time)
        and trainer_is_available(trainer_id, session_date, start_time, end_time)
    ):
        print("Trainer not available at the requested time.")
        return
    db.execute_query(
        "INSERT INTO PTSession (session_date, start_time, end_time, trainer_id, member_id) VALUES (%s, %s, %s, %s, %s);",
        (session_date, start_time, end_time, trainer_id, member_id),
    )
    db.execute_query(
    "INSERT INTO Billing (category, amount, date, member_id, status) VALUES (%s, %s, CURRENT_DATE, %s, %s)",
    ("Personal Training", 50, member_id, "Pending"))
    print("Session scheduled successfully.")


def trainer_is_available(trainer_id, session_date, start_time, end_time):
    trainer = db.execute_query(
        "SELECT * FROM PTSession WHERE trainer_id = %s AND session_date = %s AND ((start_time <= %s AND end_time > %s) OR (start_time < %s AND end_time >= %s));",
        (trainer_id, session_date, start_time, start_time, end_time, end_time),
        fetch=True,
    )
    trainerHours = db.execute_query(
        "SELECT * FROM traineravailability WHERE trainer_id = %s AND date = %s AND (%s >= start_time AND %s <= end_time);",
        (trainer_id, session_date, start_time, end_time),
        fetch=True,
    )

    if trainer or not trainerHours:
        return False
    else:
        return True


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

def billingsAndPayment():
    print("\n--- Billings and Payment ---")
    print("1. View Billings")
    print("2. Process Payments")
    print("3. Exit")
    choice = input("Enter Choice: ")

    if choice == '1':
        while True:
            print("\n--- Billings ---")
            print("1. View Unpaid Billings")
            print("2. View Paid Billings")
            print("3. Exit")
            billing_choice = input("Enter Choice: ")

            if billing_choice == '1':
                unpaid_billings = db.execute_query("SELECT * FROM billing WHERE status = %s;", ('Pending',), fetch=True)
                print("\n--- Unpaid Billings ---")
                for billing in unpaid_billings:
                    print(f"Billing ID: {billing['billing_id']}, Amount: {billing['amount']}, Date: {billing['date']}")
                
            elif billing_choice == '2':
                paid_billings = db.execute_query("SELECT * FROM billing WHERE status = %s;", ('Paid',), fetch=True)
                print("\n--- Paid Billings ---")
                for billing in paid_billings:
                    print(f"Billing ID: {billing['billing_id']}, Amount: {billing['amount']}, Date: {billing['date']}")
                
            elif billing_choice == '3':
                break
            else:
                print("Invalid option.")
    
    elif choice == '2':
        billing_id = input("\nEnter Billing ID to process payment: ")

        billing = db.execute_query("SELECT * FROM billing WHERE billing_id = %s;", (billing_id,), fetch=True)
        if billing:
            db.execute_query("UPDATE billing SET status = %s WHERE billing_id = %s;", ('Paid', billing_id,), fetch=False)
            print(f"Billing ID {billing_id} has been charged and is now paid.")
        else:
            print("Billing ID does not exist.")

    elif choice == '3':
        return
    else:
        print("Invalid option.")
def isRegistered(member_id, class_id):
    return db.execute_query(
        """ SELECT EXISTS (
                SELECT 1 FROM EnrolledMembers
                WHERE member_id = %s AND class_id = %s
            ) AS is_member;""",
        (member_id, class_id),
        fetch=True,
    )[0]["is_member"]


def registerForClass(member_id, class_id):
    db.execute_query(
        "INSERT INTO EnrolledMembers (class_id,member_id) VALUES (%s, %s);",
        (class_id, member_id),
    )
    db.execute_query(
        "UPDATE fitnessclass SET num_participants = num_participants + 1 WHERE class_id = %s;",
        (class_id),
    )
    db.execute_query(
    "INSERT INTO Billing (category, amount, date, member_id, status) VALUES (%s, %s, CURRENT_DATE, %s, %s)",
    ("Fitness Class", 25, member_id, "Pending"))
