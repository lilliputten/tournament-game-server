# -*- coding:utf-8 -*-
# @module GameConstants
# @desc Game Constants
# @since 2023.02.13, 13:52
# @changed 2023.02.13, 13:52


from src.core.lib import utils


dbName = 'Game'  # Relative to `config['dbPath']`

# Time to wait game to start (ms) -- used to remove obsolette waiting for start games in GameController:removeObsoleteWaitingGamesForPartners
validWaitingGamePeriodMs = utils.msTimeFromMin(5)

# Total game validity period (ms) -- used in gameSessionFinished:gameSessionFinished, and removeAllObsoleteGames
storeOldGamePeriodMs = utils.msTimeFromHours(3)

__all__ = [  # Exporting objects...
    'dbName',
    'validWaitingGamePeriodMs',
]
