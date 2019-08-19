from aiohttp.web import *
import subprocess
import settings

async def handler(request: Request):
    return Response(text='Hello, world!')

def init(port=settings.DEFAULT_PORT):
    app = Application()
    app.add_routes([get('/', handler)])

    server = mp.Process(target=run_app, args=(app,), daemon=True)
    server.start()
    server.join()
    print(server.pid)
    