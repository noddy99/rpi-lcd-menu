from rpilcdmenu.rpi_lcd_submenu import RpiLCDSubMenu
from rpilcdmenu.helpers.text_helper import get_scrolled_text, get_text_lines


class MessageView(RpiLCDSubMenu):
    async def __init__(self, base_menu, text, scrollable=False):
        """
        Initialize MessageView
        :ivar RpiLCDMenu base_menu: The menu which this item belongs to
        :ivar str text: Message to be shown on display
        :ivar bool scrollable: is scrolling allowed
        """

        self.scrollable = scrollable
        self.line_index = 0
        self.text_lines = 0
        self.text = ''

        self.setText(text)

        await super(MessageView, self).__init__(base_menu)

    async def render(self):
        """
        Render menu
        """
        await self.clearDisplay()

        if self.scrollable:
            await self.message(get_scrolled_text(self.text, self.line_index))
        else:
            await self.message(self.text)

        return self

    async def processUp(self):
        if self.line_index > 0 and self.scrollable:
            self.line_index -= 1
            await self.render()

        return self

    async def processDown(self):
        if self.line_index < self.text_lines - 1 and self.scrollable:
            self.line_index += 1
            await self.render()

        return self

    async def processEnter(self):
        return self.exit()

    def setText(self, text):
        self.text = text
        self.text_lines = get_text_lines(text)
