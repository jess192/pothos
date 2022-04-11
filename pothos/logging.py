from loguru import logger
import sys
import os

log_location: str = os.path.abspath(__file__ + '/../../')

logging_config = {
    'handlers': [
        {
            'sink': log_location + '/logs/info_{time:MM_DD_YYYY}.log',
            'level': 'INFO',
            'rotation': '00:00',
            'retention': '30 days'
        },
        {
            'sink': log_location + '/logs/error_{time:MM_DD_YYYY}.log',
            'level': 'ERROR',
            'rotation': '00:00',
            'retention': '30 days'
        }
    ]
}


def configure_logging():
    try:
        logger.configure(**logging_config)
    except Exception as e:
        print('Logger configuration failed. ', e)
        sys.exit(1)
