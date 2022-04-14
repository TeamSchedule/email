import os
import sys
import time

from email_sender.queue_handler import queue_handler


if __name__ == '__main__':
    time.sleep(45)

    try:
        queue_handler()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)
