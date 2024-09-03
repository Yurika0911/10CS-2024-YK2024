# Get the user to input their name
# Get the user to input their birth year
# calculate the user's age
# Expected output "Hi NAME, you are 15 years old." as an F-strings
# Test the program with your own name and birth year
# Test with my name and birth year 1976 and I am not 48 years old
import os
repeat = "yes"
while repeat == "yes":
    # Get the user to input their name
    name = input("Enter your name: ").strip()
    # Get the user to input their birth year
    birth_year = int(input("Enter your birth year: ").strip())
    # Calculate the user's age
    age = 2024 - birth_year
    # Ask the user if they have had their birthday this year
    # Add a python string method to convert the user's input to lowercase
    # https://www.w3schools.com/python/python_ref_string.asp
    birthday = input(" have you had your birthday this year? (Yes/No): ").lower().strip()
    if birthday == "no":
        age = age - 1
    # Expected output: " Hi NAME, you are 15 years old." as an F-string
    print(f"Hi {name}, you are {age} years old.")
    # Test the program with your own name and birth year
    # Test with my name and birth year 1976 and I am not 48 years old
    repeat = input("Would you like to run the program again? (Yes/No): ").lower().strip()
    os.system("cls||clear")
# if repeat == "no": thank the used and exit program
print("Thank you for using the age calculater.")