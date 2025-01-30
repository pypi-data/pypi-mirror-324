import pytest
import requests
from iwashi.service.nicovideo import Nicovideo
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_nicovideo():
    if (
        requests.get(
            "https://www.nicovideo.jp/user/2008672",
            allow_redirects=False,
        ).status_code
        != 200
    ):
        pytest.skip("nicovideo.jp is not available")
    service = Nicovideo()
    correct = Result(
        service=service,
        id="2008672",
        url="https://www.nicovideo.jp/user/2008672",
        name="生パン",
        description='東方アレンジや絵など。UPした曲は、すべて自サイトにmp3を置いてあります！生パン庫： <a href="http://www.namapann.com/" target="_blank" rel="noopener nofollow">http://www.namapann.com/</a><br>',
        profile_picture="https://secure-dcdn.cdn.nimg.jp/nicoaccount/usericon/200/2008672.jpg?1263354782",
        links={
            "https://www.youtube.com/channel/UCVYIzyZuQvyzuQFzihLnA8Q",
            "https://twitter.com/namapann",
        },
    )
    await _test_service(service, correct, "https://www.nicovideo.jp/user/2008672")
