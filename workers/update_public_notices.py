from data.public_notices import PublicNoticesStorage
from parsers import parse_public_notices


async def update_public_notices():
    actual_public_notices = await parse_public_notices()
    PublicNoticesStorage().update(actual_public_notices)
