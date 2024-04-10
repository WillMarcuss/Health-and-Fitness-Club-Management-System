import functions as fs

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
        print('\nAll scheduled room bookings (starting from earliest date):')

        roomBookings = fs.getRoomBookings()

        if roomBookings:
            for roomBooking in roomBookings:
                print('\n---')

                print("\nRoom: " + roomBooking['room_name'] + '\n')
                
                print(f"Booking ID: {roomBooking['booking_id']}")
                print(f"Class: {roomBooking['class_name']}")
                print(f"Date: {roomBooking['class_date']}")
                print(f"Start Time: {roomBooking['start_time']}")
                print(f"End Time: {roomBooking['end_time']}")
        else:
            print('No room bookings found.')

        print('\n====================================================')

    elif choice == '2':
        while True:
            bookingID = input("\nEnter Booking ID: ")
            if bookingID.isdigit():
                break
            else:
                print("Invalid input. Enter a valid ID.")
        
        while True:
            newRoomName = input("Enter new name for the room: ")
            if newRoomName:
                break
            print('\nInvalid room name.\n')

        successfulUpdate = fs.updateRoomBooking(bookingID, newRoomName)

        if successfulUpdate:
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

        maintenanceRecords = fs.getMaintenanceRecords()
        
        if maintenanceRecords:
            for record in maintenanceRecords:
                print(f"Equipment ID: {record['equipment_id']}")
                print(f"Equipment Name: {record['equipment_name']}")
                print(f"Last Maintenance Date: {record['last_maintenance']}\n")
        else:
            print('No maintenance records found.')
        
        print('====================================================')

    elif choice == '2':
        while True:
            equipmentID = input("\nEnter Equipment ID to update maintenance date: ")
            if equipmentID.isdigit():
                break
            else:
                print("Invalid input. Enter a valid ID.")
        
        while True:
            newDate = input("Enter new maintenance date (YYYY-MM-DD): ")
            if newDate:
                break
            print('\nInvalid date.\n')

        equipment = fs.updateEquipmentMaintenance(equipmentID, newDate)

        if equipment:
            print("\nSuccessfully updated equipment maintenance date!\n")
        else:
            print('\nEquipment ID does not exist.\n')

    elif choice == '3':
        while True:
            equipmentName = input("\nEnter new Equipment Name: ")
            if equipmentName:
                break
            print('\nInvalid equipment name.\n')

        while True:
            maintenanceDate = input("Enter Maintenance Date (YYYY-MM-DD): ")
            if maintenanceDate:
                break
            print('\nInvalid date.\n')

        fs.addEquipment(equipmentName, maintenanceDate)

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
        
        classSchedules = fs.getClassSchedules()

        if classSchedules:
            for schedule in classSchedules:
                print(f"Class Name: {schedule['class_name']}")
                print(f"Class Date: {schedule['class_date']}")
                print(f"Start Time: {schedule['start_time']}")
                print(f"End Time: {schedule['end_time']}\n")
        else:
            print('No class schedules found.')

        print('====================================================')

    elif choice == '2':
        while True:
            classID = input("\nEnter Class ID to update: ")
            newDate = input("Enter new class date (YYYY-MM-DD): ")
            newStartTime = input("Enter new start time (HH:MM): ")
            newEndTime = input("Enter new end time (HH:MM): ")

            if not ((classID and newDate and newStartTime and newEndTime) and classID.isdigit()):
                print("\nInvalid input. Please ensure are fields are inputted and are in proper format.")
            else:
                break

        successfulUpdate = fs.updateClassSchedule(classID, newDate, newStartTime, newEndTime)
        
        if successfulUpdate:
            print("\nClass schedule updated successfully!")
        else:
            print("\nClass ID not found.")

    elif choice == '3':
        while True:
            className = input("\nEnter new class name: ")
            classDate = input("Enter class date (YYYY-MM-DD): ")
            startTime = input("Enter start time (HH:MM): ")
            endTime = input("Enter end time (HH:MM): ")
            maxParticipants = input("Enter max participants (#): ")
            trainerID = input("Enter trainer ID: ")

            if not ((className and classDate and startTime and endTime and maxParticipants and trainerID) and trainerID.isdigit() and maxParticipants.isdigit()):
                print("\nInvalid input. Please ensure all fields are inputted and are in proper format.")
            else:
                break
        
        trainerAvailable = fs.checkTrainerAvailability(className, classDate, startTime, endTime, maxParticipants, trainerID)

        if trainerAvailable:
            print("\nNew class schedule added successfully!")
        else:
            print("\nThe trainer is not available during the given date and time or there is a collision with an existing session/class.")

    elif choice == '4':
        return

    else:
        print("\nInvalid choice, please try again.")

# 4. Process Payments

def billingsAndPayment():
    print("\n--- Billings and Payment ---\n")
    print("1. View Billings")
    print("2. Process Payments")
    print("3. Exit")
    choice = input("Enter Choice: ")

    if choice == '1':
        while True:
            print("\n--- View Billings ---\n")
            print("1. View Unpaid Billings")
            print("2. View Paid Billings")
            print("3. Exit")
            billing_choice = input("Enter Choice: ")

            if billing_choice == '1':
                unpaid_billings = fs.getUnpaidBillings()
                print("\n--- Unpaid Billings ---\n")
                if unpaid_billings:
                    for billing in unpaid_billings:
                        print(f"Billing ID: {billing['billing_id']}, Amount: {billing['amount']}, Date: {billing['date']}")
                else:
                    print("No unpaid billings.")
                
            elif billing_choice == '2':
                paid_billings = fs.getPaidBillings()
                print("\n--- Paid Billings ---\n")
                if paid_billings:
                    for billing in paid_billings:
                        print(f"Billing ID: {billing['billing_id']}, Amount: {billing['amount']}, Date: {billing['date']}")
                else:
                    print("No paid billings.")
                
            elif billing_choice == '3':
                break
            else:
                print("Invalid option.")
    
    elif choice == '2':
        while True:
            billingID = input("\nEnter Billing ID to process payment: ")
            if billingID and billingID.isdigit():
                break
            else:
                print("Invalid input. Enter a valid ID.")

        successfulPayment = fs.processPayment(billingID)

        if successfulPayment:
            print(f"Billing ID {billingID} has been charged and is now paid.")
        else:
            print("Billing ID does not exist.")

    elif choice == '3':
        return
    else:
        print("Invalid option.")