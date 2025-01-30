from __future__ import annotations

import re
from typing import Dict, List, TypedDict, Union

import bs4

from iwashi.helper import BASE_HEADERS, HTTP_REGEX, assert_none, option
from iwashi.visitor import Context, Service


class MarshmallowQA(Service):
    def __init__(self):
        super().__init__(
            name="MarshmallowQA",
            regex=re.compile(
                HTTP_REGEX + r"marshmallow-qa.com/(?P<id>\w+)", re.IGNORECASE
            ),
        )

    async def visit(self, context: Context, id: str):
        url = f"https://marshmallow-qa.com/{id}"
        res = await context.session.get(
            url,
            headers=BASE_HEADERS,
        )
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")

        name = assert_none(
            soup.select_one(".card > .card-body > h1"), "Could not find name"
        ).text
        description = (
            option(
                soup.select_one(".card > .card-body > div.text-sm.leading-normal"),
            )
            .map(lambda x: x.text)
            .get()
        )
        profile_picture = assert_none(
            soup.select_one(".card > .card-body > * > picture > img"),
            "Could not find profile picture",
        ).attrs.get("src")

        context.create_result(
            self,
            id=id,
            url=url,
            name=name,
            description=description,
            profile_picture=profile_picture,
        )

        links = soup.select(
            ".card > .card-body > ul > li > a[rel~='noopener'][rel~='noreferrer'][target='_blank']"
        )
        for link in links:
            href = link.attrs.get("href")
            if not href:
                continue
            context.enqueue_visit(href)
