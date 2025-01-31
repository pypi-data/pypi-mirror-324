from wialon.api import Wialon, WialonError
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from .errors import (
    WialonLogoutError,
    WialonLoginError,
    WialonSessionDuplicationError,
    WialonSessionInvalidError,
)


class WialonSession:
    def __init__(
        self,
        token: str | None = None,
        sid: str | None = None,
        scheme: str = "https",
        host: str = "hst-api.wialon.com",
        port: int = 443,
    ) -> None:
        """
        Starts or continues a Wialon API session.

        :param token: An optional Wialon API token. Default is :confval:`WIALON_TOKEN`.
        :type token: :py:obj:`str` | :py:obj:`None`
        :param sid: An optional Wialon API session id. If provided, the session is continued.
        :type sid: :py:obj:`str` | :py:obj:`None`
        :raises ImproperlyConfigured: If either :confval:`WIALON_TOKEN` or :confval:`WIALON_ADMIN_ID` is not set.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        if not hasattr(settings, "WIALON_TOKEN"):
            raise ImproperlyConfigured("'WIALON_TOKEN' setting is required.")
        if not hasattr(settings, "WIALON_ADMIN_ID"):
            raise ImproperlyConfigured("'WIALON_ADMIN_ID' setting is required.")

        self.wialon_api = Wialon(scheme=scheme, host=host, port=port, sid=sid)
        self.token = token
        self._username = None
        self._gis_sid = None
        self._hw_gp_ip = None
        self._wsdk_version = None
        self._uid = None

    def __enter__(self) -> "WialonSession":
        assert self.token, "Wialon API token was not set"
        self.login(self.token)
        return self

    def __exit__(self, *args, **kwargs) -> None:
        self.logout()

    @property
    def active(self) -> bool:
        """
        Whether or not the Wialon session is currently active.

        :type: :py:obj:`bool`
        :value: :py:obj:`False`
        """
        is_active = False

        try:
            response = self.wialon_api.core_duplicate(**{"restore": 1})
            is_active = bool(response)
        except WialonError as e:
            raise WialonSessionInvalidError(self.id, e)
        finally:
            return is_active

    @property
    def gis_geocode(self) -> str | None:
        """
        Gis geocode URL.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_geocode

    @property
    def gis_render(self) -> str | None:
        """
        Gis rendering URL.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_render

    @property
    def gis_routing(self) -> str | None:
        """
        Gis routing URL.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_routing

    @property
    def gis_search(self) -> str | None:
        """
        Gis search URL.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_search

    @property
    def gis_sid(self) -> str | None:
        """
        Gis session id.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._gis_sid

    @property
    def host(self) -> str | None:
        """
        IP of the client hosting the Wialon session.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._host

    @property
    def hw_gw_ip(self) -> str | None:
        """
        Hardware gateway IP.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._hw_gw_ip

    @property
    def hw_gw_dns(self) -> str | None:
        """
        Hardware gateway domain name, should evaluate to :py:attr:`hw_gw_ip` if present.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._hw_gw_dns

    @property
    def wsdk_version(self) -> str | None:
        """
        The Wialon Source Developer Kit (WSDK) version number of the session.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._wsdk_version

    @property
    def uid(self) -> str | None:
        """
        A Wialon user ID this session is operating as.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`
        """
        return self._uid

    @property
    def username(self) -> str | None:
        """
        A Wialon username the session is operating as.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self._username

    @property
    def id(self) -> str | None:
        """
        Shortcut property for :py:attr:`WialonSession.wialon_api.sid`.

        Returns :py:obj:`None` if the session wasn't logged in.

        :type: :py:obj:`str` | :py:obj:`None`
        :value: :py:obj:`None`

        """
        return self.wialon_api.sid

    @property
    def token(self) -> str:
        """
        A Wialon API token set during :py:meth:`WialonSession.__init__`.

        Default token value is :confval:`WIALON_TOKEN`.

        :type: :py:obj:`str`
        :value: :confval:`WIALON_TOKEN`

        """
        return self._token

    @token.setter
    def token(self, value: str | None = None) -> None:
        self._token = value if value else settings.WIALON_TOKEN

    def duplicate(self, username: str | None = None, continued: bool = False) -> str:
        """
        Duplicates the active Wialon API session.

        :param username: A Wialon user to operate as in the session.
        :type username: :py:obj:`str` | :py:obj:`None`
        :param continue_session: Whether or not the original session id should be valid after duplication.
        :type continue_session: :py:obj:`bool`
        :raises WialonSessionDuplicationError: If the Wialon session was not duplicated.
        :raises AssertionError: If the session was already active.
        :returns: The new session id.
        :rtype: :py:obj:`str`

        """
        try:
            assert self.active, "Cannot duplicate an inactive session."
            response = self.wialon_api.core_duplicate(
                **{"operateAs": username, "continueCurrentSession": continued}
            )
            self._set_login_response(response)
            return response.get("eid")
        except (WialonError, AssertionError) as e:
            raise WialonSessionDuplicationError(self.id, e)

    def login(self, token: str, flags: int = sum([0x1, 0x2, 0x20])) -> str:
        """
        Logs into the Wialon API and starts a new session.

        :param token: An active Wialon API token.
        :type token: :py:obj:`str`
        :param user_id: A user to operate as in the Wialon API session.
        :type user_id: :py:obj:`str` | :py:obj:`None`
        :param flags: A login response flag integer.
        :type flags: :py:obj:`int`
        :raises WialonLoginError: If the login fails.
        :raises AssertionError: If the session was already active.
        :returns: The new session id.
        :rtype: :py:obj:`str`

        """
        try:
            assert not self.active, "Cannot login to an active session."
            response = self.wialon_api.token_login(**{"token": token, "fl": flags})
            self._set_login_response(response)
            return response.get("eid")
        except (WialonError, AssertionError) as e:
            raise WialonLoginError(token, e)

    def logout(self) -> None:
        """
        Logs out of the Wialon API session.

        :raises WialonLogoutError: If the logout fails.
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        response: dict = self.wialon_api.core_logout({})
        if response.get("error") != 0:
            raise WialonLogoutError(str(self.id))

    def _set_login_response(self, login_response: dict) -> None:
        """
        Sets the Wialon API session's attributes based on a login response.

        :param login_response: A response returned from :py:meth:`login` or :py:meth:`duplicate`.
        :type login_response: :py:obj:`dict`
        :returns: Nothing.
        :rtype: :py:obj:`None`

        """
        self.wialon_api.sid = login_response.get("eid")
        self._gis_geocode = login_response.get("gis_geocode")
        self._gis_render = login_response.get("gis_render")
        self._gis_routing = login_response.get("gis_routing")
        self._gis_search = login_response.get("gis_search")
        self._gis_sid = login_response.get("gis_sid")
        self._host = login_response.get("host")
        self._hw_gw_dns = login_response.get("hw_gw_dns")
        self._hw_gw_ip = login_response.get("hw_gw_ip")
        self._uid = login_response.get("user", {}).get("id")
        self._nm = login_response.get("user", {}).get("nm")
        self._username = login_response.get("au")
        self._video_service_url = login_response.get("video_service_url")
        self._wsdk_version = login_response.get("wsdk_version")


def main() -> None:
    session = WialonSession()
    session.login(token=settings.WIALON_TOKEN)
    session.duplicate(username="chrissyron@gmail.com", continued=False)
    session.logout()
    return


if __name__ == "__main__":
    main()
