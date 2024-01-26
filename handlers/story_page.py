from aiogram import Router
from texts import STORY_TEXT
from callbacks import *
from aiogram.types.input_file import FSInputFile
from aiogram import types
from keyboards.keyboard import kb


router = Router()


@router.callback_query(StoryOffers.filter())
async def update_profile_to_story(
        call: types.CallbackQuery
):
    try:
        media = types.InputMediaPhoto(media=FSInputFile('media/story.png'), caption=STORY_TEXT)
        await call.message.edit_media(media=media, reply_markup=kb.story())
    except Exception:
        await call.message.answer_photo(photo=FSInputFile('media/story.png'),
                                        caption=STORY_TEXT,
                                        reply_markup=kb.story())
    await call.answer()
