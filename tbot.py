import asyncio
import logging
import os
import sys

from dotenv import load_dotenv
from typing import List, Coroutine

from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger

from commands import CheckByApplication
from data.public_notices import PublicNoticesStorage
from data.users import UsersStorage, User

from services.user_service import send_public_notice_to_user_if_exists

from workers.update_public_notices import update_public_notices
from workers.check_public_notices import check_public_notices

load_dotenv(".env")

TOKEN = os.getenv("BOT_TOKEN")
ALLOWED_USER_IDS = set(map(int, os.getenv("ALLOWED_USER_IDS", "").split(","))) if os.getenv("ALLOWED_USER_IDS") else set()

user_storage = UsersStorage()
dp = Dispatcher()
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))


def is_user_allowed(user_id: int) -> bool:
    """Check if user is allowed to use the bot"""
    return user_id in ALLOWED_USER_IDS


async def send_unauthorized_message(message: Message) -> None:
    """Send message to unauthorized users"""
    await message.answer(
        "🔒 This is a private bot for personal use only.\n\n"
        "We do not want to work with any personal information and GDPR restrictions, "
        "so you can just delete this bot.\n\n"
        "Thank you for understanding!"
    )


@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    """
    This handler receives messages with `/start` command
    """
    user_storage.update(User(
        id=message.from_user.id,
        application_number=None
    ))

    if not is_user_allowed(message.from_user.id):
        await send_unauthorized_message(message)
        return

    await message.answer(
        f"Hello, {html.bold(message.from_user.full_name)}! "
        f"Send me your application number, and I will track the public notices for you.")


@dp.message(CheckByApplication())
async def check_by_application_number(message: Message) -> None:
    if not is_user_allowed(message.from_user.id):
        await send_unauthorized_message(message)
        return

    user = UsersStorage().get_by_id(message.from_user.id)
    if user is None:
        await message.answer("I am not currently tracking your application. "
                             "Please provide the application number (f.e. OAM-99999/DP-2024).")
        return

    public_notices = PublicNoticesStorage().get_as_dict()
    if not (await send_public_notice_to_user_if_exists(user, public_notices, bot)):
        await message.answer(f"There are no public notices issued for "
                             f"the {html.bold(user.application_number)}.")


@dp.message()
async def begin_application_tracking(message: Message) -> None:
    if not is_user_allowed(message.from_user.id):
        await send_unauthorized_message(message)
        return

    user_storage.update(User(
        id=message.from_user.id,
        application_number=message.text))
    await message.answer(f"Got it! We will track your application {message.text}.")


async def run_bot() -> None:
    await dp.start_polling(bot)


def register_workers(scheduler: AsyncIOScheduler) -> List[Coroutine]:
    scheduler.add_job(update_public_notices, trigger=IntervalTrigger(hours=24))
    scheduler.add_job(check_public_notices, trigger=IntervalTrigger(hours=6), args=(bot,))
    return [
        update_public_notices(),
        check_public_notices(bot)
    ]


async def main() -> None:
    scheduler = AsyncIOScheduler()
    workers_tasks = register_workers(scheduler)
    scheduler.start()
    await asyncio.gather(run_bot(), *workers_tasks)
    scheduler.shutdown()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
