import asyncio
from typing import Annotated
from fastapi import FastAPI, Depends
from fastapi.responses import HTMLResponse
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from infrastructure.api.metadata import tags_metadata
from infrastructure.api.routes.user import user_route
from infrastructure.api.routes.auth import auth_route
from infrastructure.api.utils.docs import get_openapi_json
from infrastructure.api.utils.docs import get_openapi_docs
from infrastructure.api.utils.docs import get_openapi_redoc
from infrastructure.api.utils.auth import basic_http_log_in
from infrastructure.database.database import create_tables_if_not_exists


asyncio.gather(create_tables_if_not_exists())

app = FastAPI(
    title="FastAPI",
    version="0.1.0",
    docs_url=None,
    redoc_url=None,
    openapi_url=None,
    openapi_tags=tags_metadata
)


origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_route)
app.include_router(user_route, prefix="/users")


needBasicAuth=Annotated[str, Depends(basic_http_log_in)]

@app.get("/openapi.json", response_class=JSONResponse, include_in_schema=False)
async def get_json(
            user: needBasicAuth
        )->JSONResponse:
    return await get_openapi_json(
        app=app
    )


@app.get("/docs", include_in_schema=False, response_class=HTMLResponse)
async def get_docs(
            user: needBasicAuth
        )->HTMLResponse:
    return await get_openapi_docs()


@app.get("/redoc", response_class=HTMLResponse, include_in_schema=False)
async def get_redoc(
            user: needBasicAuth
        )->HTMLResponse:
    return await get_openapi_redoc()
