import logging
from .settings import CPU_LOG_FILE

logging.basicConfig(
    filename=CPU_LOG_FILE,
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

logger = logging.getLogger("ai_test_gen")
