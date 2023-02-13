# -*- coding:utf-8 -*-
# @module WaitingConstants
# @desc Waiting Constants
# @since 2023.02.12, 01:01
# @changed 2023.02.13, 21:42


#  from src.core.lib import utils
from src.core.lib.utils import msTimeFromMin
from config import config


dbName = 'Waiting'  # Relative to `config['dbPath']`

# Time for wait for valid waitings (if not renewed)
validWaitingPeriodMs = msTimeFromMin(40) if config['isDev'] else msTimeFromMin(2)


__all__ = [  # Exporting objects...
    'dbName',
    'validWaitingPeriodMs',
]
