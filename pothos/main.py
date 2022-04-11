from termcolor import cprint
from pothos.manager import Manager
from pothos.logging import configure_logging
from pothos.types import Unit, MenuArgs, Defaults
from pothos.parser import pothos_argument_parser


def run_pothos():
    configure_logging()

    defaults: Defaults = {
        'country': 'United_States',
        'status': {'quantity': 5, 'unit': Unit.MINUTE},
        'reconnect': {'quantity': 4, 'unit': Unit.HOUR}
    }

    menu_args: MenuArgs = pothos_argument_parser(defaults['country'], defaults['status'], defaults['reconnect'])

    try:
        pothos = Manager(
            menu_args['persist'], menu_args['show_countries'], menu_args['country'],
            menu_args['status'], menu_args['reconnect']
        )
        pothos.run()
    except Exception as e:
        cprint(f'{e}', 'red', attrs=['bold'])
        menu_args['help']()
