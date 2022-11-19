import argparse
import os

LOGGING_DIR = os.environ.get('tbot_log_dir', 'log')
LOG_FORMATTER = '[%(asctime)s] %(levelname)8s - %(message)s (%(filename)s:%(lineno)s)'

def parse_input_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('-l', '--loglevel', type=str,
                        default='info', choices=['debug', 'info', 'error'], help='Logging level.')
    # parser.add_argument('-t', '--tbot_token', type=str,
    #                     default=os.environ.get('TELEBOT_TOKEN', ''), help='telegram bot token')
    # parser.add_argument('-r', '--restart', type=float,
    #                     default=RESTART_INTERVAL, help='Restart period.')
    return parser.parse_args()
