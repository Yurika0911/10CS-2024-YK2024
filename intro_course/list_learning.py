'''
sports = (basketball)
print(sports)
print(type(sports))
print(len(sports))
print(sports[0])
print(sports[-1])
print(sports[-2])
print(sports[0:3])
# print(type(sports[0]))
# print(type(sports[1]))
# print(type(sports[2]))
# print(type(sports[3]))

for sport in sports:
    print(type(sport))
    print(sport)
'''
repeat = "yes"
sports = ["Basketball"]  # Empty list
while repeat == "yes":
    new_sport = input("Enter your favourite sport: ")  # Get user input
    if new_sport:
        sports.append(new_sport)
        print("Updated sports list: ", sports)
    else:
        print("No new sport added.")
        print("sport list:", sports)  # 1. FIX THIS LINE

    for i, sport in enumerate(sports):  # Loop through the sports list with index
        print(f"Sport {i}: {sport}")  # Print the index and sport, starting at one

    repeat = input("Do you want to add another sport? (yes/no): ").strip().lower()  # Ask if the user wants to add another sport
print("Thank you for using this program!")  # Print a message when the user exits the program

# Suggested Improvements:


