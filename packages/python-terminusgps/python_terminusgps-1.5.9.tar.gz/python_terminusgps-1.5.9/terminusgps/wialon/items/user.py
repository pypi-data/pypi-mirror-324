from urllib.parse import quote_plus

from terminusgps.wialon import flags
from terminusgps.wialon.items.base import WialonBase
from terminusgps.wialon import constants


class WialonUser(WialonBase):
    def create(self, **kwargs) -> int | None:
        """
        Creates a new Wialon user.

        :param creator_id: A Wialon user id.
        :type creator_id: :py:obj:`int`
        :param name: A name for the user.
        :type name: :py:obj:`str`
        :param name: A password for the user.
        :type name: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: The Wialon id for the new user.
        :rtype: :py:obj:`int` | :py:obj:`None`

        """
        if not kwargs.get("creator_id"):
            raise ValueError("'creator_id' is required on creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required on creation.")
        if not kwargs.get("password"):
            raise ValueError("'password' is required on creation.")

        response = self.session.wialon_api.core_create_user(
            **{
                "creatorId": kwargs["creator_id"],
                "name": kwargs["name"],
                "password": kwargs["password"],
                "dataFlags": flags.DATAFLAG_UNIT_BASE,
            }
        )
        return response.get("item", {}).get("id")

    def _get_access_response(self, hw_type: str) -> dict:
        """
        Returns a dict of the Wialon objects the user has access to.

        :param hw_type: A hardware type of Wialon objects to generate a list for.
        :type hw_type: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: The Wialon API response.
        :rtype: :py:obj:`dict`

        """
        return self.session.wialon_api.user_get_items_access(
            **{
                "userId": self.id,
                "directAccess": True,
                "itemSuperclass": hw_type,
                "flags": 0x2,
            }
        )

    @property
    def units(self) -> list[str]:
        """
        The user's units.

        :raises WialonError: If something goes wrong with Wialon.
        :returns: A list of unit ids the user has access to.
        :rtype: :py:obj:`list`

        """
        response = self._get_access_response(hw_type="avl_unit")
        return [key for key in response.keys()]

    @property
    def groups(self) -> list[str]:
        """
        The user's unit groups.

        :raises WialonError: If something goes wrong with Wialon.
        :returns: A list of group ids the user has access to.
        :rtype: :py:obj:`list`

        """
        response = self._get_access_response(hw_type="avl_unit_group")
        return [key for key in response.keys()]

    def has_access(self, other: WialonBase) -> bool:
        """
        Checks if the user has access to ``other``.

        :param other: A Wialon object.
        :type phone: :py:obj:`~terminusgps.wialon.items.base.WialonBase`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: :py:obj:`True` if the user can access ``other``, else :py:obj:`False`.
        :rtype: :py:obj:`bool`

        """
        response: dict = self._get_access_response(hw_type=other.hw_type)
        items: list[str] = [key for key in response.keys()]
        return True if str(other.id) in items else False

    def assign_phone(self, phone: str) -> None:
        """
        Assigns a phone number to the user.

        :param phone: A phone number, including country code.
        :type phone: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.add_cproperty(("phone", quote_plus(phone)))

    def assign_email(self, email: str) -> None:
        """
        Assigns an email address to the user.

        :param phone: An email address.
        :type phone: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.add_cproperty(("email", email))

    def grant_access(
        self, item: WialonBase, access_mask: int = constants.ACCESSMASK_UNIT_BASIC
    ) -> None:
        """
        Grants the user access to ``item``.

        :param item: A Wialon object.
        :type item: :py:obj:`~terminusgps.wialon.items.base.WialonBase`
        :param access_mask: A Wialon access mask integer.
        :type access_mask: :py:obj:`int`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.user_update_item_access(
            **{"userId": self.id, "itemId": item.id, "accessMask": access_mask}
        )

    def set_settings_flags(self, flags: int, flags_mask: int) -> None:
        """
        Sets the user's settings flags.

        :param flags: The new user settings flags.
        :type flags: :py:obj:`int`
        :param flags_mask: A user settings flag mask.
        :type flags_mask: :py:obj:`int`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.user_update_user_flags(
            **{"userId": self.id, "flags": flags, "flagsMask": flags_mask}
        )

    def update_password(self, old_password: str, new_password: str) -> None:
        """
        Updates the password of the user.

        :param old_password: The user's original password.
        :type old_password: :py:obj:`str`
        :param new_password: A new password.
        :type new_password: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.user_update_password(
            **{
                "userId": self.id,
                "oldPassword": old_password,
                "newPassword": new_password,
            }
        )
