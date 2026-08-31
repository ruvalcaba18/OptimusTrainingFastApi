from fastapi import status

from app.core.exceptions import (
    BadRequestError,
    ConflictError,
    ForbiddenError,
    InternalServerError,
    NotFoundError,
)


def test_domain_exceptions_structure():
    err = NotFoundError("Usuario no encontrado")
    assert err.status_code == status.HTTP_404_NOT_FOUND
    assert err.code == "NOT_FOUND"
    assert err.message == "Usuario no encontrado"

    bad = BadRequestError("Parámetro inválido")
    assert bad.status_code == status.HTTP_400_BAD_REQUEST
    assert bad.code == "BAD_REQUEST"

    forbidden = ForbiddenError("Sin permiso")
    assert forbidden.status_code == status.HTTP_403_FORBIDDEN
    assert forbidden.code == "FORBIDDEN"

    conflict = ConflictError("Recurso ya existe")
    assert conflict.status_code == status.HTTP_409_CONFLICT
    assert conflict.code == "CONFLICT"

    internal = InternalServerError()
    assert internal.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
    assert internal.code == "INTERNAL_SERVER_ERROR"


def test_api_returns_formatted_error_for_not_found(client, test_user):
    login = client.post(
        "/api/v1/auth/login",
        json={"email": "testuser@optimus.com", "password": "Passw0rd!"},
    )
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    resp = client.get("/api/v1/users/999999", headers=headers)
    assert resp.status_code == status.HTTP_404_NOT_FOUND
    json_data = resp.json()
    assert "error" in json_data
    assert json_data["error"]["code"] == "NOT_FOUND"
    assert json_data["error"]["message"] == "Usuario no encontrado"


def test_api_returns_formatted_error_for_invalid_login(client):
    resp = client.post(
        "/api/v1/auth/login",
        json={"email": "wrong@optimus.com", "password": "wrongpassword"},
    )
    assert resp.status_code == status.HTTP_401_UNAUTHORIZED
    json_data = resp.json()
    assert "error" in json_data
    assert json_data["error"]["code"] == "UNAUTHORIZED"
    assert json_data["error"]["message"] == "Correo o contraseña incorrectos"
