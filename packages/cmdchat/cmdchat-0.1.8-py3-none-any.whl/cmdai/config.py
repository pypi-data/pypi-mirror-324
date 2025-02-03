import configparser
import os

CONFIG_FILE = os.path.expanduser('~/.cmdai_config.ini')

def create_config():
    """Creates a default config file if it doesn't exist."""
    config = configparser.ConfigParser()
    config['DEFAULT'] = {'DefaultModel': 'gpt-4o-mini'}
    config['API_KEYS'] = {}
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def read_config():
    """Reads the configuration file."""
    if not os.path.exists(CONFIG_FILE):
        create_config()
    config = configparser.ConfigParser()
    config.read(CONFIG_FILE)
    return config

def set_default_model(model_name):
    """Sets the default AI model in the config file."""
    config = read_config()
    config['DEFAULT']['DefaultModel'] = model_name
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def get_default_model():
    """Gets the default AI model from the config file."""
    config = read_config()
    return config['DEFAULT'].get('DefaultModel', 'gpt-4o-mini')

def set_api_key(provider, api_key):
    """Stores an API key for a given provider."""
    config = read_config()
    if 'API_KEYS' not in config:
        config['API_KEYS'] = {}
    config['API_KEYS'][provider] = api_key
    with open(CONFIG_FILE, 'w') as configfile:
        config.write(configfile)

def get_api_key(provider):
    """Retrieves the API key for a given provider."""
    config = read_config()
    return config['API_KEYS'].get(provider, '')
