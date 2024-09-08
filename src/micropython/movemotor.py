import time

from machine import Pin, SoftSPI


def readonly(out_ba, in_ba):
    cs(0)
    spi.write_readinto(out_ba, in_ba)
    cs(1)


def readwrite(out_ba, in_ba):
    out_ba[0] = out_ba[0] | 0x80
    cs(0)
    spi.write_readinto(out_ba, in_ba)
    cs(1)


# Pin(17, Pin.IN, Pin.PULL_DOWN)
spi = SoftSPI(baudrate=1000000, polarity=1, phase=1, sck=25, mosi=33, miso=27)
cs = Pin(26, mode=Pin.OUT, value=1)
enable = Pin(32, mode=Pin.OUT, value=0)

out_ba = bytearray([0, 0, 0, 0, 0])
in_ba = bytearray(5)

# Set off time TPOWERDOWN (0x11)

# Set blank time (24)

# Set microsteps (16)

# Set current to 400mA
out_ba[0] = 0x10
out_ba[3] = 0x0F
out_ba[4] = 0x00
readwrite(out_ba, in_ba)

# Set RAMPMODE
out_ba[0] = 0x20
out_ba[4] = 0x01
readwrite(out_ba, in_ba)
# print("DRV_STATUS: ", in_ba.hex())

# Set velocity, acceleration and deceleration
# VSTART (0x23)
out_ba[0] = 0x23
out_ba[4] = 0x0
readwrite(out_ba, in_ba)

# A1 (0x24) First Acceleration (not needed)
out_ba[0] = 0x24
out_ba[3] = 0x00
out_ba[4] = 0x00
readwrite(out_ba, in_ba)

# V1 (0x25) First velocity. Set to zero to disable first stage
out_ba[0] = 0x25
out_ba[3] = 0x00
out_ba[4] = 0x00
readwrite(out_ba, in_ba)

# AMAX (0x26) usteps/t2
out_ba[0] = 0x26
out_ba[3] = 0x7F
out_ba[4] = 0x7F
readwrite(out_ba, in_ba)

# VMAX (0x27) usteps/t
out_ba[0] = 0x27
out_ba[3] = 0x7F
out_ba[4] = 0x7F
readwrite(out_ba, in_ba)

# DMAX (0x28) usteps/t2
out_ba[0] = 0x28
out_ba[3] = 0x7F
out_ba[4] = 0x7F
readwrite(out_ba, in_ba)

# Get current position XACTUAL (0x21)
out_ba[0] = 0x21
readonly(out_ba, in_ba)
readonly(out_ba, in_ba)
print("XACTUAL:", in_ba[1], in_ba[2], in_ba[3], in_ba[4])

# Move to new position
# Set XTARGET (0x2D)
out_ba[0] = 0x2D
out_ba[3] = 0xFF
out_ba[4] = 0xFF
readwrite(out_ba, in_ba)
