from typing import Any, Optional

from core_infinity_stones.core.local_cache import AbstractLocalCache

from .errors import AuthHttpException

from .schemas import S2sAuthResponse, S2sToken, UserAuthResponse
from core_infinity_stones.network_router import HttpRequest, APIAuth, HttpMethod, NetworkRouter
from .config import AuthConfig
import core_infinity_stones.auth.constants as constants
import logging

logger = logging.getLogger()

class Authenticator:
    def __init__(self, config: AuthConfig, network_router: NetworkRouter = NetworkRouter()):
        self._config = config
        self._network_router = network_router

    async def authenticate_user_request(
        self, request_headers: dict[str, str], s2s_access_token: str
    ) -> UserAuthResponse:
        user_access_token = self._extract_bearer_token(request_headers)

        if not user_access_token:
            raise AuthHttpException(status_code=401, detail="Missing user access token")

        request = HttpRequest[Any](
            method=HttpMethod.POST,
            base_url=self._config.auth_service_base_url,
            path=self._config.authenticate_user_endpoint_path,
            headers=APIAuth.bearer(s2s_access_token),
            body={"bearer_token": user_access_token},
        )

        try:
            response = await self._network_router.execute_http_request(request)

            if response.status_code != 200:
                raise AuthHttpException(status_code=response.status_code, detail=response.body)

        except Exception as e:
            logger.error(f"Error while authenticating user {e}")
            raise AuthHttpException(status_code=500, detail="Error while authenticating user")

        return UserAuthResponse(**response.body)

    async def get_s2s_token(
        self,
        client_id: str,
        client_secret: str,
        local_cache: AbstractLocalCache
    ) -> S2sToken:
        cache_key = constants.S2S_TOKEN_CACHE_KEY

        cached_s2s_token = local_cache.get(cache_key)

        if cached_s2s_token:
            return S2sToken.model_validate_json(cached_s2s_token)

        new_s2s_token = await self._generate_new_s2s_token(client_id, client_secret)

        local_cache.set(cache_key, new_s2s_token.model_dump_json())

        return new_s2s_token

    async def authenticate_s2s_request(
        self,
        request_headers: dict[str, str],
        s2s_token: str,
        scope: str
    ) -> S2sAuthResponse:
        to_be_validated_s2s_access_token = self._extract_bearer_token(request_headers)

        if not to_be_validated_s2s_access_token:
            raise AuthHttpException(status_code=401, detail="Missing s2s access token")

        request = HttpRequest[Any](
            method=HttpMethod.POST,
            base_url=self._config.auth_service_base_url,
            path=self._config.authenticate_s2s_token_endpoint_path,
            headers=APIAuth.bearer(s2s_token),
            body={
                "scope": scope,
                "bearer_token": to_be_validated_s2s_access_token
            }
        )

        try:
            response = await self._network_router.execute_http_request(request)

            if response.status_code != 200:
                raise AuthHttpException(status_code=response.status_code, detail=response.body)

        except Exception as e:
            logger.error(f"Error while authenticating s2s token {e}")
            raise AuthHttpException(status_code=500, detail="Error while authenticating s2s token")

        return S2sAuthResponse(**response.body)

    # MARK: Convenience methods

    async def _generate_new_s2s_token(self, client_id: str, client_secret: str) -> S2sToken:
        request = HttpRequest[Any](
            method=HttpMethod.POST,
            base_url=self._config.auth_service_base_url,
            path=self._config.generate_s2s_token_endpoint_path,
            headers=APIAuth.basic(client_id, client_secret),
        )

        try:
            response = await self._network_router.execute_http_request(request)

            if response.status_code != 200:
                raise AuthHttpException(status_code=response.status_code, detail=response.body)

        except Exception as e:
            logger.error(f"Error while generating s2s token {e}")
            raise AuthHttpException(status_code=500, detail="Error while generating s2s token")

        return S2sToken(**response.body)

    def _extract_bearer_token(self, request_headers: dict[str, str]) -> Optional[str]:
        auth_header_key = "Authorization"
        authorization = request_headers.get(auth_header_key)

        if not authorization:
            return None

        split_auth_header = authorization.split(" ")

        if len(split_auth_header) < 2:
            return None

        token = split_auth_header[1]

        return token
