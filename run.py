from app import app as application
import config
import os

application.debug = config.DEBUG_MODE
if os.environ.get('KICKER_API_CONFIG') is None:
    application.config.from_object('config')
else:
    application.config.from_envvar('KICKER_API_CONFIG')

if __name__ == '__main__':
    application.run()
