from rpilcdmenu import RpiLCDMenu


class RpiLCDSubMenu(RpiLCDMenu):
    def __init__(self, base_menu):
        """
        Initialize SubMenu
        """
        self.lcd = base_menu.lcd
        super(RpiLCDMenu, self).__init__(self.lcd)
    
    async def async_init(self):
        return self
    def __await__(self):    
        return self.async_init().__await__()
