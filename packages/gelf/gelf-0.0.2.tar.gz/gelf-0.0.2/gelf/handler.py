import socket
import zlib
from logging.handlers import SocketHandler

from gelf.formatter import GELFFormatter


class GELFHandlerTCP(SocketHandler):
    def __init__(
        self,
        host,
        port,
        service: str,
        debug: bool = False,
        include_extra_fields: bool = True,
        compress: bool = False,
    ):
        super().__init__(host, port)
        self.compress = compress
        self.gelf_formatter = GELFFormatter(
            hostname=socket.gethostname(),
            service=service,
            debug=debug,
            include_extra_fields=include_extra_fields,
        )

    def makePickle(self, record):
        gelf_message = self.gelf_formatter.format(record)
        packed = gelf_message.encode("utf-8")
        if self.compress:
            packed = zlib.compress(packed)
        return packed + b"\n"
