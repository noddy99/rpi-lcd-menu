#!/usr/bin/python

"""
multi level menu
"""

from rpilcdmenu import *
from rpilcdmenu.items import *


async def main():
    menu = RpiLCDMenu()
    await menu.setup(26, 19, [13, 6, 5, 19])
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


def exitSubMenu(submenu):
    return submenu.exit()


if __name__ == "__main__":
    main()
