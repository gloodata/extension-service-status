import asyncio
import json
from dataclasses import dataclass
from typing import Dict, List, Optional, Self

import httpx


@dataclass
class StatusPageInfo:
    id: str
    name: str
    time_zone: str
    updated_at: str
    url: str


@dataclass
class StatusEntry:
    created_at: str
    updated_at: str
    start_date: Optional[str]
    description: Optional[str]
    name: str
    status: str
    position: int
    id: str
    page_id: str
    group: bool
    group_id: Optional[str]
    showcase: bool
    only_show_if_degraded: bool


@dataclass
class StatusRoot:
    page: StatusPageInfo
    components: List[StatusEntry]

    @classmethod
    def from_data(cls, data: Dict, name: str, url: str) -> Self:
        if "page" in data:
            page_data = data["page"]
            page = StatusPageInfo(
                id=page_data["id"],
                name=page_data["name"],
                time_zone=page_data["time_zone"],
                updated_at=page_data["updated_at"],
                url=page_data["url"],
            )
        else:
            page = StatusPageInfo(
                id="?",
                name=name,
                time_zone="?",
                updated_at="?",
                url=url,
            )

        components = []
        for comp_data in data["components"]:
            component = StatusEntry(
                created_at=comp_data["created_at"],
                updated_at=comp_data["updated_at"],
                start_date=comp_data.get("start_date"),
                description=comp_data.get("description"),
                name=comp_data["name"],
                status=comp_data["status"],
                position=comp_data["position"],
                id=comp_data["id"],
                page_id=comp_data["page_id"],
                group=comp_data.get("group", False),
                group_id=comp_data.get("group_id"),
                showcase=comp_data.get("showcase", False),
                only_show_if_degraded=comp_data.get(
                    "only_show_if_degraded", False),
            )
            components.append(component)

        return StatusRoot(page=page, components=components)


async def get_status_for_url(url: str) -> Dict:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        response.raise_for_status()
        return response.json()


async def main():
    import pprint

    from toolbox import Service

    print("=== Service Status Test ===\n")

    for service in Service:
        label = service.value
        url = service.url()
        print()
        print(label)

        data = None
        try:
            data = await get_status_for_url(url)
            status = StatusRoot.from_data(data, label, url)
            pprint.pprint(status)
        except httpx.HTTPError as e:
            print("Request error", e)
        except (json.JSONDecodeError, KeyError, TypeError) as e:
            print("Response format error", e, data)


if __name__ == "__main__":
    asyncio.run(main())
