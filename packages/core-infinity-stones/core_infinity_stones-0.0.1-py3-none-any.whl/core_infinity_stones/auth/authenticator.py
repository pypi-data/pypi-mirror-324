from typing import Any

from .errors import AuthHttpException

from .user_auth_schemas import UserAuthResponse
from core_infinity_stones.network_router import HttpRequest, APIAuth, HttpMethod, NetworkRouter
from .config import AuthConfig
import logging

logger = logging.getLogger()

class Authenticator:
    def __init__(self, config: AuthConfig, network_router: NetworkRouter = NetworkRouter()):
        self._config = config
        self._network_router = network_router


    async def get_user_details(self, user_access_token: str, s2s_access_token: str) -> UserAuthResponse:
        request = HttpRequest[Any](
            method=HttpMethod.POST,
            base_url=self._config.auth_service_base_url,
            path=self._config.authenticate_user_endpoint_path,
            headers=APIAuth.bearer(s2s_access_token),
            body={"bearer_token": user_access_token},
        )

        print(request)

        try:
            response = await self._network_router.execute_http_request(request)

            if response.status_code != 200:
                raise AuthHttpException(status_code=401, detail=response.body)

        except Exception as e:
            logger.error(f"Error while authenticating user {e}")
            raise AuthHttpException(status_code=401, detail="Error while authenticating user")

        return UserAuthResponse(**response.body)