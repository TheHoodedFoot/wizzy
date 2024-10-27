import math


def print_bit_values(byte_array, value_pairs):
    """
       This function takes a list of bytes (byte array) and a list of tuples consisting of a string and value pair which represent the names of
       bit positions within those bytes. It prints any string for which the corresponding bit is set to 1.

    :param byte_array: The list of byte values in integer form where each bit represents a state (0 or 1).
       :type byte_array: list[int]
       :param value_pairs: A list of tuple pairs, where each pair contains a string representing the name of a bit and an integer
                           representing the position of that bit in the bytes. The integer must be within the range of 0-31 (inclusive).
       :type value_pairs: list[(str, int)] or dict[str, int]

    Example usage:
       print_bit_values([2], [("Enable Motor", 1)])  # Should print "Enable Motor" because the second bit is set to 1.
    """
    for byte_value in byte_array:
        if not (0 <= byte_value < math.pow(2, 8)):
            raise ValueError(
                "byte value must be an integer between 0 and 255 inclusive."
            )

    result = []
    for pos in range(max([bit_pos for _, bit_pos in value_pairs]) + 1):
        name = next(
            (
                name
                for name, bit_pos in value_pairs
                if (byte_array[pos // 8] & (1 << (pos % 8))) >> (pos % 8) == 1
            ),
            None,
        )
        if name is not None:
            result.append(name)
    print(", ".join(result))
