from loguru import logger
import sys
from os import environ


# taken from Loguru but with the addition of the extra field
def env(key, type_, default=None):
    if key not in environ:
        return default

    val = environ[key]

    if type_ == str:
        return val
    if type_ == bool:
        if val.lower() in ["1", "true", "yes", "y", "ok", "on"]:
            return True
        if val.lower() in ["0", "false", "no", "n", "nok", "off"]:
            return False
        raise ValueError(
            "Invalid environment variable '%s' (expected a boolean): '%s'" % (key, val)
        )
    if type_ == int:
        try:
            return int(val)
        except ValueError:
            raise ValueError(
                "Invalid environment variable '%s' (expected an integer): '%s'" % (key, val)
            ) from None
    raise ValueError("The requested type '%r' is not supported" % type_)


# If the user has set the log level manually, we should honor it.
log_level = environ.get("LOG_LEVEL") or environ.get("LOGURU_LEVEL") or "INFO"

# If we are running from the code repository, we are in development mode, and we want to see the logs.
# Python dotenv sets this environment variable when we run the code from the root of the repository.
if "DEVELOPMENT" in environ or log_level == "DEBUG":
    LOG_FORMAT = env(
        "LOGURU_FORMAT",
        str,
        # "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        # "{message}",
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    )
    log_level = "DEBUG"
# Otherwise, we don't want users to see the logs - we just want the print statements.
else:
    LOG_FORMAT = env(
        "LOGURU_FORMAT",
        str,
        "{message}",
    )
    log_level = "INFO"


def init_logger():
    # Remove existing handlers
    logger.remove()
    stdout_handler = {
        "sink": sys.stdout,
        "serialize": False,
        "level": log_level,
        "format": LOG_FORMAT,
    }
    logger.add(**stdout_handler)
    # logger.add(sys.stdout, format="{time} | {level} | {message}", filter="sub.module")
