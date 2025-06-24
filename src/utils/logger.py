import logging

logger = logging.getLogger("blackjac")
logger.setLevel(logging.DEBUG)

handler = logging.StreamHandler()
formatter = logging.Formatter("[%(levelname)s] %(message)s")
handler.setFormatter(formatter)

logger.addHandler(handler)
logger.propagate = False