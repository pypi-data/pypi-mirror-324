import pytest
from iwashi.service.skeb import Skeb
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_skeb():
    service = Skeb()
    correct = Result(
        service=service,
        id="Daydream_Ed",
        url="https://skeb.jp/@Daydream_Ed",
        name="Daydreamed ☁",
        description="He/Him | 20+ | 🔞 | ABDL art/animator | Characters I depict sexually will always be 18+ | @bunnychuo 💕💖 | 🇲🇾",
        profile_picture="https://pbs.twimg.com/profile_images/1771562476104208384/rvy1W031.jpg",
        links={
            "https://twitter.com/Daydream_Ed",
            "http://Ko-fi.com/daydreamed",
        },
    )
    await _test_service(
        service,
        correct,
        "https://skeb.jp/@Daydream_Ed",
    )
