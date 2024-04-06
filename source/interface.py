import psycopg2
import psycopg2.extras
import sys


# Database connection setup
def connect_db():
    return psycopg2.connect(
        host="localhost", database="Health-Fitness-Club", user="postgres", password="comp3005", port="5432"
    )


# Generic query execution helper
def execute_query(query, args=(), fetch=False):
    conn = connect_db()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    cursor.execute(query, args)
    if fetch:
        result = cursor.fetchall()
        conn.commit()
        cursor.close()
        conn.close()
        return result
    else:
        conn.commit()
        cursor.close()
        conn.close()


# Register a new member
def register_member():
    print("Register New Member")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    height = input("Height (cm): ")
    weight = input("Weight (kg): ")
    member_id = execute_query(
        "INSERT INTO member (first_name, last_name, height, weight) VALUES (%s, %s, %s, %s) RETURNING member_id;",
        (first_name, last_name, float(height), float(weight)),
        fetch=True,
    )[0]["member_id"]
    print(
        f"Registered successfully. Your member ID is {member_id}. Please remember it for login."
    )


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
            member_interface(member_id)
        elif choice == "2":
            trainer_id = input("Enter Trainer ID: ")
            trainer_interface(trainer_id)
        elif choice == "3":
            admin_interface()
        elif choice == "4":
            register_member()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid option.")


main()
