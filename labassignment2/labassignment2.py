# gradebook.py
# Name: Unnati 
# Task 1: Project Setup and Initialization
def display_welcome_and_menu():
    """Prints a welcome message and the main menu options."""
    print("\n--- Welcome to the Simple Gradebook Analyzer! ---")
    print("This program helps you analyze student marks.")
    print("\n--- Main Menu ---")
    print("1. Enter student grades manually")
    print("2. Analyze and Display Results")
    print("3. Exit")
def get_user_choice():
    """Gets a valid menu choice from the user."""
    while True:
        choice = input("Please choose an option (1, 2, or 3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
# Task 2: Data Entry
def get_manual_grades():
    """Allows manual entry of student names and marks."""
    student_marks = {}
    print("\n--- Manual Grade Entry ---")
    print("Enter student names and marks. Type 'done' for name to finish.")
    while True:
        name = input("Enter student name (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        if not name:
            print("Name cannot be empty. Please try again.")
            continue
        while True:
            try:
                mark_str = input(f"Enter mark for {name} (0-100): ").strip()
                mark = int(mark_str)
                if 0 <= mark <= 100:
                    student_marks[name] = mark
                    break
                else:
                    print("Mark must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a whole number for the mark.")
    return student_marks
# Task 3, 4, 5: Combined Analysis Function
def perform_and_display_analysis(student_marks):
    """
    Calculates statistics, assigns grades, filters pass/fail,
    and displays all results. Returns student_grades for table.
    """
    if not student_marks:
        print("\nNo student data to analyze.")
        return {}
    print("\n--- Grade Analysis Results ---")
    marks_list = list(student_marks.values())
    total_students = len(marks_list)
    # To find Average Score
    average_score = sum(marks_list) / total_students
    print(f"Total students: {total_students}")
    print(f"Average score: {average_score:.2f}")
    # To find Median Score
    sorted_marks = sorted(marks_list)
    mid = total_students // 2
    if total_students % 2 == 0:
        median_score = (sorted_marks[mid - 1] + sorted_marks[mid]) / 2
    else:
        median_score = float(sorted_marks[mid])
    print(f"Median score: {median_score:.2f}")
    # To find Max and Min Score
    max_score = max(marks_list)
    min_score = min(marks_list)
    print(f"Maximum score: {max_score}")
    print(f"Minimum score: {min_score}")
    top_students = [name for name, mark in student_marks.items() if mark == max_score]
    bottom_students = [name for name, mark in student_marks.items() if mark == min_score]
    print(f"Highest score by: {', '.join(top_students)}")
    print(f"Lowest score by: {', '.join(bottom_students)}")
    # Task 4: Grade Assignment and Distribution
    student_grades = {}
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for name, mark in student_marks.items():
        if mark >= 90:
            grade = 'A'
        elif mark >= 80:
            grade = 'B'
        elif mark >= 70:
            grade = 'C'
        elif mark >= 60:
            grade = 'D'
        else:
            grade = 'F'
        student_grades[name] = grade
        grade_counts[grade] += 1
    print("\n--- Grade Distribution ---")
    for letter, count in sorted(grade_counts.items()):
        print(f"{letter}: {count} student(s)")
    # Task 5: Pass/Fail Filter with List Comprehension
    passing_score_threshold = 40
    passed_students = [name for name, mark in student_marks.items() if mark >= passing_score_threshold]
    failed_students = [name for name, mark in student_marks.items() if mark < passing_score_threshold]
    print(f"\n--- Pass/Fail Summary (Passing score >= {passing_score_threshold}) ---")
    print(f"Passed students ({len(passed_students)}): {', '.join(sorted(passed_students)) if passed_students else 'None'}")
    print(f"Failed students ({len(failed_students)}): {', '.join(sorted(failed_students)) if failed_students else 'None'}")
    return student_grades 
# Task 6: Results Table 
def print_results_table(student_marks, student_grades):
    """Prints a formatted table of all student results."""
    print("\n--- Detailed Student Results Table ---")
    if not student_marks:
        print("No student data to display in the table.")
        return
    max_name_len = max(len("Name"), *(len(name) for name in student_marks.keys()))
    mark_col_width = max(len("Marks"), 3)
    grade_col_width = max(len("Grade"), 1)
    header_line = f"{{:<{max_name_len}}} {{:>{mark_col_width}}} {{:>{grade_col_width}}}"
    print(header_line.format("Name", "Marks", "Grade"))
    print("-" * (max_name_len + mark_col_width + grade_col_width + 6))
    for name in sorted(student_marks.keys()):
        mark = student_marks[name]
        grade = student_grades.get(name, 'N/A')
        print(header_line.format(name, mark, grade))
    print("-" * (max_name_len + mark_col_width + grade_col_width + 6))
# Main program execution
def main():
    current_student_marks = {}
    current_student_grades = {}
    while True: # loop of Main program
        display_welcome_and_menu()
        choice = get_user_choice()
        if choice == '1': 
            current_student_marks = get_manual_grades()
            if current_student_marks:
                print(f"Data loaded for {len(current_student_marks)} students. Select option 2 to analyze.")
                current_student_grades = {} 
            else:
                current_student_grades = {}
                print("No student data loaded.")
        elif choice == '2': 
            if current_student_marks:
                current_student_grades = perform_and_display_analysis(current_student_marks)
                print_results_table(current_student_marks, current_student_grades)
            else:
                print("No student data loaded. Please load data first (Option 1).")
            
        elif choice == '3': 
            print("Exiting Gradebook Analyzer. Goodbye!")
            break
if __name__ == "__main__":
    main()# gradebook.py
# Name: [Your Name]
# Date: [Current Date]
# Title: Simple Gradebook Analyzer for Beginners
# Task 1: Project Setup and Initialization 
def display_welcome_and_menu():
    """Prints a welcome message and the main menu options."""
    print("\n--- Welcome to the Simple Gradebook Analyzer! ---")
    print("This program helps you analyze student marks.")
    print("\n--- Main Menu ---")
    print("1. Enter student grades manually")
    print("2. Analyze and Display Results")
    print("3. Exit")
def get_user_choice():
    """Gets a valid menu choice from the user."""
    while True:
        choice = input("Please choose an option (1, 2, or 3): ").strip()
        if choice in ['1', '2', '3']:
            return choice
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")
# Task 2: Data Entry
def get_manual_grades():
    """Allows manual entry of student names and marks."""
    student_marks = {}
    print("\n--- Manual Grade Entry ---")
    print("Enter student names and marks. Type 'done' for name to finish.")
    while True:
        name = input("Enter student name (or 'done' to finish): ").strip()
        if name.lower() == 'done':
            break
        if not name:
            print("Name cannot be empty. Please try again.")
            continue
        while True:
            try:
                mark_str = input(f"Enter mark for {name} (0-100): ").strip()
                mark = int(mark_str)
                if 0 <= mark <= 100:
                    student_marks[name] = mark
                    break
                else:
                    print("Mark must be between 0 and 100.")
            except ValueError:
                print("Invalid input. Please enter a whole number for the mark.")
    return student_marks
# Task 3, 4, 5: Combined Analysis Function 
def perform_and_display_analysis(student_marks):
    """
    Calculates statistics, assigns grades, filters pass/fail,
    and displays all results. Returns student_grades for table.
    """
    if not student_marks:
        print("\nNo student data to analyze.")
        return {} 
    print("\n--- Grade Analysis Results ---")
    marks_list = list(student_marks.values())
    total_students = len(marks_list)
    # To find Average Score
    average_score = sum(marks_list) / total_students
    print(f"Total students: {total_students}")
    print(f"Average score: {average_score:.2f}")
    # To find Median Score
    sorted_marks = sorted(marks_list)
    mid = total_students // 2
    if total_students % 2 == 0:
        median_score = (sorted_marks[mid - 1] + sorted_marks[mid]) / 2
    else:
        median_score = float(sorted_marks[mid])
    print(f"Median score: {median_score:.2f}")
    # To find Max and Min Score
    max_score = max(marks_list)
    min_score = min(marks_list)
    print(f"Maximum score: {max_score}")
    print(f"Minimum score: {min_score}")
    top_students = [name for name, mark in student_marks.items() if mark == max_score]
    bottom_students = [name for name, mark in student_marks.items() if mark == min_score]
    print(f"Highest score by: {', '.join(top_students)}")
    print(f"Lowest score by: {', '.join(bottom_students)}")
    # Task 4: Grade Assignment and Distribution
    student_grades = {}
    grade_counts = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'F': 0}
    for name, mark in student_marks.items():
        if mark >= 90:
            grade = 'A'
        elif mark >= 80:
            grade = 'B'
        elif mark >= 70:
            grade = 'C'
        elif mark >= 60:
            grade = 'D'
        else:
            grade = 'F'
        student_grades[name] = grade
        grade_counts[grade] += 1
    print("\n--- Grade Distribution ---")
    for letter, count in sorted(grade_counts.items()):
        print(f"{letter}: {count} student(s)")
    # Task 5: Pass/Fail Filter with List Comprehension
    passing_score_threshold = 40
    passed_students = [name for name, mark in student_marks.items() if mark >= passing_score_threshold]
    failed_students = [name for name, mark in student_marks.items() if mark < passing_score_threshold]
    print(f"\n--- Pass/Fail Summary (Passing score >= {passing_score_threshold}) ---")
    print(f"Passed students ({len(passed_students)}): {', '.join(sorted(passed_students)) if passed_students else 'None'}")
    print(f"Failed students ({len(failed_students)}): {', '.join(sorted(failed_students)) if failed_students else 'None'}")
    return student_grades # Return the grades for the table
# Task 6: Results Table 
def print_results_table(student_marks, student_grades):
    """Prints a formatted table of all student results."""
    print("\n--- Detailed Student Results Table ---")
    if not student_marks:
        print("No student data to display in the table.")
        return
    max_name_len = max(len("Name"), *(len(name) for name in student_marks.keys()))
    mark_col_width = max(len("Marks"), 3)
    grade_col_width = max(len("Grade"), 1)
    header_line = f"{{:<{max_name_len}}} {{:>{mark_col_width}}} {{:>{grade_col_width}}}"
    print(header_line.format("Name", "Marks", "Grade"))
    print("-" * (max_name_len + mark_col_width + grade_col_width + 6))
    for name in sorted(student_marks.keys()):
        mark = student_marks[name]
        grade = student_grades.get(name, 'N/A')
        print(header_line.format(name, mark, grade))
    print("-" * (max_name_len + mark_col_width + grade_col_width + 6))
# Main program execution 
def main():
    current_student_marks = {}
    current_student_grades = {}
    while True: # Main program loop
        display_welcome_and_menu()
        choice = get_user_choice()
        if choice == '1': 
            current_student_marks = get_manual_grades()
            if current_student_marks:
                print(f"Data loaded for {len(current_student_marks)} students. Select option 2 to analyze.")
                current_student_grades = {} # Clear grades so analysis must be rerun
            else:
                current_student_grades = {}
                print("No student data loaded.")
        elif choice == '2':
            if current_student_marks:
                current_student_grades = perform_and_display_analysis(current_student_marks)
                print_results_table(current_student_marks, current_student_grades)
            else:
                print("No student data loaded. Please load data first (Option 1).")
            
        elif choice == '3': 
            print("Exiting Gradebook Analyzer. Goodbye!")
            break
if __name__ == "__main__":
    main()