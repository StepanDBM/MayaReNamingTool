def format_number_ranges(numbers):

    if not numbers:
        return ""

    ranges = []

    start = numbers[0]
    end = numbers[0]

    for number in numbers[1:]:

        if number == end + 1:
            end = number
            continue

        if start == end:
            ranges.append(str(start))
        else:
            ranges.append(f"{start}-{end}")

        start = number
        end = number

    if start == end:
        ranges.append(str(start))
    else:
        ranges.append(f"{start}-{end}")

    return ", ".join(ranges)