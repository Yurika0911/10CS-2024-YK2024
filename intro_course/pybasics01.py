# Variables
# Variables are used to store data in a program.
# In Python, variables are created by assigning a value to a meaningful name
# The value of a variable can be changed or updated throughout the program.
# Variables contain one type of data at a time, but the data type can change.
# Data types in Python include integers, floats, strings, and booleans.
'''
name = "Fred"  # this variable contains a strings (text)
age = 15  # this variable contains an integer 'int' which is a whole number
salary = 1000.50  # this variable contains a float 'float' which is a decimal number
is_student = True  #
'''
# Change the above variables to take input from the user
name = input("Enter your name: ")
age = int(input("Enter your age: "))
salary = float(input("Enter your salary: "))
is_student = bool(input(" Are you a student? (True/False): "))

print(type(name))
print(type(age))
print(type(salary))
print(type(is_student))
print("Name: ", name)
if is_student == True:
    student = "Yes"
# Why do we need an else statement here?
else:
    student = "No"
# the following is an F-String
print(f"{name} is {age} years old and earns $ {salary} per months. Is he a student? {is_student}")
# Fred is 15 years old and earns $ 1000.50 per month. Is he a student? True
print(f"{name} is {age} years old and earns ${salary}0 per months. Is he a student? {student}")