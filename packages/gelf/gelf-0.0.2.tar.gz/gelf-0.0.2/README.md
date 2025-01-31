# Python GELF

## Install from PyPI

```python
pip install gelf
```

## Configure handler from a python script

```python
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
# not strictly needed, this is to display logs on stdout
logger.addHandler(logging.StreamHandler())

logger.info(
    "This message gives a lot of information",
    extra={
        "request_id": "4edba63411eb4c8f808e32e904d29c1c",
        "user_id": "bf5089c16355401a9bff3efd6b2ada2e"
    },
)
```

## Configure handler using a config file

- In python script use `logging.config.fileConfig` to load logging config from file

```python
import logging
import logging.config
import time
from uuid import uuid4

logging.config.fileConfig("logging.conf")

logger = logging.getLogger("example.module")

logger.info(
    "This message gives a lot of information",
    extra={
        "request_id": "4edba63411eb4c8f808e32e904d29c1c",
        "user_id": "bf5089c16355401a9bff3efd6b2ada2e"
    },
)
```

- Put your logging config in a file. Here `logging.conf`

```toml
[formatters]
keys = 

[handlers]
keys = stdout,gelf

# not strictly needed, this is to display logs on stdout
[handler_stdout]
class = logging.StreamHandler
level = DEBUG

[handler_gelf]
class = gelf.handler.GELFHandlerTCP
args = ('localhost', '12201', os.getenv('SERVICE', 'unknown'))

[loggers]
keys = root

[logger_root]
handlers = stdout,gelf
level = DEBUG
```

> NOTE: In this example service field of log records is retrieved from `SERVICE` environment variable but you might as well provide a fixed value.