import abc
from _typeshed import Incomplete
from sqlalchemy.ext.asyncio import AsyncEngine as AsyncEngine, AsyncSession as AsyncSession, async_sessionmaker

logger: Incomplete

class BaseSaConnect(abc.ABC, metaclass=abc.ABCMeta):
    engine: AsyncEngine
    session_maker: async_sessionmaker[AsyncSession]
    def __init__(self) -> None: ...
    @abc.abstractmethod
    def make_engine(self) -> AsyncEngine: ...
    async def test_connect(self) -> None: ...
