import utility as fs
import interfaces.trainerInterface as trainer
import interfaces.memberInterface as member
import interfaces.adminInterface as admin

# Member interface
def member_interface(member_id):
    print(f"\nWelcome Member {member_id}")
    while True:
        print(
            "\n1. Update Profile\n2. View Dashboard\n3. Schedule Personal Training Session\n4. Register for Group Fitness Class\n5. Logout"
        )
        choice = input("Enter choice: ")
        if choice == "1":
            member.updateProfile(member_id)
        elif choice == "2":
            member.displayDashboard(member_id)
        elif choice == "3":
            member.schedulePTSessions(member_id)
        elif choice == "4":
            member.registerClasses(member_id)
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
    print("\nWelcome Admin") #
    while True:
        print(
            "\n1. Manage Room Bookings\n2. Monitor Equipment Maintenance\n3. Update Class Schedules\n4. Process Payments\n5. Logout"
        )
        choice = input("Enter choice: ")
        if choice == "1":
            admin.manageRoomBookings()
        elif choice == "2":
            admin.monitorEquipmentMaintenance()
        elif choice == "3":
            admin.updateClassSchedule()
            pass
        elif choice == "4":
            admin.billingsAndPayment()
            pass
        elif choice == "5":
            break
        else:
            print("Invalid option.")


# Main menu
def main():
    while True:
        print(
            "\nMain Menu\n1. Login as a Member\n2. Login as Trainer\n3. Login as Admin\n4. Register\n5. Exit"
        )
        choice = input("Enter choice: ")
        if choice == "1":
            member_id = input("Enter Member ID: ")
            try:
                if fs.check_id_exists(member_id, "member", "member_id"):
                    member_interface(member_id)
                else:
                    print("\nMember ID does not exist. Please try again.")
            except:
                print("Please enter a valid Member ID")
        elif choice == "2":
            trainer_id = input("Enter Trainer ID: ")
            if trainer_id.isdigit():
                if fs.check_id_exists(trainer_id, "trainer", "trainer_id"):
                    trainer_interface(trainer_id)
                else:
                    print("\nTrainer ID does not exist. Please try again.")
            else:
                print("Please enter a valid Trainer ID")
        elif choice == "3":
            employee_id = input("Enter Employee ID: ")
            if employee_id.isdigit():
                if fs.check_id_exists(employee_id, "adminstaff", "employee_id"):
                    admin_interface()
                else:
                    print("\nEmployee ID does not exist. Please try again.")
            else:
                print("Please enter a valid Employee ID")
        elif choice == "4":
            member.register()
        elif choice == "5":
            print("\nGoodbye!")
            break
        else:
            print("\nInvalid option.")


main()
