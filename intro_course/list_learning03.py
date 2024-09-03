# 7. Ask id the user wants to update the list again
import os

# Define the file path
file_path = 'sports03.txt'

# Initialize the sports list
sports = []

# Check if the file exists and read the existing sports list
if os.path.exists(file_path):
    with open(file_path, 'r') as file:
        sports = [line.strip() for line in file.readliness()]

repeat =