"""
This module provides an async http stream response.
"""
import asyncio
import nest_asyncio
from django.http import StreamingHttpResponse
from typing import AsyncGenerator, AsyncIterator, Any, Iterator, Union


class AsyncStreamingHttpResponse(StreamingHttpResponse):
    """
    Works like `StreamingHttpResponse` but as opposed to that,
    it does not lock the whole processing of the server.
    """
    def __init__(self, streaming_content: AsyncGenerator[str, Any], *args, **kwargs):

        sync_streaming_content = self.get_sync_iterator(streaming_content)
        super().__init__(streaming_content=sync_streaming_content, *args, **kwargs)


    @staticmethod
    async def convert_async_iterable(stream: Union[AsyncGenerator[str, Any], AsyncIterator]) -> Iterator:

        return iter([chunk async for chunk in stream])


    def get_sync_iterator(self, async_iterable: AsyncGenerator[str, Any]) -> Iterator:
        """
        Runs the `convert_async_iterable` within a non-async function.
        Thanks to `nest_asyncio` it does not get asyncio running
        event loop related errors
        """
        nest_asyncio.apply()

        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        result = loop.run_until_complete(self.convert_async_iterable(async_iterable))
        return result
