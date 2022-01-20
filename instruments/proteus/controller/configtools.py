import json
import pathlib

config_file_name = "config.json"
default_config = {
    "PORT": 20678,
    "TIMEOUT": 10000, #ms
    "HIDE_CLI_WINDOW": False,
    "VERBOSE": True
}

dirname = pathlib.Path(__file__).parent.absolute()
config_file = str(dirname.joinpath(config_file_name))


def write_config(config=None):
    if not config:
        config = default_config
    with open(config_file, 'w+') as config_fp:
        json.dump(config, config_fp)


def read_config(config_file=config_file):
    with open(config_file, 'r') as config_fp:
        config = json.load(config_fp)
    return config


if __name__ == "__main__":
    write_config()
