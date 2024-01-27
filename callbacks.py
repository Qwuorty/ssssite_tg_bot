from aiogram.filters.callback_data import CallbackData


class MakeOffer(CallbackData, prefix="make_offer"):
    back: str = None


class Profile(CallbackData, prefix="profile"):
    back: str = None


class MainPage(CallbackData, prefix="main_page"):
    pass


class Categorie(CallbackData, profile='categorie'):
    name: str = None


class Contacts(CallbackData, prefix="contacts"):
    pass


class Busket(CallbackData, prefix="busket"):
    back: str = None


class Menu(CallbackData, prefix="menu"):
    pass


class StoryOffers(CallbackData, prefix="offer_story"):
    pass
