from django.utils import timezone
from terminusgps.wialon.session import WialonSession
from terminusgps.wialon.utils import get_hw_type_id, gen_wialon_password
from terminusgps.wialon.items import WialonUser, WialonResource, WialonUnit
from terminusgps.wialon import constants


def registration_test() -> None:
    timestamp = f"{timezone.now():%y-%m-%d-%H:%M:%S}"

    with WialonSession() as session:
        print(f"Running test '{registration_test.__name__}' as '{session.username}'...")
        hw_type_id = get_hw_type_id(name="Test HW", session=session)

        super_user = WialonUser(
            creator_id=session.uid,
            name=f"super_user_{timestamp}",
            password=gen_wialon_password(length=32),
            session=session,
        )
        resource = WialonResource(
            creator_id=super_user.id, name=f"resource_{timestamp}", session=session
        )
        unit = WialonUnit(
            creator_id=session.uid,
            name=f"test_unit_{timestamp}",
            hw_type_id=hw_type_id,
            session=session,
        )
        super_user.grant_access(unit, access_mask=constants.ACCESSMASK_UNIT_MIGRATION)
        resource.create_account("terminusgps_ext_hist")
        resource.migrate_unit(unit)
        end_user = WialonUser(
            creator_id=super_user.id,
            name=f"end_user_{timestamp}",
            password=gen_wialon_password(length=32),
            session=session,
        )
        end_user.grant_access(unit, access_mask=constants.ACCESSMASK_UNIT_BASIC)


def account_days_test() -> None:
    timestamp = f"{timezone.now():%y-%m-%d-%H:%M:%S}"

    with WialonSession() as session:
        print(f"Running test '{account_days_test.__name__}' as '{session.username}'...")
        account = WialonResource(id="28990259", session=session)
        account.set_settings_flags(0x20)
        account.set_minimum_days(0)
        account.add_days(30)


if __name__ == "__main__":
    registration_test()
    account_days_test()
