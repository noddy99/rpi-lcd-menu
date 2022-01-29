from unittest import async_case
import asyncio


class BaseMenu(object):
    """
    A generic menu
    """
    def __init__(self, parent=None):
        """
        Initialzie basic menu
        """
        self.items = list()
        self.parent = parent
        self.current_option = 0
        self.selected_option = -1
    async def async_init(self):
        return self
    def __await__(self):    
        return self.async_init().__await__()

    async def start(self):
        """
        Start and render menu
        """
        self.current_option = 0
        self.selected_option = -1
        await self.render()

        return self

    def debug(self, level=1):
        """
        print menu items in console
        """
        for item in self.items:
            if hasattr(item, 'submenu') and isinstance(item.submenu, BaseMenu):
                print("|" + "--" * (level + 1) + "[" + "%s" % (item.__str__()) + "]")
                item.submenu.debug(level+1)
            else:
                print("|" + "--" * level + ">" + "%s" % (item.__str__()))
        return self

    def append_item(self, item):
        """
        Add an item to the end of the menu
        :param MenuItem item: The item to be added
        """
        item.menu = self
        self.items.append(item)
        return self

    async def render(self):
        """
        Render menu
        """
        pass

    async def clearDisplay(self):
        """
        Clear the screen/
        """
        pass

    async def processUp(self):
        """
        User triggered up event
        """
        if self.current_option == 0:
            self.current_option = len(self.items) - 1
        else:
            self.current_option -= 1
        await self.render()
        return self

    async def processDown(self):
        """
        User triggered down event
        """
        if self.current_option == len(self.items) - 1:
            self.current_option = 0
        else:
            self.current_option += 1
        await self.render()
        return self

    async def processEnter(self):
        """
        User triggered enter event
        """
        action_result = await self.items[self.current_option].action()
        if isinstance(action_result, BaseMenu):
            return action_result
        return self

    async def exit(self):
        """
        exit submenu and return parent
        """
        if self.parent is not None:
            await self.parent.render()
        return self.parent
