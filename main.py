# Pretty simple, don't really need classes...
import logging
from fortune_server import FortuneServer
from fortune_settings import __version__


def main():
    #logging.basicConfig(format='%(asctime)s %(message)s', level=logging.DEBUG,filename='js8fortune.log')
    logging.basicConfig(format='%(asctime)s %(message)s', level=logging.INFO)
    logging.info('Started')
    logging.info('JS8 Fortune Server ' + __version__)
    s = FortuneServer()     # Setup Fortune Server using settings from settings.py
    FortuneServer.run_server()

    logging.info('Finished')

if __name__ == '__main__':
    main()
