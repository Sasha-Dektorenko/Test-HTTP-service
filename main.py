import pandas as pd
from fastapi import FastAPI
from sqlalchemy import text
from database.db import Base, engine, async_session
from dotenv import load_dotenv
import logging
from contextlib import asynccontextmanager
import asyncio
from models import Plan, User, Credit, Dictionary, Payment
from core.seed import Seeder
from routers.users import user_router
from routers.plans import plan_router
from routers.performance import performance_router
from core import register_exception_handlers


logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

load_dotenv()


SEED_DATA_CONFIG = [
    (Dictionary, "static/dictionary.csv", []),
    (Plan, "static/plans.csv", ["period"]),
    (User, "static/users.csv", ["registration_date"]),
    (Credit, "static/credits.csv", ["issuance_date", "return_date", "actual_return_date"]),
    (Payment, "static/payments.csv", ["payment_date"]),
]

@asynccontextmanager
async def lifespan(app: FastAPI):
    max_retries = 10
    retry_delay = 2
    for attempt in range(1, max_retries + 1):
        try:
            async with engine.begin() as conn:
                print(f"Моделі, які бачить SQLAlchemy: {Base.metadata.tables.keys()}")
                await conn.run_sync(Base.metadata.create_all)
            logger.info("Database tables created successfully")
            break
        except Exception as e:
            logger.warning(f"Database connection attempt {attempt} failed: {e}")
            if attempt == max_retries:
                logger.error("Could not connect to DB. Exiting.")
                raise e
            await asyncio.sleep(retry_delay)
    
    async with async_session() as session:
        seeder = Seeder(session)
        try:
            for model, path, date_cols in SEED_DATA_CONFIG:
                await seeder.load_data(
                    model=model, 
                    csv_path=path, 
                    date_columns=date_cols
                )
            
            
            await session.commit()
            logger.info("Database seeding completed successfully.")
            
        except Exception as e:
            await session.rollback()
            logger.info(f"An error occured during data seeding: {e}")
        finally:
            pass
        
        

    yield

app = FastAPI(lifespan=lifespan)
app.include_router(user_router)
app.include_router(plan_router)
app.include_router(performance_router)
register_exception_handlers(app)
