from terminusgps.wialon import flags
from terminusgps.wialon.items.base import WialonBase


class WialonRoute(WialonBase):
    def create(self, **kwargs) -> int | None:
        if not kwargs.get("creator_id"):
            raise ValueError("'creator_id' is required on creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required on creation.")
        if not kwargs.get("flags"):
            kwargs["flags"] = flags.DATAFLAG_UNIT_BASE

        response = self.session.wialon_api.core_create_route(
            **{
                "creatorId": kwargs["creator_id"],
                "name": kwargs["name"],
                "dataFlags": kwargs["flags"],
            }
        )
        return response.get("item", {}).get("id")
