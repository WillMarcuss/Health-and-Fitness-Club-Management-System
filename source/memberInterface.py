import functions as fs


def register():
    print("\nRegister New Member ($120 fee)")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    height = input("Height (cm): ")
    weight = input("Weight (kg): ")
    goals = input("Fitness Goals: ")
    routines = input("Exercise Routines: ")
    member_id = fs.register_member(first_name, last_name, height, weight, goals, routines)
    print(
        f"\nRegistered successfully. Your member ID is {member_id}. Please remember it for login."
    )


def updateProfile(member_id):
    print("\n---- Update Your Profile ----")
    while True:
        try:
            first_name = input("First name: ")
            last_name = input("Last name: ")
            height = input("Height (cm): ")
            weight = input("Weight (kg): ")
            goals = input("Fitness Goals: ")
            routines = input("Exercise Routines: ")
            fs.update_member_profile(member_id, first_name, last_name, height, weight, goals, routines)
            break
        except:
            print("Please enter valid input for goals")
    


def displayDashboard(member_id):
    print("\n---- Member Dashboard ----")
    print("Member: ", member_id)
    while True:
        selection = input(
            "\n1. View Fitness Goals\n2. View Exercise Routines\n3. Manage PT Sessions\n4. View My Group Fitness Classes\n5. Exit\nEnter Choice: "
        )
        if selection == "1":
            print(f"\nFitness Goals: {fs.fetchGoals(member_id)}")
        elif selection == "2":
            print(f"\nExercise Routines: {fs.fetchRoutines(member_id)}")
        elif selection == "3":
            managePTSessions(member_id)
        elif selection == "4":
            fitnessClasses = fs.fetchMemberClasses(member_id)
            for fitclass in fitnessClasses:
                print(
                    f"\nFitness Class ID {fitclass[0]}: {fitclass[1]} scheduled for {fitclass[2]} from {fitclass[3]} to {fitclass[4]}"
                )
        if selection == "5":
            break


def schedulePTSessions(member_id):
    print("\n---- Schedule PT Session ----")
    while True:
        selection = input(
            "\n1. View Trainers\n2. Schedule Session ($50)\n3. Exit\nEnter Choice: "
        )
        if selection == "1":
            trainers = fs.fetchTrainers()
            if trainers is not None:
                for row in trainers:
                    print("\nTrainer ID: ", row["trainer_id"])
                    print("Trainer Name: ", row["first_name"], row["last_name"])
                    print("Availability Date: ", row["date"])
                    print("Start Time: ", row["start_time"])
                    print("End Time: ", row["end_time"])
                    print("---------------------")
        elif selection == "2":
            try:
                trainerID = input("Enter the trainer ID you would like to schedule with: ")
                date = input("Enter the date you would like to schedule (yyyy-mm-dd): ")
                sTime = input("Enter the start time: ")
                eTime = input("Enter the end time: ")
                fs.schedule_session(member_id, trainerID, date, sTime, eTime)
            except:
                print("Please enter valid Trainer ID")
        elif selection == "3":
            break


def registerClasses(member_id):
    print("\n---- Register for Group Fitness Classes ----")
    while True:
        selection = input(
            "\n1. View Classes\n2. Register for Classes ($25)\n3. Exit\nEnter Choice: "
        )
        if selection == "1":
            classes = fs.fetchFitnessClasses()
            for fitclass in classes:
                print(
                    f"\nFitness Class ID {fitclass[0]}: {fitclass[1]} scheduled for {fitclass[2]} from {fitclass[3]} to {fitclass[4]}"
                )
        elif selection == "2":
            classes = fs.fetchClassIDs()
            class_id = input("\nEnter the class ID you would like to register for: ")
            if not class_id in classes:
                print("\nClass ID does not exist.")
            else:
                if not fs.isRegistered(member_id, class_id):
                    fs.registerForClass(member_id, class_id)
                    print("\nSuccesfully registered for this class!")
                else:
                    print("\nYou are already registered for this class!")
        elif selection == "3":
            break


def managePTSessions(member_id):
    print("\n---- Manage PT Sessions ----")
    while True:
        selection = input(
            "\n1. View my PT sessions\n2. Reschedule session\n3. Cancel session\n4. Exit\nEnter Choice: "
        )
        if selection == "1":
            ptSessions = fs.fetchPTSessions(member_id)
            for sesh in ptSessions:
                print(
                    f"\nPT Session ID: {sesh[0]} on {sesh[1]} from {sesh[2]} to {sesh[3]} with Trainer: {sesh[6]} {sesh[7]}"
                )
        elif selection == "2":
            reschedulePTSession(member_id)
        elif selection == "3":
            cancelSession(member_id)
        elif selection == "4":
            break


def reschedulePTSession(member_id):

    session_id = input("\nEnter the session ID in which you would like to reschedule: ")
    try:
        session_exists = fs.checkPTSessionExists(member_id, session_id)
    except:
        print("Not a valid session ID, please try again")
        return
    if session_exists[0][0] == 0:
        print(
            f"No sessions were found with the specified session ID under Member ID: {member_id}."
        )
    else:
        while True:
            trainerID = fs.findTrainerForSession(session_id)
            trainerID = trainerID[0][0]
            date = input(
                "Enter the date you would like to reschedule to (yyyy-mm-dd): "
            )
            startTime = input(
                "Enter the start time you would like to reschedule to (ex: 09:00): "
            )
            endTime = input(
                "Enter the end time you would like to reschedule to (ex: 10:00): "
            )
            if fs.checkDateTimeValidity(
                date, startTime, endTime
            ) and fs.trainer_is_available(trainerID, date, startTime, endTime):
                break
            else:
                print("\nPlease enter a valid date and time. ")
        fs.reschedulePTSession(date, startTime, endTime, session_id)
        print(
            f"PT Session Reschedule successfully to: {date} from {startTime} to {endTime}"
        )


def cancelSession(member_id):
    session_id = input("Enter the session ID of the session you would like to cancel: ")
    try:
        session_exists = fs.checkPTSessionExists(member_id, session_id)
    except:
         print("Not a valid session ID, please try again")
         return
    if session_exists[0][0] == 0:
        print(
            f"No sessions were found with the specified session ID under Member ID: {member_id}."
        )
    else:
        fs.deletePTSession(member_id, session_id)
        print("PT session canceled successfully")
