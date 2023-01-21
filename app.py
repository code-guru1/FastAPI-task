from typing import Dict

import sentry_sdk
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from configurations.config import settings
from routes.candidates import candidate_router
from routes.users import user_router
from utils.constants import APP_DESCRIPTION, APP_TITLE
from utils.openapi_tags_metadata import tags_metadata
from views.users import verify_user

app = FastAPI(
    title=APP_TITLE,
    description=APP_DESCRIPTION,
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_tags=tags_metadata,
)

sentry_sdk.init(
    dsn=settings.SENTRY_DSN,
    traces_sample_rate=0.5,
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/ping", tags=["Health"])
async def health_check() -> Dict:
    """
    Health Check Endpoint.

    Returns:
        Dict
    """
    return {"message": "pong"}


app.include_router(user_router)
app.include_router(candidate_router, dependencies=[Depends(verify_user)])
