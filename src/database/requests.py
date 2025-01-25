from database.models import async_session
from database.models import User, Location
from sqlalchemy import select

async def set_user(tg_id):
    async with async_session() as session:
        user=await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_location(user_id, title, latitude, longitude):
    async with async_session() as session:
        session.add(Location(user_id=user_id,title=title,latitude=latitude,longitude=longitude))
        await session.commit()

async def get_locationsByUserID(user_id):
    async with async_session() as session:
        return await session.scalars(select(Location).where(Location.user_id == user_id))

    # id: Mapped[int] = mapped_column(primary_key=True)
    # user_id = mapped_column(BigInteger)
    # title: Mapped[str] = mapped_column(String)
    # latitude: Mapped[float] = mapped_column(Float)
    # longitude: Mapped[float] = mapped_column(Float)