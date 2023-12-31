from aiogram.filters.callback_data import CallbackData


class UserRole(CallbackData, prefix="role_change"):
    is_admin: bool


class DimasFunc(CallbackData, prefix="dimas_function"):
    operation: int
