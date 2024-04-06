import functions as fs


# Member interface
def member_interface(member_id):
    print(f"\nWelcome Member {member_id}")
    while True:
        print(
            "\n1. Update Profile\n2. View Dashboard\n3. Schedule Personal Training Session\n4. Register for Group Fitness Class\n5. Logout"
        )
        choice = input("Enter choice: ")
        if choice == "1":
            # Assume update_member_profile function exists and is implemented correctly
            pass
        elif choice == "2":
            # Assume display_member_dashboard function exists and is implemented correctly
            pass
        elif choice == "3":
            # Assume schedule_session function exists and is implemented correctly
            pass
        elif choice == "4":
            # Assume register_for_class function exists and is implemented correctly
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
            # Assume set_trainer_availability function exists and is implemented correctly
            pass
        elif choice == "2":
            # Assume view_member_profile_by_name function exists and is implemented correctly
            pass
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
            fs.register_member()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid option.")


main()
