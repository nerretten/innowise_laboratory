"""
Student Grade Analyzer
----------------------
A console-based application for managing students and their grades.

Features:
1. Add new students
2. Add grades to a student
3. Generate a full report
4. Identify the top performer
5. Exit the program
"""


def calculate_average(grades):
    """
    Calculate the average of a list of grades.

    Parameters:
        grades (list[int]): List of integer grades.

    Returns:
        float | None: The average grade or None if the list is empty.
    """
    if not grades:
        return None
    return sum(grades) / len(grades)


def find_student(students, name):
    """
    Find a student dictionary by name.

    Parameters:
        students (list[dict]): List of student dictionaries.
        name (str): The student's name to find.

    Returns:
        dict | None: The student dictionary if found, otherwise None.
    """
    for student in students:
        if student["name"].lower() == name.lower():
            return student
    return None


def add_student(students):
    """
    Add a new student to the list if they do not already exist.
    """
    name = input("Enter student name: ").strip()
    if not name:
        print("Name cannot be empty.")
        return

    if find_student(students, name):
        print(f"Student '{name}' already exists.")
        return

    students.append({"name": name, "grades": []})
    print(f"Student '{name}' added successfully.")


def add_grades(students):
    """
    Add grades to a specific student. Handles numeric validation and 'done' input.
    """
    name = input("Enter student name: ").strip()
    student = find_student(students, name)

    if not student:
        print(f"No student found with the name '{name}'.")
        return

    while True:
        grade_input = input("Enter a grade (or 'done' to finish): ").strip().lower()

        if grade_input == "done":
            break

        try:
            grade = int(grade_input)
            if 0 <= grade <= 100:
                student["grades"].append(grade)
            else:
                print("Grade must be between 0 and 100.")
        except ValueError:
            print("Invalid input. Please enter a number.")


def show_report(students):
    """
    Print a report with each student's average and overall summary statistics.
    Handles cases with no students or no grades.
    """
    if not students:
        print("No students available.")
        return

    print("\n--- Student Report ---")

    averages = []
    for student in students:
        try:
            avg = calculate_average(student["grades"])
            if avg is None:
                print(f"{student['name']}'s average grade is N/A.")
            else:
                averages.append(avg)
                print(f"{student['name']}'s average grade is {avg:.1f}.")
        except ZeroDivisionError:
            # Should not occur due to calculate_average logic, but included for safety
            print(f"{student['name']}'s average grade is N/A.")

    if not averages:
        print("-------------------------")
        print("No grades have been entered for any student.")
        return

    # Summary
    print("-------------------------")
    print(f"Max Average: {max(averages):.1f}")
    print(f"Min Average: {min(averages):.1f}")
    print(f"Overall Average: {sum(averages) / len(averages):.1f}")


def find_top_performer(students):
    """
    Identify and print the top-performing student.
    Students without grades are excluded.
    """
    # Filter out students with no valid grades
    valid_students = [
        s for s in students if s["grades"]
    ]

    if not valid_students:
        print("No students with valid grades to evaluate.")
        return

    # Using max() with lambda for highest average
    top_student = max(valid_students, key=lambda s: calculate_average(s["grades"]))
    top_avg = calculate_average(top_student["grades"])

    print(f"The student with the highest average is {top_student['name']} with a grade of {top_avg:.1f}.")


def main():
    """
    Main program loop for the Student Grade Analyzer.
    """
    students = []

    while True:
        print("\n--- Student Grade Analyzer ---")
        print("1. Add a new student")
        print("2. Add grades for a student")
        print("3. Show report (all students)")
        print("4. Find top performer")
        print("5. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Invalid input. Please enter a number from 1 to 5.")
            continue

        if choice == 1:
            add_student(students)
        elif choice == 2:
            add_grades(students)
        elif choice == 3:
            show_report(students)
        elif choice == 4:
            find_top_performer(students)
        elif choice == 5:
            print("Exiting program.")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 5.")


if __name__ == "__main__":
    main()

