import sys

from termcolor import cprint
from pothos.nord_vpn_manager import NordVPNManager
from pothos.logging import configure_logging
from pothos.types import Unit, MenuArgs, BaseValues
from pothos.parser import pothos_argument_parser


def run_pothos():
    configure_logging()
    defaults: BaseValues = {
        'country': None,
        'status': {'quantity': 5, 'unit': Unit.MINUTE},
        'reconnect': {'quantity': 4, 'unit': Unit.HOUR}
    }
    menu_args: MenuArgs = pothos_argument_parser(
        defaults['country'],
        defaults['status'],
        defaults['reconnect']
    )

    try:
        if menu_args['show_countries']:
            NordVPNManager.print_country_list()
            sys.exit()
        else:
            pothos = NordVPNManager(
                menu_args['persist'],
                menu_args['country'],
                menu_args['status'],
                menu_args['reconnect']
            )
            pothos.run()
    except Exception as e:
        cprint(f'{e}', 'red', attrs=['bold'])
        menu_args['help']()
