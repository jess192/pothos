import schedule
import time
from pothos.logging import configure_logging, logger
from pothos.nord import status, reconnect


def run_schedule():
    configure_logging()

    status()
    schedule.every(10).minutes.do(status)
    schedule.every(4).hours.do(reconnect)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning('KeyboardInterrupt: Stopped scraping for product prices')
    except Exception as e:
        logger.error(e)
