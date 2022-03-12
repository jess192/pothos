import subprocess
import re
from pothos.logging import logger


def status():
    vpn_status = subprocess.run('nordvpn status', shell=True, text=True,  capture_output=True)
    clean_vpn_status = vpn_status.stdout.strip().replace('\n-', '').strip('-').strip()
    print(clean_vpn_status)

    if re.search('Disconnected', clean_vpn_status):
        logger.warning('You are disconnected. Attempting to reconnect.')
        reconnect()


def reconnect():
    country: str = 'United_States'
    command: str = f'nordvpn c {country}'

    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)

    while True:
        line = p.stdout.readline()
        if not line:
            break

        line = line.decode('utf-8')

        if re.search('You are connected', line):
            logger.success('You are connected')
            status()
        else:
            clean_line = line.replace('-', '').replace('/', '').replace('\\', '').replace('|', '').strip()
            logger.info(clean_line)

