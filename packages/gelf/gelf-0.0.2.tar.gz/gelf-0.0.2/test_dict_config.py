import logging
import logging.config
import time
from uuid import uuid4

logging.config.fileConfig("logging.conf")

logger = logging.getLogger("example.module")


while True:
    request_id = uuid4().hex

    logger.debug(
        "Something not that important", extra={"foo": "bar", "request_id": request_id}
    )
    logger.info(
        "This message gives a lot of information",
        extra={"foo": "bar", "request_id": request_id},
    )
    logger.error(
        "Something went wrong!", extra={"foo": "bar", "request_id": request_id}
    )

    time.sleep(5)
