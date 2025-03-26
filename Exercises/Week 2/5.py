import sys


def main():
    # Get command-line arguments (excluding the script name)
    args = sys.argv[1:]

    # Convert arguments to a list of floats
    try:
        grades = [float(arg) for arg in args]
    except ValueError:
        print("Error: All inputs must be numbers.")
        return

    # Ensure at least one grade is provided
    if not grades:
        print("Error: No grades provided.")
        return

    # Compute the mean
    mean_grade = sum(grades) / len(grades)

    # Determine Pass or Fail
    result = "Pass" if mean_grade >= 5 else "Fail"

    # Print output in the required format
    print(f"{mean_grade:.2f} {result}")


if __name__ == "__main__":
    main()
