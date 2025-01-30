from terminusgps.wialon.maps.renderer import WialonMapRenderer


class WialonMapLayerBase:
    def __init__(self, renderer: WialonMapRenderer, name: str) -> None:
        self.renderer = renderer
        self.name = name
        self.bounds = dict()

    def __str__(self) -> str:
        return self.name

    def delete_layer(self) -> None:
        self.renderer.session.wialon_api.render_remove_layer(**{"layerName": self.name})

    def create_layer(self, data: list[dict], flags: int = 0x1) -> None:
        raise NotImplementedError("Subclasses must implement this method")


class WialonMapLayerGeofence(WialonMapLayerBase):
    def create_layer(self, data: list[dict], flags: int = 0x1) -> None:
        response = self.renderer.session.wialon_api.render_create_zones_layer(
            **{"layerName": self.name, "flags": flags, "zones": data}
        )
        self.bounds = {
            "min_lat": response.get("bounds")[0],
            "min_lon": response.get("bounds")[1],
            "max_lat": response.get("bounds")[2],
            "max_lon": response.get("bounds")[3],
        }


class WialonMapLayerPoi(WialonMapLayerBase):
    def create_layer(self, data: list[dict], flags: int = 0x1) -> None:
        response = self.renderer.session.wialon_api.render_create_poi_layer(
            **{"layerName": self.name, "flags": flags, "pois": data}
        )
        self.bounds = {
            "min_lat": response.get("bounds")[0],
            "min_lon": response.get("bounds")[1],
            "max_lat": response.get("bounds")[2],
            "max_lon": response.get("bounds")[3],
        }


class WialonMapLayerTrack(WialonMapLayerBase):
    def __init__(self, **kwargs) -> None:
        self.units = []
        return super().__init__(**kwargs)
