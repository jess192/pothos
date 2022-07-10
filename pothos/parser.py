import argparse
from importlib.metadata import version
from pothos.types import MenuArgs, Country, Interval
from pothos.utils import to_color


def pothos_argument_parser(default_country: Country, default_status: Interval, default_reconnect: Interval) -> MenuArgs:
    pothos_version: str = version('pothos')
    default_country_str: str = default_country or 'Fastest connecting country as chosen by NordVPN'
    default_status_str: str = f'{default_status["quantity"]}{default_status["unit"].value}'
    default_reconnect_str: str = f'{default_reconnect["quantity"]}{default_reconnect["unit"].value}'
    quantity_str: str = to_color('quantity', 'green')
    unit_str: str = to_color('unit', 'magenta')

    parser: argparse.ArgumentParser = argparse.ArgumentParser(
        prog='pothos',
        formatter_class=lambda prog: argparse.RawTextHelpFormatter(prog, max_help_position=50)
    )

    parser.add_argument('-v', '--version', action='version', version=f'Pothos version {pothos_version}')

    parser.add_argument('-p', '--persist',
                        help='By default Pothos clears the terminal on each status refresh.\n'
                             'Set -p to disable this feature.\n ',
                        action='store_true')

    parser.add_argument('-l', '--list',
                        help='View the list of countries you can connect to.\n ',
                        action='store_true')

    parser.add_argument('-c', '--country',
                        help='Set which country you want to connect to.\n'
                             f'Default country: {to_color(default_country_str)}\n ',
                        default=default_country,
                        metavar='name')

    parser.add_argument('-s', '--status',
                        help='Interval to check NordVPN status.\n'
                             f'Format: [{quantity_str}: integer]'
                             f'[{unit_str}: s(seconds), m(minutes), h(hours)]\n'
                             'Example: 10s - show status of NordVPN connection every 10 seconds\n'
                             f'Default status interval: {to_color(default_status_str)}\n ',
                        default=default_status_str,
                        metavar='time')

    parser.add_argument('-r', '--reconnect',
                        help='Interval to reconnect to NordVPN.\n'
                             f'Format: [{quantity_str}: integer]'
                             f'[{unit_str}: m(minutes), h(hours)]\n'
                             'Interval must be >= 20 minutes.\n'
                             'NordVPN does not like too many reconnects in a short amount of time.\n'
                             'Example: 3h - connect to new NordVPN server every 3 hours\n'
                             f'Default reconnect interval: {to_color(default_reconnect_str)}\n ',
                        default=default_reconnect_str,
                        metavar='time')

    parser.add_argument('-f', '--force',
                        help='Sometimes NordVPN can\'t connect after an internet connection change.\n'
                             'This attempts to rectify by restarting the NordVPN service.'
                             '(linux only, requires sudo privileges).\n ',
                        action='store_true')

    args: argparse.Namespace = parser.parse_args()

    return {
        'force_service_restart': args.force,
        'persist': args.persist,
        'show_countries': args.list,
        'country': args.country,
        'status': args.status,
        'reconnect': args.reconnect,
        'help': parser.print_help
    }
