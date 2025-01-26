from sqlalchemy import BigInteger, Float, String
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import AsyncAttrs, async_sessionmaker, create_async_engine

engine = create_async_engine(url='sqlite+aiosqlite:///db.sqlite3')

async_session = async_sessionmaker(engine)

class Base(AsyncAttrs, DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'

    id: Mapped[int]=mapped_column(primary_key=True)
    tg_id = mapped_column(BigInteger)

class Location(Base):
    __tablename__ = 'locations'

    id: Mapped[int]=mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    title: Mapped[str]=mapped_column(String)
    latitude: Mapped[float]=mapped_column(Float)
    longitude: Mapped[float]=mapped_column(Float)

class Card(Base):
    __tablename__ = 'cards'

    id: Mapped[int]=mapped_column(primary_key=True)
    user_id = mapped_column(BigInteger)
    cardname: Mapped[str]=mapped_column(String)
    cardnumber: Mapped[str]=mapped_column(String)
    cardowner: Mapped[str]=mapped_column(String)

async def async_main():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)