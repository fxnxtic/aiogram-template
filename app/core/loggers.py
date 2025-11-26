import logging
import sys
import traceback

import structlog


class MuteDropper(logging.Filter):
    def __init__(self, names_to_mute: list[str]):
        super().__init__()
        self.names_to_mute = set(names_to_mute)

    def filter(self, record: logging.LogRecord) -> bool:
        # Возвращаем False → log будет отброшен
        return record.name not in self.names_to_mute
    

def init_logging(*mute_loggers: str, debug: bool = False) -> None:
    """
    Initializes the logging system.

    Args:
        *mute_loggers (str): The names of loggers to mute.
        debug (bool, optional): Whether to enable debug logging. Defaults to False.
    """
    logging.captureWarnings(True)
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=logging.DEBUG if debug else logging.INFO,
    )

    renderer = (
        structlog.dev.ConsoleRenderer(colors=True)
        if debug
        else structlog.processors.JSONRenderer()
    )

    structlog.configure(
        processors=[
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            renderer,
        ],
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    formatter = structlog.stdlib.ProcessorFormatter(
        processor=renderer,
        foreign_pre_chain=[
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
        ]
    )

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    handler.addFilter(MuteDropper(mute_loggers))

    root_logger = logging.getLogger()
    root_logger.handlers = [handler]


def log_errors(raise_error: bool = False):
    def decorator(func):
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                logger = structlog.get_logger(__name__)
                logger.error(traceback.format_exc())
                if raise_error:
                    raise e

        return wrapper

    return decorator
