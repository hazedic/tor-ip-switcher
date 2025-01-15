import json
import time
import urllib.request
import argparse
from stem import Signal
from stem.control import Controller


class TorIPSwitcher:
    def __init__(self, host, port, passwd, interval):
        self.host = host
        self.port = port
        self.passwd = passwd
        self.interval = interval

    def start(self):
        print('Tor IP Switcher starting.')
        self.newnym()

    def stop(self):
        print('Tor IP Switcher stopping.')

    def write(self, message):
        timestamp = time.localtime()
        formatted_message = '[{:02}:{:02}:{:02}] {}'.format(timestamp[3], timestamp[4], timestamp[5], message)
        print(formatted_message)

    def error(self):
        print('Tor daemon not running!')

    def newnym(self):
        host = self.host
        port = self.port
        passwd = self.passwd
        interval = self.interval

        try:
            with Controller.from_port(address=host, port=port) as controller:
                controller.authenticate(password=passwd)
                self.write('AUTHENTICATE accepted.')
                while True:
                    self._request_newnym(controller, interval)
        except Exception as e:
            self.write(f"There was an error: {e}")
            self.error()

    def _request_newnym(self, controller, interval):
        try:
            controller.signal(Signal.NEWNYM)  # Request a new IP
            self._show_new_ip()
            time.sleep(interval)
        except Exception as e:
            self.write(f"Error requesting NEWNYM: {e}")
            self.write('Quitting.')

    def _show_new_ip(self):
        try:
            ip_data = json.load(urllib.request.urlopen('https://check.torproject.org/api/ip'))
            new_ip = ip_data['IP']
        except (urllib.error.URLError, ValueError):
            new_ip = self._get_external_ip()
        self.write(f'Your IP is {new_ip}')

    def _get_external_ip(self):
        from subprocess import getoutput
        return getoutput('wget -qO - ident.me')


def main():
    parser = argparse.ArgumentParser(description='Tor IP Switcher.')
    parser.add_argument('--host', type=str, default='localhost', help='Tor control host (default: localhost)')
    parser.add_argument('--port', type=int, default=9051, help='Tor control port (default: 9051)')
    parser.add_argument('--passwd', type=str, default='', help='Password for Tor control port (default: empty)')
    parser.add_argument('--interval', type=int, default=30, help='Time interval between IP switches in seconds (default: 30)')

    args = parser.parse_args()

    switcher = TorIPSwitcher(args.host, args.port, args.passwd, args.interval)

    try:
        switcher.start()
    except KeyboardInterrupt:
        switcher.stop()


if __name__ == '__main__':
    main()