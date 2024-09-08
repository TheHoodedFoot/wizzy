import math
import unittest

# from tmcstats import print_bit_values


def print_bit_values(byte_array, value_pairs):
    """
       This function takes a list of bytes (byte array) and a list of tuples consisting of a string and value pair which represent the names of
       bit positions within those bytes. It returns any string for which the corresponding bit is set to 1.

    :param byte_array: The list of byte values in integer form where each bit represents a state (0 or 1).
       :type byte_array: list[int]
       :param value_pairs: A list of tuple pairs, where each pair contains a string representing the name of a bit and an integer
                           representing the position of that bit in the bytes. The integer must be within the range of 0-31 (inclusive).
       :type value_pairs: list[(str, int)] or dict[str, int]

    Example usage:
       print_bit_values([2], [("Enable Motor", 1), ("Output off", 3)])  # Should return "Enable Motor" because the second bit is set to 1.
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
    return ", ".join(result)


class TestBitValues(unittest.TestCase):

    def test_print_bit_values(self):
        # Test with single-byte input
        byte_array = [0xFF, 0x00, 0x01]
        value_pairs = [("Enable Motor", 23)]
        assert print_bit_values(byte_array, value_pairs) == "Enable Motor"

        # Test invalid byte value
        with pytest.raises(ValueError):
            print_bit_values([256], value_pairs)

        # Test with multiple-byte input and positions up to 31
        byte_array = [0x0F, 0x10, 0x11, 0x12]  # 4 bytes with 7-0 bits
        value_pairs = [("Bit7", 7), ("Bit15", 15)]
        assert print_bit_values(byte_array, value_pairs) == "Bit15"

        # Test non-existent bit position
        byte_array = [0x00, 0x01, 0x02]
        value_pairs = [("Nonexistent Bit", 32)]  # 超出范围
        assert print_bit_values(byte_array, value_pairs) == ""

        # Test using dictionary for input (equivalent to tuples)
        byte_array = [0xFF, 0x00, 0x01]
        value_dict = {"Enable Motor": 23}
        assert print_bit_values(byte_array, value_dict) == "Enable Motor"

        # Test empty value_pairs
        byte_array = [0xFF, 0x00, 0x01]
        value_pairs = []
        assert print_bit_values(byte_array, value_pairs) == ""


if __name__ == "__main__":
    unittest.main()
