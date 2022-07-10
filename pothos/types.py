from enum import Enum
from typing import TypedDict, Callable, Union

Force = bool
Persist = bool
ShowCountries = bool
Country = str
Status = str
Reconnect = str
Quantity = int


class Unit(Enum):
    SECOND = 's'
    MINUTE = 'm'
    HOUR = 'h'


class Interval(TypedDict):
    quantity: Quantity
    unit: Unit


class MenuArgs(TypedDict):
    force_service_restart: Force
    persist: Persist
    show_countries: ShowCountries
    country: Country
    status: Status
    reconnect: Reconnect
    help: Callable


class BaseValues(TypedDict):
    country: Union[Country | None]
    status: Interval
    reconnect: Interval


class NordVPNConnect(TypedDict):
    connected: bool
    debug: list[str]
