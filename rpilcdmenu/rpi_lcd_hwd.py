from time import sleep
import asyncpio
import asyncio

class RpiLCDHwd:

    # commands
    LCD_CLEARDISPLAY = 0x01
    LCD_RETURNHOME = 0x02
    LCD_ENTRYMODESET = 0x04
    LCD_DISPLAYCONTROL = 0x08
    LCD_CURSORSHIFT = 0x10
    LCD_FUNCTIONSET = 0x20
    LCD_SETCGRAMADDR = 0x40
    LCD_SETDDRAMADDR = 0x80

    # flags for display entry mode
    LCD_ENTRYRIGHT = 0x00
    LCD_ENTRYLEFT = 0x02
    LCD_ENTRYSHIFTINCREMENT = 0x01
    LCD_ENTRYSHIFTDECREMENT = 0x00

    # flags for display on/off control
    LCD_DISPLAYON = 0x04
    LCD_DISPLAYOFF = 0x00
    LCD_CURSORON = 0x02
    LCD_CURSOROFF = 0x00
    LCD_BLINKON = 0x01
    LCD_BLINKOFF = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00

    # flags for display/cursor shift
    LCD_DISPLAYMOVE = 0x08
    LCD_CURSORMOVE = 0x00
    LCD_MOVERIGHT = 0x04
    LCD_MOVELEFT = 0x00

    # flags for function set
    LCD_8BITMODE = 0x10
    LCD_4BITMODE = 0x00
    LCD_2LINE = 0x08
    LCD_1LINE = 0x00
    LCD_5x10DOTS = 0x04
    LCD_5x8DOTS = 0x00

    def __init__(self):
        """
        LCD GPIO configuration
        """
      

    async def setup(self, pin_rs=26, pin_e=19, pins_db=[13, 6, 5, 19], GPIO=None):
        
        self.GPIO = GPIO
        self.pin_rs = pin_rs
        self.pin_e = pin_e
        self.pins_db = pins_db

        self.displaycontrol = None
        self.displayfunction = None
        self.displaymode = None
        if not GPIO:
            import asyncpio 
            self.GPIO = asyncpio.pi()
            await self.GPIO.connect('192.168.1.138', 8888)
        await self.GPIO.set_mode(self.pin_rs, asyncpio.OUTPUT)
        await self.GPIO.set_mode(self.pin_e, asyncpio.OUTPUT)
        
        for pin in self.pins_db:
            await self.GPIO.set_mode(pin, asyncpio.OUTPUT)

    async def initDisplay(self):
        await self.write4bits(0x33)  # initialization
        await self.write4bits(0x32)  # initialization
        await self.write4bits(0x28)  # 2 line 5x7 matrix
        await self.write4bits(0x0C)  # turn cursor off 0x0E to enable cursor
        await self.write4bits(0x06)  # shift cursor right

        self.displaycontrol = self.LCD_DISPLAYON | self.LCD_CURSOROFF | self.LCD_BLINKOFF

        self.displayfunction = self.LCD_4BITMODE | self.LCD_1LINE | self.LCD_5x8DOTS
        self.displayfunction |= self.LCD_2LINE

        # Initialize to default text direction (for romance languages)
        self.displaymode = self.LCD_ENTRYLEFT | self.LCD_ENTRYSHIFTDECREMENT
        await self.write4bits(self.LCD_ENTRYMODESET | self.displaymode)  # set the entry mode

        return self

    async def write4bits(self, bits, char_mode=False):
        """ Send command to LCD """
        await self.delayMicroseconds(1)  # 1000 microsecond sleep
        bits = bin(bits)[2:].zfill(8)
        await self.GPIO.write(self.pin_rs, char_mode)
        for pin in self.pins_db:
            await self.GPIO.write(pin, False)

        for i in range(4):
            if bits[i] == "1":
                await self.GPIO.write(self.pins_db[::-1][i], True)

        await self.pulseEnable()

        for pin in self.pins_db:
            await self.GPIO.write(pin, False)

        for i in range(4, 8):
            if bits[i] == "1":
                await self.GPIO.write(self.pins_db[::-1][i - 4], True)

        await self.pulseEnable()

        return self

    async def delayMicroseconds(self, microseconds):
        seconds = microseconds / float(1000000)  # divide microseconds by 1 million for seconds
        await asyncio.sleep(seconds)

        return self

    async def pulseEnable(self):
        await self.GPIO.write(self.pin_e, False)
        await self.delayMicroseconds(1)  # 1 microsecond pause - enable pulse must be > 450ns
        await self.GPIO.write(self.pin_e, True)
        await self.delayMicroseconds(1)  # 1 microsecond pause - enable pulse must be > 450ns
        await self.GPIO.write(self.pin_e, False)
        await self.delayMicroseconds(1)  # commands need > 37us to settle

        return self
