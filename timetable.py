# Initialize input string

# Function to convert string to list of numbers
def convert_to_list(input_string):
    split_ranges = [splited.strip() for splited in input_string.split(",")]
    result_list = []
    for item in split_ranges:
        if '-' in item:
            start, end = map(int, item.split('-'))
            result_list.extend(range(start, end + 1))
        else:
            result_list.append(int(item))
    return result_list


# Call the function and print the result
def is_duplicated(timetable1, timetable2):
    if timetable1['dayOfWeek'] != timetable2['dayOfWeek']:
        return False
    weeks1 = set(convert_to_list(timetable1["week"]))
    weeks2 = set(convert_to_list(timetable2["week"]))

    # Check if there is any overlapping week
    overlapping_weeks = weeks1.intersection(weeks2)
    if not overlapping_weeks:
        return False

    start_time1 = int(timetable1["from"])
    end_time1 = int(timetable1["to"])
    start_time2 = int(timetable2["from"])
    end_time2 = int(timetable2["to"])

    # Check if there is any overlapping time
    if end_time1 <= start_time2 or end_time2 <= start_time1:
        return False

    return True

