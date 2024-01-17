from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession

from config import PG_DSN


engine = create_async_engine(PG_DSN)
Session = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

