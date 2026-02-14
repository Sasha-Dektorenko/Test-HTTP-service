from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse
import logging
from core.exceptions import BaseAppException
from sqlalchemy.exc import SQLAlchemyError


logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def register_exception_handlers(app: FastAPI):
    @app.exception_handler(BaseAppException)
    async def base_app_exception_handler(request: Request, exc: BaseAppException):
        logger.error(f"BaseAppException: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )

    @app.exception_handler(SQLAlchemyError)
    async def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
        logger.error(f"SQLAlchemyError: {str(exc)}")
        return JSONResponse(
            status_code=500,
            content={"detail": "Database error occurred"}
        )
