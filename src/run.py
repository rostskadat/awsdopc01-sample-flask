# -*- encoding: utf-8 -*-
import os
from sys import exit

from microservice import create_app
from microservice.config import config_dict

# WARNING: Don't run with debug turned on in production!
DEBUG = (os.getenv('DEBUG', 'False') == 'True')

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:

    # Load the configuration using the default values
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app(app_config)

if DEBUG:
    app.config['TEMPLATES_AUTO_RELOAD'] = True

if __name__ == "__main__":
    app.run()
