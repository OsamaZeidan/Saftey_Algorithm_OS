"""
[+] this code to simulate the safety algorithm in computer OS...
[+] This code is suitable for any number of processes and resources (General)
[+] made by: Osama Zeidan
[+] ID: 1210601
"""
import csv
import os

# Dictionaries of Dictionaries
Allocation = {}
Request = {}
Available = {}


def validate_file(file_path):
    """
    this function to validate the file
    """
    # Check if file exists
    if not os.path.exists(file_path):
        print(f"[-] File {file_path} does not exist.")
        return False

    # Check if file is not empty
    if os.path.getsize(file_path) == 0:
        print(f"[-] File {file_path} is empty.")
        return False

    # Check if file can be read as a CSV
    try:
        with open(file_path, "r") as file:
            reader = csv.DictReader(file)
            if not reader.fieldnames:
                print(f"[-] File {file_path} does not have any headers.")
                return False
    except Exception as error:
        print(f"[-] Error reading file {file_path}: {error}")
        return False

    return True


def get_valid_file_name(prompt):
    """
    this function to get the file name from the user
    """
    while True:
        file_name = input(prompt)
        if not validate_file(file_name):
            continue
        return file_name


def validate_files_content():
    """
    this function to validate the files content (if same resources, processes....)
    """
    # check if all files have the same processes
    for process in Allocation:
        if process not in Request:
            print(f"[-] Process {process} is not in Request file.")
            return False

    # check if all files have the same processes
    for process in Request:
        if process not in Allocation:
            print(f"[-] Process {process} is not in Allocation file.")
            return False

    # check if all files have the same resources
    for process in Allocation:
        for resource in Allocation[process]:
            if resource not in Request[process]:
                print(f"[-] Resource {resource} is not in Request file.")
                return False
            if resource not in Available:
                print(f"[-] Resource {resource} is not in Available file.")
                return False

    # check if all files have the same resources
    for process in Request:
        for resource in Request[process]:
            if resource not in Allocation[process]:
                print(f"[-] Resource {resource} is not in Allocation file.")
                return False
            if resource not in Available:
                print(f"[-] Resource {resource} is not in Available file.")
                return False

    # check if all files have the same resources
    for resource in Available:
        if resource not in Allocation[process]:
            print(f"[-] Resource {resource} is not in Allocation file.")
            return False
        if resource not in Request[process]:
            print(f"[-] Resource {resource} is not in Request file.")
            return False

    return True


# ask files names
Allocation_file = get_valid_file_name("[+] Enter 'Allocation' file name: ")
Request_file = get_valid_file_name("[+] Enter 'Request' file name: ")
Available_file = get_valid_file_name("[+] Enter 'Available' file name: ")


# chaeck if the system in a safe state
def is_safe_state():
    """
    this function to check if the system in a safe state
    """
    # work dict
    work = Available
    # finish dict
    finish = {}
    # initialize finish dict
    for process in Allocation:
        finish[process] = False
    # initialize safe sequence
    safe_sequence = []
    # loop through all processes
    while True:
        flag = False
        for process in Allocation:
            # check if the process not finished
            if finish[process] is False:
                # check if the process needs <= work
                if all(
                    [
                        Request[process][resource] <= work[resource]
                        for resource in Request[process]
                    ]
                ):
                    flag = True
                    # add process to safe sequence
                    safe_sequence.append(process)
                    # add allocated resources to work
                    for resource in Allocation[process]:
                        work[resource] += Allocation[process][resource]
                    # mark process as finished
                    finish[process] = True
                    # return to the firs Index
                    break
        # check if no process needs <= work
        if flag is False:
            break

    # check if all processes finished
    for process in finish:
        if finish[process] is False:
            return False, safe_sequence
    return True, safe_sequence


# Read Allocation.csv
print("\n[+] Allocation Table:\n----------")
with open(Allocation_file, "r") as file:
    reader = csv.DictReader(file)
    # print Allocation Table
    for row in reader:
        print(f"{row['Process']}", end=", ")
        # Add to Allocation dictionary
        Allocation[row["Process"]] = {}
        # iterate on all Resources
        for resource in row:
            if resource != "Process":
                print(f"{resource}: {row[resource]}", end=", ")
                try:
                    Allocation[row["Process"]][resource] = int(row[resource])
                except ValueError:
                    print(
                        f"\n[-] Error in {resource} value in {row['Process']} process"
                    )
                    exit()
        print("")
print("\n----------\n")
# Read the Request.csv
print("\n[+] Request Table:\n----------")
with open(Request_file, "r") as file:
    reader = csv.DictReader(file)
    # Print Request Table
    for row in reader:
        print(f"{row['Process']}", end=", ")
        # Add to Request dictionary
        Request[row["Process"]] = {}
        # iterate on all Resources
        for resource in row:
            if resource != "Process":
                print(f"{resource}: {row[resource]}", end=", ")
                try:
                    Request[row["Process"]][resource] = int(row[resource])
                except ValueError:
                    print(
                        f"\n[-] Error in {resource} value in {row['Process']} process"
                    )
                    exit()
        print("")
print("\n----------\n")

# Read Available.csv
print("\n[+] Available Table:\n----------")
with open(Available_file, "r") as file:
    # read column by column
    reader = csv.DictReader(file)
    # print Available Table
    for row in reader:
        # iterate on all Resources
        for resource in row:
            print(f"{resource}: {row[resource]}", end=", ")
            # Add to Available dictionary
            try:
                Available[resource] = int(row[resource])
            except ValueError:
                print(f"\n[-] Error in {resource} value")
                exit()
        print("")
print("\n----------\n")

# check the validity of contents
if not validate_files_content():
    print("[-] Files content is not valid Check All Files and Try Again!")
    exit()

print("\n**********\nResult:\n**********\n")
# check if the system in a safe state (Result):
safe, safe_sequence = is_safe_state()
if safe:
    print("\n[+] The system is in a safe state\n----------\n")
    print(f"[+] Safe sequence: {safe_sequence}")
else:
    print("\n[-] The system is not in a safe state\n----------\n")
    # print deadlocked processes
    for process in Allocation:
        if process not in safe_sequence:
            print(f"[-] Process {process} is deadlocked")
print("\n\n")
