from typing import Dict

from data.users import User
from parsers import PublicNotice

from aiogram import Bot, html


async def send_public_notice_to_user_if_exists(user: User, public_notices: Dict[str, PublicNotice], bot: Bot) -> bool:
    notice_for_user = public_notices.get(user.application_number)
    if not notice_for_user:
        return False
    await bot.send_message(
        chat_id=user.id,
        text=f"There is the public notice for the application "
             f"{html.bold(user.application_number)}: {html.link('View notice', notice_for_user.link)}.")

    return True
