import asyncio
import threading
from typing import Self, Optional, Union, Tuple, Dict
import aiolimiter
import aiohttp
from collections.abc import Iterable
from .error import WPIGetInstanceError, WPIInstanceInitError, check_wg_response
import sys
from .decorators import retry_decorator


class WPIClient:
    _instances = {}
    _lock = threading.Lock()

    def __new__(cls, application_id: str, *args, **kwargs) -> Self:
        assert application_id
        with cls._lock:
            if application_id not in cls._instances:
                cls._instances[application_id] = super().__new__(cls)
            return cls._instances[application_id]

    def __init__(
        self,
        application_id: str,
        max_rate: Optional[float] = 10,
        rate_time_period: Optional[float] = 1,
    ) -> None:
        if not application_id:
            raise WPIInstanceInitError()
        self.application_id = application_id
        self.limiter = aiolimiter.AsyncLimiter(max_rate, rate_time_period)
        self.player = WPIPlayer(self.application_id, self.limiter)
        self.encyclopedia = WPIEncyclopedia(self.application_id, self.limiter)
        self.warships = WPIWarships(self.application_id, self.limiter)
        self.clans = WPIClans(self.application_id, self.limiter)

    @classmethod
    async def get_instance(cls, application_id: str) -> "WPIClient":
        if instance := cls._instances.get(application_id, None):
            return instance
        else:
            raise WPIGetInstanceError()


class WPIBase:
    def __init__(self, application_id: str, limiter: aiolimiter.AsyncLimiter) -> None:
        assert application_id
        self.application_id = application_id
        self.limiter = limiter


class WPIPlayer(WPIBase):
    @retry_decorator()
    async def serch(
        self,
        server: str,
        search: str,
        fields: Optional[Union[str, Iterable[str]]] = None,
        language: Optional[str] = None,
        limit: Optional[int] = None,
        search_type: Optional[str] = None,
    ) -> Optional[Tuple[Tuple[str, int]]]:
        assert server
        assert search
        async with self.limiter:
            async with aiohttp.ClientSession(server) as session:
                api_uri = "/wows/account/list/"
                payload = {
                    "application_id": self.application_id,
                    "search": search,
                }
                if fields:
                    if isinstance(fields, Iterable):
                        fields = ",".join(fields)
                    payload["fields"] = fields
                if language:
                    payload["language"] = language
                if limit:
                    assert limit <= 100
                    payload["limit"] = limit
                if search_type:
                    payload["type"] = search_type
                async with session.get(
                    api_uri, params=payload, raise_for_status=True
                ) as response:
                    resp_json = await response.json()
                    await check_wg_response(resp_json)
                    return tuple(
                        ((i["nickname"], i["account_id"]) for i in resp_json["data"])
                    )

    @retry_decorator()
    async def personal_data(
        self,
        server: str,
        account_id: Union[int, Iterable[int], str] = None,
        access_token: Optional[str] = None,
        extra: Optional[Union[str, Iterable[str]]] = None,
        fields: Optional[Union[str, Iterable[str]]] = None,
        language: Optional[str] = None,
    ) -> Optional[Tuple[Dict]]:
        assert server
        assert account_id

        async with self.limiter:
            async with aiohttp.ClientSession(server) as session:
                api_uri = "/wows/account/info/"
                payload = {
                    "application_id": self.application_id,
                }

                if account_id:
                    if isinstance(account_id, (list, tuple)):
                        account_id = ",".join(map(str, account_id))
                    elif not isinstance(account_id, str):
                        account_id = str(account_id)
                    payload["account_id"] = account_id

                if access_token:
                    payload["access_token"] = access_token

                if fields:
                    if isinstance(fields, (list, tuple)):
                        fields = ",".join(fields)
                    payload["fields"] = fields

                if language:
                    payload["language"] = language

                if extra:
                    if isinstance(extra, (list, tuple)):
                        extra = ",".join(extra)
                    payload["extra"] = extra

                async with session.get(
                    api_uri, params=payload, raise_for_status=True
                ) as response:
                    resp_json = await response.json()
                    await check_wg_response(resp_json)
                    return tuple(resp_json["data"].values())


