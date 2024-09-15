from aiogram.filters.command import Command, MagicFilter
from typing import Optional


class CheckByApplication(Command):
    def __init__(
            self,
            ignore_case: bool = False,
            ignore_mention: bool = False,
            magic: Optional[MagicFilter] = None,
    ):
        super().__init__(
            "check",
            prefix="/",
            ignore_case=ignore_case,
            ignore_mention=ignore_mention,
            magic=magic,
        )
