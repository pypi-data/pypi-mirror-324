import os


from .exceptions import RhoStoreError


class Config:
    CLIENT_ID = "python-sdk"

    default_api_url = "https://rho-api-kegbmbvpna-ew.a.run.app"
    default_client_url = "https://rho.store"

    def __init__(self):
        self.CLIENT_URL: str = os.getenv("RHO_CLIENT_URL", default=self.default_client_url)
        self.API_URL: str = os.getenv("RHO_API_URL", default=self.default_api_url)
        self.GRAPHQL_URL = f"{self.API_URL}/graphql"

        self._validate()

    @property
    def uptime_check_url(self) -> str:
        return f"{self.API_URL}/health/up"

    def _validate(self) -> None:
        if not self.API_URL:
            raise RhoStoreError("Invalid API url")

        if not self.CLIENT_URL:
            raise RhoStoreError("Invalid client url")


def init_config() -> Config:
    # load_dotenv()
    return Config()
