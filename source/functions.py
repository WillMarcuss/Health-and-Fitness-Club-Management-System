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
    # First, check if the date and time formats are valid
    if not checkDateTimeValidity(date, sTime, eTime):
        print("Invalid date or time formats.")
        return False

    # Fetch all existing time slots for the same trainer and date
    fetch_query = """
    SELECT start_time, end_time FROM TrainerAvailability
    WHERE trainer_id = %s AND date = %s
    """
    existing_slots = db.execute_query(fetch_query, (trainer_id, date), fetch=True)

    # Check for unacceptable time overlaps
    for slot in existing_slots:
        if not is_acceptable_overlap(
            sTime, eTime, slot["start_time"], slot["end_time"]
        ):
            print("Unacceptable overlap detected with existing trainer availability.")
            return False

    # Insert the new availability into the TrainerAvailability table
    insert_query = """
    INSERT INTO TrainerAvailability (trainer_id, date, start_time, end_time)
    VALUES (%s, %s, %s, %s)
    """
    db.execute_query(insert_query, (trainer_id, date, sTime, eTime))
    print("Trainer availability successfully added.")
    return True


def checkDateTimeValidity(date, sTime, eTime):
    try:
        # Check if the date, start time, and end time are in the correct format
        datetime.datetime.strptime(date, "%Y-%m-%d")  # Date in 'yyyy-mm-dd' format
        datetime.datetime.strptime(sTime, "%H:%M")  # Start time in 'hh:mm' format
        datetime.datetime.strptime(eTime, "%H:%M")  # End time in 'hh:mm' format

        # Combine date and time to create datetime objects
        start_datetime = datetime.datetime.strptime(f"{date} {sTime}", "%Y-%m-%d %H:%M")
        end_datetime = datetime.datetime.strptime(f"{date} {eTime}", "%Y-%m-%d %H:%M")

        # Check if the end time is after the start time
        return end_datetime > start_datetime
    except ValueError:
        # Return False if there is a parsing error (invalid format)
        return False


def is_acceptable_overlap(new_start, new_end, existing_start, existing_end):
    # Convert string times to datetime.time objects for comparison
    new_start = datetime.datetime.strptime(new_start, "%H:%M").time()
    new_end = datetime.datetime.strptime(new_end, "%H:%M").time()

    # Check if new time slot overlaps with the existing one
    return new_end <= existing_start or new_start >= existing_end


def search_for_member(fName=None, lName=None):
    # Check if the strings are not None and not just empty or spaces
    if (fName is None or fName.strip() == "") and (
        lName is None or lName.strip() == ""
    ):
        return None

    # Start building the query with the condition that exists
    query = "SELECT * FROM Member WHERE "
    args = []

    if fName is not None and fName.strip() != "":
        # Add condition for first name using LOWER for case-insensitive comparison
        query += "LOWER(first_name) = LOWER(%s)"
        args.append(fName.strip())  # Use strip() to remove any extra spaces

    if lName is not None and lName.strip() != "":
        if args:
            # Add 'AND' only if the first name condition is also included
            query += " AND "
        # Add condition for last name using LOWER for case-insensitive comparison
        query += "LOWER(last_name) = LOWER(%s)"
        args.append(lName.strip())  # Use strip() to remove any extra spaces

    # Execute the query and fetch the results
    results = db.execute_query(query, args, fetch=True)
    return results
