import dbController as db

# Register a new member
def register_member():
    print("Register New Member")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    height = input("Height (cm): ")
    weight = input("Weight (kg): ")
    member_id = db.execute_query(
        "INSERT INTO member (first_name, last_name, height, weight) VALUES (%s, %s, %s, %s) RETURNING member_id;",
        (first_name, last_name, float(height), float(weight)),
        fetch=True,
    )[0]["member_id"]
    print(
        f"Registered successfully. Your member ID is {member_id}. Please remember it for login."
    )

# 2. Profile Management
def update_member_profile(member_id, first_name=None, last_name=None, height=None, weight=None):
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
    db.execute_query("UPDATE Member SET " + ", ".join(fields) + " WHERE member_id = %s;", tuple(values),fetch=True,)

# 3. Dashboard Display
def display_member_dashboard(member_id):
    routines = db.execute_query("SELECT * FROM ExerciseRoutines WHERE member_id = %s;", (member_id,),fetch=True,)[0]["routines"]
    goals = db.execute_query("SELECT * FROM FitnessGoals WHERE member_id = %s;", (member_id,),fetch=True,)[0]["goals"]
    print(f"Exercise Routines: {routines}")
    print(f"Fitness Goals: {goals}")

# 4. Schedule Management
def schedule_session(member_id, trainer_id, session_date, start_time, end_time):
    trainer = db.execute_query("SELECT * FROM PTSession WHERE trainer_id = %s AND session_date = %s AND ((start_time <= %s AND end_time > %s) OR (start_time < %s AND end_time >= %s));",
                   (trainer_id, session_date, start_time, start_time, end_time, end_time),fetch=True,)[0]
    if trainer:
        print("Trainer not available at the requested time.")
        return
    db.execute_query("INSERT INTO PTSession (session_date, start_time, end_time, trainer_id, member_id) VALUES (%s, %s, %s, %s, %s);",
                   (session_date, start_time, end_time, trainer_id, member_id),fetch=True,)
    print("Session scheduled successfully.")