import spidev
import time

# Define TMC2130 registers and constants
WRITE_FLAG = 0x80
READ_FLAG = 0x00
REG_GCONF = 0x00
REG_GSTAT = 0x01
REG_IHOLD_IRUN = 0x10
REG_CHOPCONF = 0x6C
REG_COOLCONF = 0x6D
REG_DCCTRL = 0x6E
REG_DRVSTATUS = 0x6F

spi = spidev.SpiDev()

def tmc_write(cmd, data):
    spi.xfer2([cmd | WRITE_FLAG] + [(data >> i) & 0xFF for i in range(24, -1, -8)])

def tmc_read(cmd, data):
    spi.xfer2([cmd | READ_FLAG])
    data[0] = spi.readbytes(1)[0]
    data[1] = spi.readbytes(1)[0]
    data[2] = spi.readbytes(1)[0]
    data[3] = spi.readbytes(1)[0]

def setup():
    # Configure SPI and TMC2130 here
    spi.open(0, 1)  # Open SPI bus 0, device 1
    spi.max_speed_hz = 1000000  # Set max speed to 1MHz
    pass

def loop():
    # Main loop logic here
    pass

if __name__ == "__main__":
    setup()
    data = [0, 0, 0, 0]
    tmc_read(REG_DRVSTATUS, data)
    print(data)
    tmc_read(REG_DRVSTATUS, data)
    print(data)
    # try:
    #     while True:
    #         loop()
    # except KeyboardInterrupt:
    #     print("Exiting...")

