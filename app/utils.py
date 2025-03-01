import logging

# logging.basicConfig()
# logging.getLogger()

logger = logging.getLogger(__name__)

logger.setLevel(logging.DEBUG)

class Status:
    ok = "[✅ OK!]"
    not_ok = "[❌ Not ok!]"
    overriding = "[⚠️ Overriding!]"
    warning = "[🚨️Warning]"
    wip = "[⏳️WIP]"


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
logger.critical("error")