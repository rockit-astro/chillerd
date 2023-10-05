## CLASP camera chiller daemon

`chillerd` wraps a Thermotek T257P Precision Chiller attached via a USB-RS232 adaptor and
provides control/monitoring for camera cooling

`chiller` is a commandline utility that controls and reports the latest data from the chiller.


### Configuration

Configuration is read from json files that are installed by default to `/etc/chillerd`.
A configuration file is specified when launching the server, and the `chiller` frontend will search this location when launched.

The configuration options are:
```python
{
  "daemon": "clasp_chiller", # Run the server as this daemon. Daemon types are registered in `rockit.common.daemons`.
  "log_name": "chillerd@clasp",        # The name to use when writing messages to the observatory log.
  "serial_port": "/dev/chiller", # The serial port device to use
  "serial_baud": 9600,             # The serial baud rate to use
  "serial_timeout": 5,              # The serial time out to use
  "query_delay": 30                 # Delay (in seconds) between measurement updates
}
```

### Initial Installation

The automated packaging scripts will push 4 RPM packages to the observatory package repository:

| Package                   | Description                                                                 |
|---------------------------|-----------------------------------------------------------------------------|
| rockit-chiller-server     | Contains the `chillerd` server and systemd service file.                    |
| rockit-chiller-client     | Contains the `chiller` commandline utility for querying the chiller server. |
| python3-rockit-chiller    | Contains the python module with shared code.                                |
| rockit-chiller-data-clasp | Contains the json configuration and udev rules for CLASP.                   |

After installing packages, the systemd service should be enabled:

```
sudo systemctl enable --now chillerd@clasp
```

Now open a port in the firewall:
```
sudo firewall-cmd --zone=public --add-port=<port>/tcp --permanent
sudo firewall-cmd --reload
```
where `port` is the port defined in `rockit.common.daemons` for the daemon specified in the config.

### Upgrading Installation

New RPM packages are automatically created and pushed to the package repository for each push to the `master` branch.
These can be upgraded locally using the standard system update procedure:
```
sudo yum clean expire-cache
sudo yum update
```

The daemon should then be restarted to use the newly installed code:
```
sudo systemctl restart chillerd@clasp
```

### Testing Locally

The server and client can be run directly from a git clone:
```
./chillerd clasp.json
CHILLERD_CONFIG_PATH=./clasp.json ./chiller status
```
