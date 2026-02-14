from core.config import DB_URL
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base

engine = create_async_engine(DB_URL, echo=True)

async_session = async_sessionmaker(bind=engine, autoflush=False, autocommit=False)

Base = declarative_base()

async def get_session():
    db_session = async_session()
    try:
        yield db_session
    except Exception as e:
        await db_session.rollback()
        raise e 
    finally:
        await db_session.close()