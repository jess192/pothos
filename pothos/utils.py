from requests import Response, get
from termcolor import colored, cprint


def get_external_ip():
    try:
        url: str = 'https://myexternalip.com/raw'
        r: Response = get(url)
    except Exception as e:
        print('Unable to get external IP', e)
        return 'no connection'
    else:
        return r.text


def to_color(string: str, color: str = 'cyan'):
    return colored(string, color, attrs=['bold'])


def color_print(string: str, color: str = 'cyan'):
    cprint(string, color, attrs=['bold'])
