import sys

import schedule
import time
import os
import re
from typing import Callable
from datetime import datetime
from pothos.logging import logger
from pothos.utils import get_external_ip, to_color, color_print
from pothos.types import Persist, Country, Status, Reconnect, Quantity, Unit, Interval, NordVPNConnect
from pothos.nord_vpn import NordVPN


class NordVPNManager:
    def __init__(self, persist: Persist, country: Country, status: Status, reconnect: Reconnect):
        self._is_valid_country(country)
        self._country: Country = country
        self._schedule: schedule = schedule
        self._tested_nordvpn_version: str = '3.12.5'
        self._user_nordvpn_version: str = NordVPN.get_version()
        self._persist: Persist = persist
        self._status: Interval = self._set_status_interval(status)
        self._reconnect: Interval = self._set_reconnect_interval(reconnect)
        self._prev_external_ip: str = '-'
        self._curr_external_ip: str = get_external_ip()

    @staticmethod
    def _is_valid_country(country: Country) -> bool:
        if country not in NordVPN.get_countries() and country is not None:
            color_print(f'{country} is not a valid country.', 'red')
            NordVPNManager.print_country_list()
            sys.exit()
        return True

    @staticmethod
    def _set_status_interval(status: Status) -> Interval:
        try:
            quantity: Quantity = int(status[:-1])
            unit: Unit = Unit(status[-1])
        except ValueError:
            raise Exception('Status time is invalid. Check out -h for help.')
        else:
            return {'quantity': quantity, 'unit': unit}

    @staticmethod
    def _set_reconnect_interval(reconnect: Reconnect) -> Interval:
        try:
            quantity: Quantity = int(reconnect[:-1])
            unit: Unit = Unit(reconnect[-1])
        except ValueError:
            raise Exception('Refresh time is invalid. Check out -h for help.')
        else:
            if unit is Unit.SECOND or unit is Unit.MINUTE and quantity < 20:
                raise Exception('Refresh time is too low. Check out -h for help.')

            return {'quantity': quantity, 'unit': unit}

    @staticmethod
    def print_country_list() -> None:
        color_print('Choose a country from this list:')

        for count, country in enumerate(sorted(NordVPN.get_countries()), 1):
            print(country.ljust(25), end='')
            if count % 5 == 0:
                print()

    def _print_header(self) -> None:
        status_color: str = 'green' if self._tested_nordvpn_version == self._user_nordvpn_version else 'yellow'
        color_print(f'NOTE:\tPothos was tested with NordVPN Version: {self._tested_nordvpn_version}\n'
                    f'\tYou are on NordVPN Version: {self._user_nordvpn_version}\n', status_color)
        color_print('Pothos - NordVPN Manager '.ljust(60, '_'))

    def _print_details(self) -> None:
        if not self._persist:
            os.system('cls' if os.name == 'nt' else 'clear')
            self._print_header()

        detail_list: list[tuple] = [
            ('Status Last Updated: ', datetime.now().strftime("%m/%d/%Y %H:%M:%S")),
            ('Previous External IP: ', to_color(self._prev_external_ip, 'yellow')),
            ('Current External IP: ', to_color(self._curr_external_ip, 'green')),
            ('Country: ', to_color(self._country)),
            ('Status Interval: ', to_color(f'{self._status["quantity"]}{self._status["unit"].value}')),
            ('Reconnect Interval: ', to_color(f'{self._reconnect["quantity"]}{self._reconnect["unit"].value}'))
        ]

        for item in detail_list:
            print(f'{item[0].ljust(40, "-")} {item[1]}')
        print()

    def _connect(self) -> None:
        self._print_details()
        connection_status: NordVPNConnect = NordVPN.connect(self._country)
        print()

        if connection_status['connected']:
            if self._curr_external_ip != 'no connection':
                self._prev_external_ip = self._curr_external_ip
            self._curr_external_ip = get_external_ip()
            logger.success(f'New external IP: {self._curr_external_ip}')
            self._get_status()
        else:
            for line in connection_status['debug']:
                logger.info(line)

    def _get_status(self) -> None:
        self._print_details()
        status: str = NordVPN.status()
        print(status, '\n')

        if re.search('Disconnected', status):
            msg: str = 'You are disconnected. Attempting to reconnect.'
            logger.info(msg)
            color_print(msg, 'red')
            self._connect()

    def _setup_schedule(self, interval: Interval, job: Callable) -> None:
        match interval['unit']:
            case Unit.SECOND:
                self._schedule.every(interval['quantity']).seconds.do(job)
            case Unit.MINUTE:
                self._schedule.every(interval['quantity']).minutes.do(job)
            case Unit.HOUR:
                self._schedule.every(interval['quantity']).hours.do(job)

    def run(self):
        try:
            self._setup_schedule(self._status, self._get_status)
            self._setup_schedule(self._reconnect, self._connect)
            self._print_header()
            self._connect()

            while True:
                self._schedule.run_pending()
                time.sleep(1)

        except KeyboardInterrupt:
            color_print('Pothos stopped.', 'yellow')
        except Exception as e:
            color_print(f'{e}', 'red')
