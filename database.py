from os import getenv

from sqlalchemy import select
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from dotenv import load_dotenv

load_dotenv()

async_engine = create_async_engine(getenv("URL_DATABASE"))
async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass


class Books(Base):
    __tablename__ = "books"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str]


async def create_tables():
    async with async_engine.begin() as engine:
        await engine.run_sync(Base.metadata.drop_all)
        await engine.run_sync(Base.metadata.create_all)


async def check_id(id: int):
    async with async_session() as session:
        result = await session.get(Books, id)
        if result is None:
            return False
        else:
            return True


class CreateReadUpdateDelete:
    async def create(self, name):
        async with async_session.begin() as session:
            book = Books(name=name)

            session.add(book)

    async def read(self):
        async with async_session() as session:
            query = select(Books)
            result = await session.execute(query)

            return result.scalars().all()

    async def update(self, book_id, new_name):
        async with async_session.begin() as session:
            book = await session.get(Books, book_id)
            if book is None:
                return None
            else:
                book.name = new_name
                return True

    async def delete(self, book_id):
        async with async_session.begin() as session:
            book = await session.get(Books, book_id)
            if book is None:
                return None
            else:
                await session.delete(book)
                return True
