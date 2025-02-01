"""
This module is responsible for parsing the configuration file.
It reads the configuration file and returns the provider and its configuration as a dictionary.
It also provides a function to determine if a local shelf should be used based on the file extension.

At this level, the only necessary configuration is the provider name.
Other configurations are loaded into a dictionary and passed to the provider for further configuration.
"""
from logging import Logger
from collections import namedtuple
import configparser
from pathlib import Path
from typing import Dict, Tuple


# Default ini section containing the provider and its configuration.
DEFAULT_CONFIG_STORE = "default"
# Key containing the provider name.
PROVIDER_KEY = "provider"
# Logging configuration section.
LOGGING_KEY_STORE = "logging"
# Compression configuration section.
COMPRESSION_KEY_STORE = "compression"
# Encryption configuration section.
ENCRYPTION_KEY_STORE = "encryption"


# Tuple containing the provider name and its configuration.
Config = namedtuple(
    "Config", ["provider", "default", "logging", "compression", "encryption"]
)


def use_local_shelf(filename: Path) -> bool:
    """
    If the user specify a filename with an extension different of '.ini', a local shelf (the standard library) must be used.
    """
    return not filename.suffix == ".ini"


def load(logger: Logger, filename: Path) -> Tuple[str, Dict[str, str]]:
    """
    Load the configuration file and return it as a dictionary.
    """
    logger.debug(f"Loading configuration file: {filename}.")
    config = configparser.ConfigParser()
    config.read(filename)

    c = config[DEFAULT_CONFIG_STORE]
    logging_config = config[LOGGING_KEY_STORE] if LOGGING_KEY_STORE in config else {}
    compression_config = (
        config[COMPRESSION_KEY_STORE] if COMPRESSION_KEY_STORE in config else {}
    )
    encryption_config = (
        config[ENCRYPTION_KEY_STORE] if ENCRYPTION_KEY_STORE in config else {}
    )

    logger.debug(f"Configuration file '{filename}' loaded.")
    return Config(
        provider=c[PROVIDER_KEY],
        default=c,
        logging=logging_config,
        compression=compression_config,
        encryption=encryption_config,
    )
