import asyncio

import uvloop

from avengers.app import create_app
from avengers.config import VaultClient, settings

if __name__ == "__main__":
    asyncio.set_event_loop_policy(uvloop.EventLoopPolicy())

    VaultClient.initialize()

    app = create_app()  # pylint: disable=invalid-name

    app.run(
        host=settings.RUN_HOST, port=settings.RUN_PORT, debug=settings.DEBUG
    )
