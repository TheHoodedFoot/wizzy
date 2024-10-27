# tmcstats.py: Get the current status of the TMC5160 registers

import math
import sys
import time

# from machine import Pin, SoftSPI

# Constants
REG_GCONF = 0x00
REG_GSTAT = 0x01
REG_IOIN = 0x04
REG_DRV_STATUS = 0x6F


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


def print_bit_values(byte_value, value_pairs):
    """
       This function takes a byte and a list of tuples consisting of string-integer pairs which represent the names of
       bit positions within that byte. It prints any string for which the corresponding bit is set to 1.

    :param byte_value: The byte value in integer form where each bit represents a state (0 or 1).
       :type byte_value: int
       :param value_pairs: A list or dictionary of pairs, where each pair contains a string representing the name of a bit and an integer
                           representing the position of that bit in the byte. The integer must be within the range of 0-7 (inclusive).
       :type value_pairs: list[(str, int)] or dict[str, int]

    Example usage:
       print_bit_values(2, [("Enable Motor", 1)])  # Should print "Enable Motor" because the second bit is set to 1.
    """
    if not (0 <= byte_value < math.pow(2, 8)):
        raise ValueError("byte_value must be an integer between 0 and 255 inclusive.")

    result = []
    for name, pos in value_pairs:
        bit_value = (
            byte_value & (1 << pos)
        ) >> pos  # Check if the bit at position is set to 1.
        if bit_value == 1:
            if len(result) > 0:
                result[-1] += ", " + name
            else:
                result.append(name)
    print(", ".join(result))


def readreg(register):
    out_ba = bytearray([register, 0, 0, 0, 0])
    in_ba = bytearray(5)
    cs(0)
    spi.write(out_ba)
    cs(1)
    cs(0)
    spi.write_readinto(out_ba, in_ba)
    cs(1)
    return in_ba


def writereg(register, out_ba):
    out_ba[0] = register | 0x80
    cs(0)
    spi.write(out_ba)
    cs(1)


def printreg(register, name):
    ba = readreg(register)
    numspaces = 20 - len(name)
    print(
        name,
        " " * numspaces,
        hex(ba[0]),
        hex(ba[1]),
        hex(ba[2]),
        hex(ba[3]),
        hex(ba[4]),
    )


if __name__ == "__main__":
    # Setup SPI pins
    spi = SoftSPI(baudrate=1000000, polarity=1, phase=1, sck=25, mosi=33, miso=27)
    cs = Pin(26, mode=Pin.OUT, value=1)
    enable = Pin(32, mode=Pin.OUT, value=0)

    gconf = readreg(REG_GCONF)
    # Global flags, so only print once
    print("SPI_STATUS")
    print_bit_values(
        gconf[0],
        [
            ("status_stop_r", 7),
            ("status_stop_l", 6),
            ("position_reached", 5),
            ("velocity_reached", 4),
            ("Standstill", 3),
            ("Stallguard", 2),
            ("Driver Error", 1),
            ("Reset Flag", 0),
        ],
    )
    print()

    printreg(REG_GCONF, "GCONF")
    print_bit_values(
        gconf[4],
        [("Inverse Motor Direction", 4), ("DIAG0 on errors", 5)],
    )
    print_bit_values(
        gconf[3],
        [("Emergency Stop", 7)],
    )

    printreg(REG_GSTAT, "GSTAT")
    gconf = readreg(REG_GSTAT)
    print_bit_values(
        gconf[4],
        [("Reset", 0), ("Driver Error Shutdown", 1), ("Undervoltage", 2)],
    )

    printreg(REG_IOIN, "IOIN")
    gconf = readreg(REG_IOIN)
    print_bit_values(
        gconf[4],
        [("REFL_STEP", 0), ("REFR_DIR", 1), ("DRV_ENN", 4), ("SD_MODE", 6)],
    )

    printreg(REG_DRV_STATUS, "DRV_STATUS")
    gconf = readreg(REG_DRV_STATUS)
    print_bit_values(
        gconf[1],
        [
            ("Standstill", 7),
            ("Open Load B", 6),
            ("Open Load A", 5),
            ("Short to ground B", 4),
            ("Short to ground A", 3),
            ("Overtemp pre warning", 2),
            ("Overtemperature", 1),
            ("Motor stall", 0),
        ],
    )
    print_bit_values(
        gconf[3],
        [
            ("Short to supply A", 4),
            ("Short to supply B", 5),
            ("Stealthchop", 6),
            ("Full step", 6),
        ],
    )

    # print("Clearing errors")
    # writereg(REG_GSTAT, bytearray([0, 0, 0, 0, 0x07]))
    sys.exit()

    printreg(0x04, "IOIN")
    printreg(0x6F, "DRV_STATUS")

    # Set off time TPOWERDOWN (0x11)
    printreg(0x11, "TPOWERDOWN")

    # Set blank time (24)

    # Set microsteps (16)

    # Set current to 400mA
    printreg(0x10, "CURRENT")

    # Set RAMPMODE
    printreg(0x20, "RAMPMODE")

    # Set velocity, acceleration and deceleration

    # VSTART (0x23)
    writereg(0x23, bytearray([0, 0, 0, 0, 0xAB]))
    printreg(0x23, "VSTART")

    # A1 (0x24)
    printreg(0x24, "A1")

    # V1 (0x25)
    printreg(0x25, "V1")

    # AMAX (0x26) usteps/t2
    printreg(0x26, "AMAX")

    # VMAX (0x27) usteps/t
    printreg(0x27, "VMAX")

    # DMAX (0x28) usteps/t2
    printreg(0x28, "DMAX")

    # Get current position XACTUAL (0x21)
    printreg(0x21, "XACTUAL")

    # Move to new position
    # Set XTARGET (0x2D)
    printreg(0x2D, "XTARGET")

    print()
