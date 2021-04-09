from machine import I2C, Pin, reset
import gc
from esp32_i2c_lcd import I2cLcd
from aht10 import AHT10
from thermistor import THERMISTOR
from time import sleep_ms
from time import sleep

    
    
i2c = I2C(scl=Pin(22),sda=Pin(21), freq=400000)
LCD = I2cLcd(i2c, 0x27, 2, 16)
AHT = AHT10(i2c, 0x38)
THERM = THERMISTOR(34)


LCD.custom_char(0, bytearray([0x04, 0x0A, 0x0A, 0x0E, 0x0E, 0x1F, 0x1F, 0x0E])) # Temperature icon
LCD.custom_char(1, bytearray([0x04, 0x0E, 0x0E, 0x1F, 0x1F, 0x1F, 0x0E, 0x00])) # Humidity icon    
LCD.custom_char(2, bytearray([0x00, 0x04, 0x0E, 0x04, 0x00, 0x0E, 0x00, 0x00])) # Plus/Minus icon
DEGREE_SYMBOL = 0xDF

LCD.blink_cursor_off()
LCD.hide_cursor()
LCD.clear()

# set up static characters
def setupStatic():
    # AHT10 temperature
    LCD.move_to(0, 0)
    LCD.putchar(chr(0))
    LCD.move_to(6, 0)
    LCD.putchar(chr(DEGREE_SYMBOL))
    LCD.move_to(7, 0)
    LCD.putstr(" ")

    # AHT10 humidity
    LCD.move_to(8, 0)
    LCD.putchar(chr(1))
    LCD.move_to(14, 0)
    LCD.putstr("%")
    LCD.move_to(15, 0)
    LCD.putstr(" ")

    # Thermistor
    LCD.move_to(0, 1)
    LCD.putstr("E3v2CPU:")
    LCD.move_to(8, 1)
    LCD.putchar(chr(2))
    LCD.move_to(9, 1)
    LCD.putchar(chr(0))
    LCD.move_to(15, 1)
    LCD.putchar(chr(DEGREE_SYMBOL))

setupStatic()

def readSensors():
    try:
        t = AHT.temperature()
        h = AHT.humidity()
    except Exception as exc:
        print("Couldn't get information from AHT10 sensor for lcd ", exc.args[0])
        pass

    try:
        th = THERM.temperature()
    except Exception as exc:
        print("Couldn't get information from thermistor for lcd ", exc.args[0])
        pass


    global temp, humi, therm, myList
    myList = []
    temp = '%.2f' % round(t, 2) # round int to 2 decimals and convert to string
    humi = '%.2f' % round(h, 2) # round int to 2 decimals and convert to string
    therm = '%.2f' % round(th, 2) # round int to 2 decimals and convert to string.
    
    myList.append(temp)
    myList.append(humi)
    myList.append(therm)

    # try:
    #     f = open('vars.txt', 'w')
    #     f.write('{}\n {}\n {}'.format(temp, humi, therm))
    #     f.close
    # except Exception as exc:
    #     print("Couldn't write sensor information to file ", exc.args[0])
    #     pass

counter = 0

while True:
    if gc.mem_free() < 54000:
        gc.collect()

    readSensors()

    LCD.move_to(1, 0)
    LCD.putstr(temp)

    LCD.move_to(9, 0)
    LCD.putstr(humi)
    LCD.move_to(10, 1)
    LCD.putstr(therm)

    if counter < 25:
        counter += 1
    elif counter >= 25:
        print("DEBUG: T:{} H:{} C:{}".format(temp,humi,therm))
        counter = 0

    sleep_ms(1000)
    setupStatic()