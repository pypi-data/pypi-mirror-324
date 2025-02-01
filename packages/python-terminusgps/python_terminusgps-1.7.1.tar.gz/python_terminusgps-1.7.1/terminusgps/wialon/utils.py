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


def get_hw_type_id(name: str, session: WialonSession) -> int | None:
    response = session.wialon_api.core_get_hw_types(
        **{
            "filterType": "id",
            "filterValue": "name,id",
            "includeType": "true",
            "ignoreRename": "true",
        }
    )
    hw_types = {item.get("name"): item.get("id") for item in response}
    return int(hw_types.get(name)) if name in hw_types.keys() else None


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


def gen_wialon_password(length: int = 32) -> str:
    """Generates a Wialon compliant password."""
    min_length, max_length = 4, 64
    if length > max_length:
        raise ValueError(
            f"Password cannot be greater than {max_length} characters in length. Got {length}."
        )
    elif length < min_length:
        raise ValueError(
            f"Password cannot be less than {min_length} characters in length. Got {length}."
        )

    s0 = list(string.ascii_uppercase)
    s1 = list(string.ascii_lowercase)
    s2 = list(string.digits)
    s3 = list("!@#$%^*()[]-_+")

    while True:
        password = "".join([secrets.choice(s0 + s1 + s2 + s3) for _ in range(length)])
        if (
            any(c.islower() for c in password)
            and any(c.isupper() for c in password)
            and sum(c.isdigit() for c in password) >= 3
            and any(c in s3 for c in password)
        ):
            break
    return password


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
