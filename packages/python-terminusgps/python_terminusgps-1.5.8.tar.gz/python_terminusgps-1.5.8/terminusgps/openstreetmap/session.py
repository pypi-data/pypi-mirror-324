import os
import requests
from urllib.parse import urlencode


class OpenStreetMapSession:
    def __init__(self, client_id: str, redirect_uri: str, scopes: list[str]) -> None:
        self.client_id = client_id
        self.redirect_uri = redirect_uri
        self.scopes = scopes
        self.base_token_url = "https://master.apis.dev.openstreetmap.org/oauth2/token?"
        self.base_auth_url = (
            "https://master.apis.dev.openstreetmap.org/oauth2/authorize?"
        )

    def generate_auth_url(self) -> str:
        params = urlencode(
            {
                "response_type": "code",
                "client_id": self.client_id,
                "redirect_uri": self.redirect_uri,
                "scope": "%20".join(self.scopes),
            }
        )
        return self.base_auth_url + params

    def get_token(self, auth_code: str, client_secret: str) -> str | None:
        params = urlencode(
            {
                "grant_type": "authorization_code",
                "code": auth_code,
                "redirect_uri": self.redirect_uri,
                "client_id": self.client_id,
                "client_secret": client_secret,
            }
        )
        response = requests.post(self.base_token_url + params).json()
        self.scopes = [response.get("scope").split(" ")]
        return response.get("access_token")


def main() -> None:
    scopes = os.getenv("OSM_SCOPES").split(" ")
    session = OpenStreetMapSession(
        client_id=os.getenv("OSM_CLIENT_ID"),
        redirect_uri=os.getenv("OSM_REDIRECT_URI"),
        scopes=scopes,
    )
    print(f"{session.generate_auth_url() = }")
    return


if __name__ == "__main__":
    main()
