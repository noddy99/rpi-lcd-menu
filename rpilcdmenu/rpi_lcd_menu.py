from rpilcdmenu.base_menu import BaseMenu
from rpilcdmenu.rpi_lcd_hwd import RpiLCDHwd


class RpiLCDMenu(BaseMenu):
    def __init__(self):
        """
        Initialize menu
        """
        super(self.__class__, self).__init__()

    async def setup(self, pin_rs=26, pin_e=19, pins_db=[13, 6, 5, 9], GPIO=None):
        if 'lcd' not in dir(self):
            print("LCD HWD obj does not exist: creating now")
            self.lcd = RpiLCDHwd()
            await self.lcd.setup(pin_rs, pin_e, pins_db, GPIO)
        await self.lcd.initDisplay()
        await self.clearDisplay()

    async def clearDisplay(self):
        """
        Clear LCD Screen
        """
        await self.lcd.write4bits(RpiLCDHwd.LCD_CLEARDISPLAY)  # command to clear display
        await self.lcd.delayMicroseconds(3000)  # 3000 microsecond sleep, clearing the display takes a long time

        return self

    async def message(self, text):
        """ Send long string to LCD. 17th char wraps to second line"""
        i = 0
        lines = 0

        for char in text:
            if char == '\n':
                await self.lcd.write4bits(0xC0)  # next line
                i = 0
                lines += 1
            else:
                await self.lcd.write4bits(ord(char), True)
                i = i + 1

            if i == 16:
                await self.lcd.write4bits(0xC0)  # last char of the line
            elif lines == 2:
                break

        return self

    async def displayTestScreen(self):
        """
        Display test screen to see if your LCD screen is wokring
        """
        await self.message('Hum. body 36,6\xDFC\nThis is test')

        return self

    async def render(self):
        """
        Render menu
        """
        await self.clearDisplay()

        if len(self.items) == 0:
            await self.message('Menu is empty')
            return self
        elif len(self.items) <= 2:
            options = (self.current_option == 0 and ">" or " ") + self.items[0].text
            if len(self.items) == 2:
                options += "\n" + (self.current_option == 1 and ">" or " ") + self.items[1].text
            print(options)
            await self.message(options)
            return self

        options = ">" + self.items[self.current_option].text

        if self.current_option + 1 < len(self.items):
            options += "\n " + self.items[self.current_option + 1].text
        else:
            options += "\n " + self.items[0].text

        await self.message(options)

        return self
