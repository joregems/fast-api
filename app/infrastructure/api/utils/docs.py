from fastapi import FastAPI
from fastapi.openapi.docs import get_swagger_ui_html
from fastapi.openapi.docs import get_redoc_html
from fastapi.responses import JSONResponse
from fastapi.responses import HTMLResponse

async def get_openapi_json(
    app: FastAPI,
    ) -> JSONResponse:
    from fastapi.openapi.utils import get_openapi
    openapi_schema = get_openapi(
        title="SERVICE TITLE",
        version="1.0.0",
        description="API documentation",
        routes=app.routes,
    )
    return JSONResponse(openapi_schema)


async def get_openapi_docs(
        ) -> HTMLResponse:
    return get_swagger_ui_html(openapi_url="/openapi.json", title="docs")


async def get_openapi_redoc(
        ) -> HTMLResponse:
    return get_redoc_html(openapi_url="/openapi.json", title="redoc")

