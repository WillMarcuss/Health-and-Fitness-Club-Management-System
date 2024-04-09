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


def display_member_dashboard(member_id,selection):
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
    fitnessClasses = db.execute_query(
    "SELECT fc.* FROM EnrolledMembers em JOIN fitnessclass fc ON em.class_id = fc.class_id WHERE em.member_id = %s",
    (member_id,),
    fetch=True
)
    if selection == "1":
        print(f"Fitness Goals: {goals}")
    elif selection == "2":
        print(f"Exercise Routines: {routines}")
    elif selection == "3":
        manage_pt_session(member_id)
    elif selection == "4":
        for fitclass in fitnessClasses:
            print(f"\nFitness Class: {fitclass[1]} scheduled for {fitclass[2]} from {fitclass[3]} to {fitclass[4]}")

def manage_pt_session(member_id):
    print("\n---- Manage PT Sessions ----")
    while True:
        ptSessions = db.execute_query( "SELECT pts.*, tr.first_name AS trainer_first_name, tr.last_name AS trainer_last_name FROM ptsession pts JOIN trainer tr ON pts.trainer_id = tr.trainer_id WHERE pts.member_id = %s",(member_id,),fetch=True)
        selection = input("\n1. View my PT sessions\n2. Reschedule session\n3. Cancel session\n4. Exit\nEnter Choice: ")
        if selection == "1":
            for sesh in ptSessions:
                print(f"\nPT Session ID: {sesh[0]} on {sesh[1]} from {sesh[2]} to {sesh[3]} with Trainer: {sesh[6]} {sesh[7]}")
        elif selection == "2":
            sessionID = input("\nEnter the session ID in which you would like to reschedule: ")
            while True:
                date = input("Enter the date you would like to reschedule to (yyyy-mm-dd): ")
                startTime = input("Enter the start time you would like to reschedule to (ex: 09:00): ")
                endTime = input("Enter the end time you would like to reschedule to (ex: 10:00): ")
                if checkDateTimeValidity(date,startTime,endTime):
                    break
                else:
                    print("-- Please enter a valid date -- ")
            db.execute_query("UPDATE PTsession SET session_date = %s, start_time = %s, end_time = %s WHERE session_id = %s;",(date,startTime,endTime,sessionID))
            print(f"PT Session Reschedule successfully to: {date} from {startTime} to {endTime}")

        elif selection == "3":
            sessionID = input("Enter the session ID of the session you would like to cancel: ")
            session_exists = db.execute_query("SELECT COUNT(*) FROM PTsession WHERE session_id = %s AND member_id = %s;", (sessionID, member_id), fetch=True)
            if session_exists[0][0] == 0:
                print(f"No sessions were found with the specified session ID under Member ID: {member_id}.")
            else:
                db.execute_query("DELETE FROM PTsession WHERE session_id = %s AND member_id = %s;", (sessionID,member_id))
                print("PT session canceled successfully")
            

        
        elif selection == "4":
            break
        

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
