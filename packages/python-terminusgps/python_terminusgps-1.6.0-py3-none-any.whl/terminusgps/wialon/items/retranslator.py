from terminusgps.wialon import flags
from terminusgps.wialon.items.base import WialonBase


class WialonRetranslator(WialonBase):
    def create(self, **kwargs) -> int | None:
        """
        Creates a Wialon retranslator.

        :param creator_id: A Wialon user that will create the retranslator.
        :type creator_id: :py:obj:`str`
        :param name: A name for the new retranslator.
        :type name: :py:obj:`str`
        :param config: A Wialon retranslator configuration object.
        :type config: :py:obj:`dict`
        :raises ValueError: If a required parameter was not provided.
        :raises WialonError: If something went wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if not kwargs.get("creator_id"):
            raise ValueError("'creator_id' is required on creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required on creation.")
        if not kwargs.get("config"):
            raise ValueError("'config' is required on creation.")

        response = self.session.wialon_api.core_create_retranslator(
            **{
                "creatorId": kwargs["creator_id"],
                "name": kwargs["name"],
                "config": kwargs["config"],
                "dataFlags": flags.DATAFLAG_UNIT_BASE,
            }
        )
        return response.get("item", {}).get("id")

    def update_config(self, new_config: dict) -> None:
        """
        Updates the retranslator config to the new config.

        :param new_config: A Wialon retranslator configuration.
        :type units: :py:obj:`dict`
        :raises WialonError: If something went wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.retranslator_update_config(
            **{"itemId": self.id, "config": new_config}
        )

    def add_units(self, units: list[WialonBase]) -> None:
        """
        Adds a list of units to the Wialon retranslator.

        :param units: A list of Wialon unit objects.
        :type units: :py:obj:`list`
        :raises WialonError: If something went wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.retranslator_update_units(
            **{
                "itemId": self.id,
                "units": [{"a": unit.id, "i": unit.hw_type} for unit in units],
                "callMode": "add",
            }
        )

    def rm_units(self, units: list[WialonBase]) -> None:
        """

        Naively removes a list of units from the Wialon retranslator.

        :param units: A list of Wialon unit objects.
        :type units: :py:obj:`list`
        :raises WialonError: If something went wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.retranslator_update_units(
            **{
                "itemId": self.id,
                "units": [{"a": unit.id, "i": unit.hw_type} for unit in units],
                "callMode": "remove",
            }
        )

    def start(self, stop: int | None = None) -> None:
        """
        Starts the Wialon retranslator.

        :raises WialonError: If something went wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.retranslator_update_operating(
            **{"itemId": self.id, "operate": int(True), "stopTime": stop}
        )

    def stop(self) -> None:
        """
        Stops the Wialon retranslator.

        :raises WialonError: If something went wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.retranslator_update_operating(
            **{"itemId": self.id, "operate": int(False)}
        )
