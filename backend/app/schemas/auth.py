from pydantic import BaseModel


class LoginRequest(BaseModel):
    vk_user_id: str
    username: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"