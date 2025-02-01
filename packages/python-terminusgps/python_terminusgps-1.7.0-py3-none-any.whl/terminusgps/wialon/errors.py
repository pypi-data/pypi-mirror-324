from wialon.api import WialonError


class WialonBaseError(Exception):
    def __init__(
        self, message: str, wialon_err: WialonError | AssertionError | None = None
    ) -> None:
        self.wialon_err = wialon_err
        return super().__init__(message)


class WialonLoginError(WialonBaseError):
    def __init__(
        self, token: str | None, wialon_err: WialonError | AssertionError | None = None
    ) -> None:
        message = f"Failed to login to the Wialon API using token: '{token}'\n"
        if wialon_err:
            message += str(wialon_err)
        return super().__init__(message, wialon_err)


class WialonSessionDuplicationError(WialonBaseError):
    def __init__(
        self,
        session_id: str | None,
        wialon_err: WialonError | AssertionError | None = None,
    ) -> None:
        message = f"Failed to duplicate the Wialon session: '#{session_id}'\n"
        if wialon_err:
            message += str(wialon_err)
        return super().__init__(message, wialon_err)


class WialonLogoutError(WialonBaseError):
    def __init__(
        self, session_id: str, wialon_err: WialonError | AssertionError | None = None
    ) -> None:
        message = f"Failed to logout of the Wialon API session: '{session_id}'\n"
        if wialon_err:
            message += str(wialon_err)
        return super().__init__(message, wialon_err)


class WialonSessionInvalidError(WialonBaseError):
    def __init__(
        self,
        session_id: str | None,
        wialon_err: WialonError | AssertionError | None = None,
    ) -> None:
        message = f"The session was invalid/expired: '{session_id}'\n"
        if wialon_err:
            message += str(wialon_err)
        return super().__init__(message, wialon_err)
