from terminusgps.wialon import flags
from terminusgps.wialon.items.base import WialonBase


class WialonResource(WialonBase):
    def create(self, **kwargs) -> int | None:
        if not kwargs.get("creator_id"):
            raise ValueError("'creator_id' is required for creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required for creation.")
        if not kwargs.get("flags"):
            kwargs["flags"] = flags.DATAFLAG_UNIT_BASE

        response = self.session.wialon_api.core_create_resource(
            **{
                "creatorId": kwargs["creator_id"],
                "name": kwargs["name"],
                "dataFlags": kwargs["flags"],
                "skipCreatorCheck": int(True),
            }
        )
        return response.get("item", {}).get("id")
