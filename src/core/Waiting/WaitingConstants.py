# -*- coding:utf-8 -*-
# @module WaitingConstants
# @desc Waiting Constants
# @since 2023.02.12, 01:01
# @changed 2023.02.12, 22:18


from src.core.lib import utils


dbName = 'Waiting'  # Relative to `config['dbPath']`

# Time for wait for valid waitings (if not renewed)
validWaitingPeriodMs = utils.msTimeFromMin(10)


__all__ = [  # Exporting objects...
    'dbName',
    'validWaitingPeriodMs',
]
