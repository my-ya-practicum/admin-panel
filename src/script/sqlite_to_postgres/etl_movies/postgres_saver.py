from types import TracebackType
from typing import AsyncGenerator, Optional, Type
from script.sqlite_to_postgres.etl_movies.settings import Settings


class PostgresSaver:
    def __init__(self, settings: Settings):
        self.settings = settings

    async def __aenter__(self):
        pass

    async def __aexit__(
        self,
        exc_type: Optional[Type[BaseException]] = None,
        exc_value: Optional[BaseException] = None,
        traceback: Optional[TracebackType] = None,
    ) -> None:
        pass

    async def load_data(self, data: AsyncGenerator):
        async for i in data:
            print(i)
