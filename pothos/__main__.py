import schedule
import time
from pothos.logging import configure_logging, logger
from pothos.nord import status, reconnect


def run_schedule():
    configure_logging()

    status()
    schedule.every().hour.do(status)
    schedule.every().day.at('01:00').do(reconnect)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.warning('KeyboardInterrupt: Stopped scraping for product prices')
    except Exception as e:
        logger.error(e)
