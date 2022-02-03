import asyncio
from .menu_item import MenuItem


class FunctionItem(MenuItem):
    """
    A menu item to call a Python function
    """

    def __init__(self, text, function, args=None, kwargs=None, menu=None):
        """
        :ivar function: The function to be called
        :ivar list args: An optional list of arguments to be passed to the function
        :ivar dict kwargs: An optional dictionary of keyword arguments to be passed to the function
        :ivar RpiLCDMenu menu: The menu which this item belongs to
        """
        super(FunctionItem, self).__init__(text=text, menu=menu)

        self.function = function

        if args is not None:
            self.args = args
        else:
            self.args = []
        if kwargs is not None:
            self.kwargs = kwargs
        else:
            self.kwargs = {}

        self.returned_value = None

    async def action(self):
        """
        This class overrides this method
        """
        if asyncio.iscoroutinefunction(self.function):
            self.returned_value = await self.function(*self.args, **self.kwargs)
            return self.returned_value
        else:
            self.returned_value = self.function(*self.args, **self.kwargs)
            return self.returned_value

    def get_return(self):
        """
        :return: The return value from the function call
        """
        return self.returned_value