class WPIEncyclopedia(WPIBase):
    @retry_decorator()
    async def _1page_warships(
        self,
        server: str,
        fields: Optional[Union[str, Iterable[str]]] = None,
        language: Optional[str] = None,
        limit: Optional[int] = None,
        nation: Optional[Union[str, Iterable[str]]] = None,
        page_no: Optional[int] = None,
        ship_id: Optional[Union[str, Iterable[int], int]] = None,
        ship_type: Optional[Union[str, Iterable[str]]] = None,
    ) -> Optional[Tuple[int, Tuple]]:
        assert server

        async with self.limiter:
            async with aiohttp.ClientSession(server) as session:
                api_uri = "/wows/encyclopedia/ships/"
                payload = {
                    "application_id": self.application_id,
                }

                if fields:
                    if isinstance(fields, (list, tuple)):
                        fields = ",".join(fields)
                    payload["fields"] = fields

                if language:
                    payload["language"] = language

                if limit:
                    assert limit <= 100
                    payload["limit"] = limit

                if nation:
                    if isinstance(nation, (list, tuple)):
                        nation = ",".join(nation)
                    payload["nation"] = nation

                if page_no:
                    payload["page_no"] = page_no

                if ship_id:
                    if isinstance(ship_id, (list, tuple)):
                        ship_id = ",".join(map(str, ship_id))
                    payload["ship_id"] = ship_id

                if ship_type:
                    if isinstance(ship_type, (list, tuple)):
                        ship_type = ",".join(ship_type)
                    payload["type"] = ship_type

                async with session.get(
                    api_uri, params=payload, raise_for_status=True
                ) as response:
                    resp_json = await response.json()
                    await check_wg_response(resp_json)

                    return (
                        resp_json["meta"]["page_total"],
                        tuple(resp_json["data"].values()),
                    )

    @retry_decorator()
    async def warships(
        self,
        server: str,
        fields: Optional[Union[str, Iterable[str]]] = None,
        language: Optional[str] = None,
        limit: Optional[int] = None,
        nation: Optional[Union[str, Iterable[str]]] = None,
        ship_id: Optional[Union[str, Iterable[int], int]] = None,
        ship_type: Optional[Union[str, Iterable[str]]] = None,
        page_no: Optional[int] = None,
    ) -> Tuple[Dict]:
        if page_no != -1:
            _, data = await self._1page_warships(
                server, fields, language, limit, nation, page_no, ship_id, ship_type
            )
            return data
        else:
            # page_no = -1, get all page data
            total_pages, first_page_data = await self._1page_warships(
                server, fields, language, limit, nation, 1, ship_id, ship_type
            )

            tasks = []

            if sys.version_info >= (3, 11):
                async with asyncio.TaskGroup() as tg:
                    for page in range(2, total_pages + 1):
                        tasks.append(
                            tg.create_task(
                                self._1page_warships(
                                    server,
                                    fields,
                                    language,
                                    limit,
                                    nation,
                                    page,
                                    ship_id,
                                    ship_type,
                                )
                            )
                        )
                all_pages_data = [t.result() for t in tasks]
            else:
                for page in range(2, total_pages + 1):
                    tasks.append(
                        self._1page_warships(
                            server,
                            fields,
                            language,
                            limit,
                            nation,
                            page,
                            ship_id,
                            ship_type,
                        )
                    )
                all_pages_data = await asyncio.gather(*tasks)

            all_data = [first_page_data]
            all_data.extend(data for _, data in all_pages_data)

            return tuple(all_data)


class WPIWarships(WPIBase):
    @retry_decorator()
    async def _1statistics(
        self,
        server: str,
        account_id: int,
        access_token: Optional[str] = None,
        extra: Optional[Union[str, Iterable[str]]] = None,
        fields: Optional[Union[str, Iterable[str]]] = None,
        in_garage: Optional[str] = None,
        language: Optional[str] = None,
        ship_id: Optional[Union[int, Iterable[int]]] = None,
    ) -> Dict:
        assert server
        assert account_id

        async with self.limiter:
            async with aiohttp.ClientSession(server) as session:
                api_uri = "/wows/ships/stats/"
                payload = {
                    "application_id": self.application_id,
                    "account_id": account_id,
                }

                if access_token:
                    payload["access_token"] = access_token

                if extra:
                    if isinstance(extra, (list, tuple)):
                        extra = ",".join(extra)
                    payload["extra"] = extra

                if fields:
                    if isinstance(fields, (list, tuple)):
                        fields = ",".join(fields)
                    payload["fields"] = fields

                if in_garage:
                    payload["in_garage"] = in_garage

                if language:
                    payload["language"] = language

                if ship_id:
                    if isinstance(ship_id, (list, tuple)):
                        ship_id = ",".join(map(str, ship_id))
                    payload["ship_id"] = ship_id

                async with session.get(
                    api_uri, params=payload, raise_for_status=True
                ) as response:
                    resp_json = await response.json()
                    await check_wg_response(resp_json)

                    return resp_json["data"].get(str(account_id), None)

    @retry_decorator()
    async def statistics(
        self,
        server: str,
        account_id: Union[int, Iterable[int]] = None,
        access_token: Optional[str] = None,
        extra: Optional[Union[str, Iterable[str]]] = None,
        fields: Optional[Union[str, Iterable[str]]] = None,
        in_garage: Optional[str] = None,
        language: Optional[str] = None,
        ship_id: Optional[Union[int, Iterable[int]]] = None,
    ) -> Tuple[Dict]:
        if isinstance(account_id, int):
            account_id = (account_id,)

        if isinstance(account_id, Iterable):
            if sys.version_info >= (3, 11):
                async with asyncio.TaskGroup() as tg:
                    tasks = [
                        tg.create_task(
                            self._1statistics(
                                server=server,
                                account_id=acc_id,
                                access_token=access_token,
                                extra=extra,
                                fields=fields,
                                in_garage=in_garage,
                                language=language,
                                ship_id=ship_id,
                            )
                        )
                        for acc_id in account_id
                    ]
                results = tuple(t.result() for t in tasks)
            else:
                tasks = [
                    asyncio.create_task(
                        self._1statistics(
                            server=server,
                            account_id=acc_id,
                            application_id=application_id,
                            access_token=access_token,
                            extra=extra,
                            fields=fields,
                            in_garage=in_garage,
                            language=language,
                            ship_id=ship_id,
                        )
                    )
                    for acc_id in account_id
                ]
                responses = await asyncio.gather(*tasks)
                results = tuple(responses)

        return results


