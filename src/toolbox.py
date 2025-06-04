import json
from enum import Enum
from typing import Optional, Self

import httpx
from glootil import Toolbox

from status import StatusRoot, get_status_for_url

tb = Toolbox("gd-service-status", "Service Status", "Show Status for Services")


@tb.enum(icon="server")
class Service(Enum):
    AKAMAI = "Akamai"
    BITBUCKET = "Bitbucket"
    CLOUDFLARE = "Cloudflare"
    COINBASE = "Coinbase"
    DIGITALOCEAN = "Digital Ocean"
    DISCORD = "Discord"
    DROPBOX = "Dropbox"
    GITHUB = "Github"
    HASHICORP = "HashiCorp"
    HUBSPOT = "Hubspot"
    LINEAR = "Linear"
    LOOM = "Loom"
    NEWRELIC = "New Relic"
    NPM = "Npm"
    OPENAI = "OpenAI"
    REDDIT = "Reddit"
    SENDGRID = "Sendgrid"
    SNOWFLAKE = "Snowflake"
    SQUARESPACE = "Squarespace"
    TWILIO = "Twilio"
    TWITCH = "Twitch"
    VANTA = "Vanta"
    VERCEL = "Vercel"
    WORKOS = "WorkOS"

    @classmethod
    def from_name(cls, s: str) -> Optional[Self]:
        try:
            return cls(s)
        except ValueError:
            return None

    def base_url(self) -> str:
        return SERVICE_TO_URL[self]

    def url(self) -> str:
        base_url = self.base_url()
        return f"https://{base_url}/api/v2/components.json"


SERVICE_TO_URL = {
    Service.AKAMAI: "www.akamaistatus.com",
    Service.BITBUCKET: "bitbucket.status.atlassian.com",
    Service.CLOUDFLARE: "www.cloudflarestatus.com",
    Service.COINBASE: "status.coinbase.com",
    Service.DIGITALOCEAN: "status.digitalocean.com",
    Service.DISCORD: "discordstatus.com",
    Service.DROPBOX: "status.dropbox.com",
    Service.GITHUB: "www.githubstatus.com",
    Service.HASHICORP: "status.hashicorp.com",
    Service.HUBSPOT: "status.hubspot.com",
    Service.LINEAR: "linearstatus.com",
    Service.LOOM: "loom.status.atlassian.com",
    Service.NEWRELIC: "status.newrelic.com",
    Service.NPM: "status.npmjs.org",
    Service.OPENAI: "status.openai.com",
    Service.REDDIT: "www.redditstatus.com",
    Service.SENDGRID: "status.sendgrid.com",
    Service.SNOWFLAKE: "status.snowflake.com",
    Service.SQUARESPACE: "status.squarespace.com",
    Service.TWILIO: "status.twilio.com",
    Service.TWITCH: "status.twitch.com",
    Service.VANTA: "status.vanta.com",
    Service.VERCEL: "www.vercel-status.com",
    Service.WORKOS: "status.workos.com",
}

DEFAULT_SERVICE = Service.GITHUB


@tb.tool(
    name="Service Status",
    args={"service": "for"},
    examples=["is github up?", "is openai down?", "service status for vercel"],
)
async def status_for_service(service: Service = DEFAULT_SERVICE):
    "Shows Status for a service"
    try:
        url = service.url()
        label = service.value
        data = await get_status_for_url(url)
        status = StatusRoot.from_data(data, label, url)
        rows = [
            (r.name, r.status, ["datetime", {"iso": r.updated_at}])
            for r in status.components
        ]

        return {
            "type": "Table",
            "columns": ["Name", "Status", "Updated"],
            "rows": rows,
        }
    except httpx.HTTPError as e:
        print(e)
        return f"Service Status Request Error: {e}"
    except (json.JSONDecodeError, KeyError, TypeError) as e:
        print(e)
        return "Response Format Error"


@tb.tool(
    name="Service Status Table",
    examples=["Show all Services", "Show available services"],
)
async def service_status_table():
    rows = []
    for service in Service:
        base_url = service.base_url()
        url = f"https://{base_url}"
        rows.append(
            ([service.to_data_tag(), [
             "link", {"url": url, "label": base_url}]])
        )

    return {
        "type": "Table",
        "columns": ["Name", "Site"],
        "rows": rows,
    }
