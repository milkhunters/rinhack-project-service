import time

import jwt
from fastapi import Request
from pydantic import ValidationError

from src.config import Config
from src.models import schemas


class JWTManager:
    ALGORITHM = "HS256"

    COOKIE_PATH = "/api"
    COOKIE_DOMAIN = None
    COOKIE_ACCESS_KEY = "access_token"
    COOKIE_REFRESH_KEY = "refresh_token"

    def __init__(self, config: Config):
        self._config = config

        self.JWT_ACCESS_SECRET_KEY = config.JWT.ACCESS_SECRET_KEY
        self.JWT_REFRESH_SECRET_KEY = config.JWT.REFRESH_SECRET_KEY

    def is_valid_refresh_token(self, token: str | None) -> bool:
        """
        Проверяет refresh-токен на валидность
        :param token:
        :return:
        """
        if not token:
            return False

        return self._is_valid_jwt(token, self.JWT_REFRESH_SECRET_KEY)

    def is_valid_access_token(self, token: str | None) -> bool:
        """
        Проверяет access-токен на валидность
        :param token:
        :return:
        """
        if not token:
            return False

        return self._is_valid_jwt(token, self.JWT_ACCESS_SECRET_KEY)

    def decode_access_token(self, token: str) -> schemas.TokenPayload:
        """
        Декодирует access-токен (получает payload)
        :param token:
        :return:
        """
        return self._decode_jwt(token, self.JWT_ACCESS_SECRET_KEY)

    def decode_refresh_token(self, token: str) -> schemas.TokenPayload:
        """
        Декодирует refresh-токен (получает payload)
        :param token:
        :return:
        """
        return self._decode_jwt(token, self.JWT_REFRESH_SECRET_KEY)

    def get_jwt_cookie(self, req_obj: Request) -> schemas.Tokens:
        """
        Получает из кук access и refresh-токены
        :param req_obj:
        :return: None или Tokens
        """
        access_token = req_obj.cookies.get(self.COOKIE_ACCESS_KEY)
        refresh_token = req_obj.cookies.get(self.COOKIE_REFRESH_KEY)
        return schemas.Tokens(access_token=access_token, refresh_token=refresh_token)

    def _is_valid_jwt(self, token: str, secret_key: str) -> bool:
        try:
            data = jwt.decode(token, secret_key, algorithms=self.ALGORITHM)
            schemas.TokenPayload.model_validate(data)
        except (
                jwt.exceptions.InvalidTokenError,
                jwt.exceptions.ExpiredSignatureError,
                jwt.exceptions.DecodeError,
                ValidationError
        ):
            return False
        return True

    def _generate_token(self, exp: int, secret_key: str, **kwargs) -> str:
        """
        param: exp: время жизни токена
        param: secret_key: секретный ключ
        param: kwargs: параметры для payload
        :return: токен
        """
        payload = schemas.TokenPayload(**kwargs, exp=int(time.time() + exp))
        return jwt.encode(payload.model_dump(), secret_key, algorithm=self.ALGORITHM)

    def _decode_jwt(self, token: str, secret_key: str) -> schemas.TokenPayload:
        """
        param: token: токен
        param: secret_key: секретный ключ
        :return: payload
        """
        return schemas.TokenPayload.model_validate(jwt.decode(
            token,
            secret_key,
            algorithms=self.ALGORITHM,
            options={"verify_signature": False}
        ))
