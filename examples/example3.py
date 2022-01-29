#!/usr/bin/python

"""
multi level menu
"""
import asyncio, asyncpio
from rpilcdmenu import *
from rpilcdmenu.items import *


async def main():
    # GPIO = asyncpio.pi()
    # await GPIO.connect('192.168.1.138', 8888)
    menu = await RpiLCDMenu(26, 19, [13, 6, 5, 9])
    print(menu)

    function_item1 = FunctionItem("Item 1", fooFunction, [1])
    function_item2 = FunctionItem("Item 2", fooFunction, [2])
    await menu.append_item(function_item1)
    await menu.append_item(function_item2)

    submenu = await RpiLCDSubMenu(menu)
    submenu_item = await SubmenuItem("SubMenu (3)", submenu, menu)
    menu.append_item(submenu_item)

    submenu.append_item(FunctionItem("Item 31", fooFunction, [31])).append_item(FunctionItem("Item 32", fooFunction, [32]))
    submenu.append_item(FunctionItem("Back", exitSubMenu, [submenu]))

    menu.append_item(FunctionItem("Item 4", fooFunction, [4]))

    await menu.start()
    menu.debug()
    print("----")
    # press first menu item and scroll down to third one
    await menu.processEnter()
    await menu.processDown()
    await menu.processDown()
    # enter submenu, press Item 32, press Back button
    await menu.processEnter()
    await menu.processDown()
    await menu.processEnter()
    await menu.processDown()
    await menu.processEnter()
    # press item4 back in the menu
    await menu.processDown()
    await menu.processEnter()


def fooFunction(item_index):
    """
	sample method with a parameter
	"""
    print("item %d pressed" % (item_index))


async def exitSubMenu(submenu):
    return await submenu.exit()


if __name__ == "__main__":
    asyncio.run(main())
    
