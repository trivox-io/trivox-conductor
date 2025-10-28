from trivox_conductor.common.logging import setup_logging
from trivox_conductor.common.logger import logger


def initialize():
    setup_logging(
        overrides={
            "handlers": {
                "file": {
                    "maxBytes": 10485760,
                    "backupCount": 5,
                },
            },
            "root": {"level": "INFO"},
            "loggers": {
                "trivox_conductor": {
                    "level": "INFO",
                    "propagate": True,
                },
            },
        }
    )
    logger.info("Trivox Conductor application started.")


if __name__ == "__main__":
    initialize()
