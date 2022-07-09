import subprocess
import re
from halo import Halo
from pothos.types import NordVPNConnect


class NordVPN:
    @staticmethod
    def _get_update_alert() -> str:
        return 'A new version of NordVPN is available! Please update the application.'

    @staticmethod
    def get_version() -> str:
        version_raw: subprocess.CompletedProcess = subprocess.run(
            'nordvpn version', shell=True, text=True, capture_output=True
        )

        version: str = version_raw.stdout.strip() \
            .replace(NordVPN._get_update_alert(), '') \
            .replace('\n-', '').strip('-') \
            .replace('NordVPN Version', '').strip()

        return version

    @staticmethod
    def get_countries() -> list[str]:
        countries_raw: subprocess.CompletedProcess = subprocess.run(
            'nordvpn countries list', shell=True, text=True, capture_output=True
        )

        country_list: list[str] = countries_raw.stdout.strip() \
            .replace(NordVPN._get_update_alert(), '') \
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
        selected_country: str = country or ''
        subprocess_connect_command: str = f'nordvpn c {selected_country}'.rstrip()
        spinner = Halo(text='Connecting...')
        is_connected: bool = False
        debug: list[str] = []

        p: subprocess.Popen = subprocess.Popen(subprocess_connect_command, shell=True, stdout=subprocess.PIPE)
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
