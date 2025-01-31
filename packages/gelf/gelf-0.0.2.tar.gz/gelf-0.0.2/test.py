import logging
import time
from uuid import uuid4

from gelf.handler import GELFHandlerTCP

logger = logging.getLogger("example.module")
logger.setLevel(logging.DEBUG)

handler = GELFHandlerTCP(
    host="127.0.0.1",
    port=12201,
    service="example",
    include_extra_fields=True,
    debug=True,
)
handler.setLevel(logging.DEBUG)
logger.addHandler(handler)
logger.addHandler(logging.StreamHandler())

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
