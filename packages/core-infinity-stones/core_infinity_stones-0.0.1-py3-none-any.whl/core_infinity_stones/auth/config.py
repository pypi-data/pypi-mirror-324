from pydantic import BaseModel


class AuthConfig(BaseModel):
    auth_service_base_url: str
    authenticate_user_endpoint_path: str
