#
# This file is part of the Robotic Observatory Control Kit (rockit)
#
# rockit is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# rockit is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with rockit.  If not, see <http://www.gnu.org/licenses/>.

"""Helper function to validate and parse the json config file"""

import json
from rockit.common import daemons, IP, validation

CONFIG_SCHEMA = {
    'type': 'object',
    'additionalProperties': False,
    'required': [
        'daemon', 'log_name', 'control_machines', 'serial_port', 'serial_baud', 'serial_timeout', 'query_delay',
        'power_daemon', 'power_channels', 'temperature_daemon', 'temperature_value_key',
        'antifreeze_enable_limit', 'antifreeze_disable_limit'
    ],
    'properties': {
        'daemon': {
            'type': 'string',
            'daemon_name': True
        },
        'log_name': {
            'type': 'string',
        },
        'control_machines': {
            'type': 'array',
            'items': {
                'type': 'string',
                'machine_name': True
            }
        },
        'serial_port': {
            'type': 'string',
        },
        'serial_baud': {
            'type': 'number',
            'min': 0
        },
        'serial_timeout': {
            'type': 'number',
            'min': 0
        },
        'query_delay': {
            'type': 'number',
            'min': 0
        },
        'power_daemon': {
            'daemon_name': True,
            'type': 'string',
        },
        'power_channels': {
            'type': 'array',
            'items': {
                'type': 'string',
            }
        },
        'temperature_daemon': {
            'daemon_name': True,
            'type': 'string',
        },
        'temperature_value_key': {
            'type': 'string',
        },
        'temperature_valid_key': {
            'type': 'string',
        },
        'antifreeze_enable_limit': {
            'type': 'number'
        },
        'antifreeze_disable_limit': {
            'type': 'number'
        },

    }
}


class Config:
    """Daemon configuration parsed from a json file"""
    def __init__(self, config_filename):
        # Will throw on file not found or invalid json
        with open(config_filename, 'r', encoding='utf-8') as config_file:
            config_json = json.load(config_file)

        # Will throw on schema violations
        validators = {
            'daemon_name': validation.daemon_name_validator
        }

        validation.validate_config(config_json, CONFIG_SCHEMA, validators)

        self.daemon = getattr(daemons, config_json['daemon'])
        self.log_name = config_json['log_name']
        self.control_ips = [getattr(IP, machine) for machine in config_json['control_machines']]
        self.serial_port = config_json['serial_port']
        self.serial_baud = int(config_json['serial_baud'])
        self.serial_timeout = int(config_json['serial_timeout'])
        self.query_delay = config_json['query_delay']
        self.power_daemon = getattr(daemons, config_json['power_daemon'])
        self.power_channels = config_json['power_channels']
        self.temperature_daemon = getattr(daemons, config_json['temperature_daemon'])
        self.temperature_value_key = config_json['temperature_value_key']
        if 'temperature_valid_key' in config_json:
            self.temperature_valid_key = config_json['temperature_valid_key']
        else:
            self.temperature_valid_key = None
        self.antifreeze_enable_limit = config_json['antifreeze_enable_limit']
        self.antifreeze_disable_limit = config_json['antifreeze_disable_limit']
