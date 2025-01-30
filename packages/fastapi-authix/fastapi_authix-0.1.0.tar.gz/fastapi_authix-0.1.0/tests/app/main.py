from dataclasses import dataclass

from fastapi import FastAPI, Depends
from starlette.responses import Response, JSONResponse
from starlette.requests import Request
from pydantic import BaseModel

from fastapi_authix.vault import Vault

app = FastAPI()
vault = Vault(use_header=True)


@dataclass(frozen=True)
class TestData:
    a: int = 0


class TestModel(BaseModel):
    a: int = 0


@app.get("/login")
async def login() -> JSONResponse:
    r = JSONResponse(content={"asd": True})
    vault.set_access_token(r, payload={"asd": True})
    return r

@app.get("/logout")
async def logout(request: Request) -> JSONResponse:
    vault.disable_access_token(vault.extract_access_token(request))
    r = JSONResponse(content={"ok": True})
    vault.remove_access_token(r)
    return r

@app.get("/test")
async def show_test_page(user: TestData = Depends(vault.require_data)) -> Response:
    print(user)
    return Response(content="hello world!")
