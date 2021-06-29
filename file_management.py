class MalformedPlaneError(Exception):
    def __init__(self):
        super().__init__("Malformed plane detected")


def read_from_txt(path):
    plane = []
    zero_counter = 0
    start_x, start_y = (0, 0)
    finish_x, finish_y = (0, 0)

    with open(path, "r") as file_handle:

        first_line = file_handle.readline().rstrip()

        if not first_line.isdigit():
            raise MalformedPlaneError

        row_size = len(first_line)
        row = []
        j = 0  # x of current element

        for digit in first_line:
            digit = int(digit)

            if digit == 0:
                zero_counter += 1
                if zero_counter == 1:
                    start_x = j
                elif zero_counter == 2:
                    finish_x = j
                else:
                    raise MalformedPlaneError

            row.append(digit)
            j += 1

        plane.append(row)

        # loop starts from second line because of using readline() before
        i = 1   # y of current element
        for line in file_handle:
            line = line.rstrip()

            if len(line) != row_size or not line.isdigit():
                raise MalformedPlaneError

            row = []
            j = 0   # x of current element

            for digit in line:
                digit = int(digit)

                if digit == 0:
                    zero_counter += 1
                    if zero_counter == 1:
                        start_x = j
                        start_y = i
                    elif zero_counter == 2:
                        finish_x = j
                        finish_y = i
                    else:
                        raise MalformedPlaneError

                row.append(digit)
                j += 1

            i += 1
            plane.append(row)

    if zero_counter < 2:
        raise MalformedPlaneError

    return plane, start_x, start_y, finish_x, finish_y
