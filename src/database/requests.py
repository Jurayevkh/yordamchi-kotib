from database.models import async_session
from database.models import User, Location, Card
from sqlalchemy import select

async def set_user(tg_id):
    async with async_session() as session:
        user=await session.scalar(select(User).where(User.tg_id == tg_id))

        if not user:
            session.add(User(tg_id=tg_id))
            await session.commit()


async def set_card(user_id,card_name, card_number, card_owner):
    async with async_session() as session:
        card=await session.scalar(select(Card).where((Card.user_id==user_id)&(Card.cardname == card_name) & (Card.cardnumber==card_number) & (Card.cardowner==card_owner)))

    if not card:
        new_user=session.add(Card(user_id=user_id,cardname=card_name,cardnumber=card_number,cardowner=card_owner))
        await session.commit()


async def set_location(user_id, title, latitude, longitude):
    async with async_session() as session:
        session.add(Location(user_id=user_id,title=title,latitude=latitude,longitude=longitude))
        await session.commit()


async def get_locationsByUserID(user_id):
    async with async_session() as session:
        result = await session.execute(select(Location).where(Location.user_id == user_id))
        locations = result.scalars().all()
        return locations

async def get_cardsByUserID(user_id):
    async with async_session() as session:
        result = await session.execute(select(Card).where(Card.user_id == user_id))
        cards = result.scalars().all()
        return cards

        # return await session.scalars(select(Location).where(Location.user_id == user_id))

    # id: Mapped[int] = mapped_column(primary_key=True)
    # user_id = mapped_column(BigInteger)
    # title: Mapped[str] = mapped_column(String)
    # latitude: Mapped[float] = mapped_column(Float)
    # longitude: Mapped[float] = mapped_column(Float)