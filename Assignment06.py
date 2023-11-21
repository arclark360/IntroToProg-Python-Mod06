# ------------------------------------------------------------------------------------------ #
# Title: Assignment05
# Desc: This assignment demonstrates using dict and exceptions to work with data
# Change Log: (Who, When, What)
#   Alexander Reese Clark,11/13/2023,Updating Registration Program with Dict and Error Handling
# ------------------------------------------------------------------------------------------ #

import json
from typing import TextIO

# Define the Data Constants
MENU: str = """
---- Course Registration Program ----
  Select from the following menu:  
    1. Register a Student for a Course.
    2. Show current data.  
    3. Save data to a file.
    4. Exit the program.
----------------------------------------- 
"""
FILE_NAME: str = "Enrollments.json"

# Define the Data Variables
menu_choice: str = ""  # Hold the choice made by the user.
students: list[dict[str, str, str]] = []  # Holds the list of dictionary's for the JSON

#IO class to handle any Input & Output functions


class IO:
    """
    Handles all functions that deal with program Input and Output
    """

    @staticmethod
    def output_error_messages(message: str, error: Exception = None):
        """
        Reads the error that gets passed to it and outputs a custom message to the user and error specific information.
        :param message: The custom error message you want to user to see when an error occurs
        :param error: The exception or specific error type
        """
        print(message)
        print(error, error.__doc__, type(error), sep="\n")

    @staticmethod
    def output_menu(menu: str):
        """
        Prints the Menu for the student registration app
        :param menu: The MENU constant for the student registration app
        """
        print(menu)

    @staticmethod
    def input_menu_choice():
        """
        Collects the user input for the menu choice item
        """
        global menu_choice
        menu_choice = input("What would you like to do: ")

    @staticmethod
    def output_student_courses(student_matrix: list[dict[str, str, str]]):
        """
        Outputs all students currently stored in the students directory
        :param student_matrix: The students list of dictionaries
        """
        print("\nThe current data is:")
        print(f"List Data: {student_matrix}")
        print("String Format:")
        for single_student in student_matrix:
            print(f"{single_student["first_name"]},{single_student["last_name"]},{single_student["course_name"]}")

    @staticmethod
    def input_student_data(students_matrix: list[dict[str, str, str]]) -> list[dict[str, str, str]]:
        """
        Adds a new student to the registration student list
        :param students_matrix: The initial students list of dictionaries
        :return: The updated students list of dictionaries
        """
        student_first_name: str = ""  # Holds the first name of a student entered by the user.
        student_last_name: str = ""  # Holds the last name of a student entered by the user.
        course_name: str = ""  # Holds the name of a course entered by the user.
        student_data: dict[str, str, str] = {}  # Holds a dictionary value of student information for the JSON

        while True:
            try:
                student_first_name = input("Enter the student's first name: ")
                if not student_first_name.isalpha():
                    raise ValueError("first name must be alphabetic")
                break
            except ValueError as e:
                print(e)
            # While loop and error handling to ensure user enters an accurate last name
        while True:
            try:
                student_last_name = input("Enter the student's last name: ")
                if not student_last_name.isalpha():
                    raise ValueError("last name must be alphabetic")
                break
            except ValueError as e:
                print(e)
        course_name = input("Please enter the name of the course: ")
        # Stores user input as a dictionary item in the students list
        student_data = {"first_name": student_first_name, "last_name": student_last_name, "course_name": course_name}
        students_matrix.append(student_data)


# FileProcessor Class for processing the JSON

class FileProcessor:
    """
    Handles all functions that deal with processing and working with the JSON File
    """

    @staticmethod
    def read_data_from_file(file_name: str, students_matrix: list[dict[str, str, str]]) -> list[dict[str, str, str]]:
        """
        Reads the stored JSON file into the application and stores it as a list of dictionaries in students
        :param file_name: The file name that the program will read
        :param students_matrix: The students list of dictionaries
        :return: The updated students list of dictionaries
        """
        file = TextIO
        while True:
            try:
                file = open(file_name, "r")
                students_matrix += json.load(file)
                break
            except FileNotFoundError as e:
                IO.output_error_messages(message="JSON File not found, creating JSON file", error=e)
                file = open(file_name, "w")
                json.dump(students_matrix, file)
            except json.JSONDecodeError as e:
                IO.output_error_messages(
                    message="File is not in right format and can't load students, please review file for error",
                    error=e)
                break
            except Exception as e:
                IO.output_error_messages(message="Undefined Error", error=e)
                break
            finally:
                file.close()

    @staticmethod
    def write_data_to_file(file_name: str, students_matrix: list[dict[str, str, str]]):
        """
        Writes the current students list to the JSON file then outputs the students that were registered
        :param file_name: The JSON File you'll be writing to
        :param students_matrix: The students list of dictionaries
        :return:
        """
        # Error handling setup to catch any errors that might occur when writing to the file that will notify the user
        # an error occurred and the data wasn't saved
        file = TextIO
        try:
            file = open(file_name, "w")
            json.dump(students_matrix, file)
            file.close()
            for single_student in students_matrix:
                print(
                    f"You have registered {single_student["first_name"]} {single_student["last_name"]} for {single_student["course_name"]}.")
        except Exception as e:
            IO.output_error_messages(message="Undefined Error Data was not saved", error=e)


# At the start of the program it reads the json file and stores the student info.  If a file does not exist an error
# check will create the file for the user.  If the file is in the wrong format it will notify the user to check the
# file.


FileProcessor.read_data_from_file(file_name=FILE_NAME, students_matrix=students)

# Begins the while loop for the program and won't close till option 4 is chosen
while True:
    # Present the menu of choices
    IO.output_menu(MENU)
    # Input menu selection
    IO.input_menu_choice()
    # Option 1 Input user data
    if menu_choice == "1":  # This will not work if it is an integer!
        IO.input_student_data(students_matrix=students)
    # Option 2 Present the current data of both the list and a string version of the list
    elif menu_choice == "2":
        IO.output_student_courses(student_matrix=students)
    # Option 3 Save the data to a file
    elif menu_choice == "3":
        # Error handling setup to catch any errors that might occur when writing to the file that will notify the user
        # an error occurred and the data wasn't saved
        FileProcessor.write_data_to_file(file_name=FILE_NAME, students_matrix=students)
    # Option 4 Stop the loop
    elif menu_choice == "4":
        break
    # Option 5 Catch-all
    else:
        print("Please only choose option 1, 2, or 3")
print("Program Ended")
