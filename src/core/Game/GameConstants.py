# -*- coding:utf-8 -*-
# @module GameConstants
# @desc Game Constants
# @since 2023.02.13, 13:52
# @changed 2023.02.13, 13:52


from src.core.lib import utils


dbName = 'Game'  # Relative to `config['dbPath']`

# Time of game validity (ms)
validGamePeriodMs = utils.msTimeFromMin(5)


__all__ = [  # Exporting objects...
    'dbName',
    'validGamePeriodMs',
]
