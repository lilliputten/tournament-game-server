# -*- coding:utf-8 -*-
# @module config_helpers
# @since 2022.02.07, 00:04
# @changed 2022.04.02, 17:52

from os import path
import yaml
#  import json
#  import sys


def updateConfigWithYaml(config, file):
    """
    Extend config from file
    """
    if path.isfile(file):
        with open(file, encoding='UTF-8') as handler:
            #  print('Extending config with', file)
            yamlConfigData = yaml.load(handler, Loader=yaml.FullLoader)
            #  print('yamlConfigData:', yamlConfigData)
            config.update(yamlConfigData)


def readFiletoString(file, defaultValue=''):
    """
    Read text string from file
    """
    if path.isfile(file):
        with open(file, encoding='UTF-8') as handler:
            #  print('Extending config with', file)
            data = handler.read().strip()
            handler.close()
            return data
    return defaultValue


__all__ = [  # Exporting objects...
    'updateConfigWithYaml',
    'readFiletoString',
]
