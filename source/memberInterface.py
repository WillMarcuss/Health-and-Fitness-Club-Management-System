import functions as fs


def register():
    print("Register New Member")
    first_name = input("First name: ")
    last_name = input("Last name: ")
    height = input("Height (cm): ")
    weight = input("Weight (kg): ")
    fs.register_member(first_name, last_name, height, weight)