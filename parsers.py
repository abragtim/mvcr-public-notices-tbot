import aiohttp
import bs4
import logging
import json

from dataclasses import dataclass, asdict
from typing import List

logger = logging.getLogger(__name__)


@dataclass
class PublicNotice:
    title: str
    link: str
    description: str


async def parse_public_notices() -> List[PublicNotice]:
    public_notices = []

    total_pages_count = None
    current_page = 1
    url = 'https://www.mvcr.cz/verejne-vyhlasky-oamp'
    while url is not None:
        logger.info("Parsing %i. page - %s", current_page, url)

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                assert response.status == 200  # todo: error message
                bs = bs4.BeautifulSoup(await response.text(), 'html.parser')

        pager = bs.find(class_='stranky')
        total_pages_count = total_pages_count or int(pager.find_all('a')[-2].text)

        for article in bs.find_all(class_='article'):
            infobox = article.find(class_='infobox')
            link = 'https://www.mvcr.cz/' + infobox.find('a')['href']
            title = infobox.find('a').text
            description = (infobox.find('p').text
                           .replace('\n', '').replace('\xa0', '').replace('\r', '').strip())
            public_notices.append(PublicNotice(title, link, description))

        url = 'https://www.mvcr.cz/' + pager.find('a', string=str(current_page + 1))['href'] \
            if current_page < total_pages_count else None
        current_page += 1

    return public_notices


if __name__ == '__main__':
    notices = parse_public_notices()  # use asyncio
    notices = [asdict(public_notice) for public_notice in notices]

    with open("data/storage/public-notices.json", "w") as f:
        f.write(json.dumps(notices))
