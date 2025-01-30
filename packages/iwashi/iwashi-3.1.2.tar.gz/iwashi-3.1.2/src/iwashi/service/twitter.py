from __future__ import annotations
import base64
import hashlib
import json
import math
from pathlib import Path
import random
import re
import time
from typing import Any, List, TypedDict

import bs4
from loguru import logger
import yarl

from iwashi.helper import HTTP_REGEX
from iwashi.visitor import Context, Service


class Twitter(Service):
    def __init__(self) -> None:
        super().__init__(
            name="Twitter",
            regex=re.compile(
                HTTP_REGEX + r"(twitter|x)\.com/(#!/)?@?(?P<id>\w+)", re.IGNORECASE
            ),
        )
        self.headers = {
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "ja",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0",
        }
        self.bearer_token: str | None = None
        self.guest_token: str | None = None
        self.endpoints: dict[str, Endpoint] = {}
        self.scripts: dict[str, str] | None = None
        self.response: bs4.BeautifulSoup | None = None
        self.main_script: str | None = None
        self.twitter_site_verification: str | None = None

    async def fetch_scripts(self, context: Context) -> dict[str, str]:
        if self.scripts:
            return self.scripts
        soup = await self.fetch_twitter_page(context)
        script_elements = soup.select("script")
        scripts_loaded_regex = re.compile(r"^window\.__SCRIPTS_LOADED__\s*=\s*{\s*};?")
        for script_element in script_elements:
            if not script_element.string:
                continue
            if not scripts_loaded_regex.match(script_element.string):
                continue
            break
        else:
            raise ValueError("[Twitter] Could not find scripts")
        scripts_map_regex = re.compile(
            r"{\s*[\"'][a-zA-Z0-9-_\s/\\.~]*[\"']\s*:\s*[\"'][a-zA-Z0-9-_\s/\\.~]*[\"'](?:\s*,\s*\s*[\"'][a-zA-Z0-9-_\s/\\.~]*[\"']\s*:\s*[\"'][a-zA-Z0-9-_\s/\\.~]*[\"'])*\s*}"
        )
        scripts_map = scripts_map_regex.findall(script_element.string)
        required = [
            "ondemand.s",
        ]
        for script_map in scripts_map:
            try:
                obj = json.loads(script_map)
            except json.JSONDecodeError:
                logger.warning(f"[Twitter] Could not parse script map: {script_map}")
                continue
            for key in required:
                if key in obj:
                    break
            else:
                continue
            self.scripts = obj
            break
        else:
            raise ValueError("[Twitter] Could not find required scripts")
        return obj

    async def fetch_script(self, context: Context, script_name: str) -> str:
        scripts = await self.fetch_scripts(context)
        if script_name not in scripts:
            raise ValueError(f"[Twitter] Could not find script: {script_name}")
        if script_name not in scripts:
            raise ValueError(f"[Twitter] Could not find script: {script_name}")
        key = scripts[script_name]
        script_url = (
            f"https://abs.twimg.com/responsive-web/client-web/{script_name}.{key}a.js"
        )
        script_res = await context.session.get(
            script_url,
            headers=self.headers,
        )
        script_res.raise_for_status()
        return await script_res.text()

    async def retrieve_endpoints(self, context: Context) -> None:
        script_text = await self.fetch_script_text(context)
        # find e.exports
        exports: list[str] = []
        index = 0
        length = len(script_text)
        while index < length:
            index = script_text.find("e.exports", index)
            if index == -1:
                break
            index += len("e.exports")
            next_open = script_text.find("{", index)
            next_close = script_text.find("}", index)
            if next_open == -1:
                break
            if next_close == -1:
                break
            if next_close < next_open:
                continue
            start = next_open
            index = next_open + 1
            indent = 1
            while index < length:
                next_open = script_text.find("{", index)
                next_close = script_text.find("}", index)
                if next_open == -1:
                    break
                if next_close == -1:
                    break
                if next_open < next_close:
                    indent += 1
                    index = next_open + 1
                else:
                    indent -= 1
                    index = next_close + 1
                if indent <= 0:
                    exports.append(script_text[start:index])
                    break
        # filter json
        object_regex = re.compile(r"^{[a-zA-Z][a-zA-Z0-9]*\s*\:\s*(?:[\"']|\[|{).+}$")
        exports = list(filter(object_regex.match, exports))
        print("\n".join(exports))
        # map to json
        endpoints: list[Endpoint] = []
        for export in exports:
            obj = self._parse_export_to_dict(export)
            if (
                "queryId" not in obj
                or "operationName" not in obj
                or "operationType" not in obj
                or "metadata" not in obj
            ):
                logger.warning(f"[Twitter] Unexpected export: {export}")
                continue
            endpoints.append(Endpoint(**obj))
        self.endpoints = {endpoint["operationName"]: endpoint for endpoint in endpoints}

    async def fetch_script_text(self, context: Context) -> str:
        if self.main_script:
            return self.main_script
        soup = await self.fetch_twitter_page(context)
        script_element = soup.select_one(
            'script[src^="https://abs.twimg.com/responsive-web/client-web/main."]'
        )
        assert script_element
        src = script_element["src"]
        assert isinstance(src, str)
        src_url = yarl.URL(src)
        script_res = await context.session.get(
            src_url,
            headers=self.headers,
        )
        script_res.raise_for_status()
        script_text = await script_res.text()
        self.main_script = script_text
        return script_text

    async def fetch_twitter_page(self, context: Context) -> bs4.BeautifulSoup:
        if self.response:
            return self.response
        res = await context.session.get(
            "https://x.com/?mx=2",
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36 Edg/132.0.0.0"
            },
        )
        res.raise_for_status()
        soup = bs4.BeautifulSoup(await res.text(), "html.parser")
        self.response = soup
        return soup

    def _parse_export_to_dict(self, export):
        obj = {}
        index = 0
        length = len(export)
        while index < length:
            key_match = re.search(r"([a-zA-Z][a-zA-Z0-9]*)\s*\:", export[index:])
            if not key_match:
                break
            key = key_match.group(1)
            index += key_match.end()
            value = None
            if export[index] == "[":
                end = export.find("]", index)
                raw_value = export[index : end + 1]
                value = json.loads(raw_value)
                index = end + 1
            elif export[index] == "{":
                end = export.find("}", index)
                raw_value = export[index : end + 1]
                value = self._parse_export_to_dict(raw_value)
                index = end + 1
            elif export[index] in ["'", '"']:
                end = export.find(export[index], index + 1)
                value = export[index + 1 : end]
                index = end + 1
            else:
                raise ValueError(f"Unexpected value: {export[index:]}")
            obj[key] = value
        return obj

    async def fetch_authorization(self, context: Context) -> str:
        if self.bearer_token:
            return self.bearer_token

        main_script = await self.fetch_script_text(context)
        match = re.search('(AAAAA.*?)"', main_script)
        assert match
        bearer_token = "Bearer " + match.group(1)
        self.bearer_token = bearer_token
        return bearer_token

    async def fetch_guest_token(self, context: Context) -> str:
        if self.guest_token:
            return self.guest_token
        res = await context.session.post(
            "https://api.x.com/1.1/guest/activate.json",
            headers=self.headers,
        )
        res.raise_for_status()
        data = await res.json()
        self.guest_token = data["guest_token"]
        return data["guest_token"]

    async def fetch_twitter_site_verification(self, context: Context) -> str:
        if self.twitter_site_verification:
            return self.twitter_site_verification
        soup = await self.fetch_twitter_page(context)
        twitter_site_verification = soup.select_one(
            '[name="twitter-site-verification"]'
        )
        assert twitter_site_verification
        twitter_site_verification = twitter_site_verification["content"]
        assert isinstance(twitter_site_verification, str)
        self.twitter_site_verification = twitter_site_verification
        return twitter_site_verification

    async def setup_headers(self, context: Context) -> None:
        self.headers["authorization"] = await self.fetch_authorization(context)
        self.headers["x-guest-token"] = await self.fetch_guest_token(context)

    async def fetch_indices(self, context: Context) -> list[int]:
        ondemand_script = await self.fetch_script(context, "ondemand.s")
        indices: list[int] = []
        regex = re.compile(r"\(\w{1}\[(?P<indice>\d{1,2})\],\s*16\)")
        for match in regex.finditer(ondemand_script):
            indices.append(int(match.group("indice")))
        return indices

    async def get_frames(self, context: Context) -> list[bs4.Tag]:
        # [id^="loading-x-anim"]
        soup = await self.fetch_twitter_page(context)
        frames = soup.select('[id^="loading-x-anim"]')
        return frames

    async def get2d_array(
        self, context: Context, key_bytes: bytes
    ) -> list[list[float]]:
        frames = await self.get_frames(context)
        frame_path_data = frames[key_bytes[5] % 4].select("path")[1]
        assert frame_path_data
        path_d = frame_path_data.attrs["d"][9:]
        return [
            list(map(float, re.sub(r"[^\d]+", " ", item).strip().split(" ")))
            for item in path_d.split("C")
        ]

    def solve(
        self, value: float, min_val: float, max_val: float, rounding: bool
    ) -> float:
        result = value * (max_val - min_val) / 255 + min_val
        return int(result) if rounding else round(result, 2)

    def _calculate_cubic_curve(self, a: float, b: float, m: float) -> float:
        return 3.0 * a * (1 - m) * (1 - m) * m + 3.0 * b * (1 - m) * m * m + m * m * m

    def get_value_cubic_curve(self, curves: list[float], time: float) -> float:
        start_gradient = 0.0
        end_gradient = 0.0
        start = 0.0
        mid = 0.0
        end = 1.0
        if time <= 0.0:
            if curves[0] > 0.0:
                start_gradient = curves[1] / curves[0]
            elif curves[1] == 0.0 and curves[2] > 0.0:
                start_gradient = curves[3] / curves[2]
            return start_gradient * time
        if time >= 1.0:
            if curves[2] < 1.0:
                end_gradient = (curves[3] - 1.0) / (curves[2] - 1.0)
            elif curves[2] == 1.0 and curves[0] < 1.0:
                end_gradient = (curves[1] - 1.0) / (curves[0] - 1.0)
            return 1.0 + end_gradient * (time - 1.0)
        while start < end:
            mid = (start + end) / 2
            x_est = self._calculate_cubic_curve(curves[0], curves[2], mid)
            if abs(time - x_est) < 0.00001:
                return self._calculate_cubic_curve(curves[1], curves[3], mid)
            if x_est < time:
                start = mid
            else:
                end = mid
        return self._calculate_cubic_curve(curves[1], curves[3], mid)

    def _interpolate_num(self, from_val: float, to_val: float, f: float) -> float:
        if isinstance(from_val, (int, float)) and isinstance(to_val, (int, float)):
            return from_val * (1 - f) + to_val * f
        if isinstance(from_val, bool) and isinstance(to_val, bool):
            return from_val if f < 0.5 else to_val

    def _interpolate(
        self, from_list: list[float], to_list: list[float], f: float
    ) -> list[float]:
        if len(from_list) != len(to_list):
            raise ValueError(
                f"Mismatched interpolation arguments {from_list}: {to_list}"
            )
        return [
            self._interpolate_num(from_val, to_list[i], f)
            for i, from_val in enumerate(from_list)
        ]

    def _convert_rotation_to_matrix(self, rotation: float) -> list[float]:
        rad = (rotation * 3.141592653589793) / 180
        return [math.cos(rad), -math.sin(rad), math.sin(rad), math.cos(rad)]

    def animate(self, frame_row: list[float], target_time: float):
        from_color = [*map(float, frame_row[:3]), 1]
        to_color = [*map(float, frame_row[3:6]), 1]
        from_rotation = [0.0]
        to_rotation = [self.solve(frame_row[6], 60.0, 360.0, True)]
        remaining_frames = frame_row[7:]
        # isOdd: return num % 2 ? -1.0 : 0.0;
        curves = [
            self.solve(item, -1.0 if counter % 2 else 0.0, 1.0, False)
            for counter, item in enumerate(remaining_frames)
        ]
        val = self.get_value_cubic_curve(curves, target_time)
        color = self._interpolate(from_color, to_color, val)
        color = [value if value > 0 else 0 for value in color]
        rotation = self._interpolate(from_rotation, to_rotation, val)
        matrix = self._convert_rotation_to_matrix(rotation[0])

        str_arr = [
            *map(
                lambda value: hex(round(value))[2:],
                color[:-1],
            ),
            *map(
                lambda value: hex(int(abs(round(value * 100) / 100)))[2:].lower()
                if (
                    hex_value := hex(int(abs(round(value * 100) / 100)))[2:]
                ).startswith(".")
                else f"0{hex_value}"
                if hex_value
                else "0",
                matrix,
            ),
            "0",
            "0",
        ]
        return "".join(str_arr).replace(".", "").replace("-", "")

    async def get_animation_key(self, context: Context, key_bytes: bytes) -> str:
        total_time = 4096
        row_index = key_bytes[0] % 16
        frame_time = 1
        for indice in await self.fetch_indices(context):
            frame_time *= key_bytes[indice] % 16
        arr = await self.get2d_array(context, key_bytes)
        frame_row = arr[row_index]
        target_time = frame_time / total_time
        return self.animate(frame_row, target_time)

    async def _create_tid(self, context: Context, method: str, path: str) -> str:
        time_now = int(time.time() * 1000 - 1682924400000 // 1000)
        time_now_bytes = [(time_now >> (i * 8)) & 0xFF for i in range(4)]
        key = await self.fetch_twitter_site_verification(context)
        key_bytes = base64.b64decode(key)
        animation_key = await self.get_animation_key(context, key_bytes)
        hash_input = f"{method}!{path}!{time_now}!{animation_key}"
        hash_val = hashlib.sha256(hash_input.encode()).digest()
        hash_bytes = list(hash_val)
        random_num = math.floor(random.random() * 256)
        bytes_arr = [
            *key_bytes,
            *time_now_bytes,
            *hash_bytes[:16],
            random_num,
            3,
        ]
        out = bytes([random_num, *map(lambda item: item ^ random_num, bytes_arr)])
        return base64.b64encode(out).decode().replace("=", "")

    async def _call_endpoint(
        self,
        context: Context,
        endpoint: Endpoint,
        variables: dict,
        fieldToggles: dict | None = None,
    ) -> Any:
        path = f"/i/api/graphql/{endpoint['queryId']}/{endpoint['operationName']}"
        ctid = await self._create_tid(context, "GET", path)
        url = f"https://x.com{path}"
        res = await context.session.get(
            url,
            params={
                "variables": json.dumps(variables),
                "features": json.dumps(
                    {key: True for key in endpoint["metadata"]["featureSwitches"]}
                ),
                "fieldToggles": json.dumps(fieldToggles or {}),
            },
            headers={
                **self.headers,
                "x-client-transaction-id": ctid,
            },
        )
        res.raise_for_status()
        return await res.json()

    async def visit(self, context: Context, id: str) -> None:
        url = f"https://twitter.com/{id}"
        await self.setup_headers(context)
        await self.retrieve_endpoints(context)

        info: Root = await self._call_endpoint(
            context,
            self.endpoints["UserByScreenName"],
            {"screen_name": id},
            {"withAuxiliaryUserLabels": False},
        )

        if not info["data"]:
            logger.warning(f"[Twitter] Could not find data for {url}")
            return
        result = info["data"]["user"]["result"]
        if result["__typename"] == "UserUnavailable":
            context.create_result(
                self,
                id=id,
                url=url,
                name="<UserUnavailable>",
            )
            return

        data = result["legacy"]
        context.create_result(
            self,
            id=id,
            url=url,
            name=data["name"],
            description=data["description"],
            profile_picture=data["profile_image_url_https"],
        )

        if "url" not in data["entities"]:
            return

        for link in data["entities"]["url"]["urls"]:
            context.enqueue_visit(link["expanded_url"])

        for link in data["entities"]["description"]["urls"]:
            context.enqueue_visit(link["expanded_url"])


class EndpointMetadata(TypedDict):
    featureSwitches: list[str]
    fieldToggles: list[str]


class Endpoint(TypedDict):
    queryId: str
    operationName: str
    operationType: str
    metadata: EndpointMetadata


class LocationsItem0(TypedDict):
    line: int
    column: int


class Tracing(TypedDict):
    trace_id: str


class Extensions(TypedDict):
    name: str
    source: str
    code: int
    kind: str
    tracing: Tracing


class ErrorsItem0(TypedDict):
    message: str
    locations: List[LocationsItem0]
    path: List[str]
    extensions: Extensions
    code: int
    kind: str
    name: str
    source: str
    tracing: Tracing


class AffiliatesHighlightedLabel(TypedDict):
    pass


class UrlsItem0(TypedDict):
    display_url: str
    expanded_url: str
    url: str
    indices: List[int]


class Description(TypedDict):
    urls: List[UrlsItem0]


class Entities(TypedDict):
    description: Description
    url: Description


class Rgb(TypedDict):
    blue: int
    green: int
    red: int


class PaletteItem0(TypedDict):
    percentage: float
    rgb: Rgb


class Ok(TypedDict):
    palette: List[PaletteItem0]


class R(TypedDict):
    ok: Ok


class MediaColor(TypedDict):
    r: R


class ProfileBannerExtensions(TypedDict):
    mediaColor: MediaColor


class Legacy(TypedDict):
    created_at: str
    default_profile: bool
    default_profile_image: bool
    description: str
    entities: Entities
    fast_followers_count: int
    favourites_count: int
    followers_count: int
    friends_count: int
    has_custom_timelines: bool
    is_translator: bool
    listed_count: int
    location: str
    media_count: int
    name: str
    normal_followers_count: int
    pinned_tweet_ids_str: List[str]
    possibly_sensitive: bool
    profile_banner_extensions: ProfileBannerExtensions
    profile_banner_url: str
    profile_image_extensions: ProfileBannerExtensions
    profile_image_url_https: str
    profile_interstitial_type: str
    screen_name: str
    statuses_count: int
    translator_type: str
    url: str
    verified: bool
    withheld_in_countries: List


class Result(TypedDict):
    __typename: str
    id: str
    rest_id: str
    affiliates_highlighted_label: AffiliatesHighlightedLabel
    is_blue_verified: bool
    legacy: Legacy
    business_account: AffiliatesHighlightedLabel
    legacy_extended_profile: AffiliatesHighlightedLabel
    is_profile_translatable: bool
    verification_info: AffiliatesHighlightedLabel


class User(TypedDict):
    result: Result


class Data(TypedDict):
    user: User


class Root(TypedDict):
    errors: List[ErrorsItem0]
    data: Data
