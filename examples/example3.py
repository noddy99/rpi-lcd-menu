#!/usr/bin/python

"""
multi level menu
"""

# from msilib.schema import Class
from rpilcdmenu import *
from rpilcdmenu.items import *
import asyncio
import time

async def main():
    menu = RpiLCDMenu()
    await menu.setup(26, 19, [13, 6, 5, 9])
    function_item1 = FunctionItem("Item 1", fooFunction, [1])
    function_item2 = FunctionItem("Item 2", fooFunction, [2])
    menu.append_item(function_item1).append_item(function_item2)

    submenu = RpiLCDSubMenu(menu)
    await submenu.setup()
    submenu_item = SubmenuItem("SubMenu (3)", submenu, menu)
    menu.append_item(submenu_item)

    submenu.append_item(FunctionItem("Item 31", fooFunction, [31])).append_item(
        FunctionItem("Item 32", fooFunction, [32]))
    submenu.append_item(FunctionItem("Back", exitSubMenu, [submenu]))

    menu.append_item(FunctionItem("Item 4", fooFunction, [4]))

    await menu.start()
    menu.debug()
    print("----")
    # press first menu item and scroll down to third one
    # print(await menu.processEnter())
    # print(await menu.processDown())
    # await menu.processDown()
    # enter submenu, press Item 32, press Back button
    # entermenu = await menu.processEnter()
    # menudown = await entermenu.processDown()
   
    control = Controls(menu)
    await control.down()
    time.sleep(2)
    await control.enter()  # press item 2
    await control.down()
    await control.enter() # press item 3
    await control.enter()
    await control.down() # move to back item in sub
    await control.enter()
    await control.down()
    await control.down()
    await control.up() 
    await control.enter()
    time.sleep(2)
    await control.down() 
    time.sleep(2)
    await control.down() 
    time.sleep(2)
    await control.down() 
    time.sleep(2)
    await control.enter() # exit sub
    await control.down() 
    await control.down()  # MOVE TO ITEM 1
    await control.enter() # PRESS ITEM 1

class Controls(object):

    def __init__(self,menu) -> None:
        self.currentmenu = menu
        super().__init__()

    async def down(self):
        await self.currentmenu.processDown()
        
    async def up(self):
        await self.currentmenu.processUp()
    async def enter(self):
        self.currentmenu = await self.currentmenu.processEnter()

        
def fooFunction(item_index):
    """
	sample method with a parameter
	"""
    print("item %d pressed" % (item_index))


async def exitSubMenu(submenu):
    return await submenu.exit()


if __name__ == "__main__":
    asyncio.run(main())
    time.sleep(30)
