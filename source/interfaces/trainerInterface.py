import utility as util


def setAvailability(trainer_id):
    print("\n---- Set Your Availability ----")
    date = input("Date (yyyy-mm-dd): ")
    start_time = input("Start Time (hh:mm): ")
    end_time = input("End Time (hh:mm): ")
    util.set_trainer_availability(trainer_id, date, start_time, end_time)


def searchForMember():
    print("\n---- Search Member Profiles ----")
    fName = input("Member's First Name: ")
    lName = input("Member's Last Name: ")
    results = util.search_for_member(fName, lName)
    if results is not None:
        print("\n---- Showing Matching Members ----")
        for member in results:
            print(
                f"\n{member['first_name']} {member['last_name']} -- Attributes: Height: {member['height']} cm, Weight: {member['weight']} kg"
            )
