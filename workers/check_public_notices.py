import logging

from data.public_notices import PublicNoticesStorage
from data.users import UsersStorage

from aiogram import Bot

from services.user_service import send_public_notice_to_user_if_exists

logger = logging.getLogger(__name__)


async def check_public_notices(bot: Bot):
    users = UsersStorage().get_all()
    public_notices = PublicNoticesStorage().get_as_dict()
    for user in users:
        logger.info("Checking public notices for user %s...", user.id)
        await send_public_notice_to_user_if_exists(user, public_notices, bot)
