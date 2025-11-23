from fastapi import FastAPI

from app.adapters.router import user, dialog
from app.adapters.router.common import router as common_routers
from app.config import settings
from app.infrastructure.db.postgres import init_db


def create_app() -> FastAPI:
    app = FastAPI(title=getattr(settings, "RUN366", "run366"))
    app.include_router(common_routers, prefix="/api")
    return app


app = create_app()


def main():
    init_db()


if __name__ == "__main__":
    main()
