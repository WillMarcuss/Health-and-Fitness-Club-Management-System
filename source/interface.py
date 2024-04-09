import functions as fs
import trainerInterface as trainer
import memberInterface as member

# Member interface
def member_interface(member_id):
    print(f"\nWelcome Member {member_id}")
    while True:
        print(
            "\n1. Update Profile\n2. View Dashboard\n3. Schedule Personal Training Session\n4. Register for Group Fitness Class\n5. Logout"
        )
        choice = input("Enter choice: ")
        if choice == "1":
            print("---- Update Your Profile ----")
            first_name = input("First name: ")
            last_name = input("Last name: ")
            height = input("Height (cm): ")
            weight = input("Weight (kg): ")
            goals = input("Fitness Goals: ")
            routines = input("Exercise Routines: ")
            fs.update_member_profile(member_id, first_name, last_name, height, weight,goals,routines)
        elif choice == "2":
            print("\n---- Member Dashboard ----")
            print("Member: ",member_id)
            while True:
                selection = input("\n1. View Fitness Goals\n2. View Exercise Routines\n3. Manage PT Sessions\n4. View My Group Fitness Classes\n5. Exit\nEnter Choice: ")
                if selection == "5":
                    break
                fs.display_member_dashboard(member_id,selection)
            pass
        elif choice == "3":
            print("\n---- Schedule PT Session ----")
            while True:
                selection = input("\n1. View Trainers\n2. Schedule Session\n3. Exit\nEnter Choice: ")
                if selection == "1":
                    fs.print_trainers()
                elif selection == "2":
                    trainerID = input("Enter the trainer ID you would like to schedule with: ")
                    date = input("Enter the date you would like to schedule (yyyy-mm-dd): ")
                    sTime = input("Enter the start time: ")
                    eTime = input("Enter the end time: ")
                    fs.schedule_session(member_id,trainerID,date,sTime,eTime)
                elif selection == "3":
                    break
                

            pass
        elif choice == "4":
            print("\n---- Register for Group Fitness Classes ----")
            while True:
                selection = input("\n1. View Classes\n2. Register for Classes\n3. Exit\nEnter Choice: ")
                if selection == "1":
                    fs.print_classes()
                elif selection == "2":
                    fs.register_for_class(member_id)
                elif selection == "3":
                    break
            pass
        elif choice == "5":
            break
        else:
            print("Invalid option.")


# Trainer interface
def trainer_interface(trainer_id):
    print(f"\nWelcome Trainer {trainer_id}")
    while True:
        print("\n1. Set Availability\n2. View Member Profiles\n3. Logout")
        choice = input("Enter choice: ")
        if choice == "1":
            trainer.setAvailability(trainer_id)
        elif choice == "2":
            trainer.searchForMember()
        elif choice == "3":
            break
        else:
            print("Invalid option.")


# Admin interface
def admin_interface():
    print("\nWelcome Admin")
    while True:
        print(
            "\n1. Manage Room Bookings\n2. Monitor Equipment Maintenance\n3. Update Class Schedules\n4. Process Payments\n5. Logout"
        )
        choice = input("Enter choice: ")
        if choice == "1":
            # Assume book_room function exists and is implemented correctly
            pass
        elif choice == "2":
            # Assume update_equipment_maintenance function exists and is implemented correctly
            pass
        elif choice == "3":
            # Assume update_class_schedule function exists and is implemented correctly
            pass
        elif choice == "4":
            # Assume process_payment function exists and is implemented correctly
            pass
        elif choice == "5":
            break
        else:
            print("Invalid option.")


# Main menu
def main():
    while True:
        print("\nMain Menu")
        print("1. Login as a Member")
        print("2. Login as Trainer")
        print("3. Login as Admin")
        print("4. Register")
        print("5. Exit")
        choice = input("Enter choice: ")
        if choice == "1":
            member_id = input("Enter Member ID: ")
            if fs.check_id_exists(member_id, "member", "member_id"):
                member_interface(member_id)
            else:
                print("\nMember ID does not exist. Please try again.")
        elif choice == "2":
            trainer_id = input("Enter Trainer ID: ")
            if fs.check_id_exists(trainer_id, "trainer", "trainer_id"):
                trainer_interface(trainer_id)
            else:
                print("\nTrainer ID does not exist. Please try again.")
        elif choice == "3":
            employee_id = input("Enter Employee ID: ")
            if fs.check_id_exists(employee_id, "employee", "employee_id"):
                admin_interface()
            else:
                print("\nEmployee ID does not exist. Please try again.")
        elif choice == "4":
           member.register()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid option.")


main()
