import re

def increment_numbers_in_list(input_list, times):
    res_list=[]
    # Define a regular expression pattern to extract the numeric part
    pattern = re.compile(r'([a-zA-Z_]+)(\d+)')

    # Function to increment the numeric part of a string
    def increment_number(match):
        prefix, number = match.groups()
        return f"{prefix}{int(number) + 1}"

    # Append the original input_list to res_list
    res_list.append(input_list.copy())

    # Perform incrementation multiple times
    for _ in range(times):
        input_list = [pattern.sub(increment_number, element) for element in input_list]
        res_list.append(input_list.copy())  # Append the modified list to res_list

    return res_list

