import os

# Define the file path
file_path = 'sports02.txt'


# Function to read the sports list from the file
def read_sports(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as file:
            return [line.strip() for line in file.readlines()]
    return []
# Function to write the sports list to the file
def write_sports(file_path, sportslist):
    with open(file_path, 'w') as file:
        for sport in sportslist:
            file.write(f"{sport}\n")

repeat = "yes"
while repeat == "yes":
    # Read the current sports list from the file
    sports = read_sports(file_path)
    # Get user input
    new_sport = input("Enter your favourite sport: ").capitalize().strip()
    # Append the new sport if provided
    if new_sport:
        if new_sport in sports:
            print(f"{new_sport} is already in the list.")
        else:
            sports.append(new_sport)
            print("Updated sports list:", sports)
    else:
        print("No new sport added.")
    # write the updated sports list back to the file
    write_sports(file_path, sports)
    # Print the updated sports list
    print("Sports list:")
    for i, sport in enumerate(sports):
        print(f"{i+1}: {sport}")
    # Ask if the user wants to add more sports
    repeat = input("Do you want to add another sport? (yes/no): ").strip().lower()
print("Thank you for using this program!")
    # End of code
