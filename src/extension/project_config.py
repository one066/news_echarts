import importlib
import os


def get_config(config_name: str = None):
    if not config_name:
        config_name = os.environ.get('STAGE')

    if not config_name:
        config_name = 'testing'

    configs_module = importlib.import_module('configs')
    return getattr(configs_module, config_name.capitalize())
