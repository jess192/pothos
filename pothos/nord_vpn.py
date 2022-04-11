import subprocess
import re
from halo import Halo
from pothos.types import NordVPNConnect


class NordVPN:
    def __init__(self):
        self.version = self._get_version()
        self.countries = self._get_countries()

    @staticmethod
    def _get_version() -> str:
        version_raw: subprocess.CompletedProcess = subprocess.run(
            'nordvpn version', shell=True, text=True, capture_output=True
        )

        version: str = version_raw.stdout.strip() \
            .replace('\n-', '').strip('-') \
            .replace('NordVPN Version', '').strip()

        return version

    @staticmethod
    def _get_countries() -> list[str]:
        countries_raw: subprocess.CompletedProcess = subprocess.run(
            'nordvpn countries list', shell=True, text=True, capture_output=True
        )

        country_list: list[str] = countries_raw.stdout.strip() \
            .replace('\n-', '').replace('\n', '\t') \
            .strip('-').strip() \
            .replace('\t\t', '\t').replace('\t\t', '\t') \
            .split('\t')

        return country_list

    @staticmethod
    def status() -> str:
        status_raw: subprocess.CompletedProcess = subprocess.run(
            'nordvpn status', shell=True, text=True, capture_output=True
        )
        status: str = status_raw.stdout.strip() \
            .replace('\n-', '') \
            .strip('-').strip('\\').strip('|').strip('/') \
            .strip()

        return status

    @staticmethod
    def connect(country: str) -> NordVPNConnect:
        spinner = Halo(text='Connecting...')
        is_connected: bool = False
        debug: list[str] = []

        p: subprocess.Popen = subprocess.Popen(f'nordvpn c {country}', shell=True, stdout=subprocess.PIPE)
        spinner.start()
        while True:
            line_raw: str = p.stdout.readline().decode('utf-8').strip()
            line: str = line_raw.replace('-', '').replace('/', '').replace('\\', '').replace('|', '').strip()

            if not line:
                break

            if re.search('You are connected', line):
                is_connected: bool = True
            else:
                debug.append(line)

            spinner.text = line

        spinner.stop_and_persist(symbol='🌱')

        return {
            'connected': is_connected,
            'debug': debug
        }