class WPIClans(WPIBase):
    @retry_decorator()
    async def search(
        self,
        server: str,
        search: str,
        fields: Optional[Union[str, Iterable[str]]] = None,
        language: Optional[str] = None,
        limit: Optional[int] = None,
        page_no: Optional[int] = None,
    ) -> Dict:
        assert server
        assert search and len(search) >= 2, "Search term must be at least 2 characters."

        async with self.limiter:
            async with aiohttp.ClientSession(server) as session:
                api_uri = "/wows/clans/list/"
                payload = {
                    "application_id": self.application_id,
                    "search": search,
                }

                if fields:
                    if isinstance(fields, (list, tuple)):
                        fields = ",".join(fields)
                    payload["fields"] = fields

                if language:
                    payload["language"] = language

                if limit:
                    assert limit <= 100, "Limit cannot exceed 100."
                    payload["limit"] = limit

                if page_no:
                    assert page_no >= 1, "Page number must be 1 or greater."
                    payload["page_no"] = page_no

                async with session.get(
                    api_uri, params=payload, raise_for_status=True
                ) as response:
                    resp_json = await response.json()
                    await check_wg_response(resp_json)

                    return tuple(
                        (
                            clan["clan_id"],
                            clan["tag"],
                            clan["name"],
                            clan["created_at"],
                            clan["members_count"],
                        )
                        for clan in resp_json["data"]
                    )

    @retry_decorator()
    async def details(
        self,
        server: str,
        clan_id: Union[int, Iterable[int], str] = None,
        extra: Optional[Union[str, Iterable[str]]] = None,
        fields: Optional[Union[str, Iterable[str]]] = None,
        language: Optional[str] = None,
    ) -> Dict:
        assert server
        assert clan_id

        async with self.limiter:
            async with aiohttp.ClientSession(server) as session:
                api_uri = "/wows/clans/info/"
                payload = {
                    "application_id": self.application_id,
                    "clan_id": (
                        clan_id
                        if isinstance(clan_id, int) or isinstance(clan_id, str)
                        else ",".join(map(str, clan_id))
                    ),
                }

                if extra:
                    if isinstance(extra, (list, tuple)):
                        extra = ",".join(extra)
                    payload["extra"] = extra

                if fields:
                    if isinstance(fields, (list, tuple)):
                        fields = ",".join(fields)
                    payload["fields"] = fields

                if language:
                    payload["language"] = language

                async with session.get(
                    api_uri, params=payload, raise_for_status=True
                ) as response:
                    resp_json = await response.json()
                    await check_wg_response(resp_json)

                    return tuple(clan for clan in resp_json["data"].values())

    @retry_decorator()
    async def account_info(
        self,
        server: str,
        account_id: Union[int, Iterable[int], str] = None,
        extra: Optional[Union[str, Iterable[str]]] = None,
        fields: Optional[Union[str, Iterable[str]]] = None,
        language: Optional[str] = None,
    ):
        assert server
        assert account_id
        async with self.limiter:
            async with aiohttp.ClientSession(server) as session:
                api_uri = "/wows/clans/accountinfo/"
                payload = {
                    "application_id": self.application_id,
                    "account_id": (
                        account_id
                        if isinstance(account_id, int) or isinstance(account_id, str)
                        else ",".join(map(str, account_id))
                    ),
                }

                if extra:
                    if isinstance(extra, (list, tuple)):
                        extra = ",".join(extra)
                    payload["extra"] = extra

                if fields:
                    if isinstance(fields, (list, tuple)):
                        fields = ",".join(fields)
                    payload["fields"] = fields

                if language:
                    payload["language"] = language

                async with session.get(
                    api_uri, params=payload, raise_for_status=True
                ) as response:
                    resp_json = await response.json()
                    await check_wg_response(resp_json)

                    return tuple(
                        player_clan for player_clan in resp_json["data"].values()
                    )
