# src/core/exceptions.py

from fastapi import HTTPException, status


class BaseHTTPException(HTTPException):
    """Базовый класс для всех кастомных HTTP исключений."""

    def __init__(self, status_code: int, detail: str, headers: dict | None = None):
        super().__init__(status_code=status_code, detail=detail, headers=headers)


# -------------------- 400 Bad Request --------------------


class UserAlreadyExistsException(BaseHTTPException):
    """Вызывается, когда пользователь с указанным email уже существует."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Пользователь с таким email уже существует",
        )


class InvalidCurrentPasswordException(BaseHTTPException):
    """Вызывается, когда указан неверный текущий пароль."""

    def __init__(self):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Указан неверный текущий пароль",
        )


# -------------------- 401 Unauthorized --------------------


class UnauthorizedException(BaseHTTPException):
    """Базовый класс для всех 401 ошибок."""

    def __init__(self, detail: str):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )


class InvalidEmailOrPasswordException(UnauthorizedException):
    """Неверный email или пароль."""

    def __init__(self):
        super().__init__("Неверный email или пароль. Проверьте введенные данные")


class InvalidCredentialsException(UnauthorizedException):
    """Невозможно проверить учетные данные."""

    def __init__(self):
        super().__init__("Не удалось проверить учетные данные. Авторизация отклонена")


class InvalidTokenException(UnauthorizedException):
    """Недействительный токен доступа."""

    def __init__(self):
        super().__init__("Недействительный токен доступа")


class InvalidTokenPayloadException(UnauthorizedException):
    """Некорректная структура токена (payload)."""

    def __init__(self):
        super().__init__("Некорректная структура токена (payload)")


class AccessTokenMissingException(UnauthorizedException):
    """Отсутствует токен доступа."""

    def __init__(self):
        super().__init__("Отсутствует токен доступа. Авторизуйтесь для продолжения")


# -------------------- 403 Forbidden --------------------


class ForbiddenException(BaseHTTPException):
    """Ошибка доступа: Forbidden."""

    def __init__(self, detail: str = "Доступ запрещен"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail,
        )


# -------------------- 404 Not Found --------------------


class NotFoundException(BaseHTTPException):
    """Ошибка ресурса: Not Found."""

    def __init__(self, entity: str = "Ресурс"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"{entity} не найден",
        )
