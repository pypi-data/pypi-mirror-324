from terminusgps.wialon import constants, flags
from terminusgps.wialon.items.base import WialonBase


class WialonUnitGroup(WialonBase):
    def create(self, **kwargs) -> int | None:
        """
        Creates a new Wialon unit group.

        :param creator_id: A Wialon user id.
        :type creator_id: :py:obj:`int`
        :param name: A name for the group.
        :type name: :py:obj:`str`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: The Wialon id for the new group.
        :rtype: :py:obj:`int` | :py:obj:`None`

        """

        if not kwargs.get("creator_id"):
            raise ValueError("'creator_id' is required on creation.")
        if not kwargs.get("name"):
            raise ValueError("'name' is required on creation.")

        response = self.session.wialon_api.core_create_unit_group(
            **{
                "creatorId": kwargs["creator_id"],
                "name": kwargs["name"],
                "dataFlags": flags.DATAFLAG_UNIT_BASE,
            }
        )
        return response.get("item", {}).get("id")

    def _update_items(self, new_items: list[str]) -> None:
        """
        Sets this group's members to a list of Wialon unit ids.

        :param new_items: A list of Wialon unit ids.
        :type new_items: :py:obj:`list`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """

        self.session.wialon_api.unit_group_update_units(
            **{"itemId": self.id, "units": new_items}
        )

    def is_member(self, item: WialonBase) -> bool:
        """
        Determines whether or not ``item`` is a member of the group.

        :param item: A Wialon object.
        :type item: :py:obj:`~terminusgps.wialon.items.base.WialonBase`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: :py:obj:`True` if ``item`` is a member of the group, else :py:obj:`False`.
        :rtype: :py:obj:`bool`

        """
        return True if str(item.id) in self.items else False

    def grant_access(
        self, item: WialonBase, access_mask: int = constants.ACCESSMASK_UNIT_BASIC
    ) -> None:
        """
        Grants ``item`` access to the group, if it didn't already have access.

        :param item: A Wialon object.
        :type item: :py:obj:`~terminusgps.wialon.items.base.WialonBase`
        :param access_mask: A Wialon access mask.
        :type access_mask: :py:obj:`int`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.user_update_item_access(
            **{"userId": item.id, "itemId": self.id, "accessMask": access_mask}
        )

    def revoke_access(self, item: WialonBase) -> None:
        """
        Revokes ``item``'s access from the group, if it had access.

        :param item: A Wialon object.
        :type item: :py:obj:`~terminusgps.wialon.items.base.WialonBase`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.session.wialon_api.user_update_item_access(
            **{"userId": item.id, "itemId": self.id, "accessMask": 0}
        )

    def add_item(self, item: WialonBase) -> None:
        """
        Adds a Wialon unit to the group.

        :param item: A Wialon object.
        :type item: :py:obj:`~terminusgps.wialon.items.base.WialonBase`
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        new_items: list[str] = self.items.copy() + [str(item.id)]
        self._update_items(new_items)

    def rm_item(self, item: WialonBase) -> None:
        """
        Removes a Wialon unit from the group, if it's a member of the group.

        :param item: A Wialon object.
        :type item: :py:obj:`~terminusgps.wialon.items.base.WialonBase`
        :raises AssertionError: If the item wasn't in the group.
        :raises WialonError: If something goes wrong with Wialon.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_member(item), f"Cannot remove {item}, it's not in the group"
        new_items: list[str] = self.items.copy()
        new_items.remove(str(item.id))
        self._update_items(new_items)

    @property
    def items(self) -> list[str]:
        """
        Returns a list of the group's Wialon unit ids.

        :type: :py:obj:`list`

        """
        response = self.session.wialon_api.core_search_items(
            **{
                "spec": {
                    "itemsType": "avl_unit_group",
                    "propName": "sys_id",
                    "propValueMask": str(self.id),
                    "sortType": "sys_id",
                    "propType": "property",
                    "or_logic": 0,
                },
                "force": 1,
                "flags": flags.DATAFLAG_UNIT_BASE,
                "from": 0,
                "to": 0,
            }
        )
        return [str(unit_id) for unit_id in response.get("items")[0].get("u", [])]
