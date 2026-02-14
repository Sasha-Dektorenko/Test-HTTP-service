from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession 
from models import User, Credit, Dictionary, Payment, Plan
import pandas as pd
from database.uow import get_uow   
import logging

logger = logging.getLogger(__name__) 

class Seeder:
    def __init__(self, session: AsyncSession):
        self.session = session
        
    async def table_has_data(self, model):
        result = await self.session.execute(select(func.count()).select_from(model))
        count = result.scalar() or 0
        return count > 0
        
    async def load_data(self, model, csv_path, date_columns=None):
        if await self.table_has_data(model):
            print(f"{model.__tablename__} already has data. Skipping seeding.")
            return
        
        df = pd.read_csv(csv_path, sep='\t')
        if "id" in df.columns:
            df = df.drop(columns=["id"])
            
        if date_columns:
            for col in date_columns:
                df[col] = pd.to_datetime(df[col], dayfirst=True, errors='coerce')
        
            
        objects = [
            model(**{str(k): (None if pd.isna(v) else v) for k, v in row.items()}) 
            for row in df.to_dict('records')
        ]
        
        self.session.add_all(objects)
        await self.session.flush()
        logger.info(f"Seeded {len(objects)} records into {model.__tablename__}")
        