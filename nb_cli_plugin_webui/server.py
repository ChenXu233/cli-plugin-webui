import os
import asyncio
import threading

os.environ["PYTHONDONTWRITEBYTECODE"] = "1"

from pathlib import Path

import uvicorn
import watchfiles

from nb_cli_plugin_webui.app.logging import LOG_LEVEL
from nb_cli_plugin_webui.app.logging import logger as log

_PKG_DIR = Path(__file__).parent

LOG_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "default": {
            "class": "nb_cli_plugin_webui.app.logging.LoguruHandler",
        },
    },
    "loggers": {
        "uvicorn.error": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
        "uvicorn.access": {
            "handlers": ["default"],
            "level": LOG_LEVEL,
        },
    },
}


def _make_config(host: str, port: int) -> uvicorn.Config:
    return uvicorn.Config(
        "nb_cli_plugin_webui.app:app",
        host=host,
        port=port,
        log_config=LOG_CONFIG,
    )


async def run_server(host: str, port: int, reload: bool = False):
    if not reload:
        config = _make_config(host, port)
        server = uvicorn.Server(config)
        await server.serve()
        return

    restart_count = 0
    while True:
        restart_count += 1
        if restart_count > 1:
            log.warning("Restarting server... (restart #{})", restart_count - 1)

        config = _make_config(host, port)
        server = uvicorn.Server(config)
        server_task = asyncio.create_task(server.serve())

        change_detected = threading.Event()

        def _watch_files():
            for changes in watchfiles.watch(_PKG_DIR, stop_event=change_detected):
                changed = ", ".join(
                    str(Path(p).relative_to(_PKG_DIR)) for _, p in changes
                )
                log.warning("Detected changes in: {}", changed)
                loop.call_soon_threadsafe(setattr, server, "should_exit", True)
                break

        loop = asyncio.get_running_loop()
        watcher_thread = threading.Thread(target=_watch_files, daemon=True)
        watcher_thread.start()

        try:
            await server_task
        except KeyboardInterrupt:
            server.should_exit = True
            server_task.cancel()
            change_detected.set()
            watcher_thread.join(timeout=3)
            break

        change_detected.set()
        watcher_thread.join(timeout=3)

        if not server.should_exit:
            break
