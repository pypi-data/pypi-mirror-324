import pytest
from iwashi.service.marshmallowqa import MarshmallowQA
from iwashi.visitor import Result
from tests.service_tester import _test_service


@pytest.mark.asyncio
async def test_marshmallowqa():
    service = MarshmallowQA()
    correct = Result(
        service=service,
        id="wug0lycjx6zg13v",
        url="https://marshmallow-qa.com/wug0lycjx6zg13v",
        name="一般山羊",
        description="プロフィール",
        profile_picture="https://marshmallow-qa.com/assets/initial-7df60e1334a612d6084881c5f4ea592ea678ba7b.png",
        links={
            "https://x.com/am4_02",
            "https://youtube.com/@2ji_han",
        },
    )
    await _test_service(
        service,
        correct,
        "https://marshmallow-qa.com/wug0lycjx6zg13v",
        "https://marshmallow-qa.com/wug0lycjx6zg13v#profile",
    )
