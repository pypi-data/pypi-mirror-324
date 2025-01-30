from urllib.parse import quote_plus

from terminusgps.wialon import flags
from terminusgps.wialon.items.base import WialonBase


class WialonUnit(WialonBase):
    def create(self, **kwargs) -> int | None:
        """
        Creates a new Wialon unit.

        :param creator_id: A Wialon user id.
        :type creator_id: :py:obj:`int`
        :param name: A new name for the unit.
        :type name: :py:obj:`str`
        :param hw_type: A Wialon hardware type.
        :type hw_type: :py:obj:`str`
        :returns: The Wialon id for the new unit.
        :rtype: :py:obj:`int` | :py:obj:`None`

        """
        if not kwargs.get("creator_id"):
            raise ValueError("'creator_id' is required on creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required on creation.")
        if not kwargs.get("hw_type"):
            raise ValueError("'hw_type' is required on creation.")

        response = self.session.wialon_api.core_create_unit(
            **{
                "creatorId": kwargs["creator_id"],
                "name": kwargs["name"],
                "hwTypeId": kwargs["hw_type"],
                "dataFlags": flags.DATAFLAG_UNIT_BASE,
            }
        )
        return response.get("item", {}).get("id")

    def execute_command(
        self,
        name: str,
        link_type: str,
        timeout: int = 5,
        flags: int = 0,
        param: dict | None = None,
    ) -> None:
        """
        Executes a command on this Wialon unit.

        :param name: A Wialon command name.
        :type name: :py:obj:`str`
        :param link_type: A protocol to use for the Wialon command.
        :type link_type: :py:obj:`str`
        :param timeout: How long (in seconds) to wait before timing out command execution. Default is ``5``.
        :type timeout: :py:obj:`int`
        :param flags: Flags to pass to the Wialon command execution.
        :type flags: :py:obj:`int`
        :param param: Additional parameters to execute the command with.
        :type param: :py:obj:`dict` | :py:obj:`None`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        self.session.wialon_api.unit_exec_cmd(
            **{
                "itemId": self.id,
                "commandName": name,
                "linkType": link_type,
                "timeout": timeout,
                "flags": flags,
                "param": param if param else {},
            }
        )

    def set_access_password(self, password: str) -> None:
        """
        Sets a new access password for this Wialon unit.

        :param password: A new access password.
        :type name: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        self.session.wialon_api.unit_update_access_password(
            **{"itemId": self.id, "accessPassword": password}
        )

    def activate(self) -> None:
        """
        Activates this Wialon unit.

        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        self.session.wialon_api.unit_set_active(
            **{"itemId": self.id, "active": int(True)}
        )

    def deactivate(self) -> None:
        """
        Deactivates this Wialon unit.

        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        self.session.wialon_api.unit_set_active(
            **{"itemId": self.id, "active": int(False)}
        )

    def assign_phone(self, phone: str) -> None:
        """
        Assigns a phone number to this Wialon unit.

        :param phone: A phone number beginning with a country code.
        :type phone: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        self.session.wialon_api.unit_update_phone(
            **{"itemId": self.id, "phoneNumber": quote_plus(phone)}
        )

    def get_phone_numbers(self) -> list[str]:
        """
        Retrieves all phone numbers assigned to this Wialon unit.

        This includes the usually assigned phone number + custom/admin fields labeled ``to_number``.

        :raises WialonError: If something goes wrong with Wialon.
        :returns: A list of phone numbers.
        :rtype: :py:obj:`list`

        """

        phones = []
        for field in self.cfields | self.afields:
            if field["n"] == "to_number":
                phones.append(field["v"])
        return phones
