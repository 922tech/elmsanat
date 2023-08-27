import time
import datetime
from .services import AsyncStreamingHttpResponse
import datetime
import time


async def stream(request):

    async def event_stream():
        for i in range(10):
            time.sleep(1)
            yield 'data: The server time is: %s\n\n' % datetime.datetime.now()
            
    return AsyncStreamingHttpResponse(event_stream(), content_type='text/event-stream')

