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
            }
        )
        return response.get("item", {}).get("id")

    @property
    def is_account(self) -> bool:
        response = self.session.wialon_api.core_search_item(
            **{"id": self.id, "flags": flags.DATAFLAG_RESOURCE_BILLING_PROPERTIES}
        )
        return response.get("item", {}).get("bact") == self.id

    def migrate_unit(self, unit: WialonBase) -> None:
        """
        Migrates a :py:obj:`WialonUnit` into the account.

        :param unit: A Wialon object.
        :type unit: :py:obj:`~terminusgps.wialon.items.base.WialonBase`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_account, "The resource is not an account"
        self.session.wialon_api.account_change_account(
            **{"itemId": unit.id, "resourceId": self.id}
        )

    def update_plan(self, new_plan: str) -> None:
        """
        Updates the account billing plan.

        :param new_plan: The name of a billing plan.
        :type new_plan: :py:obj:`str`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_account, "The resource is not an account"
        self.session.wialon_api.account_update_plan(
            **{"itemId": self.id, "plan": new_plan}
        )

    def create_account(self, billing_plan: str) -> None:
        """
        Transforms the resource into an account.

        :param billing_plan: The name of a billing plan.
        :type billing_plan: :py:obj:`str`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_account, "The resource is already an account"
        self.session.wialon_api.account_create_account(
            **{"itemId": self.id, "plan": billing_plan}
        )

    def delete_account(self) -> None:
        """
        Deletes the account if it exists, as well as any micro-objects and macro-objects it contains.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_account, "The resource is not an account"
        self.session.wialon_api.account_delete_account(**{"itemId": self.id})

    def enable_account(self) -> None:
        """
        Enables the Wialon account.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_account, "The resource is not an account"
        self.session.wialon_api.account_enable_account(
            **{"itemId": self.id, "enable": int(True)}
        )

    def disable_account(self) -> None:
        """
        Disables the Wialon account.

        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_account, "The resource is not an account"
        self.session.wialon_api.account_enable_account(
            **{"itemId": self.id, "enable": int(False)}
        )

    def set_minimum_days(self, days: int = 0) -> None:
        """
        Sets the minimum days counter value to ``days``.

        :param days: Number of days to set the counter to. Default is ``0``.
        :type days: :py:obj:`int`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_account, "The resource is not an account"
        self.session.wialon_api.account_update_min_days(
            **{"itemId": self.id, "minDays": days}
        )

    def add_days(self, days: int = 30) -> None:
        """
        Adds days to the account.

        :param days: Number of days to add to the account. Default is ``30``.
        :type days: :py:obj:`int`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_account, "The resource is not an account"
        self.session.wialon_api.account_do_payment(
            **{
                "itemId": self.id,
                "balanceUpdate": "0.00",
                "daysUpdate": days,
                "description": f"{self.session.id} - Added {days} days.",
            }
        )

    def set_settings_flags(
        self,
        flags: int = 0x20,
        block_balance_val: float = 0.00,
        deny_balance_val: float = 0.00,
    ) -> None:
        """
        Sets account settings flags.

        :param flags: A flag integer to set on the account.
        :type flags: :py:obj:`int`
        :param block_balance_val: Minimum amount on the account's balance before blocking the account.
        :type block_balance_val: :py:obj:`float`
        :param deny_balance_val: Minimum amount on the account's balance before denying the account.
        :type deny_balance_val: :py:obj:`float`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        assert self.is_account, "The resource is not an account"
        self.session.wialon_api.account_update_flags(
            **{
                "itemId": self.id,
                "flags": flags,
                "blockBalance": block_balance_val,
                "denyBalance": deny_balance_val,
            }
        )
