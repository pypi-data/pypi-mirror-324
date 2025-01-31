import secrets
import string

from typing import Any
from .session import WialonSession
from .flags import DATAFLAG_UNIT_BASE

from terminusgps.wialon.items import (
    WialonUser,
    WialonUnit,
    WialonUnitGroup,
    WialonResource,
)


def get_wialon_cls(items_type: str) -> Any:
    """Returns a Wialon object class based on items_type."""
    match items_type:
        case "user":
            wialon_cls = WialonUser
        case "avl_unit":
            wialon_cls = WialonUnit
        case "avl_unit_group":
            wialon_cls = WialonUnitGroup
        case "avl_resource":
            wialon_cls = WialonResource
        case _:
            raise ValueError(f"Invalid items_type '{items_type}'")
    return wialon_cls


def is_unique(value: str, session: WialonSession, items_type: str = "avl_unit") -> bool:
    """Determines if the value is unique among Wialon objects of type 'items_type'."""
    result = session.wialon_api.core_check_unique(
        **{"type": items_type, "value": value.strip()}
    ).get("result")
    return not bool(result)


def gen_wialon_password(length: int = 16) -> str:
    """Generates a Wialon compliant password."""
    if length > 64:
        raise ValueError(f"Passwords cannot be greater than 64 chars. Got '{length}'.")
    if length < 4:
        raise ValueError(f"Password cannot be less than 4 chars. Got '{length}'.")

    symbols: str = "!@#$%^*()[]-_+"
    alphabet: str = string.ascii_letters + string.digits + symbols
    password: str = "".join(secrets.choice(alphabet) for _ in range(length - 4))
    return (
        password
        + secrets.choice(string.ascii_lowercase)
        + secrets.choice(string.ascii_uppercase)
        + secrets.choice(string.digits)
        + secrets.choice(symbols)
    )


def get_id_from_iccid(iccid: str, session: WialonSession) -> str | None:
    """Takes a Wialon unit's IMEI # and returns its unit id, if it exists."""
    response = session.wialon_api.core_search_items(
        **{
            "spec": {
                "itemsType": "avl_unit",
                "propName": "rel_admin_field_value",
                "propValueMask": str(iccid),
                "sortType": "admin_fields",
                "propType": "adminfield",
                "or_logic": 0,
            },
            "force": 0,
            "flags": DATAFLAG_UNIT_BASE,
            "from": 0,
            "to": 0,
        }
    )

    if response.get("totalItemsCount", 0) == 1:
        return response["items"][0].get("id")


def main() -> None:
    with WialonSession() as session:
        wialon_id = get_id_from_iccid("89015809000307608963", session)
        print(f"{wialon_id = }")
    return


if __name__ == "__main__":
    main()
