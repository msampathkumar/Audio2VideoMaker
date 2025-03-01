import logging

logger = logging.getLogger(__name__)


class Status:
    ok = "[✅ OK!]"
    OK = "[✅ OK!]"
    not_ok = "[❌ Not ok!]"
    NOT_OK = "[❌ Not ok!]"
    overriding = "[⚠️ Overriding!]"
    OVERRIDING = "[⚠️ Overriding!]"
    warning = "[🚨️Warning]"
    WARNING = "[🚨️Warning]"
    wip = "[⏳️WIP]"
    WIP = "[⏳️WIP]"


if __name__ == "__main__":
    logging.basicConfig()
    logger.setLevel(logging.DEBUG)
    # Logging and levels
    # 10
    logger.debug("debug")
    # 20
    logger.info("info")
    # 30
    logger.warning("warning")
    # 40
    logger.error("error")
    # 50
    logger.critical("critical")
