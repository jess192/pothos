<h1 align="center">Pothos</h1>

<div align="center">
	<img src="assets/pothos.png" width="300">
</div>


## About
`pothos` is a simple command line tool for managing NordVPN connections.

## Requirements
- [pipx](https://github.com/pypa/pipx "pipx") or [poetry](https://github.com/python-poetry/poetry "poetry")
- Python 3.10^
- NordVPN

## Install

With pipx:
```shell
$ pipx install git+https://github.com/jess192/pothos.git
```

or

Local build with poetry:
```shell
$ git clone https://github.com/jess192/pothos.git
$ poetry install
$ poetry run pothos
```

## Usage
With pipx:
```shell
$ pothos
```

With poetry:
```shell
$ poetry run pothos
```

## Flags
| Flag    | Title           | Description                                                                      |
|---------|-----------------|----------------------------------------------------------------------------------|
| -h      | help            | Show help menu                                                                   |
| -v      | version         | Show `pothos` version                                                            |
| -p      | persist         | By default Pothos clears the terminal on each status refresh. Set -p to disable. |
| -l      | list            | Show list of countries you can connect to.                                       |
| -c name | country name    | Set which country you want to connect to. Default: United_States                 |
| -s time | status interval | Interval to check NordVPN status. Default: 5m                                    |
| -r time | reconnect time  | Interval to reconnect to NordVPN. Default: 4h                                    |


## Examples
> Connect to a NordVPN server in Canada. Show a status update every 5 seconds and connect to a new server every 3 hours.
```shell
$ pothos -c Canada -s 5s -r 3h
```

> Connect to a NordVPN server in the United_States (default). Show a status update every 5 ninutes (default) and connect to a new server every 20 minutes. Persist is set, so the terminal will not clear on each status update.
```shell
$ pothos -r 20m -p
```


<br/>
<a href="https://www.flaticon.com/free-icons/pothos" title="pothos icon" style="font-size: 11px;}">Pothos icon created by Flat Icons - Flaticon</a>

