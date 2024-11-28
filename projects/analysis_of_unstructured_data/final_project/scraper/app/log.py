import logging

logging.basicConfig(
    format="%(asctime)s %(levelname)-8s - %(message)s",
    datefmt="%Y-%m-%d:%H:%M:%S",
    level=logging.NOTSET,
)
log = logging.getLogger(__file__)
