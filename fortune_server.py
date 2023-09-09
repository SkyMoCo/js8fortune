from js8call_api import *


class FortuneServer:

    def __init__(self):
        logging.info("fortune server init")
        js8call_api = Js8CallApi()
        js8call_api.connect()
        js8call_api.send('STATION.GET_GRID', '')
        logging.info( 'call: STATION.GET_GRID')
        if js8call_api.connected:
            message = js8call_api.listen()
            if message:
                typ = message.get('type', '')
                value = message.get('value', '')
                if typ == 'STATION.GRID':
                    logging.info( 'resp: ' + value)
                    js8call_api.set_my_grid(value)
            else:
                logging.warning( 'Unable to get My Grid.')
                logging.warning( 'Check in File -> Settings -> General -> '
                       'Station -> Station Details -> My Maidenhead Grid Locator')

            js8call_api.send('STATION.GET_CALLSIGN', '')
            logging.info( 'call: STATION.GET_CALLSIGN')
            if js8call_api.connected:
                message = js8call_api.listen()
                if message:
                    typ = message.get('type', '')
                    value = message.get('value', '')
                    if typ == 'STATION.CALLSIGN':
                        logging.info('resp: ' + value)
                        js8call_api.set_my_station(value)

                else:
                    logging.warning( 'Unable to get My Callsign.')
                    logging.warning( 'Check in File -> Settings -> General -> Station -> Station Details -> My Callsign')

            js8call_api.send('RIG.GET_FREQ', '')
            logging.info('call: RIG.GET_FREQ')
            if js8call_api.connected:
                message = js8call_api.listen()
                if message:
                    typ = message.get('type', '')
                    if typ == 'RIG.FREQ':
                        value = message.get('params', '')
                        logging.info('resp: ' + str(value["DIAL"]))
                        js8call_api.set_my_frequency(value["DIAL"])

                else:
                    logging.warning('Unable to get Rig Frequency.')

    def run_server():

        logging.info("Starting run loop")
        # Load all our fortunes
        if not os.path.exists(fortunes_dir):
            logging.warning( "err: Can't find the fortunes directory")
            logging.warning( 'info: Check that the fortunes_dir value in fortune_settings.py is correct')
            exit(1)


        mb_announcement = MbAnnouncement()

        # this debug code block processes simulated incoming commands

        try:
            while js8call_api.connected:
                if announce:
                    mb_announcement.send_mb_announcement(js8call_api)

                message = js8call_api.listen()

                if not message:
                    continue

                typ = message.get('type', '')
                value = message.get('value', '')

                if not typ:
                    return

                elif typ == 'STATION.GRID':
                    logmsg(3, 'resp: ' + value)
                    js8call_api.set_my_grid(value)

                elif typ == 'STATION.CALLSIGN':
                    logmsg(3, 'resp: ' + value)
                    js8call_api.set_my_station(value)
                    js8call_api.set_my_blog(value)  # this is a temp measure until we fully implement blog names

                elif typ == 'RX.DIRECTED':  # We have a message directed to us
                    rsp_message = self.process(message)
                    if rsp_message:
                        logging.warn( 'resp: ' + rsp_message)
                        js8call_api.send('TX.SEND_MESSAGE', rsp_message)

        finally:
            js8call_api.close()
