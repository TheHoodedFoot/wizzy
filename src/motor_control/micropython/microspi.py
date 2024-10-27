import time

from machine import Pin, SoftSPI


def readwrite(out_ba, in_ba):
    cs(0)
    spi.write_readinto(out_ba, in_ba)
    cs(1)


# Pin(17, Pin.IN, Pin.PULL_DOWN)
spi = SoftSPI(baudrate=100000, polarity=1, phase=0, sck=32, mosi=22, miso=17)
cs = Pin(2, mode=Pin.OUT, value=1)

out_ba = bytearray([0, 0, 0, 0, 0])
in_ba = bytearray(5)

while True:
    # GCONF: 0x00
    out_ba[0] = 0x00
    readwrite(out_ba, in_ba)
    print("DRV_STATUS: ", in_ba.hex())

    # GSTAT: 0x01
    out_ba[0] = 0x01
    readwrite(out_ba, in_ba)
    print("GCONF: ", in_ba.hex())

    # IOIN: 0x04
    out_ba[0] = 0x04
    readwrite(out_ba, in_ba)
    print("GSTAT: ", in_ba.hex())

    # DRV_STATUS: 0x6F
    out_ba[0] = 0x6F
    readwrite(out_ba, in_ba)
    print("IOIN: ", in_ba.hex())

    time.sleep(1)
