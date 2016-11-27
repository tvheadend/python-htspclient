import json
import os

CONFIG = {
    'hostname': 'enter-your-tvheadend-hostname-or-ip',
    'username': 'enter-your-tvheadend-username',
    'password': 'enter-your-tvheadend-password',
}

if os.path.exists('config.json'):
    with open('config.json', 'r') as config_file:
        CONFIG = json.load(config_file)
        config_file.close()

