from aiogram.filters.callback_data import CallbackData


class MakeOffer(CallbackData, prefix="make_offer"):
    back: str = None


class Profile(CallbackData, prefix="profile"):
    back: str = None


class MainPage(CallbackData, prefix="main_page"):
    pass


class Options(CallbackData, prefix='options'):
    type_name: str = None
    option_name: str = None
    drink_id: int = None


class Categories(CallbackData, prefix='categories'):
    name: str = None


class Count_drink(CallbackData, prefix='count'):
    name: str = None
    drink_id: str = None


class AddDrink(CallbackData, prefix='add_tov'):
    back: str = None
    drink_id: str = None


class Drink(CallbackData, prefix='drink'):
    drink_id: int = None


class Contacts(CallbackData, prefix="contacts"):
    pass


class RedOffer(CallbackData, prefix="redoffer"):
    offer_id: int = None
    back: str
    drink_id: str


class Busket(CallbackData, prefix="busket"):
    back: str = None
    drink_id: str = None


class AddBusket(CallbackData, prefix="addbusket"):
    back: str = None
    drink_id: str = None
    offer_id: str = None
    name: str = None


class Menu(CallbackData, prefix="menu"):
    pass


class StoryOffers(CallbackData, prefix="offer_story"):
    pass
