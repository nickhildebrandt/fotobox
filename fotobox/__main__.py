import logging
import configparser
from fotobox import Fotobox, WebserverThread
import signal

def signal_handler(sig, frame, fotobox, webserver_thread):
    logging.info(f"Received signal {sig}, shutting down gracefully.")
    fotobox.close()
    if webserver_thread.is_alive():
        webserver_thread.stop()
        webserver_thread.join()
    logging.info("Shutdown complete.")

def main():
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    config = configparser.ConfigParser()
    config.read('/etc/fotobox.ini')

    webserver_thread = WebserverThread()
    webserver_thread.start()

    fotobox = Fotobox(
        config['DEFAULT'].get('width', '1280'),
        config['DEFAULT'].get('height', '720'),
        config['DEFAULT'].get('fontsize', '80'),
        config['DEFAULT'].get('welcometext', 'Press the red button'),
        config['DEFAULT'].get('countdown', 'Get Ready,Set,Capture!').split(',')
    )

    signal.signal(signal.SIGINT, lambda sig, frame: signal_handler(sig, frame, fotobox, webserver_thread))
    signal.signal(signal.SIGTERM, lambda sig, frame: signal_handler(sig, frame, fotobox, webserver_thread))

if __name__ == "__main__":
    main()
