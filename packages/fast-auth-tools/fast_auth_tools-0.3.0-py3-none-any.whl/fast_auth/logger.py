import os
from logging import getLogger, StreamHandler, Formatter, DEBUG, INFO

logger = getLogger("auth")

handler = StreamHandler()
handler.setLevel(DEBUG if os.getenv("AUTH_DEBUG") else INFO)

# Match the FastAPI logger format
handler.setFormatter(Formatter("%(levelname)s:\t\t%(message)s"))

logger.addHandler(handler)
