import os
import sys
import asyncio
import logging
import datetime

from pathlib import Path

from config import *
from app import bot, filters

if __name__ == '__main__':
    args = None
    try:
        assert sys.version_info >= (3, 10), "Python 3.10+ required"
        args = parse_input_args()

        os.makedirs(LOGGING_DIR, exist_ok=True)
        logging.basicConfig(
            level=args.loglevel.upper(),
            format=LOG_FORMATTER,
            force=True,
            handlers=[
                logging.FileHandler(filename=Path(LOGGING_DIR) / f'ts_{datetime.datetime.utcnow().strftime("%Y%m%d_%H-%M-%S")}.log', mode='w'),
                logging.StreamHandler()
            ]
        )
        logger = logging.getLogger(__name__)
        logger.info('tbot started with args: %s', args)
        logger.info('tbot_token: %s', os.environ.get("TBOT_TOKEN"))

        filters.bind_filters(bot.bot)
        bot.bot.infinity_polling()

    except KeyboardInterrupt:
        logging.info('tbot is stopped by user.')
    except BaseException as err:
        logging.exception(f'tbot  stopped unexpectedly due to error: %s', err, stack_info=True if not args or args.loglevel.upper() == 'DEBUG' else False)