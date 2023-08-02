<h1 align="center">Pothos</h1>

<div align="center">
	<img src="assets/pothos.png" width="300">
</div>


## About
`pothos` is a simple command line tool for managing NordVPN connections on a `Fedora Linux` setup. 

Pothos was built using `Fedora Linux 36`. Other flavors of Linux may work as well, but have not been tested.

## Requirements
- [pipx](https://github.com/pypa/pipx) or [Poetry](https://github.com/python-poetry/poetry)
- [Python](https://www.python.org/) - `3.10`
- [NordVPN for Linux](https://nordvpn.com/download/linux/) - `3.16.5`

## Install

With pipx:
```shell
pipx install git+https://github.com/jess192/pothos.git
```

or

Local build with poetry:
```shell
git clone https://github.com/jess192/pothos.git
poetry install
poetry run pothos
```

## Usage
With pipx:
```shell
pothos
```

With poetry:
```shell
poetry run pothos
```

## Flags
| Flag    | Title                 | Description                                                                                             |
|---------|-----------------------|---------------------------------------------------------------------------------------------------------|
| -h      | help                  | Show help menu                                                                                          |
| -v      | version               | Show `pothos` version                                                                                   |
| -p      | persist               | By default Pothos clears the terminal on each status refresh. Set -p to disable.                        |
| -l      | list                  | Show list of countries you can connect to.                                                              |
| -f      | force service restart | Attempt to restart NordVPN daemon if NordVPN is not connected.                                          |
| -c name | country name          | Set which country you want to connect to. <br/>Default: Fastest connecting country as chosen by NordVPN |
| -s time | status interval       | Interval to check NordVPN status. Default: 5m                                                           |
| -r time | reconnect time        | Interval to reconnect to NordVPN. Default: 4h<br/>                                                      |


## Examples
> Connect to a NordVPN server in Canada. Show a status update every 5 seconds and connect to a new server every 3 hours.
```shell
pothos -c Canada -s 5s -r 3h
```

> Connect to a NordVPN server in a country that NordVPN chooses. Show a status update every 5 ninutes (default) and connect to a new server every 20 minutes. Persist is set, so the terminal will not clear on each status update.
```shell
pothos -r 20m -p
```


<br/>
<a href="https://www.flaticon.com/free-icons/pothos" title="pothos icon" style="font-size: 11px;}">Pothos icon created by Flat Icons - Flaticon</a>

