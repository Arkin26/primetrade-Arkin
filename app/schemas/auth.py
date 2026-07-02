from pydantic import BaseModel, ConfigDict


class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"


class RegisterResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    user: "UserResponse"
    access_token: str
    token_type: str = "bearer"


from app.schemas.user import UserResponse  # noqa: E402

RegisterResponse.model_rebuild()
