from django.conf import ImproperlyConfigured, settings

from terminusgps.wialon.session import WialonSession


class WialonMapRenderer:
    def __init__(
        self, sid: str | None = None, gis_host: str = "hst-api.wialon.com"
    ) -> None:
        if not hasattr(settings, "WIALON_TOKEN"):
            raise ImproperlyConfigured("'WIALON_TOKEN' setting is required.")

        self.host = gis_host
        self.layers = []
        self.session = WialonSession(sid=sid)

    @property
    def total_layers(self) -> int:
        return len(self.layers)

    def get_events(self):
        return self.session.wialon_api.avl_evts()

    def toggle_layer(self, name: str, enabled: bool = True) -> None:
        self.session.wialon_api.render_enable_layer(
            **{"layerName": name, "enable": enabled}
        )

    def delete_all_layers(self) -> None:
        self.session.wialon_api.render_remove_all_layers({})
        self.layers = []

    def get_tiles_url(self, x: int, y: int, z: int) -> str:
        MIN_ZOOM, MAX_ZOOM = 2, 17
        z = min(max(z, MIN_ZOOM), MAX_ZOOM)
        return f"http://{self.host}/avl_render/{x}_{y}_{z}/{self.session.id}.png"

    def update_locale(
        self,
        tz: int,
        lang: str = "en",
        flags: int = 1,
        date_fmt: str = "%m-%E-%Y %H:%M:%S",
        density: int = 256 * 256,
    ) -> None:
        """
        Updates the renderer locale.


        Date Format:

        +-----------+------------------------------------------------------------------------+
        | Parameter | Description                                                            |
        +===========+========================================================================+
        | ``%H``    | The hour of the day with leading zero if required ("00" to "23")       |
        +-----------+------------------------------------------------------------------------+
        | ``%B``    | The full month name ("January" to "December")                          |
        +-----------+------------------------------------------------------------------------+
        | ``%b``    | Abbreviated month name ("Jan" to "Dec")                                |
        +-----------+------------------------------------------------------------------------+
        | ``%m``    | The month of the year with leading zero if required ("01" to "12")     |
        +-----------+------------------------------------------------------------------------+
        | ``%l``    | The month of the year between 1-12 ("1" to "12")                       |
        +-----------+------------------------------------------------------------------------+
        | ``%P``    | Format Persian calendar ("01 Farvardin 1392 00:00:00")                 |
        +-----------+------------------------------------------------------------------------+
        | ``%A``    | The full day name ("Monday" to "Sunday")                               |
        +-----------+------------------------------------------------------------------------+
        | ``%a``    | Abbreviated day name ("Mon" to "Sun")                                  |
        +-----------+------------------------------------------------------------------------+
        | ``%E``    | The day of the month with a leading zero if required ("01" to "31")    |
        +-----------+------------------------------------------------------------------------+
        | ``%e``    | The day of the month between 1 and 31 ("1" to "31")                    |
        +-----------+------------------------------------------------------------------------+
        | ``%I``    | The hour of the day with leading zero if required ("01" to "12")       |
        +-----------+------------------------------------------------------------------------+
        | ``%M``    | The minute of the hour with leading zero if required ("00" to "59")    |
        +-----------+------------------------------------------------------------------------+
        | ``%S``    | The seconds of the minute with leading zero if required ("00" to "59") |
        +-----------+------------------------------------------------------------------------+
        | ``%p``    | Displays the A.M./P.M. designator ("AM" or "PM")                       |
        +-----------+------------------------------------------------------------------------+
        | ``%Y``    | The full four digit year ("1999" or "2000")                            |
        +-----------+------------------------------------------------------------------------+
        | ``%y``    | The year as a two digit number ("99" or "00")                          |
        +-----------+------------------------------------------------------------------------+

        """
        self.session.wialon_api.render_set_locale(
            **{
                "tzOffset": tz,
                "language": lang,
                "flags": flags,
                "formatDate": date_fmt,
                "density": density,
            }
        )


def main() -> None:
    from terminusgps.wialon.maps.layers import WialonMapLayerPoi

    with WialonSession() as session:
        renderer = WialonMapRenderer(session.id)
        layer = WialonMapLayerPoi(renderer, "terminusgps_office")
    return


if __name__ == "__main__":
    main()
