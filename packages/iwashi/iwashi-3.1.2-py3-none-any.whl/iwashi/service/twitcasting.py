import re

import bs4
from loguru import logger

from iwashi.helper import HTTP_REGEX, normalize_url
from iwashi.visitor import Context, Service


class TwitCasting(Service):
    def __init__(self) -> None:
        super().__init__(
            name="TwitCasting",
            regex=re.compile(
                HTTP_REGEX + r"twitcasting\.tv/(?P<id>[-\w]+)", re.IGNORECASE
            ),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://twitcasting.tv/{id}"
        res = await context.session.get(url)
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        element = soup.select_one("meta[property='og:title']")
        if element is None:
            logger.warning(f"[TwitCasting] Could not find name for {url}")
            return
        name = element.attrs.get("content")
        element = soup.select_one("meta[property='og:image']")
        profile_picture = None
        if element is not None:
            attr = element.attrs.get("content")
            if isinstance(attr, str):
                profile_picture = normalize_url(attr)
        description: str | None = None
        element = soup.select_one('meta[name="description"]')
        if element is not None:
            description = element.attrs.get("content")

        context.create_result(
            self,
            id=id,
            url=url,
            name=name,
            description=description,
            profile_picture=profile_picture,
        )

        links: set[str] = set()
        for element in soup.select(".tw-live-author__commandbox--socials a"):
            links.add(str(element.attrs.get("href")))
        for link in links:
            if link.startswith("/"):
                continue
            context.enqueue_visit(link)
