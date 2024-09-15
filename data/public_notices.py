import json

from dataclasses import asdict
from typing import List, Dict

from parsers import PublicNotice
from utils.application_number_transformations import transform_to_lower_resolution


class PublicNoticesStorage:
    __PATH_TO_PUBLIC_NOTICES_JSON = 'data/storage/public_notices.json'

    @staticmethod
    def get() -> List[PublicNotice]:
        with open(PublicNoticesStorage.__PATH_TO_PUBLIC_NOTICES_JSON, 'r') as fd:
            notices_json = json.load(fd)
        return [PublicNotice(**notice_json) for notice_json in notices_json]

    def get_as_dict(self) -> Dict[str, PublicNotice]:
        public_notices = self.get()
        return {transform_to_lower_resolution(
            notice.description.replace('Č. j. ', '')): notice
                for notice in public_notices}

    @staticmethod
    def update(public_notices: List[PublicNotice]) -> None:
        notices_dict = map(asdict, public_notices)
        with open(PublicNoticesStorage.__PATH_TO_PUBLIC_NOTICES_JSON, 'w') as fd:
            json.dump(list(notices_dict), fd)
